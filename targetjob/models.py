"""Structured data models for a Targetjob candidate profile."""

from dataclasses import dataclass
from enum import Enum


class CandidateType(str, Enum):
    """The three user-facing candidate categories."""

    STUDENT = "student"
    INTERN = "intern"
    EXPERIENCED = "experienced"


class ExperienceType(str, Enum):
    WORK = "work"
    INTERNSHIP = "internship"
    PART_TIME = "part_time"
    VOLUNTEER = "volunteer"


@dataclass(frozen=True)
class Education:
    school: str
    major: str
    degree: str
    graduation_year: int | None = None


@dataclass(frozen=True)
class Experience:
    experience_type: ExperienceType
    organization: str
    description: str
    start_date: str | None = None
    end_date: str | None = None


@dataclass(frozen=True)
class ProjectExperience:
    name: str
    description: str
    source_type: str = "manual_description"
    source_locator: str | None = None
    is_team_project: bool = False
    platform_username: str | None = None
    contribution_description: str | None = None


@dataclass(frozen=True)
class Competition:
    name: str
    result: str
    description: str = ""


@dataclass(frozen=True)
class JobPreferences:
    target_roles: list[str]
    target_work_content: str
    target_cities: list[str]
    salary_expectation: str
    remote_preference: str
    company_types: list[str]


@dataclass(frozen=True)
class CandidateProfile:
    candidate_type: CandidateType
    skills: list[str]
    education: list[Education]
    experiences: list[Experience]
    projects: list[ProjectExperience]
    competitions: list[Competition]
    preferences: JobPreferences

