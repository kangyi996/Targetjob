import unittest

from targetjob.models import (
    CandidateProfile,
    CandidateType,
    Competition,
    Education,
    JobPreferences,
    ProjectExperience,
)
from targetjob.profile_validator import validate_profile


def make_preferences(**overrides):
    values = {
        "target_roles": ["AI 应用开发实习生"],
        "target_work_content": "大模型应用、Agent 和 RAG 开发",
        "target_cities": ["北京"],
        "salary_expectation": "15000+ / 月",
        "remote_preference": "接受",
        "company_types": ["外企"],
    }
    values.update(overrides)
    return JobPreferences(**values)


def make_intern_profile(**overrides):
    values = {
        "candidate_type": CandidateType.INTERN,
        "skills": ["C++", "大模型应用"],
        "education": [Education("北京科技大学", "信息安全", "本科", 2028)],
        "experiences": [],
        "projects": [],
        "competitions": [Competition("ICPC", "银牌")],
        "preferences": make_preferences(),
    }
    values.update(overrides)
    return CandidateProfile(**values)


class ProfileValidatorTests(unittest.TestCase):
    def test_intern_with_competition_can_search_without_project(self):
        result = validate_profile(make_intern_profile())
        self.assertTrue(result.can_search)
        self.assertEqual(result.missing_fields, [])
        self.assertTrue(any("项目" in item for item in result.recommendations))

    def test_missing_search_preference_blocks_search(self):
        profile = make_intern_profile(
            preferences=make_preferences(target_cities=[]),
        )
        result = validate_profile(profile)
        self.assertFalse(result.can_search)
        self.assertIn("目标城市", result.missing_fields)

    def test_team_project_needs_identity_or_contribution(self):
        project = ProjectExperience(
            name="安全知识库 Agent",
            description="实现文档检索和问答流程。",
            source_type="repository",
            source_locator="https://example.com/repo",
            is_team_project=True,
        )
        result = validate_profile(make_intern_profile(projects=[project]))
        self.assertFalse(result.can_search)
        self.assertTrue(any("团队项目" in item for item in result.missing_fields))

    def test_team_project_with_contribution_can_search(self):
        project = ProjectExperience(
            name="安全知识库 Agent",
            description="实现文档检索和问答流程。",
            is_team_project=True,
            contribution_description="负责检索模块和后端接口。",
        )
        result = validate_profile(make_intern_profile(projects=[project]))
        self.assertTrue(result.can_search)


if __name__ == "__main__":
    unittest.main()
