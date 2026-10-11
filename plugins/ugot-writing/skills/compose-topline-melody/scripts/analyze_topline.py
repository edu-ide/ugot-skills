#!/usr/bin/env python3
"""Measure a chorus topline from a preferably isolated vocal WAV."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import torch
import torchaudio
import torchcrepe
from scipy.ndimage import binary_closing, binary_opening, median_filter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate pitch-contour and note-motion metrics for a vocal chorus."
    )
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--confidence", type=float, default=0.70)
    parser.add_argument("--fmin", type=float, default=65.0)
    parser.add_argument("--fmax", type=float, default=1000.0)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def mask_runs(mask: np.ndarray) -> list[tuple[int, int]]:
    edges = np.diff(np.r_[False, mask, False].astype(np.int8))
    return list(zip(np.where(edges == 1)[0], np.where(edges == -1)[0]))


def merge_close_runs(
    runs: list[tuple[int, int]], max_gap: int
) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for left, right in runs:
        if merged and left - merged[-1][1] <= max_gap:
            merged[-1] = (merged[-1][0], right)
        else:
            merged.append((left, right))
    return merged


def finite_float(value: float) -> float | None:
    return round(float(value), 4) if math.isfinite(float(value)) else None


def main() -> None:
    args = parse_args()
    if not args.audio.is_file():
        raise SystemExit(f"Audio file not found: {args.audio}")
    if args.start < 0 or (args.end is not None and args.end <= args.start):
        raise SystemExit("Require 0 <= start < end")
    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA was requested but is not available")

    waveform, sample_rate = torchaudio.load(str(args.audio))
    waveform = waveform.mean(dim=0)
    start_frame = round(args.start * sample_rate)
    end_frame = len(waveform) if args.end is None else round(args.end * sample_rate)
    if start_frame >= len(waveform) or end_frame > len(waveform):
        raise SystemExit("Requested segment falls outside the audio duration")
    waveform = waveform[start_frame:end_frame]
    waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
    model_input = waveform.unsqueeze(0).to(args.device)

    with torch.inference_mode():
        pitch, periodicity = torchcrepe.predict(
            model_input,
            16000,
            160,
            args.fmin,
            args.fmax,
            model="full",
            batch_size=2048,
            device=args.device,
            decoder=torchcrepe.decode.viterbi,
            return_periodicity=True,
            pad=True,
        )

    pitch_hz = pitch[0].cpu().numpy()
    confidence = periodicity[0].cpu().numpy()
    midi = 69.0 + 12.0 * np.log2(np.maximum(pitch_hz, 1e-6) / 440.0)
    midi = median_filter(midi, size=9)

    voiced = confidence >= args.confidence
    voiced = binary_closing(voiced, structure=np.ones(12))
    voiced = binary_opening(voiced, structure=np.ones(5))
    values = midi[voiced]
    if len(values) < 20:
        raise SystemExit("Too few confident voiced frames; lower --confidence or isolate vocals")

    p05, p20, p50, p80, p95 = np.percentile(values, [5, 20, 50, 80, 95])
    high_pitch = np.percentile(values, 90)
    high_frames = np.where(voiced & (midi >= high_pitch))[0]
    high_position = np.median(high_frames) / len(midi)
    high_zone = voiced & (midi >= p80)
    high_zone = binary_closing(high_zone, structure=np.ones(15))
    high_zone = binary_opening(high_zone, structure=np.ones(8))
    high_zone_runs = merge_close_runs(
        [
            (left, right)
            for left, right in mask_runs(high_zone)
            if right - left >= 10
        ],
        max_gap=125,
    )
    high_zone_positions = [
        finite_float(((left + right) / 2.0) / len(midi))
        for left, right in high_zone_runs
    ]

    voiced_indices = np.where(voiced)[0]
    fifth = max(1, len(voiced_indices) // 5)
    start_pitch = np.median(midi[voiced_indices[:fifth]])
    end_pitch = np.median(midi[voiced_indices[-fifth:]])
    midpoint = len(midi) // 2
    first_half = midi[:midpoint][voiced[:midpoint]]
    second_half = midi[midpoint:][voiced[midpoint:]]
    late_lift = np.median(second_half) - np.median(first_half)

    boundaries = np.linspace(0, len(midi), 9, dtype=int)
    contour: list[float | None] = []
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        local_mask = voiced[left:right]
        if local_mask.sum() < 5:
            contour.append(None)
        else:
            contour.append(
                finite_float(np.median(midi[left:right][local_mask]) - p50)
            )

    quantized = np.round(midi)
    notes: list[tuple[int, int, float]] = []
    for run_start, run_end in mask_runs(voiced):
        cursor = run_start
        while cursor < run_end:
            note_end = cursor + 1
            while note_end < run_end and quantized[note_end] == quantized[cursor]:
                note_end += 1
            if note_end - cursor >= 8:
                notes.append(
                    (cursor, note_end, float(np.median(midi[cursor:note_end])))
                )
            cursor = note_end

    intervals = np.diff([note[2] for note in notes])
    abs_intervals = np.abs(intervals)
    note_durations = [(end - start) / 100.0 for start, end, _ in notes]
    note_centers = np.asarray([(start + end) / 2.0 for start, end, _ in notes])
    half_duration = len(waveform) / 16000.0 / 2.0
    first_half_density = (
        float(np.sum(note_centers < midpoint)) / half_duration
        if half_duration > 0
        else float("nan")
    )
    second_half_density = (
        float(np.sum(note_centers >= midpoint)) / half_duration
        if half_duration > 0
        else float("nan")
    )
    valid_contour = [
        (index, value) for index, value in enumerate(contour) if value is not None
    ]

    metrics = {
        "audio": str(args.audio.resolve()),
        "segment_start_s": args.start,
        "segment_end_s": args.end,
        "segment_duration_s": round(len(waveform) / 16000.0, 4),
        "voiced_ratio": finite_float(voiced.mean()),
        "midi_p05": finite_float(p05),
        "midi_median": finite_float(p50),
        "midi_p95": finite_float(p95),
        "robust_range_semitones": finite_float(p95 - p05),
        "core_range_semitones": finite_float(p80 - p20),
        "high_point_position": finite_float(high_position),
        "high_zone_episode_count": len(high_zone_runs),
        "high_zone_episode_positions": high_zone_positions,
        "high_zone_episode_min_gap_s": 1.25,
        "start_to_end_semitones": finite_float(end_pitch - start_pitch),
        "high_zone_to_end_semitones": finite_float(end_pitch - high_pitch),
        "second_half_lift_semitones": finite_float(late_lift),
        "contour_eighths_relative_to_median": contour,
        "stable_note_count": len(notes),
        "stable_notes_per_second": finite_float(
            len(notes) / (len(waveform) / 16000.0)
        ),
        "first_half_stable_notes_per_second": finite_float(
            first_half_density
        ),
        "second_half_stable_notes_per_second": finite_float(
            second_half_density
        ),
        "second_minus_first_half_note_density": finite_float(
            second_half_density - first_half_density
        ),
        "highest_eighth_index": (
            max(valid_contour, key=lambda item: item[1])[0] + 1
            if valid_contour
            else None
        ),
        "lowest_eighth_index": (
            min(valid_contour, key=lambda item: item[1])[0] + 1
            if valid_contour
            else None
        ),
        "median_stable_note_duration_s": finite_float(
            np.median(note_durations) if note_durations else float("nan")
        ),
        "repeated_note_ratio": finite_float(
            np.mean(abs_intervals < 1.5) if len(intervals) else float("nan")
        ),
        "step_ratio_1_to_2_semitones": finite_float(
            np.mean((abs_intervals >= 1.5) & (abs_intervals < 3.5))
            if len(intervals)
            else float("nan")
        ),
        "leap_ratio_5plus_semitones": finite_float(
            np.mean(abs_intervals >= 4.5) if len(intervals) else float("nan")
        ),
        "confidence_threshold": args.confidence,
    }

    output = json.dumps(metrics, ensure_ascii=False, indent=2)
    if args.output is None:
        print(output)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
        print(args.output)


if __name__ == "__main__":
    main()
