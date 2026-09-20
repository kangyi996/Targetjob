"""A small, explainable analyzer for the first Targetjob MVP.

This module intentionally uses local keyword matching instead of an external
model. It gives us a working end-to-end demo before adding model integration.
"""

from dataclasses import dataclass
import re


PERSONA_LABELS = {
    "student": "应届生",
    "intern": "实习生",
    "experienced": "有工作经验的求职者",
}

PERSONA_FOCUS = {
    "student": "重点关注课程项目、校园经历、实习经历和成长潜力。",
    "intern": "重点关注基础技能、课程项目、学习能力和实习目标。",
    "experienced": "重点关注工作成果、业务影响、职责深度和专业能力。",
}

# This is deliberately a small, readable catalog for the first demo.
# Later, the model layer can extract richer requirements from free-form text.
KEYWORD_CATALOG = {
    "Python": ("python", "py"),
    "Java": "java",
    "C++": "c++",
    "SQL": "sql",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "React": "react",
    "Vue": "vue",
    "FastAPI": "fastapi",
    "Django": "django",
    "Streamlit": "streamlit",
    "Git": "git",
    "Docker": "docker",
    "AWS": "aws",
    "数据分析": "数据分析",
    "机器学习": "机器学习",
    "产品设计": "产品设计",
    "用户研究": "用户研究",
    "英语": "英语",
    "Excel": "excel",
    "沟通": "沟通",
    "团队协作": "团队协作",
}


@dataclass(frozen=True)
class AnalysisResult:
    """Structured result rendered by the web interface."""

    role_summary: str
    matched_strengths: list[str]
    gaps: list[str]
    evidence: list[str]
    resume_advice: list[str]
    interview_questions: list[str]


def _normalise(text: str) -> str:
    """Make matching less sensitive to case and extra whitespace."""

    return re.sub(r"\s+", " ", text.strip().lower())


def _find_keywords(text: str) -> set[str]:
    normalised = _normalise(text)
    found = set()
    for label, keyword in KEYWORD_CATALOG.items():
        keywords = keyword if isinstance(keyword, tuple) else (keyword,)
        if any(item in normalised for item in keywords):
            found.add(label)
    return found


def _validate_inputs(candidate_type: str, resume_text: str, job_description: str) -> None:
    if candidate_type not in PERSONA_LABELS:
        raise ValueError("candidate_type 不是受支持的身份类型。")
    if len(resume_text.strip()) < 10:
        raise ValueError("简历内容太短，请提供更多教育、项目、实习或工作信息。")
    if len(job_description.strip()) < 10:
        raise ValueError("职位描述太短，请提供更多职责或任职要求。")


def analyze(candidate_type: str, resume_text: str, job_description: str) -> AnalysisResult:
    """Analyze resume/job text with a deterministic local rule set."""

    _validate_inputs(candidate_type, resume_text, job_description)

    resume_keywords = _find_keywords(resume_text)
    job_keywords = _find_keywords(job_description)
    matched_keywords = sorted(resume_keywords & job_keywords)
    missing_keywords = sorted(job_keywords - resume_keywords)
    persona_label = PERSONA_LABELS[candidate_type]

    if matched_keywords:
        matched_strengths = [
            f"你的简历提到了「{keyword}」，与职位要求中的相关内容匹配。"
            for keyword in matched_keywords
        ]
    else:
        matched_strengths = [
            "暂时没有识别到明确的关键词匹配，建议补充具体技能、项目或工作成果。"
        ]

    if missing_keywords:
        gaps = [
            f"职位要求中出现了「{keyword}」，但简历中暂未识别到对应证据。"
            for keyword in missing_keywords
        ]
    else:
        gaps = ["已识别到的职位关键词都在简历中出现，仍建议补充量化成果来增强可信度。"]

    evidence = [
        f"本次分析身份：{persona_label}。{PERSONA_FOCUS[candidate_type]}",
        f"从职位描述中识别到 {len(job_keywords)} 个演示关键词，"
        f"其中 {len(matched_keywords)} 个也出现在简历中。",
    ]

    resume_advice = [
        "把与目标职位最相关的经历放在更靠前的位置。",
        "尽量用“做了什么 + 使用什么方法 + 产生什么结果”描述经历。",
    ]
    if missing_keywords:
        resume_advice.append(
            "如果你确实具备这些能力，请在简历中补充对应项目、课程、实习或工作证据："
            + "、".join(missing_keywords)
            + "。"
        )
    resume_advice.append(f"结合你的身份（{persona_label}），{PERSONA_FOCUS[candidate_type]}")

    interview_questions = [
        "请介绍一段最能证明你适合这个职位的经历。",
        "职位要求中的哪些能力是你的优势？请结合具体例子说明。",
        "如果入职后需要补足某项能力，你会如何安排学习和实践？",
    ]
    if missing_keywords:
        interview_questions.append(
            "你对职位要求中的这些能力了解多少？如果目前经验不足，你准备如何补足："
            + "、".join(missing_keywords)
            + "？"
        )

    return AnalysisResult(
        role_summary=(
            f"你选择的身份是“{persona_label}”。本次报告会结合该身份，"
            "对比职位要求和简历中能够识别到的内容。"
        ),
        matched_strengths=matched_strengths,
        gaps=gaps,
        evidence=evidence,
        resume_advice=resume_advice,
        interview_questions=interview_questions,
    )
