import unittest

from targetjob.analyzer import PERSONA_LABELS, analyze


class AnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resume = "我使用 Python 和 SQL 完成过数据分析项目，并通过 Git 管理代码。"
        self.job_description = "岗位要求 Python、SQL、Docker，以及良好的沟通能力。"

    def test_all_personas_are_supported(self) -> None:
        for persona in PERSONA_LABELS:
            result = analyze(persona, self.resume, self.job_description)
            self.assertIn("身份", result.role_summary)
            self.assertGreater(len(result.matched_strengths), 0)

    def test_matching_and_gap_are_explained(self) -> None:
        result = analyze("intern", self.resume, self.job_description)
        self.assertTrue(any("Python" in item for item in result.matched_strengths))
        self.assertTrue(any("Docker" in item for item in result.gaps))
        self.assertGreaterEqual(len(result.evidence), 2)

    def test_short_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            analyze("student", "太短", self.job_description)
        with self.assertRaises(ValueError):
            analyze("student", self.resume, "太短")

    def test_unknown_persona_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            analyze("unknown", self.resume, self.job_description)


if __name__ == "__main__":
    unittest.main()
