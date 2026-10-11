#!/usr/bin/env python3
"""Audit a music prompt and mechanism card for prototype convergence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MOOD_TERMS = (
    "bittersweet",
    "cinematic",
    "emotional",
    "gentle",
    "intimate",
    "minimal",
    "restrained",
    "soft",
    "warm",
    "youthful",
    "감성적",
    "따뜻한",
    "부드러운",
    "시네마틱",
    "쓸쓸한",
    "절제된",
)
PROTOTYPE_TERMS = (
    "4/4",
    "minor",
    "repeated-note",
    "repeated note",
    "emotional lift",
    "sparse piano",
    "sustained bass",
    "distant guitar",
    "dry centered",
    "indie",
    "alternative-pop",
    "warm cinematic",
)
MECHANISM_TERMS = (
    "accompaniment waits",
    "asymmetric",
    "barline",
    "beat cycle",
    "breath",
    "cadence",
    "consonant",
    "contour",
    "density",
    "descending",
    "falling",
    "formant",
    "fundamental",
    "grain",
    "handoff",
    "meter",
    "mixed meter",
    "opening summit",
    "prediction",
    "prediction debt",
    "phrase-length",
    "phrase length",
    "raised floor",
    "rest",
    "silence",
    "stable handle",
    "spectral body",
    "two-shelf",
    "vibrato",
    "withheld",
    "invariant",
    "operator",
    "closure",
    "비대칭",
    "비브라토",
    "성대음",
    "마디",
    "박자",
    "자음",
    "질감",
    "쉼",
    "호흡",
    "하강",
    "프레이즈",
    "예측",
    "부채",
    "불변",
    "연산",
    "종결",
)
PROTO_GENRE_FIELDS = (
    "name",
    "frontier_stall",
    "inherited_shell",
    "rejected_law",
    "replacement_law",
    "predicted_effect",
    "audible_invariants",
    "allowed_variations",
    "stable_handle",
    "three_song_test",
    "generator_failure_mode",
    "rejection_condition",
)
LAW_MECHANISM_TERMS = (
    "accompaniment",
    "bar",
    "barline",
    "beat",
    "breath",
    "cadence",
    "chord",
    "contour",
    "density",
    "entrance",
    "form",
    "harmony",
    "meter",
    "phrase",
    "pulse",
    "rhythm",
    "silence",
    "voice",
    "마디",
    "박",
    "박자",
    "보컬",
    "쉼",
    "프레이즈",
    "화성",
    "호흡",
)
REQUIRED_CARD_FIELDS = (
    "frontier_stall",
    "dense_prior",
    "familiar_shell",
    "primary_axis",
    "mechanism",
    "stable_handle",
    "measurable_signature",
    "randomness_guard",
    "rejection_condition",
)
SIGNATURE_FIELDS = (
    "meter",
    "tempo_band",
    "chorus_bars",
    "phrase_vector",
    "peak_zone",
    "contour",
    "core_range",
    "hook_carrier",
    "ending_direction",
    "density_delta",
    "timbre_transform",
)
ALLOWED_AXES = {"melody", "rhythm", "harmony", "form", "lyric", "timbre"}
TIMBRE_CARD_FIELDS = (
    "voice_base",
    "spectral_body",
    "air_harmonicity",
    "grain_behavior",
    "attack_diction",
    "vibrato_behavior",
    "space",
    "inverted_default",
    "positive_replacement",
    "time_varying_event",
    "stable_identity",
    "predicted_effect",
    "rejection_condition",
    "compact_prompt",
)
SURFACE_TIMBRE_TERMS = (
    "female",
    "male",
    "alto",
    "mezzo",
    "soprano",
    "tenor",
    "baritone",
    "warm",
    "bright",
    "dark",
    "dry",
    "centered",
    "emotional",
    "여성",
    "남성",
    "알토",
    "메조",
    "소프라노",
    "테너",
    "바리톤",
    "따뜻",
    "밝",
    "어둡",
    "건조",
    "중앙",
)
DETAILED_TIMBRE_TERMS = (
    "fundamental",
    "low mid",
    "spectral",
    "harmonic",
    "air",
    "breath",
    "grain",
    "rasp",
    "fry",
    "consonant",
    "attack",
    "vibrato",
    "formant",
    "vowel",
    "reflection",
    "성대음",
    "저중역",
    "스펙트럼",
    "배음",
    "공기",
    "호흡",
    "거친",
    "질감",
    "자음",
    "어택",
    "비브라토",
    "포먼트",
    "모음",
    "초기 반사",
)
TIME_LOCATION_TERMS = (
    "phrase",
    "ending",
    "end",
    "onset",
    "attack",
    "sustain",
    "after",
    "before",
    "return",
    "first half",
    "second half",
    "프레이즈",
    "끝",
    "말미",
    "시작",
    "어택",
    "지속",
    "이후",
    "이전",
    "반복",
    "전반",
    "후반",
)
TOPLINE_CARD_FIELDS = (
    "inherited_representation",
    "rejected_law",
    "replacement_law",
    "state_variable",
    "stable_invariant",
    "return_operator",
    "cycle_closure",
    "harmony_interaction",
    "pronunciation_interaction",
    "predicted_effect",
    "measurable_signature",
    "rejection_condition",
)
TRANSFORMATION_TERMS = (
    "preserve",
    "inherit",
    "previous",
    "prior",
    "each return",
    "next phrase",
    "migrate",
    "move",
    "rotate",
    "substitute",
    "transform",
    "cycle",
    "유지",
    "상속",
    "이전",
    "매 반복",
    "다음 프레이즈",
    "이동",
    "회전",
    "대체",
    "변형",
    "순환",
)
PRONUNCIATION_CARD_FIELDS = (
    "lyric_fragment",
    "load_bearing_word",
    "spoken_baseline",
    "intelligibility_anchor",
    "phoneme_split",
    "displaced_element",
    "timing_rule",
    "vowel_trajectory",
    "consonant_role",
    "coda_release_role",
    "return_transformation",
    "semantic_effect",
    "rejection_condition",
)
PHONEME_PART_TERMS = (
    "onset",
    "nucleus",
    "coda",
    "consonant",
    "vowel",
    "초성",
    "중성",
    "종성",
    "자음",
    "모음",
)
PRONUNCIATION_TIMING_TERMS = (
    "beat",
    "pulse",
    "before",
    "after",
    "ahead",
    "behind",
    "pickup",
    "rest",
    "박",
    "맥박",
    "앞",
    "뒤",
    "당김",
    "쉼",
)
HOOKING_CARD_FIELDS = (
    "frontier_stall",
    "familiar_seed",
    "hook_mode",
    "primary_hook_axis",
    "stable_invariant",
    "listener_prediction",
    "withheld_event",
    "debt_carrier",
    "return_operator",
    "closure_return",
    "supporting_axis",
    "predicted_listener_action",
    "one_listen_test",
    "two_return_test",
    "matched_loudness_control",
    "rejection_condition",
)
VOCAL_MOTOR_HOOK_FIELDS = (
    "language",
    "actual_hook_text",
    "heard_syllable_count",
    "target_duration_seconds",
    "onset_pattern",
    "vowel_frame",
    "motor_contrast",
    "pitch_inventory_size",
    "speakable_without_pitch_test",
)
HOOK_SURFACE_TERMS = (
    "catchy",
    "earworm",
    "addictive",
    "anthemic",
    "instant hook",
    "big chorus",
    "high-note climax",
    "strong beat",
    "반복적인",
    "중독성",
    "귀에 꽂히",
    "큰 후렴",
    "고음 클라이맥스",
    "강한 비트",
)
HOOK_DEBT_TERMS = (
    "predict",
    "prediction",
    "withhold",
    "defer",
    "carry",
    "inherit",
    "unresolved",
    "restore",
    "resolve",
    "migrate",
    "rotate",
    "예측",
    "보류",
    "지연",
    "상속",
    "미해결",
    "복원",
    "해결",
    "이동",
    "회전",
)
LISTENER_ACTION_TERMS = (
    "anticipate",
    "predict",
    "hum",
    "sing",
    "clap",
    "complete",
    "supply",
    "expect",
    "예상",
    "예측",
    "흥얼",
    "노래",
    "박수",
    "완성",
    "채우",
    "기대",
)
PITCHLESS_TEST_TERMS = (
    "speak",
    "say",
    "chant",
    "without pitch",
    "pitchless",
    "말",
    "읽",
    "외치",
    "음정 없이",
    "무음정",
)


def read_text(path: str) -> str:
    return sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")


def read_json(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def contains_term(text: str, term: str) -> bool:
    if re.fullmatch(r"[a-z -]+", term):
        return re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE) is not None
    return term.lower() in text.lower()


def contains_hook_debt_mechanism(text: str) -> bool:
    english_inflection = re.search(
        r"\b(?:predict\w*|withhold\w*|defer\w*|carr(?:y|ies|ied|ying)|"
        r"inherit\w*|unresolv\w*|unfinish\w*|restor\w*|resolv\w*|"
        r"migrat\w*|rotat\w*)\b",
        text,
        re.IGNORECASE,
    )
    return bool(english_inflection) or any(
        contains_term(text, term) for term in HOOK_DEBT_TERMS
    )


def normalized_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "|".join(normalized_value(item) for item in value)
    return re.sub(r"\s+", " ", str(value).strip().lower())


def numeric_value(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    match = re.search(r"-?\d+(?:\.\d+)?", normalized_value(value))
    return float(match.group()) if match else None


def signature_from(card: dict[str, Any]) -> dict[str, str]:
    raw = card.get("measurable_signature", {})
    if not isinstance(raw, dict):
        return {}
    return {
        field: normalized_value(raw.get(field))
        for field in SIGNATURE_FIELDS
        if normalized_value(raw.get(field))
    }


def signature_similarity(
    current: dict[str, str], previous: dict[str, str]
) -> tuple[float | None, int, int]:
    shared = [
        field for field in SIGNATURE_FIELDS if current.get(field) and previous.get(field)
    ]
    if not shared:
        return None, 0, 0
    matches = sum(current[field] == previous[field] for field in shared)
    return matches / len(shared), matches, len(shared)


def audit_proto_genre(value: Any) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, dict):
        return None, ["proto_genre must be a JSON object, not a genre-name string"]

    warnings = []
    missing = [
        field for field in PROTO_GENRE_FIELDS if not normalized_value(value.get(field))
    ]
    if missing:
        warnings.append("proto-genre card is missing: " + ", ".join(missing))

    invariants = value.get("audible_invariants", [])
    if not isinstance(invariants, list) or len(
        [item for item in invariants if normalized_value(item)]
    ) != 3:
        warnings.append("proto-genre must define exactly three audible invariants")

    variations = value.get("allowed_variations", [])
    if not isinstance(variations, list) or len(
        [item for item in variations if normalized_value(item)]
    ) < 3:
        warnings.append(
            "allowed_variations must list at least three changing dimensions"
        )

    rejected = normalized_value(value.get("rejected_law"))
    replacement = normalized_value(value.get("replacement_law"))
    if rejected and replacement and rejected == replacement:
        warnings.append("rejected_law and replacement_law must differ")
    if replacement and not any(
        contains_term(replacement, term) for term in LAW_MECHANISM_TERMS
    ):
        warnings.append(
            "replacement_law appears surface-level; name a phrase, meter, harmony, rhythm, or arrangement mechanism"
        )

    transfer_test = normalized_value(value.get("three_song_test"))
    if transfer_test and not re.search(r"(?:\b3\b|\bthree\b|세\s*곡|삼\s*곡)", transfer_test):
        warnings.append("three_song_test must require transfer across three songs")

    return {
        "name": value.get("name"),
        "missing_fields": missing,
        "audible_invariant_count": len(invariants)
        if isinstance(invariants, list)
        else 0,
        "allowed_variation_count": len(variations)
        if isinstance(variations, list)
        else 0,
    }, warnings


def audit_timbre_card(
    value: Any, prompt: str
) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, dict):
        return None, ["timbre_card must be a JSON object, not a timbre label"]

    warnings = []
    missing = [
        field for field in TIMBRE_CARD_FIELDS if not normalized_value(value.get(field))
    ]
    if missing:
        warnings.append("timbre card is missing: " + ", ".join(missing))

    inverted = normalized_value(value.get("inverted_default"))
    replacement = normalized_value(value.get("positive_replacement"))
    if inverted and replacement and inverted == replacement:
        warnings.append("inverted_default and positive_replacement must differ")
    if replacement and not any(
        contains_term(replacement, term) for term in DETAILED_TIMBRE_TERMS
    ):
        warnings.append(
            "positive_replacement must name an acoustic or articulatory property"
        )

    event = normalized_value(value.get("time_varying_event"))
    if event and not any(
        contains_term(event, term) for term in TIME_LOCATION_TERMS
    ):
        warnings.append(
            "time_varying_event must locate the timbre change inside a phrase or note"
        )

    compact = normalized_value(value.get("compact_prompt"))
    inspected_prompt = compact or prompt
    surface_hits = [
        term for term in SURFACE_TIMBRE_TERMS if contains_term(inspected_prompt, term)
    ]
    detail_hits = [
        term for term in DETAILED_TIMBRE_TERMS if contains_term(inspected_prompt, term)
    ]
    negative_guards = re.findall(
        r"\b(?:no|not|never|without)\b|(?:금지|없게|않게)",
        inspected_prompt,
        re.IGNORECASE,
    )
    if inspected_prompt and len(detail_hits) < 4:
        warnings.append(
            "timbre prompt is under-specified; voice type, register, mood, and mix position do not define timbre"
        )
    if len(negative_guards) > 2 and len(detail_hits) < 5:
        warnings.append(
            "negative guards dominate; replace exclusions with positive acoustic instructions"
        )

    return {
        "missing_fields": missing,
        "surface_label_hits": surface_hits,
        "detailed_property_hits": detail_hits,
        "negative_guard_count": len(negative_guards),
        "has_time_location": bool(
            event
            and any(contains_term(event, term) for term in TIME_LOCATION_TERMS)
        ),
    }, warnings


def audit_topline_card(
    value: Any,
) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, dict):
        return None, ["topline_invention_card must be a JSON object, not a technique name"]

    warnings = []
    missing = [
        field for field in TOPLINE_CARD_FIELDS if not normalized_value(value.get(field))
    ]
    if missing:
        warnings.append("topline invention card is missing: " + ", ".join(missing))

    replacement = normalized_value(value.get("replacement_law"))
    operator = normalized_value(value.get("return_operator"))
    invariant = normalized_value(value.get("stable_invariant"))
    combined_law = f"{replacement} {operator}"
    if combined_law.strip() and not any(
        contains_term(combined_law, term) for term in TRANSFORMATION_TERMS
    ):
        warnings.append(
            "topline law names a shape or mood but no return-to-return transformation"
        )
    if operator and invariant and operator == invariant:
        warnings.append("return_operator and stable_invariant must differ")

    closure = normalized_value(value.get("cycle_closure"))
    if closure and not re.search(
        r"(?:\b[2-9]\b|\b(?:two|three|four)\b|[2-9]\s*(?:회|번째)|둘째|셋째|넷째)",
        closure,
    ):
        warnings.append("cycle_closure must name the return on which the law resolves")

    return {
        "missing_fields": missing,
        "has_transform_operator": any(
            contains_term(combined_law, term) for term in TRANSFORMATION_TERMS
        ),
        "has_numbered_closure": bool(
            closure
            and re.search(
                r"(?:\b[2-9]\b|\b(?:two|three|four)\b|[2-9]\s*(?:회|번째)|둘째|셋째|넷째)",
                closure,
            )
        ),
    }, warnings


def audit_pronunciation_card(
    value: Any,
) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, dict):
        return None, ["pronunciation_card must be a JSON object, not a diction label"]

    warnings = []
    missing = [
        field
        for field in PRONUNCIATION_CARD_FIELDS
        if not normalized_value(value.get(field))
    ]
    if missing:
        warnings.append("pronunciation card is missing: " + ", ".join(missing))

    split = normalized_value(value.get("phoneme_split"))
    split_hits = [
        term for term in PHONEME_PART_TERMS if contains_term(split, term)
    ]
    if split and len(split_hits) < 2:
        warnings.append(
            "phoneme_split must separate at least two of onset, vowel nucleus, and coda"
        )

    timing = normalized_value(value.get("timing_rule"))
    if timing and not any(
        contains_term(timing, term) for term in PRONUNCIATION_TIMING_TERMS
    ):
        warnings.append(
            "timing_rule must place a phoneme before, on, or after a beat, pulse, or rest"
        )

    transformation = normalized_value(value.get("return_transformation"))
    if transformation and not any(
        contains_term(transformation, term) for term in TRANSFORMATION_TERMS
    ):
        warnings.append(
            "return_transformation must define a repeated pronunciation change"
        )

    return {
        "missing_fields": missing,
        "phoneme_part_hits": split_hits,
        "has_timing_relation": bool(
            timing
            and any(
                contains_term(timing, term)
                for term in PRONUNCIATION_TIMING_TERMS
            )
        ),
    }, warnings


def audit_hooking_card(
    value: Any, lyrics: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, dict):
        return None, ["hooking_card must be a JSON object, not a catchiness label"]

    warnings = []
    missing = [
        field for field in HOOKING_CARD_FIELDS if not normalized_value(value.get(field))
    ]
    if missing:
        warnings.append("hooking card is missing: " + ", ".join(missing))

    hook_mode = normalized_value(value.get("hook_mode"))
    if hook_mode and hook_mode not in {"vocal", "instrumental", "보컬", "연주"}:
        warnings.append("hook_mode must be vocal or instrumental")

    vocal_missing: list[str] = []
    literal_return_count = 0
    if hook_mode in {"vocal", "보컬"}:
        vocal_missing = [
            field
            for field in VOCAL_MOTOR_HOOK_FIELDS
            if not normalized_value(value.get(field))
        ]
        if vocal_missing:
            warnings.append(
                "vocal mouth-first hook is missing: " + ", ".join(vocal_missing)
            )

        language = normalized_value(value.get("language"))
        actual_text = normalized_value(value.get("actual_hook_text"))
        if (
            actual_text
            and language in {"ko", "kor", "korean", "한국어"}
            and not re.search(r"[가-힣]", actual_text)
        ):
            warnings.append("Korean actual_hook_text must contain literal Hangul lyrics")
        if actual_text and language in {"en", "eng", "english", "영어"}:
            if not re.search(r"[A-Za-z]", actual_text):
                warnings.append(
                    "English actual_hook_text must contain the literal sung words"
                )
            words = re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", actual_text)
            if len(words) > 6:
                warnings.append(
                    f"English hook has {len(words)} words; a motor cell that must be "
                    "singable after one listen rarely exceeds six"
                )
            if re.search(r"[bcdfghjklmnpqrstvwxz]{4,}", actual_text, re.IGNORECASE):
                warnings.append(
                    "English hook contains a four-plus consonant cluster; verify it is "
                    "singable at tempo"
                )

        heard_syllables = numeric_value(value.get("heard_syllable_count"))
        if heard_syllables is not None and not 3 <= heard_syllables <= 7:
            warnings.append("heard_syllable_count should be between 3 and 7")

        duration = numeric_value(value.get("target_duration_seconds"))
        if duration is not None and not 0.8 <= duration <= 1.5:
            warnings.append(
                "target_duration_seconds should keep the motor cell near 0.8-1.5 seconds"
            )

        pitch_count = numeric_value(value.get("pitch_inventory_size"))
        if pitch_count is not None and not 1 <= pitch_count <= 3:
            warnings.append(
                "pitch_inventory_size should be 1-3 so the mouth gesture stays primary"
            )

        pitchless_test = normalized_value(value.get("speakable_without_pitch_test"))
        if pitchless_test and not any(
            contains_term(pitchless_test, term) for term in PITCHLESS_TEST_TERMS
        ):
            warnings.append(
                "speakable_without_pitch_test must require speaking or chanting without pitch"
            )

        if actual_text and lyrics:
            literal_return_count = normalized_value(lyrics).count(actual_text)
            if literal_return_count < 2:
                warnings.append(
                    "actual_hook_text must recur literally at least twice in the supplied lyrics"
                )
        elif actual_text:
            warnings.append(
                "vocal mouth-first hook requires supplied lyrics for literal-return audit"
            )

    axis = normalized_value(value.get("primary_hook_axis"))
    if axis and axis not in ALLOWED_AXES:
        warnings.append(
            "primary_hook_axis must name exactly one of: "
            + ", ".join(sorted(ALLOWED_AXES))
        )

    invariant = normalized_value(value.get("stable_invariant"))
    withheld = normalized_value(value.get("withheld_event"))
    if invariant and withheld and invariant == withheld:
        warnings.append("stable_invariant and withheld_event must differ")

    law = " ".join(
        normalized_value(value.get(field))
        for field in ("listener_prediction", "debt_carrier", "return_operator")
    )
    if law.strip() and not contains_hook_debt_mechanism(law):
        warnings.append(
            "hook law adds intensity or repetition but no prediction debt carried across returns"
        )

    closure = normalized_value(value.get("closure_return"))
    closure_pattern = (
        r"(?:\b[2-9]\b|\b(?:two|three|four)\b|"
        r"[2-9]\s*(?:회|번째)|둘째|셋째|넷째)"
    )
    if closure and not re.search(closure_pattern, closure):
        warnings.append("closure_return must name the return where the debt resolves")

    action = normalized_value(value.get("predicted_listener_action"))
    if action and not any(
        contains_term(action, term) for term in LISTENER_ACTION_TERMS
    ):
        warnings.append(
            "predicted_listener_action must be observable, such as humming, clapping, anticipating, or completing"
        )

    supporting = value.get("supporting_axis")
    support_count = (
        len([item for item in supporting if normalized_value(item)])
        if isinstance(supporting, (list, tuple))
        else (0 if normalized_value(supporting) in {"", "none", "없음"} else 1)
    )
    if support_count > 1:
        warnings.append("hooking card may use at most one supporting axis")

    return {
        "missing_fields": missing,
        "vocal_motor_missing_fields": vocal_missing,
        "literal_hook_return_count": literal_return_count,
        "has_prediction_debt": contains_hook_debt_mechanism(law),
        "has_numbered_closure": bool(
            closure and re.search(closure_pattern, closure)
        ),
        "supporting_axis_count": support_count,
        "has_observable_listener_action": any(
            contains_term(action, term) for term in LISTENER_ACTION_TERMS
        ),
    }, warnings


def audit(
    prompt: str,
    card: dict[str, Any] | None,
    previous_cards: list[tuple[str, dict[str, Any]]],
    lyrics: str = "",
) -> dict[str, Any]:
    mood_hits = [term for term in MOOD_TERMS if contains_term(prompt, term)]
    prototype_hits = [term for term in PROTOTYPE_TERMS if contains_term(prompt, term)]
    mechanism_hits = [term for term in MECHANISM_TERMS if contains_term(prompt, term)]
    hook_surface_hits = [
        term for term in HOOK_SURFACE_TERMS if contains_term(prompt, term)
    ]
    numeric_constraints = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:%|bpm|bars?|beats?|semitones?|초|마디|박)\b",
        prompt,
        re.IGNORECASE,
    )
    warnings: list[str] = []

    if len(mood_hits) >= 6 and len(mechanism_hits) + len(numeric_constraints) < 2:
        warnings.append(
            "mood adjectives dominate while causal or measurable instructions are scarce"
        )
    if len(prototype_hits) >= 6:
        warnings.append(
            "prompt contains a dense familiar prototype cluster; name one mechanism that departs from it"
        )

    missing_fields: list[str] = []
    signature: dict[str, str] = {}
    proto_genre_report = None
    timbre_card_report = None
    topline_card_report = None
    pronunciation_card_report = None
    hooking_card_report = None
    if card is None:
        warnings.append("no mechanism card supplied; recent-output convergence cannot be audited")
    else:
        missing_fields = [
            field
            for field in REQUIRED_CARD_FIELDS
            if not normalized_value(card.get(field))
        ]
        if missing_fields:
            warnings.append(
                "mechanism card is missing: " + ", ".join(missing_fields)
            )
        axis = normalized_value(card.get("primary_axis"))
        if axis and axis not in ALLOWED_AXES:
            warnings.append(
                "primary_axis must name exactly one of: "
                + ", ".join(sorted(ALLOWED_AXES))
            )
        signature = signature_from(card)
        if card.get("measurable_signature") and not signature:
            warnings.append(
                "measurable_signature must be an object with populated signature fields"
            )
        if signature and len(signature) < 5:
            warnings.append(
                "fewer than five signature fields are populated; comparison is weak"
            )
        proto_genre_report, proto_genre_warnings = audit_proto_genre(
            card.get("proto_genre")
        )
        warnings.extend(proto_genre_warnings)
        timbre_card_report, timbre_card_warnings = audit_timbre_card(
            card.get("timbre_card"), prompt
        )
        warnings.extend(timbre_card_warnings)
        topline_card_report, topline_card_warnings = audit_topline_card(
            card.get("topline_invention_card")
        )
        warnings.extend(topline_card_warnings)
        pronunciation_card_report, pronunciation_card_warnings = (
            audit_pronunciation_card(card.get("pronunciation_card"))
        )
        warnings.extend(pronunciation_card_warnings)
        hooking_card_report, hooking_card_warnings = audit_hooking_card(
            card.get("hooking_card"), lyrics
        )
        warnings.extend(hooking_card_warnings)
        if card.get("genre_name") and card.get("proto_genre") is None:
            warnings.append(
                "genre_name is only a label; provide a proto_genre card with a replacement law"
            )
        if card.get("timbre_label") and card.get("timbre_card") is None:
            warnings.append(
                "timbre_label is only a surface label; provide a time-varying timbre_card"
            )
        if axis == "timbre" and card.get("timbre_card") is None:
            warnings.append(
                "primary_axis is timbre but no timbre_card defines its acoustic behavior"
            )
        if card.get("melodic_technique") and card.get("topline_invention_card") is None:
            warnings.append(
                "melodic_technique is a named trick; provide a topline_invention_card with an invariant, operator, and closure"
            )
        if axis == "melody" and card.get("topline_invention_card") is None:
            warnings.append(
                "primary_axis is melody but no topline_invention_card defines how returns transform"
            )
        if card.get("pronunciation_style") and card.get("pronunciation_card") is None:
            warnings.append(
                "pronunciation_style is only a diction label; provide a phoneme-level pronunciation_card"
            )
        if (
            (card.get("hook_method") or hook_surface_hits)
            and card.get("hooking_card") is None
        ):
            warnings.append(
                "catchiness or hook labels do not define a listener mechanism; provide a hooking_card"
            )

    comparisons = []
    near_duplicate_count = 0
    for path, previous_card in previous_cards:
        previous_signature = signature_from(previous_card)
        similarity, matches, compared = signature_similarity(
            signature, previous_signature
        )
        comparison = {
            "path": path,
            "similarity": round(similarity, 3) if similarity is not None else None,
            "matching_fields": matches,
            "compared_fields": compared,
        }
        comparisons.append(comparison)
        if similarity is not None and compared >= 5 and similarity >= 0.75:
            near_duplicate_count += 1

    if near_duplicate_count >= 2:
        warnings.append(
            "signature matches two recent drafts at 75% or more; switch the primary axis or causal mechanism"
        )
    elif near_duplicate_count == 1:
        warnings.append(
            "signature matches a recent draft at 75% or more; verify that this is intentional"
        )

    return {
        "mood_tag_hits": mood_hits,
        "prototype_cluster_hits": prototype_hits,
        "mechanism_term_hits": mechanism_hits,
        "hook_surface_hits": hook_surface_hits,
        "numeric_constraints": numeric_constraints,
        "missing_card_fields": missing_fields,
        "signature": signature,
        "proto_genre": proto_genre_report,
        "timbre_card": timbre_card_report,
        "topline_invention_card": topline_card_report,
        "pronunciation_card": pronunciation_card_report,
        "hooking_card": hooking_card_report,
        "recent_comparisons": comparisons,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        required=True,
        help="UTF-8 prompt file, or '-' to read from standard input",
    )
    parser.add_argument("--card", help="Mechanism card as a JSON object")
    parser.add_argument("--lyrics", help="UTF-8 lyrics file for literal hook audit")
    parser.add_argument(
        "--compare-card",
        action="append",
        default=[],
        help="Recent mechanism card to compare; repeat for multiple drafts",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    try:
        prompt = read_text(args.prompt)
        lyrics = read_text(args.lyrics) if args.lyrics else ""
        card = read_json(args.card) if args.card else None
        previous_cards = [(path, read_json(path)) for path in args.compare_card]
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    report = audit(prompt, card, previous_cards, lyrics=lyrics)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"mood tags: {report['mood_tag_hits']}")
        print(f"prototype cluster: {report['prototype_cluster_hits']}")
        print(f"mechanism terms: {report['mechanism_term_hits']}")
        print(f"hook surface terms: {report['hook_surface_hits']}")
        print(f"numeric constraints: {report['numeric_constraints']}")
        if report["signature"]:
            print(f"signature: {report['signature']}")
        if report["proto_genre"]:
            print(f"proto-genre: {report['proto_genre']}")
        if report["timbre_card"]:
            print(f"timbre-card: {report['timbre_card']}")
        if report["topline_invention_card"]:
            print(f"topline-invention-card: {report['topline_invention_card']}")
        if report["pronunciation_card"]:
            print(f"pronunciation-card: {report['pronunciation_card']}")
        if report["hooking_card"]:
            print(f"hooking-card: {report['hooking_card']}")
        for comparison in report["recent_comparisons"]:
            print(
                "comparison: "
                f"{comparison['path']} similarity={comparison['similarity']} "
                f"fields={comparison['matching_fields']}/{comparison['compared_fields']}"
            )
        for warning in report["warnings"]:
            print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
