#!/usr/bin/env python3
"""Audit semantic density, overflow, and raster aspect ratios from layout boxes."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


SEMANTIC_ROLES = {"content", "heading", "data", "card"}


def _number(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def _rect(raw: dict[str, Any], label: str) -> dict[str, float]:
    rect = {
        key: _number(raw.get(key), f"{label}.{key}")
        for key in ("x", "y", "width", "height")
    }
    if rect["width"] <= 0 or rect["height"] <= 0:
        raise ValueError(f"{label} width and height must be positive")
    return rect


def _padding(raw: dict[str, Any] | None) -> dict[str, float]:
    raw = raw or {}
    return {
        key: _number(raw.get(key, 0), f"padding.{key}")
        for key in ("top", "right", "bottom", "left")
    }


def _union_length(intervals: list[tuple[float, float]]) -> float:
    if not intervals:
        return 0.0
    merged: list[list[float]] = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return sum(end - start for start, end in merged)


def _merged_intervals(intervals: list[tuple[float, float]]) -> list[list[float]]:
    merged: list[list[float]] = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def _largest_gap(
    intervals: list[tuple[float, float]],
    outer_start: float | None = None,
    outer_end: float | None = None,
) -> dict[str, float]:
    merged = _merged_intervals(intervals)
    candidates: list[tuple[float, float]] = [
        (merged[index][1], merged[index + 1][0])
        for index in range(len(merged) - 1)
    ]
    if merged and outer_start is not None:
        candidates.append((outer_start, merged[0][0]))
    if merged and outer_end is not None:
        candidates.append((merged[-1][1], outer_end))
    candidates = [(start, end) for start, end in candidates if end > start]
    if not candidates:
        anchor = outer_start or 0.0
        return {"start": anchor, "end": anchor, "pixels": 0.0}
    start, end = max(candidates, key=lambda pair: pair[1] - pair[0])
    return {"start": start, "end": end, "pixels": end - start}


def audit(
    data: dict[str, Any],
    aspect_limit: float,
    fill_floor: float,
    gap_limit: float,
    sibling_gap_limit: float = 0.06,
) -> dict[str, Any]:
    viewport = _rect({"x": 0, "y": 0, **data.get("viewport", {})}, "viewport")
    items: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(data.get("elements", [])):
        item_id = raw.get("id")
        if not isinstance(item_id, str) or not item_id:
            raise ValueError(f"elements[{index}].id must be a non-empty string")
        if item_id in items:
            raise ValueError(f"duplicate element id: {item_id}")
        items[item_id] = {
            **raw,
            "rect": _rect(raw.get("rect", {}), f"elements[{index}].rect"),
        }

    findings: list[dict[str, Any]] = []
    semantic_intervals: list[tuple[float, float]] = []

    for item_id, item in items.items():
        rect = item["rect"]
        role = item.get("role")
        if role in SEMANTIC_ROLES:
            semantic_intervals.append((rect["y"], rect["y"] + rect["height"]))

        intrinsic = item.get("intrinsic")
        if role == "asset" and intrinsic:
            iw = _number(intrinsic.get("width"), f"{item_id}.intrinsic.width")
            ih = _number(intrinsic.get("height"), f"{item_id}.intrinsic.height")
            if iw <= 0 or ih <= 0:
                raise ValueError(f"{item_id} intrinsic dimensions must be positive")
            rendered_ratio = rect["width"] / rect["height"]
            intrinsic_ratio = iw / ih
            deviation = abs(rendered_ratio / intrinsic_ratio - 1.0)
            findings.append(
                {
                    "kind": "aspect_deviation",
                    "id": item_id,
                    "value": round(deviation, 6),
                    "limit": aspect_limit,
                    "status": "review" if deviation > aspect_limit else "pass",
                    "fit": item.get("fit", "unspecified"),
                }
            )

        parent_id = item.get("parent")
        if parent_id:
            if parent_id not in items:
                raise ValueError(f"{item_id} refers to missing parent {parent_id}")
            parent = items[parent_id]
            padding = _padding(parent.get("padding"))
            pr = parent["rect"]
            bounds = {
                "left": pr["x"] + padding["left"],
                "top": pr["y"] + padding["top"],
                "right": pr["x"] + pr["width"] - padding["right"],
                "bottom": pr["y"] + pr["height"] - padding["bottom"],
            }
            overflow = max(
                bounds["left"] - rect["x"],
                bounds["top"] - rect["y"],
                rect["x"] + rect["width"] - bounds["right"],
                rect["y"] + rect["height"] - bounds["bottom"],
                0.0,
            )
            findings.append(
                {
                    "kind": "overflow",
                    "id": item_id,
                    "parent": parent_id,
                    "value": round(overflow, 3),
                    "limit": 1.0,
                    "status": "fail" if overflow > 1.0 else "pass",
                }
            )

    for container_id, container in items.items():
        if container.get("role") != "container":
            continue
        children = [
            item
            for item in items.values()
            if item.get("parent") == container_id
            and item.get("role") in SEMANTIC_ROLES
        ]
        if not children:
            continue
        padding = _padding(container.get("padding"))
        cr = container["rect"]
        usable_width = cr["width"] - padding["left"] - padding["right"]
        usable_height = cr["height"] - padding["top"] - padding["bottom"]
        if usable_width <= 0 or usable_height <= 0:
            raise ValueError(f"{container_id} padding leaves no usable interior")
        top = min(child["rect"]["y"] for child in children)
        bottom = max(
            child["rect"]["y"] + child["rect"]["height"] for child in children
        )
        area = sum(
            child["rect"]["width"] * child["rect"]["height"] for child in children
        )
        vertical_fill = min((bottom - top) / usable_height, 1.0)
        area_fill = min(area / (usable_width * usable_height), 1.0)
        child_intervals = [
            (child["rect"]["y"], child["rect"]["y"] + child["rect"]["height"])
            for child in children
        ]
        child_gap = _largest_gap(child_intervals)
        child_gap_ratio = child_gap["pixels"] / viewport["height"]
        findings.extend(
            [
                {
                    "kind": "container_vertical_fill",
                    "id": container_id,
                    "value": round(vertical_fill, 6),
                    "limit": fill_floor,
                    "status": "review" if vertical_fill < fill_floor else "pass",
                },
                {
                    "kind": "container_area_fill",
                    "id": container_id,
                    "value": round(area_fill, 6),
                    "status": "info",
                },
                {
                    "kind": "container_semantic_gap",
                    "id": container_id,
                    "value": round(child_gap_ratio, 6),
                    "pixels": round(child_gap["pixels"], 3),
                    "start": round(child_gap["start"], 3),
                    "end": round(child_gap["end"], 3),
                    "limit": sibling_gap_limit,
                    "status": (
                        "review" if child_gap_ratio > sibling_gap_limit else "pass"
                    ),
                },
            ]
        )

    largest_gap = _largest_gap(semantic_intervals)
    gap_ratio = largest_gap["pixels"] / viewport["height"]
    semantic_coverage = _union_length(semantic_intervals) / viewport["height"]
    findings.append(
        {
            "kind": "largest_semantic_gap",
            "value": round(gap_ratio, 6),
            "pixels": round(largest_gap["pixels"], 3),
            "start": round(largest_gap["start"], 3),
            "end": round(largest_gap["end"], 3),
            "limit": gap_limit,
            "status": "review" if gap_ratio > gap_limit else "pass",
        }
    )

    page_void = _largest_gap(
        semantic_intervals,
        outer_start=viewport["y"],
        outer_end=viewport["y"] + viewport["height"],
    )
    page_void_ratio = page_void["pixels"] / viewport["height"]
    findings.append(
        {
            "kind": "largest_page_void",
            "value": round(page_void_ratio, 6),
            "pixels": round(page_void["pixels"], 3),
            "start": round(page_void["start"], 3),
            "end": round(page_void["end"], 3),
            "limit": gap_limit,
            "status": "review" if page_void_ratio > gap_limit else "pass",
        }
    )

    counts = {
        status: sum(1 for finding in findings if finding["status"] == status)
        for status in ("fail", "review", "pass", "info")
    }
    return {
        "viewport": {"width": viewport["width"], "height": viewport["height"]},
        "semantic_vertical_coverage": round(semantic_coverage, 6),
        "counts": counts,
        "findings": findings,
    }


def compare_with_baseline(
    report: dict[str, Any], baseline: dict[str, Any]
) -> dict[str, Any]:
    def finding(source: dict[str, Any], kind: str) -> dict[str, Any]:
        return next(item for item in source["findings"] if item["kind"] == kind)

    current_void = finding(report, "largest_page_void")
    baseline_void = finding(baseline, "largest_page_void")
    height = report["viewport"]["height"]
    if height != baseline["viewport"]["height"]:
        raise ValueError("baseline and current viewport heights must match")
    coverage_delta = (
        report["semantic_vertical_coverage"]
        - baseline["semantic_vertical_coverage"]
    )
    void_delta = current_void["pixels"] - baseline_void["pixels"]
    location_delta = abs(current_void["start"] - baseline_void["start"])
    tolerance = max(4.0, height * 0.01)
    likely_relocated = (
        coverage_delta < 0.01
        and current_void["pixels"] >= baseline_void["pixels"] - tolerance
        and location_delta > tolerance
    )
    finding_result = {
        "kind": "whitespace_relocation",
        "status": "review" if likely_relocated else "pass",
        "coverage_delta": round(coverage_delta, 6),
        "largest_void_pixel_delta": round(void_delta, 3),
        "largest_void_start_before": baseline_void["start"],
        "largest_void_start_after": current_void["start"],
        "note": (
            "largest void moved without a material semantic coverage gain"
            if likely_relocated
            else "no likely whitespace relocation detected"
        ),
    }
    report["findings"].append(finding_result)
    report["baseline_comparison"] = finding_result
    report["counts"] = {
        status: sum(1 for item in report["findings"] if item["status"] == status)
        for status in ("fail", "review", "pass", "info")
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON manifest path, or - for stdin")
    parser.add_argument("--output", type=Path, help="write the complete JSON report here")
    parser.add_argument("--aspect-limit", type=float, default=0.05)
    parser.add_argument("--fill-floor", type=float, default=0.45)
    parser.add_argument("--gap-limit", type=float, default=0.08)
    parser.add_argument("--sibling-gap-limit", type=float, default=0.06)
    parser.add_argument(
        "--baseline", type=Path, help="compare with a before-edit manifest"
    )
    parser.add_argument(
        "--strict", action="store_true", help="return failure when review findings remain"
    )
    args = parser.parse_args()

    try:
        if args.manifest == "-":
            data = json.load(sys.stdin)
        else:
            with Path(args.manifest).open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        report = audit(
            data,
            args.aspect_limit,
            args.fill_floor,
            args.gap_limit,
            args.sibling_gap_limit,
        )
        if args.baseline:
            with args.baseline.open("r", encoding="utf-8") as handle:
                baseline_data = json.load(handle)
            baseline_report = audit(
                baseline_data,
                args.aspect_limit,
                args.fill_floor,
                args.gap_limit,
                args.sibling_gap_limit,
            )
            report = compare_with_baseline(report, baseline_report)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"layout audit error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

    if report["counts"]["fail"]:
        return 2
    if args.strict and report["counts"]["review"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
