import unittest

from targetjob.models import CandidateType
from targetjob.profile_builder import build_profile, split_values


class ProfileBuilderTests(unittest.TestCase):
    def base_form(self):
        return {
            "candidate_type": "intern",
            "skills": "C++, 大模型应用",
            "school": "北京科技大学",
            "major": "信息安全",
            "degree": "本科",
            "graduation_year": "2028",
            "experience_type": "internship",
            "experience_organization": "",
            "experience_description": "",
            "experience_start_date": "",
            "experience_end_date": "",
            "project_name": "",
            "project_description": "",
            "project_source_type": "manual_description",
            "project_source_locator": "",
            "project_is_team": False,
            "project_platform_username": "",
            "project_contribution": "",
            "competition_name": "ICPC",
            "competition_result": "银牌",
            "competition_description": "",
            "target_roles": "AI 应用开发实习生, Agent 实习生",
            "target_work_content": "大模型应用、Agent、RAG、AI 安全开发",
            "target_cities": "北京",
            "salary_expectation": "15000+ / 月",
            "remote_preference": "接受",
            "company_types": ["外企"],
        }

    def test_split_values_discards_empty_items(self):
        self.assertEqual(split_values("C++, , Python"), ["C++", "Python"])

    def test_builder_keeps_blank_optional_sections_empty(self):
        profile = build_profile(**self.base_form())
        self.assertEqual(profile.candidate_type, CandidateType.INTERN)
        self.assertEqual(profile.skills, ["C++", "大模型应用"])
        self.assertEqual(profile.projects, [])
        self.assertEqual(profile.experiences, [])
        self.assertEqual(profile.competitions[0].result, "银牌")

    def test_builder_creates_team_project_evidence(self):
        form = self.base_form()
        form.update(
            {
                "project_name": "安全知识库 Agent",
                "project_description": "实现文档检索和问答。",
                "project_source_type": "repository",
                "project_source_locator": "https://example.com/repo",
                "project_is_team": True,
                "project_platform_username": "example-user",
            }
        )
        profile = build_profile(**form)
        self.assertEqual(profile.projects[0].platform_username, "example-user")


if __name__ == "__main__":
    unittest.main()
