"""Synthetic behavior tests only: these do not establish model or proxy quality."""

import importlib.util
import io
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "calibrate_proxy.py"
SPEC = importlib.util.spec_from_file_location("calibrate_proxy_under_test", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def fixture(proxy=(1, 2, 3, 4, 5), target=(1, 2, 3, 4, 5), calibration=(100, -100)):
    lines = ["id,family,split,proxy,target", f"cal,fit-family,calibration,{calibration[0]},{calibration[1]}"]
    lines.extend(
        f"hold-{index},hold-family-{index},confirmation,{p},{t}"
        for index, (p, t) in enumerate(zip(proxy, target))
    )
    return "\n".join(lines) + "\n"


def report(text=None, **kwargs):
    options = {"proxy_direction": "higher", "target_direction": "higher"}
    options.update(kwargs)
    return MODULE.analyze(MODULE.read_csv(io.StringIO(text or fixture())), **options)


class InputValidationTests(unittest.TestCase):
    def assert_invalid(self, text):
        with self.assertRaises(MODULE.InputError):
            MODULE.read_csv(io.StringIO(text))

    def test_missing_header_or_rows(self):
        for text in ("", "id,family,split,proxy,target\n"):
            with self.subTest(text=text):
                self.assert_invalid(text)

    def test_duplicate_missing_or_extra_header(self):
        for header in (
            "id,id,split,proxy,target", "id,family,split,proxy", "id,family,split,proxy,target,extra",
        ):
            with self.subTest(header=header):
                self.assert_invalid(fixture().replace("id,family,split,proxy,target", header, 1))

    def test_missing_values_or_wrong_row_width(self):
        for row in (
            ",fit-family,calibration,1,2", "cal,,calibration,1,2", "cal,fit-family,,1,2",
            "cal,fit-family,calibration,,2", "cal,fit-family,calibration,1,",
            "cal,fit-family,calibration,1", "cal,fit-family,calibration,1,2,3",
        ):
            with self.subTest(row=row):
                self.assert_invalid(fixture().replace("cal,fit-family,calibration,100,-100", row))

    def test_duplicate_id_across_and_within_splits(self):
        self.assert_invalid(fixture().replace("hold-0,", "cal,", 1))
        self.assert_invalid(fixture().replace("hold-1,", "hold-0,", 1))

    def test_family_leakage(self):
        self.assert_invalid(fixture().replace("hold-family-3", "fit-family"))

    def test_each_split_is_required(self):
        self.assert_invalid(fixture().replace(",calibration,", ",confirmation,"))
        self.assert_invalid(fixture().replace(",confirmation,", ",calibration,"))

    def test_unknown_split(self):
        self.assert_invalid(fixture().replace(",calibration,", ",train,"))

    def test_nan_infinity_overflow_and_nonnumeric(self):
        for value in ("nan", "NaN", "inf", "-Infinity", "1e999", "oops"):
            for column in ("proxy", "target"):
                with self.subTest(value=value, column=column):
                    replacement = (f"cal,fit-family,calibration,{value},1" if column == "proxy"
                                   else f"cal,fit-family,calibration,1,{value}")
                    self.assert_invalid(fixture().replace("cal,fit-family,calibration,100,-100", replacement))

    def test_whitespace_is_normalized_before_leak_check(self):
        self.assert_invalid(fixture().replace("hold-family-0", " fit-family "))

    def test_options_reject_invalid_values(self):
        for option in ({"top_k": 0}, {"top_k": 6}, {"min_confirmation": 1},
                       {"proxy_direction": "unknown"}, {"target_direction": "unknown"}):
            with self.subTest(option=option), self.assertRaises(MODULE.InputError):
                report(**option)


class RankingTests(unittest.TestCase):
    def test_perfect_ranking_is_diagnostic_not_pass(self):
        result = report()
        self.assertEqual(result["status"], "DIAGNOSTIC_ONLY")
        self.assertAlmostEqual(result["spearman"], 1)
        self.assertEqual(result["pairwise"]["strict_discordant_pairs"], 0)
        self.assertEqual(result["top_k"]["retention_fraction_min"], 1)
        self.assertFalse(result["calibration_used_for_fitting"])
        self.assertEqual(result["metric_split"], "confirmation")

    def test_rank_reversal(self):
        result = report(fixture(target=(5, 4, 3, 2, 1)), top_k=2)
        self.assertAlmostEqual(result["spearman"], -1)
        self.assertEqual(result["pairwise"]["strict_discordance_fraction"], 1)
        self.assertEqual(result["pairwise"]["strict_discordant_pairs"], 10)
        self.assertEqual(result["top_k"]["retained_count_max"], 0)

    def test_directions_are_independent(self):
        for p_direction, t_direction, expected in (
            ("higher", "higher", 1), ("lower", "lower", 1),
            ("higher", "lower", -1), ("lower", "higher", -1),
        ):
            with self.subTest(p=p_direction, t=t_direction):
                self.assertAlmostEqual(report(proxy_direction=p_direction, target_direction=t_direction)["spearman"], expected)

    def test_lower_scores_pick_lowest_top_k(self):
        result = report(proxy_direction="lower", target_direction="lower", top_k=2)
        self.assertEqual(result["top_k"]["proxy_definite_ids"], ["hold-0"])
        self.assertEqual(result["top_k"]["proxy_boundary_ids"], ["hold-1"])
        self.assertEqual(result["top_k"]["retained_count_min"], 2)

    def test_calibration_scores_do_not_change_confirmation_metrics(self):
        first = report(fixture(calibration=(1e300, -1e300)))
        second = report(fixture(calibration=(-7, 10)))
        self.assertEqual(first, second)

    def test_zero_floor_is_uninformative(self):
        result = report(fixture(target=(0, 0, 0, 0, 0)), top_k=2)
        self.assertEqual(result["status"], "UNINFORMATIVE")
        self.assertIn("constant_target", result["reasons"])
        self.assertIsNone(result["spearman"])
        self.assertEqual(result["pairwise"]["target_tie_fraction"], 1)
        self.assertIsNone(result["pairwise"]["strict_discordance_fraction"])
        self.assertTrue(result["top_k"]["boundary_tie_ambiguous"])
        self.assertEqual(result["top_k"]["retention_fraction_min"], 0)
        self.assertEqual(result["top_k"]["retention_fraction_max"], 1)

    def test_both_axes_constant(self):
        result = report(fixture(proxy=(0,) * 5, target=(0,) * 5), top_k=3)
        self.assertEqual(result["status"], "UNINFORMATIVE")
        self.assertEqual(result["pairwise"]["both_tie_pairs"], 10)
        self.assertEqual(result["pairwise"]["either_tie_pairs"], 10)
        self.assertEqual(result["top_k"]["retained_count_min"], 1)
        self.assertEqual(result["top_k"]["retained_count_max"], 3)

    def test_tiny_sample_is_insufficient_even_with_perfect_correlation(self):
        result = report(fixture(proxy=(1, 2), target=(1, 2)))
        self.assertEqual(result["status"], "INSUFFICIENT")
        self.assertAlmostEqual(result["spearman"], 1)

    def test_single_confirmation_is_defined_but_insufficient(self):
        result = report(fixture(proxy=(1,), target=(1,)))
        self.assertEqual(result["status"], "INSUFFICIENT")
        self.assertIsNone(result["spearman"])
        self.assertIsNone(result["pairwise"]["either_tie_fraction"])

    def test_average_ranks_and_partial_tie_correlation(self):
        self.assertEqual(MODULE.average_ranks([1, 1, 3, 2]), [1.5, 1.5, 4, 3])
        self.assertAlmostEqual(MODULE.spearman([1, 1, 2, 3], [1, 2, 3, 4]), 0.9486832980505138)

    def test_partial_ties_use_strict_denominator(self):
        result = report(fixture(proxy=(1, 1, 2, 3, 4), target=(1, 2, 2, 4, 3)))
        pair = result["pairwise"]
        self.assertEqual(result["status"], "DIAGNOSTIC_ONLY")
        self.assertEqual(pair["proxy_tie_pairs"], 1)
        self.assertEqual(pair["target_tie_pairs"], 1)
        self.assertEqual(pair["jointly_strict_pairs"], 8)
        self.assertEqual(pair["strict_discordant_pairs"], 1)
        self.assertEqual(pair["strict_discordance_fraction"], 1 / 8)

    def test_duplicate_families_inside_confirmation_are_counted_not_independent(self):
        result = report(fixture().replace("hold-family-1", "hold-family-0"))
        self.assertEqual(result["counts"]["confirmation_rows"], 5)
        self.assertEqual(result["counts"]["confirmation_families"], 4)

    def test_large_finite_score_magnitudes_do_not_overflow(self):
        result = report(fixture(proxy=(-1e308, -1e200, 0, 1e200, 1e308)))
        self.assertAlmostEqual(result["spearman"], 1)
        json.dumps(result, allow_nan=False)


class CombinatorialCrossChecks(unittest.TestCase):
    def test_pairwise_matches_independent_brute_force(self):
        rng = random.Random(20260906)
        for _ in range(100):
            p = [rng.randrange(4) for _ in range(9)]
            t = [rng.randrange(4) for _ in range(9)]
            pairs = list(itertools.combinations(range(len(p)), 2))
            discord = sum((p[a] - p[b]) * (t[a] - t[b]) < 0 for a, b in pairs)
            strict = sum(p[a] != p[b] and t[a] != t[b] for a, b in pairs)
            actual = MODULE.pairwise_metrics(p, t)
            self.assertEqual(actual["strict_discordant_pairs"], discord)
            self.assertEqual(actual["jointly_strict_pairs"], strict)

    def test_top_k_bounds_match_exhaustive_tie_breaks(self):
        # Independently enumerate all legal size-k sets for small synthetic data.
        rng = random.Random(20260907)
        for _ in range(120):
            n = rng.randrange(2, 8)
            ids = [str(index) for index in range(n)]
            p = [rng.randrange(3) for _ in ids]
            t = [rng.randrange(3) for _ in ids]
            k = rng.randrange(1, n + 1)

            def legal_sets(values):
                result = []
                for subset in itertools.combinations(range(n), k):
                    selected = set(subset)
                    outside = set(range(n)) - selected
                    if not outside or min(values[i] for i in selected) >= max(values[i] for i in outside):
                        result.append(selected)
                return result

            overlaps = [len(a & b) for a in legal_sets(p) for b in legal_sets(t)]
            result = MODULE.top_k_retention(ids, p, t, k)
            self.assertEqual(result["retained_count_min"], min(overlaps), (p, t, k))
            self.assertEqual(result["retained_count_max"], max(overlaps), (p, t, k))

    def test_boundary_tie_without_arbitrary_id_tie_break(self):
        result = MODULE.top_k_retention(["a", "b", "c", "d"], [4, 3, 3, 1], [4, 3, 2, 1], 2)
        self.assertTrue(result["boundary_tie_ambiguous"])
        self.assertEqual((result["retained_count_min"], result["retained_count_max"]), (1, 2))

    def test_ties_fully_included_are_not_boundary_ambiguous(self):
        result = MODULE.top_k_retention(["a", "b", "c"], [2, 2, 1], [2, 2, 1], 2)
        self.assertFalse(result["boundary_tie_ambiguous"])
        self.assertEqual(result["retained_count_min"], 2)


class CliTests(unittest.TestCase):
    def invoke(self, text, *extra):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "-", "--proxy-direction", "higher", "--target-direction", "higher", *extra],
            input=text, text=True, capture_output=True, check=False,
        )

    def test_valid_cli_outputs_json_and_input_digest(self):
        result = self.invoke(fixture())
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "DIAGNOSTIC_ONLY")
        self.assertEqual(len(payload["input_sha256"]), 64)
        self.assertEqual(result.stderr, "")

    def test_invalid_cli_fails_closed(self):
        result = self.invoke(fixture().replace("hold-family-0", "fit-family"))
        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "INVALID_INPUT")
        self.assertNotIn("spearman", payload)

    def test_utf8_bom_is_supported(self):
        result = self.invoke("\ufeff" + fixture())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_top_k_larger_than_confirmation_fails_closed(self):
        result = self.invoke(fixture(), "--top-k", "6")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "INVALID_INPUT")


if __name__ == "__main__":
    unittest.main()
