#!/usr/bin/env python3
"""Describe held-out proxy ranking; never train, select thresholds, or certify quality.

Input is CSV with exactly id,family,split,proxy,target. Both calibration and
confirmation must exist and their family sets must be disjoint. The calibration
split is validated and counted, NOT used to fit a model. Metrics use confirmation
only. Family labels cannot prove real-world independence or prior registration.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import dataclass
import hashlib
import io
import json
import math
from pathlib import Path
import sys
from typing import TextIO


FIELDS = {"id", "family", "split", "proxy", "target"}
DIRECTIONS = {"higher", "lower"}
SCOPE = (
    "Descriptive confirmation-set ranking only; no fitting, confidence interval, "
    "success probability, SOTA forecast, or architecture promotion."
)


class InputError(ValueError):
    """Input cannot support the requested diagnostic."""


@dataclass(frozen=True)
class Record:
    id: str
    family: str
    split: str
    proxy: float
    target: float


def validate_records(records: list[Record]) -> None:
    ids: set[str] = set()
    families: dict[str, set[str]] = {"calibration": set(), "confirmation": set()}
    for record in records:
        if not record.id or not record.family:
            raise InputError("id and family must be nonempty")
        if record.id in ids:
            raise InputError(f"duplicate id: {record.id!r}")
        ids.add(record.id)
        if record.split not in families:
            raise InputError(f"invalid split for {record.id!r}: {record.split!r}")
        if not math.isfinite(record.proxy) or not math.isfinite(record.target):
            raise InputError(f"non-finite score for {record.id!r}")
        families[record.split].add(record.family)
    for split, names in families.items():
        if not names:
            raise InputError(f"missing nonempty {split} split")
    overlap = families["calibration"] & families["confirmation"]
    if overlap:
        raise InputError(f"family leakage across splits: {sorted(overlap)!r}")


def read_csv(stream: TextIO) -> list[Record]:
    reader = csv.DictReader(stream, strict=True)
    try:
        header = reader.fieldnames
        if header is None:
            raise InputError("missing CSV header")
        header = [name.strip() for name in header]
        if len(header) != len(set(header)) or set(header) != FIELDS:
            raise InputError("header must contain exactly id,family,split,proxy,target once")
        reader.fieldnames = header
        records: list[Record] = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise InputError(f"line {reader.line_num}: wrong column count")
            values = {key: value.strip() for key, value in row.items()}
            if any(not value for value in values.values()):
                raise InputError(f"line {reader.line_num}: missing value")
            try:
                proxy, target = float(values["proxy"]), float(values["target"])
            except ValueError as exc:
                raise InputError(f"line {reader.line_num}: scores must be numbers") from exc
            records.append(Record(values["id"], values["family"], values["split"], proxy, target))
    except csv.Error as exc:
        raise InputError(f"invalid CSV: {exc}") from exc
    validate_records(records)
    return records


def average_ranks(values: list[float]) -> list[float]:
    """One-based ascending ranks, using the mean rank for exact numeric ties."""
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        rank = (start + 1 + end) / 2.0
        for position in range(start, end):
            ranks[order[position]] = rank
        start = end
    return ranks


def spearman(proxy: list[float], target: list[float]) -> float | None:
    """Pearson correlation of average ranks; undefined for a constant axis."""
    if len(proxy) != len(target):
        raise InputError("score lengths differ")
    if len(proxy) < 2:
        return None
    p, t = average_ranks(proxy), average_ranks(target)
    center = (len(p) + 1) / 2.0
    p = [value - center for value in p]
    t = [value - center for value in t]
    p_ss, t_ss = math.fsum(value * value for value in p), math.fsum(value * value for value in t)
    if not p_ss or not t_ss:
        return None
    correlation = math.fsum(a * b for a, b in zip(p, t)) / math.sqrt(p_ss * t_ss)
    return max(-1.0, min(1.0, correlation))


def _inversions(values: list[float]) -> tuple[list[float], int]:
    if len(values) < 2:
        return values, 0
    midpoint = len(values) // 2
    left, left_count = _inversions(values[:midpoint])
    right, right_count = _inversions(values[midpoint:])
    merged: list[float] = []
    i = j = 0
    count = left_count + right_count
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            count += len(left) - i
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, count


def pairwise_metrics(proxy: list[float], target: list[float]) -> dict:
    """Count unordered pairs; a tie on either axis excludes strict discordance."""
    if len(proxy) != len(target):
        raise InputError("score lengths differ")
    total = len(proxy) * (len(proxy) - 1) // 2

    def ties(values) -> int:
        return sum(count * (count - 1) // 2 for count in Counter(values).values())

    proxy_ties = ties(proxy)
    target_ties = ties(target)
    both_ties = ties(zip(proxy, target))
    either_ties = proxy_ties + target_ties - both_ties
    strict = total - either_ties
    # Secondary target sorting ensures equal-proxy groups introduce no inversions.
    _, discordant = _inversions([t for _, t in sorted(zip(proxy, target))])
    return {
        "total_pairs": total,
        "jointly_strict_pairs": strict,
        "strict_concordant_pairs": strict - discordant,
        "strict_discordant_pairs": discordant,
        "strict_discordance_fraction": discordant / strict if strict else None,
        "proxy_tie_pairs": proxy_ties,
        "target_tie_pairs": target_ties,
        "both_tie_pairs": both_ties,
        "either_tie_pairs": either_ties,
        "proxy_tie_fraction": proxy_ties / total if total else None,
        "target_tie_fraction": target_ties / total if total else None,
        "either_tie_fraction": either_ties / total if total else None,
        "denominator_note": "Discordance uses jointly strict pairs; tie fractions use all unordered pairs.",
    }


def top_k_retention(ids: list[str], proxy: list[float], target: list[float], k: int) -> dict:
    """Exact overlap bounds over all size-k boundary-tie resolutions on both axes."""
    if not (len(ids) == len(proxy) == len(target)) or len(set(ids)) != len(ids):
        raise InputError("top-k inputs must have matching lengths and unique ids")
    if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k <= len(ids):
        raise InputError("top-k must be between 1 and the confirmation row count")

    def boundary(values: list[float]) -> tuple[set[str], set[str], int]:
        cutoff = sorted(values, reverse=True)[k - 1]
        definite = {item for item, value in zip(ids, values) if value > cutoff}
        tied = {item for item, value in zip(ids, values) if value == cutoff}
        return definite, tied, k - len(definite)

    p_def, p_tie, p_slots = boundary(proxy)
    t_def, t_tie, t_slots = boundary(target)
    universe = set(ids)
    p_out = universe - p_def - p_tie
    t_out = universe - t_def - t_tie
    fixed = len(p_def & t_def)
    shared_boundary = len(p_tie & t_tie)
    # First avoid overlap with items outside the opposite eligible top-k pool;
    # remaining boundary choices can be disjoint only up to shared_boundary.
    minimum = fixed + max(
        0,
        max(0, p_slots - len(p_tie & t_out))
        + max(0, t_slots - len(t_tie & p_out))
        - shared_boundary,
    )
    # One-sided definite intersections each cost one free boundary choice;
    # then spend any remaining choices on the shared boundary.
    p_to_def = min(p_slots, len(p_tie & t_def))
    t_to_def = min(t_slots, len(t_tie & p_def))
    maximum = fixed + p_to_def + t_to_def + min(
        shared_boundary, p_slots - p_to_def, t_slots - t_to_def
    )
    ambiguous = len(p_tie) > p_slots or len(t_tie) > t_slots
    return {
        "k": k,
        "boundary_tie_ambiguous": ambiguous,
        "retained_count_min": minimum,
        "retained_count_max": maximum,
        "retention_fraction_min": minimum / k,
        "retention_fraction_max": maximum / k,
        "proxy_definite_ids": sorted(p_def),
        "proxy_boundary_ids": sorted(p_tie),
        "proxy_boundary_slots": p_slots,
        "target_definite_ids": sorted(t_def),
        "target_boundary_ids": sorted(t_tie),
        "target_boundary_slots": t_slots,
        "interpretation": "Overlap divided by k, over all independent boundary tie-breaks; not a confidence interval.",
    }


def analyze(
    records: list[Record], *, proxy_direction: str, target_direction: str,
    top_k: int = 1, min_confirmation: int = 5,
) -> dict:
    validate_records(records)
    if proxy_direction not in DIRECTIONS or target_direction not in DIRECTIONS:
        raise InputError("directions must be higher or lower")
    if isinstance(min_confirmation, bool) or not isinstance(min_confirmation, int) or min_confirmation < 2:
        raise InputError("min-confirmation must be an integer of at least 2")
    calibration = [record for record in records if record.split == "calibration"]
    confirmation = [record for record in records if record.split == "confirmation"]
    p_sign = 1 if proxy_direction == "higher" else -1
    t_sign = 1 if target_direction == "higher" else -1
    proxy = [record.proxy * p_sign for record in confirmation]
    target = [record.target * t_sign for record in confirmation]
    pairwise = pairwise_metrics(proxy, target)
    top = top_k_retention([record.id for record in confirmation], proxy, target, top_k)
    reasons: list[str] = []
    if len(confirmation) < min_confirmation:
        reasons.append("confirmation_below_configured_diagnostic_minimum")
    if len(set(proxy)) < 2:
        reasons.append("constant_proxy")
    if len(set(target)) < 2:
        reasons.append("constant_target")
    if not pairwise["jointly_strict_pairs"]:
        reasons.append("no_jointly_strict_pairs")
    if len(confirmation) < min_confirmation:
        status = "INSUFFICIENT"
    elif "constant_proxy" in reasons or "constant_target" in reasons or not pairwise["jointly_strict_pairs"]:
        status = "UNINFORMATIVE"
    else:
        status = "DIAGNOSTIC_ONLY"
    warnings = [
        "The configured minimum is a diagnostic policy, not a statistical reliability threshold.",
        "Rows and pairs are not independent replications; family counts are reported, with no cluster inference.",
        "Declared family separation cannot establish actual independence, provenance, or an untouched confirmation split.",
        "Directions, top-k, and split design must be fixed before examining confirmation results.",
        "This script does not fit, tune, or calibrate anything using the calibration split.",
        "Synthetic fixtures test implementation only, not model capability or proxy reliability.",
    ]
    if pairwise["either_tie_pairs"]:
        warnings.append("Exact numeric ties exist; average-rank correlation and strict-pair discordance answer different questions.")
    if top["boundary_tie_ambiguous"]:
        warnings.append("Top-k membership is ambiguous; use the reported overlap bounds, not a favorable tie-break.")
    return {
        "schema_version": 1,
        "status": status,
        "reasons": reasons,
        "inference_scope": SCOPE,
        "calibration_used_for_fitting": False,
        "metric_split": "confirmation",
        "directions": {"proxy": proxy_direction, "target": target_direction},
        "min_confirmation": min_confirmation,
        "counts": {
            "calibration_rows": len(calibration),
            "calibration_families": len({record.family for record in calibration}),
            "confirmation_rows": len(confirmation),
            "confirmation_families": len({record.family for record in confirmation}),
        },
        "confirmation_ids": [record.id for record in confirmation],
        "spearman": spearman(proxy, target),
        "pairwise": pairwise,
        "top_k": top,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="completed-experiment CSV path, or - for stdin")
    parser.add_argument("--proxy-direction", choices=sorted(DIRECTIONS), required=True)
    parser.add_argument("--target-direction", choices=sorted(DIRECTIONS), required=True)
    parser.add_argument("--top-k", type=int, default=1, help="candidate count, default 1")
    parser.add_argument("--min-confirmation", type=int, default=5, help="diagnostic row-count floor, not reliability; default 5")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.buffer.read() if args.csv == "-" else Path(args.csv).read_bytes()
        records = read_csv(io.StringIO(raw.decode("utf-8-sig"), newline=""))
        result = analyze(
            records, proxy_direction=args.proxy_direction, target_direction=args.target_direction,
            top_k=args.top_k, min_confirmation=args.min_confirmation,
        )
        result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    except (InputError, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc), "inference_scope": SCOPE}, ensure_ascii=False, allow_nan=False))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
