"""Regression tests for token protection, including the documented limits."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

import check_preservation as checker


class PreservationTests(unittest.TestCase):
    def assertPreserved(self, original, revised, protected=()):
        self.assertTrue(checker.compare(original, revised, protected)["ok"])

    def assertChanged(self, original, revised, category, protected=()):
        result = checker.compare(original, revised, protected)
        self.assertFalse(result["ok"])
        self.assertIn(category, {item["category"] for item in result["differences"]})

    def test_plain_sentence_rewrite(self):
        self.assertPreserved("담당자에 의해 설정 변경이 수행되었습니다.", "담당자가 설정을 변경했습니다.")

    def test_reordering(self):
        self.assertPreserved("오류율은 2%, 재시도율은 5%입니다.", "재시도율은 5%이고 오류율은 2%입니다.")

    def test_number_deletion(self):
        self.assertChanged("120건 중 30건이 남았습니다.", "120건을 접수했습니다.", "numbers")

    def test_number_addition(self):
        self.assertChanged("검토 중입니다.", "2명이 검토 중입니다.", "numbers")

    def test_number_occurrence_count(self):
        self.assertChanged("5명과 5명입니다.", "5명입니다.", "numbers")

    def test_unit_change(self):
        self.assertChanged("용량은 5GB입니다.", "용량은 5MB입니다.", "numbers")

    def test_currency(self):
        self.assertChanged("비용은 12,000원입니다.", "비용은 12,000만원입니다.", "numbers")

    def test_currency_symbols(self):
        self.assertChanged("가격은 $10입니다.", "가격은 €10입니다.", "numbers")

    def test_signed_numbers(self):
        self.assertChanged("변화량은 -5%입니다.", "변화량은 +5%입니다.", "numbers")

    def test_decimal(self):
        self.assertChanged("성공률은 98.5%입니다.", "성공률은 98.6%입니다.", "numbers")

    def test_thousands_separator(self):
        self.assertEqual(checker.extract_numbers("12,000원입니다."), {"12,000원": 1})

    def test_number_before_punctuation_comma(self):
        self.assertChanged("대상은 2, 3입니다.", "대상은 9, 3입니다.", "numbers")

    def test_signed_number_before_punctuation_comma(self):
        self.assertChanged("변화는 +2, -3입니다.", "변화는 -2, -3입니다.", "numbers")

    def test_thousands_and_punctuation_comma(self):
        self.assertEqual(checker.extract_numbers("대상은 12,000, 20입니다."), {"12,000": 1, "20": 1})

    def test_decimal_without_integer_part(self):
        self.assertChanged("비율은 .5입니다.", "비율은 5입니다.", "numbers")

    def test_unicode_minus(self):
        self.assertChanged("변화량은 −5%입니다.", "변화량은 5%입니다.", "numbers")

    def test_unit_whitespace(self):
        self.assertPreserved("240 건 중 6 건에서 오류가 났습니다.", "240건 중 6건에서 오류가 났습니다.")

    def test_percentage_points(self):
        self.assertChanged("5%포인트 감소했습니다.", "5% 감소했습니다.", "numbers")

    def test_korean_dates(self):
        self.assertPreserved("2026년 10월 5일까지입니다.", "기한은 2026년 10월 5일입니다.")

    def test_iso_date_and_time(self):
        self.assertChanged("2026-10-05 10:30에 시작합니다.", "2026-10-05 11:30에 시작합니다.", "numbers")

    def test_standalone_time(self):
        self.assertPreserved("10:30에 시작해요.", "시작 시각은 10:30입니다.")

    def test_url_change(self):
        self.assertChanged("https://example.com/plan?v=2 입니다.", "https://example.com/plan?v=3 입니다.", "urls")

    def test_markdown_url(self):
        self.assertPreserved("[설명](https://example.com/plan?v=2)", "https://example.com/plan?v=2 에서 읽으세요.")

    def test_url_parentheses(self):
        self.assertEqual(checker.extract_urls("[문서](https://example.com/a_(b)).")[0], {"https://example.com/a_(b)": 1})

    def test_no_url_number_duplicates(self):
        result = checker.inventory("https://example.com/2026?v=5", ())
        self.assertEqual(result["numbers"], {})

    def test_inline_code_change(self):
        self.assertChanged("`retry_count = 3`입니다.", "`retry_count = 4`입니다.", "code")

    def test_fenced_code_change(self):
        self.assertChanged("```python\ncount = 3\n```\n설명", "```python\ncount = 4\n```\n설명", "code")

    def test_fenced_code_reorder(self):
        self.assertPreserved("먼저 설명합니다.\n```py\nx = 3\n```", "```py\nx = 3\n```\n나중에 설명합니다.")

    def test_multi_backtick_inline_code(self):
        self.assertChanged("``print(`value`)``", "``print(`other`)``", "code")

    def test_no_code_duplicates(self):
        result = checker.inventory('`count = 3; link = "https://example.com/5"`', ())
        self.assertEqual(result["numbers"], {})
        self.assertEqual(result["urls"], {})
        self.assertEqual(result["quotes"], {})

    def test_quote_delimiter_change(self):
        self.assertPreserved('담당자는 "10월 5일까지 보내 주세요"라고 말했습니다.', "담당자는 “10월 5일까지 보내 주세요”라고 말했습니다.")

    def test_single_quote_delimiter_change(self):
        self.assertPreserved("'잠시 기다려 주세요'라고 했습니다.", "‘잠시 기다려 주세요’라고 했습니다.")

    def test_single_quote_attached_to_korean(self):
        self.assertChanged("담당자는‘기다려 주세요’라고 했습니다.", "담당자는‘끝났습니다’라고 했습니다.", "quotes")

    def test_corner_quotes(self):
        self.assertPreserved("「제출하지 않았습니다」라고 말했습니다.", "『제출하지 않았습니다』라고 말했습니다.")

    def test_quote_content_change(self):
        self.assertChanged("“아직 결정하지 않았습니다”라고 했습니다.", "“결정했습니다”라고 했습니다.", "quotes")

    def test_quote_count(self):
        self.assertChanged("“확인”이라고 두 번 말했습니다. “확인”", "“확인”이라고 말했습니다.", "quotes")

    def test_english_apostrophe(self):
        self.assertPreserved("We don't know why it isn't working.", "It isn't working, and we don't know why.")

    def test_proper_name_particles(self):
        self.assertPreserved("서울에서 이서연은 검토했습니다.", "이서연이 서울에서는 검토했습니다.", ("서울", "이서연"))

    def test_proper_name_prefix_expansion(self):
        self.assertChanged("서울에서 검토했습니다.", "서울대에서 검토했습니다.", "protected_terms", ("서울",))

    def test_person_name_prefix_expansion(self):
        self.assertChanged("이서연은 검토했습니다.", "이서연구소는 검토했습니다.", "protected_terms", ("이서연",))

    def test_proper_name_copulas(self):
        for suffix in ("입니다", "이에요", "이었다", "이고"):
            with self.subTest(suffix=suffix):
                self.assertPreserved("담당자는 이서연" + suffix + ".", "이서연이 담당자입니다.", ("이서연",))

    def test_name_change_before_copula(self):
        self.assertChanged("서울입니다.", "서울대입니다.", "protected_terms", ("서울",))

    def test_english_name_boundary(self):
        self.assertChanged("OpenAI를 확인했습니다.", "OpenAIResearch를 확인했습니다.", "protected_terms", ("OpenAI",))

    def test_protected_name_count(self):
        self.assertChanged("서울에서 서울로 보냈습니다.", "서울에서 보냈습니다.", "protected_terms", ("서울",))

    def test_protect_missing_original_term(self):
        with self.assertRaises(checker.InputError):
            checker.compare("서울", "서울", ("부산",))

    def test_empty_protected_term(self):
        with self.assertRaises(checker.InputError):
            checker.compare("서울", "서울", ("",))

    def test_semantic_association_limit(self):
        # The tool intentionally cannot associate a number with its real-world subject.
        self.assertPreserved("오류율은 2%, 재시도율은 5%입니다.", "오류율은 5%, 재시도율은 2%입니다.")

    def test_negation_limit(self):
        self.assertPreserved("성공하지 않았습니다.", "성공했습니다.")

    def test_long_differences_do_not_dump_text(self):
        result = checker.compare("“" + "가" * 300 + "”", "“변경”")
        old = next(item for item in result["differences"] if item["original_count"])
        self.assertNotIn("value", old)
        self.assertEqual(old["value_length"], 300)
        self.assertLess(len(old["value_preview"]), 200)
        self.assertEqual(len(old["value_sha256"]), 64)


class CliTests(unittest.TestCase):
    def run_cli(self, args):
        stream = StringIO()
        with redirect_stdout(stream):
            status = checker.main(args)
        return status, json.loads(stream.getvalue())

    def test_cli_success_and_repeated_protect(self):
        with tempfile.TemporaryDirectory() as folder:
            original = Path(folder) / "original.txt"
            revised = Path(folder) / "revised.txt"
            original.write_text("서울에서 부산으로 3건을 보냈습니다.", encoding="utf-8")
            revised.write_text("3건을 서울에서 부산으로 보냈습니다.", encoding="utf-8")
            status, result = self.run_cli([str(original), str(revised), "--protect", "서울", "--protect", "부산"])
        self.assertEqual(status, 0)
        self.assertTrue(result["ok"])
        self.assertTrue(result["limitations"])

    def test_cli_difference(self):
        with tempfile.TemporaryDirectory() as folder:
            original = Path(folder) / "original.txt"
            revised = Path(folder) / "revised.txt"
            original.write_text("3건", encoding="utf-8")
            revised.write_text("4건", encoding="utf-8")
            status, result = self.run_cli([str(original), str(revised)])
        self.assertEqual(status, 1)
        self.assertFalse(result["ok"])

    def test_cli_missing_arguments(self):
        status, result = self.run_cli([])
        self.assertEqual(status, 2)
        self.assertIn("error", result)

    def test_cli_unknown_option(self):
        status, result = self.run_cli(["one", "two", "--unknown"])
        self.assertEqual(status, 2)
        self.assertIn("error", result)

    def test_cli_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            status, result = self.run_cli([str(Path(folder) / "missing.txt"), "other.txt"])
        self.assertEqual(status, 2)
        self.assertIn("error", result)

    def test_cli_non_utf8_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid.txt"
            path.write_bytes(b"\xff\xfe")
            status, result = self.run_cli([str(path), str(path)])
        self.assertEqual(status, 2)
        self.assertEqual(result["error"], "파일을 UTF-8로 읽을 수 없습니다.")

    def test_cli_missing_protected_term(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.txt"
            path.write_text("서울입니다.", encoding="utf-8")
            status, result = self.run_cli([str(path), str(path), "--protect", "부산"])
        self.assertEqual(status, 2)
        self.assertIn("보호 용어", result["error"])


if __name__ == "__main__":
    unittest.main()
