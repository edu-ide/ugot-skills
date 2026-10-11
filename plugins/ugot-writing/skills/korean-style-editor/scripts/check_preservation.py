#!/usr/bin/env python3
"""Compare protected token inventories without claiming semantic equivalence."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Iterable


LIMITATIONS = [
    "등장 횟수 비교이며 의미 보존이나 사실 정확성을 증명하지 않습니다.",
    "숫자의 연결 대상, 부정·조건·인과관계, 계획·완료 상태는 직접 대조해야 합니다.",
    "한글로 쓴 숫자와 지정하지 않은 고유명사는 검사하지 않습니다.",
    "명시 용어의 한국어 조사·서술격 경계는 제한된 목록으로 판단합니다.",
    "숫자 표기와 코드의 공백·구분자 변경도 차이로 표시할 수 있습니다.",
]

PARTICLES = (
    "으로부터", "에게서", "한테서", "께서는", "으로서", "으로써", "이든지",
    "이라도", "이라고", "이라는", "이란", "이랑", "으로", "에서", "에게", "한테",
    "께서", "까지", "부터", "처럼", "보다", "조차", "마저", "밖에", "든지",
    "라고", "라는", "라도", "하고", "로서", "로써", "이며", "이나", "이든",
    "은", "는", "이", "가", "을", "를", "에", "의", "께", "로", "와", "과",
    "랑", "도", "만", "든", "나", "야", "며",
)
PARTICLE_SUFFIX = re.compile("(?:" + "|".join(map(re.escape, PARTICLES)) + ")+")
COPULA_SUFFIXES = frozenset((
    "이다", "입니다", "이에요", "예요", "이었다", "였다", "이었습니다",
    "였습니다", "이고", "이면서", "이지만", "이며",
))
HANGUL_SUFFIX = re.compile(r"[가-힣]+")

UNITS = (
    "%포인트", "%p", "백만원", "천만원", "십만원", "억 원", "만 원", "조 원",
    "억원", "만원", "천원", "조원", "퍼센트", "포인트", "개월", "시간",
    "밀리초", "분기", "KiB", "MiB", "GiB", "TiB", "kWh", "GHz", "MHz",
    "kHz", "mL", "mA", "kW", "KB", "MB", "GB", "TB", "Hz", "ms", "us",
    "µs", "ns", "sec", "min", "hr", "km", "cm", "mm", "kg", "mg",
    "m²", "m³", "°C", "°F", "℃", "원", "명", "건", "회", "년", "월", "일",
    "시", "분", "초", "배", "개", "대", "장", "쪽", "주", "%", "‰",
    "s", "h", "m", "g", "L", "W", "V", "A",
)
UNIT_PATTERN = "|".join(
    re.escape(unit).replace(r"\ ", r"\s*")
    for unit in sorted(UNITS, key=len, reverse=True)
)
NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:[+−-]\s*)?(?:[$€£₩]\s*)?(?:[+−-]\s*)?"
    r"(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)"
    r"(?!\d)"
    r"(?:\s*(?:" + UNIT_PATTERN + r")(?![A-Za-z]))?"
)
DATE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])\d{4}-\d{1,2}-\d{1,2}"
    r"(?:[T ]\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?"
    r"(?:Z|[+-]\d{2}:\d{2})?)?(?!\d)"
)
TIME_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?!\d)"
)
URL_PATTERN = re.compile(r"https?://[^\s<>\"'`]+")
FENCE_OPEN = re.compile(r"(?m)^[ \t]{0,3}(`{3,})([^\n]*)\n")
BACKTICK_RUN = re.compile(r"`+")
QUOTE_PAIRS = (("“", "”"), ("‘", "’"), ("「", "」"), ("『", "』"), ('"', '"'), ("'", "'"))


class InputError(ValueError):
    """An invalid CLI request rather than a preservation difference."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError(message)


def mask_spans(text: str, spans: Iterable[tuple[int, int]]) -> str:
    chars = list(text)
    for start, end in spans:
        # Keep line boundaries so later Markdown scans remain well defined.
        for index in range(start, end):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def extract_code(text: str) -> tuple[Counter[str], list[tuple[int, int]]]:
    inventory: Counter[str] = Counter()
    spans: list[tuple[int, int]] = []
    position = 0
    while opening := FENCE_OPEN.search(text, position):
        size = len(opening.group(1))
        closing_pattern = re.compile(r"(?m)^[ \t]{0,3}`{" + str(size) + r",}[ \t]*$")
        closing = closing_pattern.search(text, opening.end())
        end = closing.end() if closing else len(text)
        inventory[text[opening.start():end]] += 1
        spans.append((opening.start(), end))
        position = end
    available = mask_spans(text, spans)
    position = 0
    while opening := BACKTICK_RUN.search(available, position):
        closing_pattern = re.compile(r"(?<!`)" + re.escape(opening.group()) + r"(?!`)")
        closing = closing_pattern.search(available, opening.end())
        if closing is None:
            position = opening.end()
            continue
        inventory[text[opening.start():closing.end()]] += 1
        spans.append((opening.start(), closing.end()))
        position = closing.end()
    return inventory, spans


def extract_urls(text: str) -> tuple[Counter[str], list[tuple[int, int]]]:
    inventory: Counter[str] = Counter()
    spans: list[tuple[int, int]] = []
    for match in URL_PATTERN.finditer(text):
        value = match.group().rstrip(".,;:!")
        # Drop surrounding prose/Markdown punctuation, preserving balanced URL parentheses.
        while value and value[-1] in ")]}":
            closer = value[-1]
            opener = {")": "(", "]": "[", "}": "{"}[closer]
            if value.count(closer) <= value.count(opener):
                break
            value = value[:-1]
        if value:
            inventory[value] += 1
            spans.append((match.start(), match.start() + len(value)))
    return inventory, spans


def is_word(char: str) -> bool:
    return char.isalnum() or char == "_"


def extract_quotes(text: str) -> Counter[str]:
    inventory: Counter[str] = Counter()
    # Inspect each delimiter pair independently; nested quotes remain protected too.
    for opener, closer in QUOTE_PAIRS:
        pattern = re.compile(re.escape(opener) + r"(.*?)" + re.escape(closer), re.DOTALL)
        position = 0
        while match := pattern.search(text, position):
            if opener in ("'", "‘"):
                before = text[match.start() - 1] if match.start() else ""
                after = text[match.end()] if match.end() < len(text) else ""
                if before and before.isascii() and is_word(before):
                    position = match.start() + 1
                    continue
                if after and after.isascii() and is_word(after):
                    position = match.start() + 1
                    continue
            inventory[match.group(1)] += 1
            position = match.end()
    return inventory


def extract_numbers(text: str) -> Counter[str]:
    inventory: Counter[str] = Counter()
    spans: list[tuple[int, int]] = []
    for pattern in (DATE_PATTERN, TIME_PATTERN):
        available = mask_spans(text, spans)
        for match in pattern.finditer(available):
            inventory[match.group()] += 1
            spans.append(match.span())
    for match in NUMBER_PATTERN.finditer(mask_spans(text, spans)):
        inventory[re.sub(r"\s+", "", match.group())] += 1
    return inventory


def count_protected(text: str, term: str) -> int:
    count = 0
    for match in re.finditer(re.escape(term), text):
        if is_word(term[0]) and match.start() and is_word(text[match.start() - 1]):
            continue
        if is_word(term[-1]) and match.end() < len(text):
            next_char = text[match.end()]
            if is_word(next_char):
                suffix = HANGUL_SUFFIX.match(text, match.end())
                if suffix is None:
                    continue
                if (PARTICLE_SUFFIX.fullmatch(suffix.group()) is None
                        and suffix.group() not in COPULA_SUFFIXES):
                    continue
                # An ASCII/digit continuation means a different identifier.
                if suffix.end() < len(text) and is_word(text[suffix.end()]):
                    continue
        count += 1
    return count


def inventory(text: str, protected: Iterable[str]) -> dict[str, Counter[str]]:
    code, code_spans = extract_code(text)
    without_code = mask_spans(text, code_spans)
    urls, url_spans = extract_urls(without_code)
    prose = mask_spans(without_code, url_spans)
    return {
        "code": code,
        "urls": urls,
        "quotes": extract_quotes(prose),
        "numbers": extract_numbers(prose),
        "protected_terms": Counter({term: count_protected(text, term) for term in protected}),
    }


def describe_value(value: str) -> dict[str, object]:
    if len(value) <= 200:
        return {"value": value}
    return {
        "value_preview": value[:160] + "…",
        "value_length": len(value),
        "value_sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
    }


def compare(original: str, revised: str, protected: Iterable[str] = ()) -> dict[str, object]:
    terms = list(dict.fromkeys(protected))
    if any(not term.strip() for term in terms):
        raise InputError("--protect에는 비어 있지 않은 실제 용어를 지정해야 합니다.")
    before = inventory(original, terms)
    after = inventory(revised, terms)
    for term in terms:
        if not before["protected_terms"][term]:
            raise InputError(f"원문에서 보호 용어를 찾을 수 없습니다: {term}")
    differences: list[dict[str, object]] = []
    for category in before:
        for value in sorted(before[category].keys() | after[category].keys()):
            original_count = before[category][value]
            revised_count = after[category][value]
            if original_count != revised_count:
                differences.append({
                    "category": category,
                    **describe_value(value),
                    "original_count": original_count,
                    "revised_count": revised_count,
                })
    return {"ok": not differences, "differences": differences, "limitations": LIMITATIONS}


def main(argv: list[str] | None = None) -> int:
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("original", help="UTF-8 원문 파일")
    parser.add_argument("revised", help="UTF-8 교정 파일")
    parser.add_argument("--protect", action="append", default=[], help="보호할 정확한 용어; 반복 지정 가능")
    try:
        args = parser.parse_args(argv)
        original = Path(args.original).read_text(encoding="utf-8")
        revised = Path(args.revised).read_text(encoding="utf-8")
        result = compare(original, revised, args.protect)
    except (InputError, OSError, UnicodeError) as error:
        message = "파일을 UTF-8로 읽을 수 없습니다." if isinstance(error, UnicodeError) else str(error)
        print(json.dumps({"ok": False, "error": message, "limitations": LIMITATIONS}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
