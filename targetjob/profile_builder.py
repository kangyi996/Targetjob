"""Convert values from the Streamlit form into a CandidateProfile."""

from targetjob.models import (
    CandidateProfile,
    CandidateType,
    Competition,
    Education,
    Experience,
    ExperienceType,
    JobPreferences,
    ProjectExperience,
)


def split_values(raw_value: str) -> list[str]:
    """Split comma-separated form input into clean values."""

    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _optional_year(raw_value: str) -> int | None:
    value = raw_value.strip()
    if not value:
        return None
    if not value.isdigit():
        raise ValueError("毕业年份必须是数字，例如 2028。")
    return int(value)


def build_profile(
    *,
    candidate_type: str,
    skills: str,
    school: str,
    major: str,
    degree: str,
    graduation_year: str,
    experience_type: str,
    experience_organization: str,
    experience_description: str,
    experience_start_date: str,
    experience_end_date: str,
    project_name: str,
    project_description: str,
    project_source_type: str,
    project_source_locator: str,
    project_is_team: bool,
    project_platform_username: str,
    project_contribution: str,
    competition_name: str,
    competition_result: str,
    competition_description: str,
    target_roles: str,
    target_work_content: str,
    target_cities: str,
    salary_expectation: str,
    remote_preference: str,
    company_types: list[str],
) -> CandidateProfile:
    """Build a profile while keeping blank optional sections empty."""

    education = []
    if any(item.strip() for item in (school, major, degree, graduation_year)):
        education.append(
            Education(
                school=school.strip(),
                major=major.strip(),
                degree=degree.strip(),
                graduation_year=_optional_year(graduation_year),
            )
        )

    experiences = []
    if any(
        item.strip()
        for item in (
            experience_organization,
            experience_description,
            experience_start_date,
            experience_end_date,
        )
    ):
        experiences.append(
            Experience(
                experience_type=ExperienceType(experience_type),
                organization=experience_organization.strip(),
                description=experience_description.strip(),
                start_date=experience_start_date.strip() or None,
                end_date=experience_end_date.strip() or None,
            )
        )

    projects = []
    if any(item.strip() for item in (project_name, project_description, project_source_locator)):
        projects.append(
            ProjectExperience(
                name=project_name.strip(),
                description=project_description.strip(),
                source_type=project_source_type,
                source_locator=project_source_locator.strip() or None,
                is_team_project=project_is_team,
                platform_username=project_platform_username.strip() or None,
                contribution_description=project_contribution.strip() or None,
            )
        )

    competitions = []
    if any(item.strip() for item in (competition_name, competition_result, competition_description)):
        competitions.append(
            Competition(
                name=competition_name.strip(),
                result=competition_result.strip(),
                description=competition_description.strip(),
            )
        )

    return CandidateProfile(
        candidate_type=CandidateType(candidate_type),
        skills=split_values(skills),
        education=education,
        experiences=experiences,
        projects=projects,
        competitions=competitions,
        preferences=JobPreferences(
            target_roles=split_values(target_roles),
            target_work_content=target_work_content.strip(),
            target_cities=split_values(target_cities),
            salary_expectation=salary_expectation.strip(),
            remote_preference=remote_preference.strip(),
            company_types=[item.strip() for item in company_types if item.strip()],
        ),
    )

