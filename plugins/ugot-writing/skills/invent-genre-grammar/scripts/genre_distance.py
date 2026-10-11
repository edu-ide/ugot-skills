#!/usr/bin/env python3
"""Measure how far a genre spec is from recent specs on six constitutive laws.

A convergence detector, not a taste judge. Reports per-axis agreement, an overall
distance, tempo and palette proximity, and the atlas law values that none of the
supplied specs has ever used.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


AXES = (
    "time_law",
    "density_law",
    "harmony_law",
    "form_law",
    "voice_law",
    "production_law",
)

# Controlled vocabularies drawn from references/genre-atlas.md. Free text is
# still accepted; it is matched by token overlap instead of exact identity.
VOCAB: dict[str, tuple[str, ...]] = {
    "time_law": (
        "isochronous-backbeat",
        "asymmetric-timeline",
        "clave",
        "additive-aksak",
        "colotomic-cycle",
        "tala-cycle",
        "cyclic-accelerating",
        "triple-duple-ambiguous",
        "free-rubato",
        "breath-clocked",
        "speech-clocked",
        "hyper-tempo",
        "pulseless",
    ),
    "density_law": (
        "straight",
        "swung",
        "offbeat-hats",
        "bass-punctuation",
        "triple-against-duple",
        "interlocking-subdivision",
        "breakbeat-split-tempo",
        "kick-clusters",
        "blast-density",
        "negative-density",
        "behind-the-beat",
    ),
    "harmony_law": (
        "functional-diatonic",
        "extended-chord-density",
        "modal-loop",
        "two-chord-vamp",
        "static-drone",
        "riff-as-harmony",
        "borrowed-chord-surprise",
        "non-western-scalar",
        "quartal-planing",
        "sample-as-harmony",
        "absent",
    ),
    "form_law": (
        "verse-chorus",
        "riddim-and-versions",
        "cyclic-no-chorus",
        "colotomic-gong-cycle",
        "call-and-response",
        "build-drop",
        "through-composed",
        "loop-with-mutation",
        "escalating-repetition",
        "abrupt-juxtaposition",
    ),
    "voice_law": (
        "belted",
        "melismatic-portamento",
        "spoken-mc",
        "shouted-chant",
        "whispered-close",
        "choral-unison",
        "call-and-response",
        "processed-as-instrument",
        "conversational-melodic",
        "declaimed-flat",
        "absent",
    ),
    "production_law": (
        "dry-close",
        "desk-as-instrument",
        "distortion-as-texture",
        "space-as-content",
        "lo-fi-artifact",
        "hyper-clean",
        "mono-forward",
        "no-low-end",
        "live-room",
        "sub-forward",
    ),
}

TOKEN_RE = re.compile(r"[a-z0-9]+")
MIN_DIFFERING_AXES = 3


def tokens(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, (list, tuple)):
        value = " ".join(str(item) for item in value)
    return set(TOKEN_RE.findall(str(value).lower()))


def canonical(axis: str, value: Any) -> str | None:
    """Map a free-text axis value onto the atlas vocabulary when possible."""
    if value is None:
        return None
    raw = str(value).strip().lower().replace("_", "-").replace(" ", "-")
    if not raw:
        return None
    vocab = VOCAB[axis]
    if raw in vocab:
        return raw
    supplied = tokens(value)
    best: tuple[float, str | None] = (0.0, None)
    for candidate in vocab:
        candidate_tokens = set(candidate.split("-"))
        overlap = len(supplied & candidate_tokens)
        # One shared generic token ("cycle", "close") is not a match; a
        # multi-word law must agree on at least two of its words.
        if overlap < min(2, len(candidate_tokens)):
            continue
        score = overlap / len(candidate_tokens) if candidate_tokens else 0.0
        if score > best[0]:
            best = (score, candidate)
    return best[1] if best[0] >= 0.5 else None


def axis_agreement(axis: str, left: Any, right: Any) -> tuple[bool, float]:
    """Return (counts as the same law, similarity in [0,1])."""
    left_canonical = canonical(axis, left)
    right_canonical = canonical(axis, right)
    if left_canonical and right_canonical:
        return left_canonical == right_canonical, 1.0 if left_canonical == right_canonical else 0.0
    left_tokens, right_tokens = tokens(left), tokens(right)
    if not left_tokens or not right_tokens:
        return False, 0.0
    jaccard = len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
    ratio = SequenceMatcher(None, str(left).lower(), str(right).lower()).ratio()
    similarity = max(jaccard, ratio)
    return similarity >= 0.6, similarity


def tempo_of(spec: dict[str, Any]) -> float | None:
    for key in ("tempo", "bpm", "tempo_band"):
        if key not in spec:
            continue
        numbers = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", str(spec[key]))]
        if numbers:
            return sum(numbers) / len(numbers)
    return None


def compare(spec: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
    per_axis = {}
    same_count = 0
    for axis in AXES:
        same, similarity = axis_agreement(axis, spec.get(axis), other.get(axis))
        per_axis[axis] = {"same_law": same, "similarity": round(similarity, 3)}
        same_count += int(same)
    differing = len(AXES) - same_count
    palette_left, palette_right = tokens(spec.get("palette")), tokens(other.get("palette"))
    palette_overlap = (
        len(palette_left & palette_right) / len(palette_left | palette_right)
        if palette_left and palette_right
        else 0.0
    )
    left_tempo, right_tempo = tempo_of(spec), tempo_of(other)
    tempo_gap = (
        abs(left_tempo - right_tempo)
        if left_tempo is not None and right_tempo is not None
        else None
    )
    return {
        "name": other.get("name") or other.get("_path", "recent"),
        "per_axis": per_axis,
        "same_law_axes": same_count,
        "differing_axes": differing,
        "distance": round(differing / len(AXES), 3),
        "palette_overlap": round(palette_overlap, 3),
        "tempo_gap_bpm": None if tempo_gap is None else round(tempo_gap, 1),
    }


def unused_vocabulary(specs: list[dict[str, Any]]) -> dict[str, list[str]]:
    unused: dict[str, list[str]] = {}
    for axis in AXES:
        used = {
            value
            for spec in specs
            if (value := canonical(axis, spec.get(axis))) is not None
        }
        missing = [value for value in VOCAB[axis] if value not in used]
        if missing:
            unused[axis] = missing
    return unused


def audit(spec: dict[str, Any], recents: list[dict[str, Any]]) -> dict[str, Any]:
    warnings: list[str] = []

    missing_axes = [axis for axis in AXES if not str(spec.get(axis, "")).strip()]
    if missing_axes:
        warnings.append(
            "spec does not state every law axis: " + ", ".join(missing_axes)
        )
    unmapped = [
        axis
        for axis in AXES
        if str(spec.get(axis, "")).strip() and canonical(axis, spec.get(axis)) is None
    ]
    if unmapped:
        warnings.append(
            "these axes did not map onto the atlas vocabulary, so they are compared "
            "as free text only: " + ", ".join(unmapped)
        )

    comparisons = [compare(spec, other) for other in recents]
    for item in comparisons:
        if item["differing_axes"] < MIN_DIFFERING_AXES:
            warnings.append(
                f"{item['name']}: only {item['differing_axes']} of {len(AXES)} law axes "
                f"differ; fewer than {MIN_DIFFERING_AXES} is a re-skin, not a new genre"
            )
        if item["tempo_gap_bpm"] is not None and item["tempo_gap_bpm"] <= 6:
            warnings.append(
                f"{item['name']}: tempo is within {item['tempo_gap_bpm']} BPM; verify the "
                "time law actually changed rather than the palette"
            )
        if item["palette_overlap"] >= 0.5:
            warnings.append(
                f"{item['name']}: palette overlap is {item['palette_overlap']}; a shared "
                "instrument list pulls the render back to the same neighborhood"
            )
    if comparisons:
        # Report unexamined defaults unconditionally: they matter most precisely
        # when convergence is worst.
        identical_axes = [
            axis
            for axis in AXES
            if all(item["per_axis"][axis]["same_law"] for item in comparisons)
        ]
        if identical_axes:
            warnings.append(
                "these axes are identical across every compared spec, so they are your "
                "unexamined default: " + ", ".join(identical_axes)
            )

    unused = unused_vocabulary([spec, *recents])
    return {
        "spec_name": spec.get("name", "candidate"),
        "spec_laws": {axis: spec.get(axis) for axis in AXES},
        "canonical_laws": {axis: canonical(axis, spec.get(axis)) for axis in AXES},
        "comparisons": comparisons,
        "min_differing_axes": min(
            (item["differing_axes"] for item in comparisons), default=None
        ),
        "unused_law_inventory": unused,
        "warnings": warnings,
    }


def load(path: str) -> dict[str, Any]:
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: spec must be a JSON object")
    data.setdefault("_path", path)
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spec", required=True, help="Candidate spec JSON, or '-' for standard input"
    )
    parser.add_argument(
        "--compare",
        action="append",
        default=[],
        help="Recent spec JSON to compare against; repeat for multiple specs",
    )
    parser.add_argument(
        "--list-vocab", action="store_true", help="Print the atlas vocabulary and exit"
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.list_vocab:
        for axis in AXES:
            print(f"{axis}: {', '.join(VOCAB[axis])}")
        return 0

    try:
        spec = load(args.spec)
        recents = [load(path) for path in args.compare]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    report = audit(spec, recents)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"spec: {report['spec_name']}")
    for axis in AXES:
        canonical_value = report["canonical_laws"][axis]
        shown = canonical_value or f"(free text) {report['spec_laws'][axis]}"
        print(f"  {axis}: {shown}")
    for item in report["comparisons"]:
        print(
            f"vs {item['name']}: distance={item['distance']} "
            f"differing_axes={item['differing_axes']}/{len(AXES)} "
            f"tempo_gap={item['tempo_gap_bpm']} palette_overlap={item['palette_overlap']}"
        )
        same = [axis for axis in AXES if item["per_axis"][axis]["same_law"]]
        if same:
            print(f"    shared laws: {', '.join(same)}")
    if report["unused_law_inventory"]:
        print("unused law inventory (never used in any compared spec):")
        for axis, values in report["unused_law_inventory"].items():
            print(f"  {axis}: {', '.join(values)}")
    for warning in report["warnings"]:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
