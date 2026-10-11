#!/usr/bin/env python3
"""Rank repeated song-section pairs without declaring that they are choruses."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import librosa
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Find beat-aligned repeated section pairs from a mix or vocal stem. "
            "The results are candidates, not automatic chorus labels."
        )
    )
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument(
        "--window-beats",
        default="16,24,32,48,64",
        help="Comma-separated candidate section lengths in beats.",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def finite_float(value: float) -> float | None:
    return round(float(value), 4) if math.isfinite(float(value)) else None


def normalize_columns(features: np.ndarray) -> np.ndarray:
    centered = features - np.median(features, axis=1, keepdims=True)
    scale = np.median(np.abs(centered), axis=1, keepdims=True) + 1e-8
    robust = centered / scale
    return librosa.util.normalize(robust, norm=2, axis=0)


def candidate_pairs(
    features: np.ndarray,
    beat_times: np.ndarray,
    beat_rms: np.ndarray,
    window: int,
    top_k: int,
) -> list[dict[str, float | int | None]]:
    frame_count = features.shape[1]
    if frame_count < window * 2 + 4:
        return []

    candidates: list[tuple[float, int, int, float]] = []
    activity_floor = float(np.quantile(beat_rms, 0.2))
    for first in range(0, frame_count - window + 1, 2):
        first_activity = float(np.mean(beat_rms[first : first + window]))
        if first_activity < activity_floor:
            continue
        first_window = features[:, first : first + window]
        for second in range(first + window + 4, frame_count - window + 1, 2):
            second_activity = float(np.mean(beat_rms[second : second + window]))
            if second_activity < activity_floor:
                continue
            second_window = features[:, second : second + window]
            aligned_similarity = np.sum(first_window * second_window, axis=0)
            score = float(np.mean(aligned_similarity))
            activity_balance = min(first_activity, second_activity) / max(
                first_activity, second_activity, 1e-8
            )
            candidates.append((score, first, second, activity_balance))

    selected: list[tuple[float, int, int, float]] = []
    exclusion = max(4, window // 4)
    for candidate in sorted(candidates, reverse=True):
        _, first, second, _ = candidate
        if any(
            abs(first - old_first) < exclusion
            and abs(second - old_second) < exclusion
            for _, old_first, old_second, _ in selected
        ):
            continue
        selected.append(candidate)
        if len(selected) == top_k:
            break

    duration_fallback = float(np.median(np.diff(beat_times)))
    results: list[dict[str, float | int | None]] = []
    for score, first, second, activity_balance in selected:
        first_end_index = min(first + window, len(beat_times) - 1)
        second_end_index = min(second + window, len(beat_times) - 1)
        results.append(
            {
                "similarity": finite_float(score),
                "activity_balance": finite_float(activity_balance),
                "first_start_s": finite_float(beat_times[first]),
                "first_end_s": finite_float(
                    beat_times[first_end_index]
                    if first_end_index > first
                    else beat_times[first] + duration_fallback * window
                ),
                "second_start_s": finite_float(beat_times[second]),
                "second_end_s": finite_float(
                    beat_times[second_end_index]
                    if second_end_index > second
                    else beat_times[second] + duration_fallback * window
                ),
                "separation_beats": second - first,
            }
        )
    return results


def main() -> None:
    args = parse_args()
    if not args.audio.is_file():
        raise SystemExit(f"Audio file not found: {args.audio}")
    if args.top_k < 1:
        raise SystemExit("--top-k must be positive")
    try:
        window_beats = sorted(
            {int(value.strip()) for value in args.window_beats.split(",")}
        )
    except ValueError as exc:
        raise SystemExit("--window-beats must contain only integers") from exc
    if not window_beats or any(value < 8 for value in window_beats):
        raise SystemExit("Each section window must be at least 8 beats")

    waveform, sample_rate = librosa.load(args.audio, sr=22050, mono=True)
    harmonic, _ = librosa.effects.hpss(waveform)
    tempo, beat_frames = librosa.beat.beat_track(
        y=waveform, sr=sample_rate, units="frames"
    )
    tempo_value = float(np.asarray(tempo).reshape(-1)[0])
    if len(beat_frames) < min(window_beats) * 2 + 4:
        raise SystemExit("Too few detected beats for repeated-section analysis")

    hop_length = 512
    chroma = librosa.feature.chroma_cens(
        y=harmonic, sr=sample_rate, hop_length=hop_length
    )
    mfcc = librosa.feature.mfcc(
        y=waveform, sr=sample_rate, n_mfcc=13, hop_length=hop_length
    )
    rms = librosa.feature.rms(y=waveform, hop_length=hop_length)
    beat_chroma = librosa.util.sync(chroma, beat_frames, aggregate=np.median)
    beat_mfcc = librosa.util.sync(mfcc, beat_frames, aggregate=np.median)
    beat_rms = librosa.util.sync(rms, beat_frames, aggregate=np.mean)[0]
    beat_count = min(
        beat_chroma.shape[1], beat_mfcc.shape[1], beat_rms.shape[0]
    )
    beat_chroma = normalize_columns(beat_chroma[:, :beat_count])
    beat_mfcc = normalize_columns(beat_mfcc[:, :beat_count])
    features = np.vstack((beat_chroma * math.sqrt(0.75), beat_mfcc * 0.5))
    features = librosa.util.normalize(features, norm=2, axis=0)
    beat_rms = beat_rms[:beat_count]
    beat_times = librosa.frames_to_time(
        beat_frames[:beat_count], sr=sample_rate, hop_length=hop_length
    )

    results = {
        "audio": str(args.audio.resolve()),
        "duration_s": finite_float(len(waveform) / sample_rate),
        "estimated_tempo_bpm": finite_float(tempo_value),
        "detected_beats": int(beat_count),
        "method": {
            "beat_aligned": True,
            "feature_mix": "75% chroma CENS, 25% MFCC",
            "interpretation": (
                "Ranked recurrence candidates only. Verify section role with "
                "lyrics, arrangement, and neighboring sections."
            ),
        },
        "pairs_by_window_beats": {
            str(window): candidate_pairs(
                features, beat_times, beat_rms, window, args.top_k
            )
            for window in window_beats
        },
    }
    output = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output is None:
        print(output)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
        print(args.output)


if __name__ == "__main__":
    main()
