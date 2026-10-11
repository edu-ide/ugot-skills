#!/usr/bin/env python3
"""Compare stem-specific timbre between two loudness-matched song sections."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import librosa
import numpy as np
import torch
import torchaudio


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare interpretable timbre descriptors for two song sections."
    )
    parser.add_argument("--mix", required=True, type=Path)
    parser.add_argument("--vocal", type=Path)
    parser.add_argument("--instrumental", type=Path)
    parser.add_argument("--before-start", required=True, type=float)
    parser.add_argument("--before-end", required=True, type=float)
    parser.add_argument("--target-start", required=True, type=float)
    parser.add_argument("--target-end", required=True, type=float)
    parser.add_argument("--disable-opensmile", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def decibels(value: float) -> float:
    return 20.0 * math.log10(max(float(value), 1e-12))


def load_segment(path: Path, start: float, end: float) -> tuple[torch.Tensor, int]:
    if not path.is_file():
        raise SystemExit(f"Audio file not found: {path}")
    waveform, sample_rate = torchaudio.load(str(path))
    left = round(start * sample_rate)
    right = round(end * sample_rate)
    if (
        start < 0
        or end <= start
        or left >= waveform.shape[-1]
        or right > waveform.shape[-1]
    ):
        raise SystemExit(f"Invalid segment {start}-{end}s for {path}")
    return waveform[:, left:right].float(), sample_rate


def rms(waveform: torch.Tensor) -> torch.Tensor:
    return torch.sqrt(torch.mean(waveform.square()) + 1e-12)


def loudness_match(waveform: torch.Tensor, target_rms: float = 0.1) -> torch.Tensor:
    return waveform * (target_rms / float(rms(waveform)))


def stereo_metrics(waveform: torch.Tensor) -> dict[str, float | None]:
    if waveform.shape[0] < 2:
        return {"side_to_mid_db": None, "left_right_correlation": None}
    left, right = waveform[0], waveform[1]
    mid = (left + right) / 2.0
    side = (left - right) / 2.0
    correlation = torch.mean(left * right) / (rms(left) * rms(right) + 1e-12)
    return {
        "side_to_mid_db": round(decibels(rms(side) / rms(mid)), 4),
        "left_right_correlation": round(float(correlation), 4),
    }


def band_ratio(
    power: torch.Tensor,
    frequencies: torch.Tensor,
    low: float,
    high: float,
    total: torch.Tensor,
) -> float:
    mask = (frequencies >= low) & (frequencies < high)
    return float(power[mask].sum() / total)


def spectral_metrics(waveform: torch.Tensor, sample_rate: int) -> dict[str, float]:
    mono = loudness_match(waveform).mean(dim=0)
    n_fft = 4096
    hop_length = 1024
    window = torch.hann_window(n_fft)
    magnitude = (
        torch.stft(
            mono,
            n_fft=n_fft,
            hop_length=hop_length,
            win_length=n_fft,
            window=window,
            return_complex=True,
        ).abs()
        + 1e-9
    )
    power = magnitude.square()
    frequencies = torch.linspace(0.0, sample_rate / 2.0, magnitude.shape[0])
    total_power = (
        power[(frequencies >= 20.0) & (frequencies < 16000.0)].sum() + 1e-12
    )

    centroid = (
        (frequencies[:, None] * magnitude).sum(dim=0) / magnitude.sum(dim=0)
    )
    flatness = torch.exp(torch.log(power).mean(dim=0)) / power.mean(dim=0)
    normalized = magnitude / (
        torch.linalg.vector_norm(magnitude, dim=0, keepdim=True) + 1e-9
    )
    spectral_flux = (
        torch.relu(normalized[:, 1:] - normalized[:, :-1])
        .square()
        .sum(dim=0)
        .sqrt()
    )

    mean_spectrum = magnitude.mean(dim=1).numpy()
    frequency_array = frequencies.numpy()
    slope_mask = (frequency_array >= 100.0) & (
        frequency_array <= min(8000.0, sample_rate / 2.0)
    )
    octave_axis = np.log2(frequency_array[slope_mask] / 100.0)
    spectrum_db = 20.0 * np.log10(mean_spectrum[slope_mask] + 1e-12)
    spectral_slope = np.polyfit(octave_axis, spectrum_db, 1)[0]

    contrast = librosa.feature.spectral_contrast(
        S=magnitude.numpy(), sr=sample_rate, n_fft=n_fft, hop_length=hop_length
    )

    return {
        "spectral_centroid_hz": round(float(torch.median(centroid)), 4),
        "spectral_slope_db_per_octave": round(float(spectral_slope), 4),
        "spectral_flatness": round(float(torch.median(flatness)), 6),
        "spectral_flux": round(float(torch.median(spectral_flux)), 6),
        "spectral_contrast_db": round(float(np.mean(contrast)), 4),
        "sub_20_150_ratio": round(
            band_ratio(power, frequencies, 20.0, 150.0, total_power), 6
        ),
        "warmth_150_500_ratio": round(
            band_ratio(power, frequencies, 150.0, 500.0, total_power), 6
        ),
        "body_500_2000_ratio": round(
            band_ratio(power, frequencies, 500.0, 2000.0, total_power), 6
        ),
        "presence_2000_5000_ratio": round(
            band_ratio(power, frequencies, 2000.0, 5000.0, total_power), 6
        ),
        "air_8000_16000_ratio": round(
            band_ratio(power, frequencies, 8000.0, 16000.0, total_power), 6
        ),
    }


def dynamics_metrics(waveform: torch.Tensor) -> dict[str, float]:
    raw_rms = rms(waveform)
    crest = waveform.abs().max() / raw_rms
    mono = waveform.mean(dim=0)
    frame_length = 2048
    hop_length = 512
    frames = mono.unfold(0, frame_length, hop_length)
    frame_db = 20.0 * torch.log10(
        torch.sqrt(frames.square().mean(dim=1)) + 1e-12
    )
    short_term_range = torch.quantile(frame_db, 0.9) - torch.quantile(
        frame_db, 0.1
    )
    return {
        "raw_rms_dbfs_control_only": round(decibels(raw_rms), 4),
        "crest_factor_db": round(decibels(crest), 4),
        "short_term_range_db": round(float(short_term_range), 4),
    }


def opensmile_vocal_metrics(
    waveform: torch.Tensor, sample_rate: int
) -> dict[str, float]:
    try:
        import opensmile
    except ImportError as exc:
        raise SystemExit(
            "openSMILE is unavailable; install opensmile or pass --disable-opensmile"
        ) from exc

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    signal = loudness_match(waveform).mean(dim=0).numpy()
    row = smile.process_signal(signal, sample_rate).iloc[0]
    requested = {
        "alpha_ratio_voiced_db": "alphaRatioV_sma3nz_amean",
        "hammarberg_index_voiced_db": "hammarbergIndexV_sma3nz_amean",
        "slope_voiced_0_500": "slopeV0-500_sma3nz_amean",
        "slope_voiced_500_1500": "slopeV500-1500_sma3nz_amean",
        "hnr_db": "HNRdBACF_sma3nz_amean",
        "spectral_flux_voiced": "spectralFluxV_sma3nz_amean",
        "jitter_local": "jitterLocal_sma3nz_amean",
        "shimmer_local_db": "shimmerLocaldB_sma3nz_amean",
        "f1_hz": "F1frequency_sma3nz_amean",
        "f2_hz": "F2frequency_sma3nz_amean",
        "f3_hz": "F3frequency_sma3nz_amean",
    }
    return {
        name: round(float(row[column]), 6) for name, column in requested.items()
    }


def section_metrics(
    paths: dict[str, Path],
    start: float,
    end: float,
    use_opensmile: bool,
) -> dict[str, dict[str, float | None]]:
    result: dict[str, dict[str, float | None]] = {}
    for stem_name, path in paths.items():
        waveform, sample_rate = load_segment(path, start, end)
        values: dict[str, float | None] = {}
        values.update(dynamics_metrics(waveform))
        values.update(spectral_metrics(waveform, sample_rate))
        values.update(stereo_metrics(waveform))
        if stem_name == "vocal" and use_opensmile:
            values.update(opensmile_vocal_metrics(waveform, sample_rate))
        result[stem_name] = values
    return result


def numeric_delta(
    before: dict[str, dict[str, float | None]],
    target: dict[str, dict[str, float | None]],
) -> dict[str, dict[str, float | None]]:
    delta: dict[str, dict[str, float | None]] = {}
    for stem_name in before:
        delta[stem_name] = {}
        for key, before_value in before[stem_name].items():
            target_value = target[stem_name][key]
            if before_value is None or target_value is None:
                delta[stem_name][key] = None
            else:
                delta[stem_name][key] = round(
                    target_value - before_value, 6
                )
    return delta


def main() -> None:
    args = parse_args()
    paths = {"mix": args.mix}
    if args.vocal is not None:
        paths["vocal"] = args.vocal
    if args.instrumental is not None:
        paths["instrumental"] = args.instrumental

    before = section_metrics(
        paths, args.before_start, args.before_end, not args.disable_opensmile
    )
    target = section_metrics(
        paths, args.target_start, args.target_end, not args.disable_opensmile
    )
    result = {
        "method": {
            "spectral_and_spatial_descriptors_are_rms_matched": True,
            "raw_rms_is_control_only": True,
            "opensmile_feature_set": (
                None
                if args.disable_opensmile or "vocal" not in paths
                else "eGeMAPSv02"
            ),
        },
        "before": before,
        "target": target,
        "delta_target_minus_before": numeric_delta(before, target),
    }
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output is None:
        print(output)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
        print(args.output)


if __name__ == "__main__":
    main()
