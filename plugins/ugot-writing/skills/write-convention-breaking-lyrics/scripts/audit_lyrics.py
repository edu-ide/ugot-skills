#!/usr/bin/env python3
"""Report structural, familiarity, and mouth-feel lyric diagnostics.

Bilingual: English (stress-timed) and Korean (syllable-timed). Language is
detected per line unless --lang forces one. Use --suno to add Suno
lyrics-field checks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


SECTION_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")
HANGUL_RE = re.compile(r"[가-힣]")
LATIN_WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
NUMBER_RE = re.compile(r"\d+")
WORD_RE = re.compile(r"[가-힣A-Za-z0-9'’]+")

KOREAN_COMMON_SYMBOLS = {
    "사랑",
    "이별",
    "그리움",
    "외로움",
    "슬픔",
    "아픔",
    "눈물",
    "기억",
    "마음",
    "운명",
    "영원",
    "별",
    "빛",
    "그림자",
    "창문",
    "계절",
}
ENGLISH_COMMON_SYMBOLS = {
    "heart",
    "hearts",
    "soul",
    "souls",
    "night",
    "nights",
    "star",
    "stars",
    "fire",
    "flames",
    "rain",
    "tear",
    "tears",
    "forever",
    "alive",
    "broken",
    "shadow",
    "shadows",
    "dream",
    "dreams",
    "sky",
    "skies",
    "light",
    "lights",
    "memory",
    "memories",
    "goodbye",
    "arms",
    "gold",
    "golden",
    "ashes",
    "storm",
    "wings",
    "ghost",
    "ghosts",
    "neon",
    "midnight",
    "ocean",
    "empty",
    "bones",
    "blood",
    "endless",
    "eternity",
    "paradise",
}
KOREAN_HEALING_ASSURANCES = (
    "괜찮아질 거야",
    "다 잘될 거야",
    "다 지나갈 거야",
    "시간이 약이야",
    "다시 일어나",
    "너는 혼자가 아니야",
    "안 괜찮아도 돼",
    "있는 그대로도 괜찮아",
    "상처는 아물",
    "빛이 되어",
)
ENGLISH_HEALING_ASSURANCES = (
    "it's gonna be alright",
    "it's going to be alright",
    "everything will be fine",
    "everything's gonna be okay",
    "you'll be okay",
    "you are not alone",
    "you're not alone",
    "you are enough",
    "you're enough",
    "just breathe",
    "hold on",
    "stay strong",
    "it gets better",
    "time heals",
    "this too shall pass",
    "the sun will rise",
    "let it go",
    "i'll be your light",
    "you'll find your way",
)
KOREAN_MEDICAL_CLAIM_PATTERNS = (
    re.compile(r"(?:몸|마음|상처|병).{0,8}(?:치유|치료|완치)"),
    re.compile(r"(?:치유|치료|완치).{0,8}(?:해\s*줄게|시켜\s*줄게|될\s*거야)"),
    re.compile(
        r"\d{3}\s*(?:hz|헤르츠).{0,10}(?:치유|치료|낫게|고쳐)",
        re.IGNORECASE,
    ),
    re.compile(r"(?:노래|사랑|주파수).{0,10}(?:병을|몸을)?.{0,5}(?:고쳐|낫게)"),
)
ENGLISH_MEDICAL_CLAIM_PATTERNS = (
    re.compile(
        r"\b(?:heal|heals|healing|cure|cures|curing|fix|fixes)\b[^.\n]{0,24}"
        r"\b(?:body|bodies|mind|minds|soul|wound|wounds|pain|illness|disease|sickness|cells)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\d{3}\s*(?:hz|hertz)[^.\n]{0,30}"
        r"\b(?:heal|heals|healing|cure|repair|restore|dna|cells|universe)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:this song|my love|the frequency|this sound)\b[^.\n]{0,20}"
        r"\b(?:will\s+)?(?:heal|cure|save)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:i(?:'ll| will)|we(?:'ll| will))\b[^.\n]{0,16}\b(?:heal|cure|fix)\b"
        r"[^.\n]{0,16}\b(?:you|your)\b",
        re.IGNORECASE,
    ),
)
SECTION_ALIASES = (
    ("pre-chorus", ("pre-chorus", "prechorus", "pre chorus", "프리코러스")),
    ("post-chorus", ("post-chorus", "postchorus", "post chorus", "포스트코러스")),
    ("chorus", ("chorus", "hook", "후렴", "코러스")),
    ("verse", ("verse", "벌스", "절")),
    ("bridge", ("bridge", "브리지")),
    ("intro", ("intro", "인트로")),
    ("outro", ("outro", "아웃트로")),
    ("refrain", ("refrain", "리프레인")),
)
CHOSEONG = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
JUNGSEONG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
OPEN_BREATH_PUNCTUATION = (",", "，", ";", "；", "…", "...")
CUTOFF_PUNCTUATION = ("-", "—", "–", "--")
CLOSED_BREATH_PUNCTUATION = (".", "。", "!", "！", "?", "？")
KOREAN_CONNECTIVE_ENDINGS = (
    "지만",
    "는데",
    "은데",
    "ㄴ데",
    "면서",
    "으며",
    "다가",
    "니까",
    "으니까",
    "도록",
    "거나",
    "든지",
    "려고",
    "으려고",
    "고",
    "며",
    "면",
    "으면",
    "서",
)
# A Korean line ending on a case, topic, or adnominal particle leaves the clause
# unfinished, which is the same debt a connective ending creates. Single-syllable
# particles can false-positive on a word that merely ends in that syllable; the
# label is a diagnostic prompt, not a parse.
KOREAN_UNFINISHED_PARTICLES = (
    "에서",
    "으로",
    "부터",
    "까지",
    "보다",
    "처럼",
    "한테",
    "에게",
    "이나",
    "라도",
    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "에",
    "로",
    "와",
    "과",
    "도",
    "만",
    "의",
)
# An English line ending on one of these leaves the syntax unfinished: the next
# breath must pay that debt. This is the English analogue of a connective ending.
ENGLISH_INHERITED_ENDINGS = {
    "and", "but", "or", "so", "because", "cause", "'cause", "that", "which",
    "who", "when", "while", "if", "though", "although", "than", "as", "till",
    "until", "unless", "before", "after", "since", "whether", "like",
    "to", "of", "for", "with", "from", "into", "onto", "on", "in", "at", "by",
    "about", "over", "under", "through", "without", "against", "between",
    "the", "a", "an", "my", "your", "his", "her", "their", "our", "its",
    "this", "these", "those", "every", "some", "any", "no", "another", "each",
    "is", "are", "was", "were", "be", "been", "being", "am", "do", "does",
    "did", "can", "could", "will", "would", "should", "shall", "might", "must",
    "have", "has", "had", "ain't", "aint", "gonna", "wanna", "gotta",
    "still", "just", "almost", "half", "not", "never", "always",
}
# Function words carry no lexical stress in ordinary speech, so the count of the
# remaining content words approximates how many strong beats the line demands.
ENGLISH_FUNCTION_WORDS = ENGLISH_INHERITED_ENDINGS | {
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "us", "them",
    "not", "there", "here", "then", "too", "very", "up", "down", "out",
    "off", "all", "im", "i'm", "ive", "i've", "ill", "i'll", "id", "i'd",
    "youre", "you're", "youll", "you'll", "its", "it's", "dont", "don't",
    "cant", "can't", "wont", "won't", "didnt", "didn't",
    "oh", "ooh", "uh", "ah", "mm", "hmm", "la", "na", "hey", "yeah", "yea",
}
# Words whose sung syllable count routinely differs from the written count.
# Values are (low, high) plausible sung counts; only the membership is used.
ELISION_AMBIGUOUS = {
    "fire": (1, 2),
    "fires": (1, 2),
    "hour": (1, 2),
    "hours": (1, 2),
    "our": (1, 2),
    "ours": (1, 2),
    "every": (2, 3),
    "everything": (3, 4),
    "everyone": (3, 4),
    "family": (2, 3),
    "different": (2, 3),
    "heaven": (1, 2),
    "real": (1, 2),
    "quiet": (1, 2),
    "flower": (1, 2),
    "power": (1, 2),
    "memory": (2, 3),
    "camera": (2, 3),
    "interesting": (3, 4),
    "comfortable": (3, 4),
    "chocolate": (2, 3),
    "tired": (1, 2),
    "hired": (1, 2),
    "wired": (1, 2),
    "fired": (1, 2),
    "desire": (2, 3),
    "higher": (1, 2),
    "smile": (1, 2),
}
# Compound words hide a medial silent vowel that the heuristic cannot see.
COMPOUND_OVERRIDES = {
    "lukewarm": 2,
    "somewhere": 2,
    "someone": 2,
    "somehow": 2,
    "sometimes": 2,
    "anywhere": 3,
    "everywhere": 3,
    "housework": 2,
    "homemade": 2,
    "lifetime": 2,
    "bedtime": 2,
    "daytime": 2,
    "downstairs": 2,
    "upstairs": 2,
    "hallway": 2,
}
# Written-form overrides where the vowel-group heuristic is wrong.
SYLLABLE_OVERRIDES = {
    "the": 1, "a": 1, "i": 1, "im": 1, "ive": 1, "ill": 1, "id": 1, "oh": 1,
    "ooh": 1, "you": 1, "your": 1, "youre": 1, "our": 1, "hour": 1, "fire": 2,
    "eye": 1, "eyes": 1, "one": 1, "once": 1, "gone": 1, "some": 1, "come": 1,
    "love": 1, "move": 1, "have": 1, "give": 1, "live": 1, "lives": 1,
    "were": 1, "where": 1, "there": 1, "here": 1, "more": 1, "before": 2,
    "everything": 3, "every": 2, "being": 2, "doing": 2, "going": 2,
    "seeing": 2, "quiet": 2, "science": 2, "poem": 2, "idea": 3, "area": 3,
    "create": 2, "people": 2, "little": 2, "middle": 2, "table": 2, "able": 2,
    "yeah": 1, "aint": 1, "cause": 1, "wanna": 2, "gonna": 2, "gotta": 2,
    "one": 1, "none": 1, "alone": 2, "someone": 2, "anyone": 3, "everyone": 3,
    "gone": 1, "done": 1, "nothing": 2, "something": 2, "anything": 3,
}
CONSONANT_CLUSTER_RE = re.compile(r"[bcdfghjklmnpqrstvwxz]{4,}", re.IGNORECASE)


def strip_word(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower().replace("’", "'"))


def english_syllables(word: str) -> int:
    """Estimate written syllables for one English word."""
    plain = strip_word(word)
    if not plain:
        return 0
    if plain in SYLLABLE_OVERRIDES:
        return SYLLABLE_OVERRIDES[plain]
    if plain in COMPOUND_OVERRIDES:
        return COMPOUND_OVERRIDES[plain]
    if len(plain) <= 3:
        return 1
    trimmed = plain
    # "-es" is pronounced after a sibilant ("ashes", "faces"), silent otherwise.
    trimmed = re.sub(r"(?<![aeiouylsxzcgh])es$", "", trimmed)
    # "-ed" is pronounced after t/d ("waited"), silent otherwise ("loved"). After
    # the /aɪ/ + r of "tired" or "desired" the "e" keeps its own beat.
    if not re.search(r"[iy]red$", trimmed):
        trimmed = re.sub(r"(?<![aeiouytd])ed$", "", trimmed)
    # Silent final "e" ("stone"), but never in "-le" ("table").
    trimmed = re.sub(r"(?<![aeiouyl])e$", "", trimmed)
    # "y" next to another vowel is a boundary, not part of one nucleus:
    # cry|ing, pla|ying, be|yond — but word-initial "y" stays a consonant.
    trimmed = re.sub(r"(?<=[^aeiouy])y(?=[aeiou])", "y|", trimmed)
    trimmed = re.sub(r"(?<=[aeiou])y(?=[aeiou])", "|y", trimmed)
    count = len(re.findall(r"[aeiouy]+", trimmed))
    # Syllabic nasal with no written vowel: "rhythm", "prism" — but not "storm".
    if re.search(r"[^aeiouyrlnwm][mn]s?$", plain):
        count += 1
    return max(1, count)


def line_language(line: str, forced: str) -> str:
    if forced in {"en", "ko"}:
        return forced
    if HANGUL_RE.search(line):
        return "ko"
    if LATIN_WORD_RE.search(line):
        return "en"
    return "ko"


def heard_syllables(line: str, lang: str) -> int:
    if lang == "ko":
        return len(HANGUL_RE.findall(line)) + len(LATIN_WORD_RE.findall(line))
    total = sum(english_syllables(word) for word in LATIN_WORD_RE.findall(line))
    total += len(HANGUL_RE.findall(line))
    total += sum(len(number) for number in NUMBER_RE.findall(line))
    return total


def stress_beats(line: str, lang: str) -> int:
    """Approximate the number of strong beats the line demands."""
    if lang == "ko":
        # Korean has no lexical stress; the spacing-unit (eojeol) count is the
        # closest rhythmic-group proxy.
        return len([token for token in line.split() if WORD_RE.search(token)])
    beats = 0
    for word in LATIN_WORD_RE.findall(line):
        plain = strip_word(word)
        if not plain:
            continue
        syllables = english_syllables(word)
        if syllables == 1 and (
            plain in ENGLISH_FUNCTION_WORDS
            or word.lower().replace("’", "'") in ENGLISH_FUNCTION_WORDS
        ):
            continue
        # One primary stress, plus one more per foot beyond the second syllable.
        beats += 1 + max(0, (syllables - 1) // 2)
    return beats


def normalize_line(line: str) -> str:
    return "".join(WORD_RE.findall(line)).lower().replace("’", "'")


def canonical_section(name: str) -> str:
    lowered = name.strip().lower()
    for canonical, aliases in SECTION_ALIASES:
        if any(alias in lowered for alias in aliases):
            return canonical
    simplified = re.sub(r"\b(?:final|last|첫|두|마지막)\b", "", lowered)
    simplified = re.sub(r"\d+", "", simplified)
    return re.sub(r"\s+", "-", simplified).strip("-") or "section"


def syllable_bucket(value: int) -> str:
    if value <= 4:
        return "xs"
    if value <= 7:
        return "s"
    if value <= 10:
        return "m"
    if value <= 13:
        return "l"
    return "xl"


def stress_bucket(value: int) -> str:
    if value <= 2:
        return "b2"
    if value <= 3:
        return "b3"
    if value <= 4:
        return "b4"
    if value <= 6:
        return "b6"
    return "b7+"


def last_hangul_body(line: str) -> str | None:
    chars = HANGUL_RE.findall(line)
    if not chars:
        return None
    index = ord(chars[-1]) - 0xAC00
    onset = index // 588
    vowel = (index % 588) // 28
    return CHOSEONG[onset] + JUNGSEONG[vowel]


def english_rhyme_tail(line: str) -> str | None:
    """Last vowel group plus its coda: the end-rhyme unit."""
    words = LATIN_WORD_RE.findall(line)
    if not words:
        return None
    plain = strip_word(words[-1])
    if not plain:
        return None
    matches = list(re.finditer(r"[aeiouy]+", plain))
    if not matches:
        return plain[-2:]
    return plain[matches[-1].start():]


def rhyme_key(line: str, lang: str) -> str | None:
    return last_hangul_body(line) if lang == "ko" else english_rhyme_tail(line)


def breath_end_role(line: str, lang: str) -> str:
    stripped = line.rstrip()
    if stripped.endswith(CUTOFF_PUNCTUATION):
        return "cutoff"
    if stripped.endswith(OPEN_BREATH_PUNCTUATION):
        return "open"
    if stripped.endswith(CLOSED_BREATH_PUNCTUATION):
        return "closed"
    words = WORD_RE.findall(stripped)
    if not words:
        return "unmarked"
    if lang == "ko":
        if any(words[-1].endswith(ending) for ending in KOREAN_CONNECTIVE_ENDINGS):
            return "inherited"
        if len(words) > 1 and any(
            words[-1].endswith(particle) for particle in KOREAN_UNFINISHED_PARTICLES
        ):
            return "inherited"
        return "unmarked"
    last = words[-1].lower().replace("’", "'")
    if last in ENGLISH_INHERITED_ENDINGS or strip_word(last) in ENGLISH_INHERITED_ENDINGS:
        return "inherited"
    return "unmarked"


def rhyme_scheme(keys: list[str | None]) -> str:
    """Render a section's end-rhyme scheme as A/B/C letters; '.' when absent."""
    labels: dict[str, str] = {}
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = []
    for key in keys:
        if not key:
            out.append(".")
            continue
        if key not in labels:
            labels[key] = letters[len(labels) % len(letters)]
        out.append(labels[key])
    return "".join(out)


def parse_lyrics(text: str) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    current_name = "Unsectioned"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        if current_lines:
            occurrences.append({"name": current_name, "lines": current_lines})
            current_lines = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        match = SECTION_RE.match(line)
        if match:
            flush()
            current_name = match.group(1).strip()
            continue
        current_lines.append(line)
    flush()
    return occurrences


def occurrence_metrics(
    occurrences: list[dict[str, Any]], forced_lang: str
) -> list[dict[str, Any]]:
    seen: Counter[str] = Counter()
    result = []
    for occurrence in occurrences:
        name = occurrence["name"]
        seen[name] += 1
        lines = occurrence["lines"]
        langs = [line_language(line, forced_lang) for line in lines]
        values = [
            heard_syllables(line, lang) for line, lang in zip(lines, langs, strict=True)
        ]
        beats = [
            stress_beats(line, lang) for line, lang in zip(lines, langs, strict=True)
        ]
        breath_roles = [
            breath_end_role(line, lang) for line, lang in zip(lines, langs, strict=True)
        ]
        keys = [rhyme_key(line, lang) for line, lang in zip(lines, langs, strict=True)]
        result.append(
            {
                "name": name,
                "occurrence": seen[name],
                "canonical_job": canonical_section(name),
                "language": "mixed" if len(set(langs)) > 1 else langs[0],
                "line_count": len(values),
                "heard_syllables": values,
                "syllable_buckets": [syllable_bucket(value) for value in values],
                "stress_beats": beats,
                "stress_buckets": [stress_bucket(value) for value in beats],
                "breath_end_roles": breath_roles,
                "rhyme_scheme": rhyme_scheme(keys),
                "min": min(values),
                "max": max(values),
                "spread": max(values) - min(values),
                "mean": round(sum(values) / len(values), 2),
                "stress_spread": max(beats) - min(beats),
            }
        )
    return result


def form_similarity(
    current: list[dict[str, Any]], previous: list[dict[str, Any]]
) -> tuple[float, float, float]:
    current_roles = [item["canonical_job"] for item in current]
    previous_roles = [item["canonical_job"] for item in previous]
    role_similarity = SequenceMatcher(None, current_roles, previous_roles).ratio()

    paired = min(len(current), len(previous))
    if not max(len(current), len(previous)):
        line_count_similarity = 1.0
    else:
        matches = sum(
            current[index]["line_count"] == previous[index]["line_count"]
            for index in range(paired)
        )
        line_count_similarity = matches / max(len(current), len(previous))

    combined = (0.6 * role_similarity) + (0.4 * line_count_similarity)
    return combined, role_similarity, line_count_similarity


def _shape(items: list[dict[str, Any]], key: str) -> list[str]:
    return [f"{item['canonical_job']}:{bucket}" for item in items for bucket in item[key]]


def syllable_shape_similarity(
    current: list[dict[str, Any]], previous: list[dict[str, Any]]
) -> float:
    return SequenceMatcher(
        None, _shape(current, "syllable_buckets"), _shape(previous, "syllable_buckets")
    ).ratio()


def stress_shape_similarity(
    current: list[dict[str, Any]], previous: list[dict[str, Any]]
) -> float:
    return SequenceMatcher(
        None, _shape(current, "stress_buckets"), _shape(previous, "stress_buckets")
    ).ratio()


def rhyme_scheme_similarity(
    current: list[dict[str, Any]], previous: list[dict[str, Any]]
) -> float:
    current_shape = [f"{item['canonical_job']}:{item['rhyme_scheme']}" for item in current]
    previous_shape = [
        f"{item['canonical_job']}:{item['rhyme_scheme']}" for item in previous
    ]
    return SequenceMatcher(None, current_shape, previous_shape).ratio()


def breath_shape_similarity(
    current: list[dict[str, Any]], previous: list[dict[str, Any]]
) -> float:
    def shape(items: list[dict[str, Any]]) -> list[str]:
        return [
            f"{item['canonical_job']}:{bucket}:{beat}:{role}"
            for item in items
            for bucket, beat, role in zip(
                item["syllable_buckets"],
                item["stress_buckets"],
                item["breath_end_roles"],
                strict=True,
            )
        ]

    return SequenceMatcher(None, shape(current), shape(previous)).ratio()


def exact_line_overlap(current_lines: list[str], previous_lines: list[str]) -> float:
    current = {
        normalized
        for line in current_lines
        if len(normalized := normalize_line(line)) >= 4
    }
    previous = {
        normalized
        for line in previous_lines
        if len(normalized := normalize_line(line)) >= 4
    }
    return len(current & previous) / len(current) if current else 0.0


def suno_checks(text: str, lines: list[str]) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    tags = Counter(
        match.group(1).strip().lower()
        for match in re.finditer(r"\[([^\]]{1,40})\]", text)
    )
    joined = "\n".join(lines)
    caps_words = sorted(
        {
            word
            for line in lines
            for word in LATIN_WORD_RE.findall(line)
            if len(word) >= 3 and word.isupper()
        }
    )
    numerals = sorted({number for number in NUMBER_RE.findall(joined)})
    risky_symbols = sorted({symbol for symbol in "&%$@#/*_=+~^" if symbol in joined})
    clusters = sorted(
        {match.group(0).lower() for match in CONSONANT_CLUSTER_RE.finditer(joined)}
    )
    tag_total = sum(tags.values())
    if tag_total > 12:
        warnings.append(
            f"{tag_total} bracket tags in the lyrics field; Suno sometimes sings or "
            "ignores dense tags, so keep only structural and delivery-critical ones"
        )
    wordy_tags = sorted(tag for tag in tags if len(tag.split()) >= 3)
    if wordy_tags:
        warnings.append(
            f"long free-text bracket tags {wordy_tags[:4]}; verify each is treated as "
            "a directive and not sung aloud"
        )
    if caps_words:
        warnings.append(
            f"ALL-CAPS words {caps_words[:6]} may be rendered as shouting; lowercase "
            "them unless the shout is intended"
        )
    if numerals:
        warnings.append(
            f"numerals {numerals[:6]} are read inconsistently; spell them out"
        )
    if risky_symbols:
        warnings.append(
            f"symbols {risky_symbols} may be voiced literally or dropped; spell them out"
        )
    if clusters:
        warnings.append(
            f"dense consonant clusters {clusters[:6]}; verify they stay singable at "
            "tempo or move them off short notes"
        )
    length = len(text)
    if length > 3000:
        warnings.append(
            f"lyrics field is {length} characters; confirm the current Suno field limit "
            "before generating"
        )
    return (
        {
            "bracket_tags": dict(tags.most_common()),
            "bracket_tag_total": tag_total,
            "all_caps_words": caps_words,
            "numerals": numerals,
            "risky_symbols": risky_symbols,
            "consonant_clusters": clusters,
            "character_count": length,
        },
        warnings,
    )


def build_report(
    text: str,
    hook: str | None,
    healing_intent: bool = False,
    forced_lang: str = "auto",
    suno: bool = False,
) -> dict[str, Any]:
    occurrences = parse_lyrics(text)
    metrics = occurrence_metrics(occurrences, forced_lang)
    lines = [line for occurrence in occurrences for line in occurrence["lines"]]
    langs = [line_language(line, forced_lang) for line in lines]
    dominant_lang = Counter(langs).most_common(1)[0][0] if langs else "en"
    normalized = [normalize_line(line) for line in lines]
    counts = Counter(line for line in normalized if line)
    repeated_instances = sum(count - 1 for count in counts.values() if count > 1)
    ending_words = Counter(
        words[-1].lower() for line in lines if (words := WORD_RE.findall(line))
    )
    tails = Counter(
        key
        for line, lang in zip(lines, langs, strict=True)
        if (key := rhyme_key(line, lang))
    )
    near_pairs = []
    for i, left in enumerate(normalized):
        if not left:
            continue
        for j in range(i + 1, len(normalized)):
            right = normalized[j]
            if not right or left == right:
                continue
            ratio = SequenceMatcher(None, left, right).ratio()
            if ratio >= 0.82:
                near_pairs.append(
                    {"line_a": i + 1, "line_b": j + 1, "similarity": round(ratio, 3)}
                )

    symbols: Counter[str] = Counter()
    for line, lang in zip(lines, langs, strict=True):
        if lang == "en":
            for word in LATIN_WORD_RE.findall(line):
                plain = strip_word(word)
                if plain in ENGLISH_COMMON_SYMBOLS:
                    symbols[plain] += 1
        else:
            for symbol in KOREAN_COMMON_SYMBOLS:
                if symbol in line:
                    symbols[symbol] += line.count(symbol)

    lowered_text = text.lower()
    healing_assurance_hits = {
        phrase: lowered_text.count(phrase.lower())
        for phrase in ENGLISH_HEALING_ASSURANCES + KOREAN_HEALING_ASSURANCES
        if phrase.lower() in lowered_text
    }
    medical_claim_hits = sorted(
        {
            match.group(0).strip()
            for pattern in KOREAN_MEDICAL_CLAIM_PATTERNS
            + ENGLISH_MEDICAL_CLAIM_PATTERNS
            for match in pattern.finditer(text)
        }
    )
    elision_hits = sorted(
        {
            plain
            for line in lines
            for word in LATIN_WORD_RE.findall(line)
            if (plain := strip_word(word)) in ELISION_AMBIGUOUS
        }
    )

    warnings = []
    for item in metrics:
        if item["line_count"] >= 3 and item["spread"] > 6:
            warnings.append(
                f"{item['name']}#{item['occurrence']}: syllable spread is "
                f"{item['spread']}; verify melodic intent"
            )
        if (
            item["language"] == "en"
            and item["line_count"] >= 3
            and item["spread"] >= 4
            and item["stress_spread"] <= 1
        ):
            warnings.append(
                f"{item['name']}#{item['occurrence']}: syllable counts vary while "
                f"stress beats stay at {item['stress_beats']}; this is ordinary "
                "stress-timed English, not a changed breath grammar"
            )

    line_count = len(lines)
    repeated_ratio = repeated_instances / line_count if line_count else 0.0
    if repeated_ratio > 0.35:
        warnings.append(
            "exact repeated lines exceed 35%; verify that each return gains information"
        )
    if len(metrics) >= 4 and len({item["line_count"] for item in metrics}) == 1:
        warnings.append(
            "all section occurrences use the same line count; inspect stanza symmetry"
        )
    if len(symbols) >= 4:
        warnings.append(
            f"four or more common lyric symbols appear ({sorted(symbols)[:6]}); verify "
            "that each changes action or information"
        )
    if healing_intent and healing_assurance_hits:
        warnings.append(
            "generic healing assurances appear; ground each one in a concrete care "
            "action or remove it"
        )
    if healing_intent and medical_claim_hits:
        warnings.append(
            "possible medical or frequency-healing promise detected; keep the lyric "
            "non-clinical and non-guaranteed"
        )
    if line_count:
        top_word, top_word_count = ending_words.most_common(1)[0]
        if top_word_count / line_count > 0.30:
            warnings.append(
                f"line ending '{top_word}' dominates {top_word_count}/{line_count} lines"
            )
        if tails:
            top_tail, top_tail_count = tails.most_common(1)[0]
            threshold = 0.45 if dominant_lang == "ko" else 0.35
            if top_tail_count / line_count > threshold:
                label = "final Korean body" if dominant_lang == "ko" else "end-rhyme tail"
                warnings.append(
                    f"{label} '{top_tail}' dominates {top_tail_count}/{line_count} lines"
                )
    multi_line_schemes = [
        item["rhyme_scheme"] for item in metrics if item["line_count"] >= 4
    ]
    textbook_schemes = {"AABB", "ABAB", "ABCB", "AABBCC", "ABABCDCD", "AAAA"}
    if (
        dominant_lang == "en"
        and len(multi_line_schemes) >= 2
        and all(scheme in textbook_schemes for scheme in multi_line_schemes)
    ):
        warnings.append(
            f"every multi-line section uses a textbook rhyme scheme "
            f"{multi_line_schemes}; the end-rhyme closure law is unbroken"
        )
    if dominant_lang == "en" and elision_hits:
        warnings.append(
            f"elision-ambiguous words {elision_hits[:6]}: decide the sung syllable count "
            "yourself, since the estimate can be off by one per occurrence"
        )
    if dominant_lang == "en" and line_count >= 8:
        inherited = sum(
            role == "inherited" for item in metrics for role in item["breath_end_roles"]
        )
        if inherited == 0:
            warnings.append(
                "no line ends on an unfinished syntactic state; every breath resets, so "
                "breath inheritance is not implemented in the text"
            )

    hook_count = None
    hook_positions: list[int] = []
    if hook:
        normalized_hook = normalize_line(hook)
        hook_count = normalize_line(text).count(normalized_hook)
        hook_positions = [
            index + 1
            for index, line in enumerate(normalized)
            if normalized_hook and normalized_hook in line
        ]
        if hook_count < 2:
            warnings.append("hook appears fewer than two times")
        elif hook_count > 6:
            warnings.append("hook appears more than six times; verify novelty")

    form_signature = ">".join(
        f"{item['canonical_job']}:{item['line_count']}" for item in metrics
    )
    breath_signature = ">".join(
        f"{item['canonical_job']}:"
        + ",".join(
            f"{bucket}/{beat}/{role}"
            for bucket, beat, role in zip(
                item["syllable_buckets"],
                item["stress_buckets"],
                item["breath_end_roles"],
                strict=True,
            )
        )
        for item in metrics
    )
    rhyme_signature = ">".join(
        f"{item['canonical_job']}:{item['rhyme_scheme']}" for item in metrics
    )
    section_metrics = {}
    for item in metrics:
        label = (
            item["name"]
            if item["occurrence"] == 1
            else f"{item['name']}#{item['occurrence']}"
        )
        section_metrics[label] = {
            key: value for key, value in item.items() if key not in {"name", "occurrence"}
        }

    report: dict[str, Any] = {
        "language": dominant_lang,
        "section_order": [item["name"] for item in metrics],
        "form_signature": form_signature,
        "breath_signature": breath_signature,
        "rhyme_signature": rhyme_signature,
        "line_count": line_count,
        "section_occurrences": metrics,
        "section_metrics": section_metrics,
        "exact_repeated_line_instances": repeated_instances,
        "exact_repeated_line_ratio": round(repeated_ratio, 3),
        "near_duplicate_pairs": near_pairs,
        "hook": hook,
        "hook_occurrences": hook_count,
        "hook_line_positions": hook_positions,
        "common_symbol_hits": dict(symbols.most_common()),
        "healing_assurance_hits": healing_assurance_hits,
        "possible_medical_claim_hits": medical_claim_hits,
        "elision_ambiguous_words": elision_hits,
        "dominant_line_end_words": ending_words.most_common(5),
        "dominant_rhyme_tails": tails.most_common(5),
        "warnings": warnings,
        "_lines": lines,
    }
    if suno:
        suno_report, suno_warnings = suno_checks(text, lines)
        report["suno"] = suno_report
        warnings.extend(suno_warnings)
    return report


def audit(
    text: str,
    hook: str | None,
    comparisons: list[tuple[str, str]],
    healing_intent: bool = False,
    forced_lang: str = "auto",
    suno: bool = False,
) -> dict[str, Any]:
    report = build_report(text, hook, healing_intent, forced_lang, suno)
    comparison_reports = []
    near_form_matches = 0
    near_breath_matches = 0
    near_rhyme_matches = 0
    for path, previous_text in comparisons:
        previous = build_report(previous_text, hook, False, forced_lang)
        combined, roles, line_counts = form_similarity(
            report["section_occurrences"], previous["section_occurrences"]
        )
        syllables = syllable_shape_similarity(
            report["section_occurrences"], previous["section_occurrences"]
        )
        stresses = stress_shape_similarity(
            report["section_occurrences"], previous["section_occurrences"]
        )
        breaths = breath_shape_similarity(
            report["section_occurrences"], previous["section_occurrences"]
        )
        rhymes = rhyme_scheme_similarity(
            report["section_occurrences"], previous["section_occurrences"]
        )
        line_overlap = exact_line_overlap(report["_lines"], previous["_lines"])
        comparison_reports.append(
            {
                "path": path,
                "form_similarity": round(combined, 3),
                "section_job_similarity": round(roles, 3),
                "line_count_similarity": round(line_counts, 3),
                "syllable_shape_similarity": round(syllables, 3),
                "stress_shape_similarity": round(stresses, 3),
                "breath_shape_similarity": round(breaths, 3),
                "rhyme_scheme_similarity": round(rhymes, 3),
                "exact_line_overlap": round(line_overlap, 3),
            }
        )
        if combined >= 0.85:
            near_form_matches += 1
        if breaths >= 0.82:
            near_breath_matches += 1
        if rhymes >= 0.85:
            near_rhyme_matches += 1
        if line_overlap > 0.20:
            report["warnings"].append(
                f"{path}: more than 20% of substantive lines repeat exactly"
            )

    if near_form_matches >= 2:
        report["warnings"].append(
            "form matches two recent drafts at 85% or more; switch architecture or "
            "information order"
        )
    elif near_form_matches == 1:
        report["warnings"].append(
            "form matches a recent draft at 85% or more; verify that the semantic "
            "engine changed"
        )
    if near_breath_matches >= 2:
        report["warnings"].append(
            "breath shape matches two recent drafts at 82% or more; switch the "
            "heard-syllable vector, stress-beat vector, or breath-boundary roles"
        )
    elif near_breath_matches == 1:
        report["warnings"].append(
            "breath shape matches a recent draft at 82% or more; verify that breath "
            "inheritance, not new wording, changed the phrasing"
        )
    if near_rhyme_matches >= 2:
        report["warnings"].append(
            "rhyme scheme matches two recent drafts at 85% or more; the rhyme grammar "
            "is a template, not a choice"
        )

    report["recent_comparisons"] = comparison_reports
    report.pop("_lines", None)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lyrics",
        required=True,
        help="UTF-8 lyrics file, or '-' to read from standard input",
    )
    parser.add_argument("--hook", help="Hook phrase to count")
    parser.add_argument(
        "--compare",
        action="append",
        default=[],
        help="Recent UTF-8 lyric file to compare; repeat for multiple drafts",
    )
    parser.add_argument(
        "--lang",
        choices=("auto", "en", "ko"),
        default="auto",
        help="Force the prosody model; 'auto' detects per line",
    )
    parser.add_argument(
        "--healing-intent",
        action="store_true",
        help="Flag generic reassurance and possible cure or frequency-healing claims",
    )
    parser.add_argument(
        "--suno",
        action="store_true",
        help="Add Suno lyrics-field checks (tags, caps, numerals, clusters, length)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    try:
        text = (
            sys.stdin.read()
            if args.lyrics == "-"
            else Path(args.lyrics).read_text(encoding="utf-8")
        )
        comparisons = [
            (path, Path(path).read_text(encoding="utf-8")) for path in args.compare
        ]
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))

    report = audit(
        text, args.hook, comparisons, args.healing_intent, args.lang, args.suno
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"language: {report['language']}")
        print(f"sections: {' -> '.join(report['section_order'])}")
        print(f"form signature: {report['form_signature']}")
        print(f"breath signature: {report['breath_signature']}")
        print(f"rhyme signature: {report['rhyme_signature']}")
        print(f"lines: {report['line_count']}")
        for item in report["section_occurrences"]:
            print(
                f"{item['name']}#{item['occurrence']}: "
                f"syllables={item['heard_syllables']} "
                f"stress={item['stress_beats']} "
                f"breath_roles={item['breath_end_roles']} "
                f"rhyme={item['rhyme_scheme']} "
                f"mean={item['mean']} spread={item['spread']}"
            )
        print(f"exact repeated line ratio: {report['exact_repeated_line_ratio']}")
        if report["hook"] is not None:
            print(f"hook occurrences: {report['hook_occurrences']}")
            print(f"hook line positions: {report['hook_line_positions']}")
        print(f"common symbol hits: {report['common_symbol_hits']}")
        if args.healing_intent:
            print(f"healing assurance hits: {report['healing_assurance_hits']}")
            print(
                "possible medical claim hits: "
                f"{report['possible_medical_claim_hits']}"
            )
        print(f"dominant endings: {report['dominant_line_end_words']}")
        print(f"dominant rhyme tails: {report['dominant_rhyme_tails']}")
        if report["elision_ambiguous_words"]:
            print(f"elision-ambiguous words: {report['elision_ambiguous_words']}")
        if "suno" in report:
            suno_report = report["suno"]
            print(
                "suno: "
                f"chars={suno_report['character_count']} "
                f"tags={suno_report['bracket_tags']} "
                f"caps={suno_report['all_caps_words']} "
                f"numerals={suno_report['numerals']} "
                f"clusters={suno_report['consonant_clusters']}"
            )
        if report["near_duplicate_pairs"]:
            print(f"near duplicate pairs: {report['near_duplicate_pairs']}")
        for comparison in report["recent_comparisons"]:
            print(
                "comparison: "
                f"{comparison['path']} form={comparison['form_similarity']} "
                f"syllable_shape={comparison['syllable_shape_similarity']} "
                f"stress_shape={comparison['stress_shape_similarity']} "
                f"breath_shape={comparison['breath_shape_similarity']} "
                f"rhyme_scheme={comparison['rhyme_scheme_similarity']} "
                f"exact_line_overlap={comparison['exact_line_overlap']}"
            )
        for warning in report["warnings"]:
            print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
