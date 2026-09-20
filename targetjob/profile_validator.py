"""Deterministic completeness checks for candidate profiles."""

from dataclasses import dataclass, field

from targetjob.models import CandidateProfile, CandidateType


@dataclass(frozen=True)
class ProfileValidation:
    can_search: bool
    missing_fields: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


def _has_text(value: str | None) -> bool:
    return bool(value and value.strip())


def _has_values(values: list[str]) -> bool:
    return any(_has_text(value) for value in values)


def validate_profile(profile: CandidateProfile) -> ProfileValidation:
    """Check whether a profile contains enough information to search jobs."""

    missing: list[str] = []
    recommendations: list[str] = []
    preferences = profile.preferences

    if not _has_values(profile.skills):
        missing.append("至少填写一项技能")
    if not profile.education:
        missing.append("至少填写一段教育经历")
    else:
        for education in profile.education:
            if not _has_text(education.school):
                missing.append("教育经历需要填写学校")
            if not _has_text(education.major):
                missing.append("教育经历需要填写专业")
            if not _has_text(education.degree):
                missing.append("教育经历需要填写学历")

    if not _has_values(preferences.target_roles):
        missing.append("目标岗位")
    if not _has_text(preferences.target_work_content):
        missing.append("目标工作内容")
    if not _has_values(preferences.target_cities):
        missing.append("目标城市")
    if not _has_text(preferences.salary_expectation):
        missing.append("薪资期望")
    if not _has_text(preferences.remote_preference):
        missing.append("远程偏好")
    if not _has_values(preferences.company_types):
        missing.append("公司类型偏好")

    if profile.candidate_type == CandidateType.EXPERIENCED and not profile.experiences:
        missing.append("有工作经验的求职者至少需要一段经历")
    elif profile.candidate_type in {CandidateType.STUDENT, CandidateType.INTERN}:
        if not (profile.experiences or profile.projects or profile.competitions):
            missing.append("应届生或实习生至少需要一项经历、项目或竞赛")

    for index, project in enumerate(profile.projects, start=1):
        if not _has_text(project.name):
            missing.append(f"第 {index} 个项目需要填写项目名称")
        if not _has_text(project.description):
            missing.append(f"第 {index} 个项目需要填写项目描述")
        if project.is_team_project:
            has_username = _has_text(project.platform_username)
            has_contribution = _has_text(project.contribution_description)
            if not (has_username or has_contribution):
                missing.append(
                    f"第 {index} 个团队项目需要填写平台用户名或个人负责内容"
                )

    if not profile.projects:
        recommendations.append("建议补充至少一个可展示的项目，增强简历证据")
    if not profile.competitions:
        recommendations.append("如果有竞赛经历，建议补充竞赛名称和结果")

    return ProfileValidation(
        can_search=not missing,
        missing_fields=missing,
        recommendations=recommendations,
    )

