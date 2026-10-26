import unittest
from datetime import date

import check_numbers as cn


def verdicts(**changes):
    spec = {**cn.SPEC, **changes}
    return {fid: mark for fid, mark, _ in cn.checks(spec)}


class EdgeCases(unittest.TestCase):
    def test_published_spec_fails(self):
        self.assertEqual(cn.main([]), 1)

    def test_zero_spend_is_a_contradiction(self):
        self.assertEqual(verdicts(week_spend=0.0)["F08"], "✗")

    def test_spend_far_above_input_cost_is_not_ok(self):
        self.assertEqual(verdicts(week_spend=0.40)["F08"], "!")

    def test_spend_equal_to_input_cost_is_unexplained(self):
        self.assertEqual(verdicts()["F08"], "!")

    def test_no_signals_does_not_crash(self):
        result = verdicts(social=0, web=0, unique=0, web_shown=0, threats=0, per_competitor=[])
        self.assertEqual(set(result), {f"F0{i}" for i in range(1, 9)})

    def test_consistent_numbers_pass(self):
        result = verdicts(
            escalated_kpi=2, brief_promised=2,
            per_competitor=[2070 // 7] * 6 + [2070 - 6 * (2070 // 7)],
            competitors_claimed=7, graph_nodes=7,
            window=(date(2026, 9, 20), date(2026, 9, 27)),
            noise=0.04, threats=600,
        )
        for fid in ("F02", "F03", "F04", "F05", "F06"):
            self.assertEqual(result[fid], "✓", fid)

    def test_duplicates_all_from_social_are_flagged(self):
        self.assertEqual(verdicts(web_shown=1158)["F01"], "!")

    def test_duplicates_split_between_sources_pass(self):
        self.assertEqual(verdicts(web_shown=947)["F01"], "✓")

    def test_assumptions_are_listed(self):
        self.assertEqual(cn.main(["--assumptions"]), 0)


if __name__ == "__main__":
    unittest.main()
