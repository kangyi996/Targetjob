"""Targetjob Streamlit entry point.

Run locally with:
    streamlit run app.py
"""

import streamlit as st

from targetjob.analyzer import PERSONA_LABELS, analyze
from targetjob.models import ExperienceType
from targetjob.profile_builder import build_profile
from targetjob.profile_validator import validate_profile


EXPERIENCE_LABELS = {
    "work": "工作",
    "internship": "实习",
    "part_time": "兼职",
    "volunteer": "志愿者",
}

PROJECT_SOURCE_LABELS = {
    "manual_description": "手动描述",
    "repository": "代码仓库",
    "uploaded_file": "上传文件",
    "portfolio_url": "作品集链接",
}


st.set_page_config(
    page_title="Targetjob · 智能求职助手",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 Targetjob 智能求职助手")
st.caption("先建立求职画像，再决定是否进入岗位搜索和匹配分析。")

st.header("第一步：建立求职画像")

with st.form("candidate_profile_form"):
    st.subheader("基本信息")
    candidate_type = st.selectbox(
        "求职身份",
        options=list(PERSONA_LABELS),
        format_func=lambda value: PERSONA_LABELS[value],
    )
    skills = st.text_input(
        "技能（多个技能用逗号分隔）",
        placeholder="例如：C++, Python, 大模型应用",
    )

    st.subheader("教育经历")
    education_left, education_right = st.columns(2)
    with education_left:
        school = st.text_input("学校")
        major = st.text_input("专业")
    with education_right:
        degree = st.text_input("学历", placeholder="例如：本科")
        graduation_year = st.text_input("预计毕业年份", placeholder="例如：2028")

    st.subheader("一段工作或实习经历（可选）")
    experience_left, experience_right = st.columns(2)
    with experience_left:
        experience_type = st.selectbox(
            "经历类型",
            options=[item.value for item in ExperienceType],
            format_func=lambda value: EXPERIENCE_LABELS[value],
        )
        experience_organization = st.text_input("公司或组织")
        experience_start_date = st.text_input("开始时间（可选）", placeholder="例如：2026-06")
    with experience_right:
        experience_description = st.text_area(
            "在这段经历中做了什么",
            placeholder="请描述主要工作、使用的技能和取得的结果。",
        )
        experience_end_date = st.text_input("结束时间（可选）", placeholder="例如：2026-09")

    st.subheader("一个项目经历（可选）")
    project_left, project_right = st.columns(2)
    with project_left:
        project_name = st.text_input("项目名称")
        project_source_type = st.selectbox(
            "项目来源类型",
            options=list(PROJECT_SOURCE_LABELS),
            format_func=lambda value: PROJECT_SOURCE_LABELS[value],
        )
        project_source_locator = st.text_input("项目链接或文件标识（可选）")
        project_is_team = st.checkbox("这是团队项目")
    with project_right:
        project_description = st.text_area(
            "项目中做了什么",
            placeholder="请描述项目目标、功能、技术和结果。",
        )
        project_platform_username = st.text_input("代码平台用户名（团队项目至少提供一项）")
        project_contribution = st.text_area("个人负责内容（团队项目至少提供一项）")

    st.subheader("竞赛经历（可选）")
    competition_left, competition_right = st.columns(2)
    with competition_left:
        competition_name = st.text_input("竞赛名称")
        competition_result = st.text_input("竞赛结果", placeholder="例如：ICPC 银牌")
    with competition_right:
        competition_description = st.text_area("竞赛补充说明（可选）")

    st.subheader("求职意向")
    target_roles = st.text_input(
        "目标岗位（多个岗位用逗号分隔）",
        placeholder="例如：AI 应用开发实习生, Agent 实习生",
    )
    target_work_content = st.text_area(
        "目标工作内容",
        placeholder="例如：大模型应用、Agent、RAG、AI 安全相关开发。",
    )
    preference_left, preference_right = st.columns(2)
    with preference_left:
        target_cities = st.text_input(
            "目标城市（多个城市用逗号分隔）",
            placeholder="例如：北京",
        )
        salary_expectation = st.text_input(
            "薪资期望",
            placeholder="例如：15000+ / 月、面议或暂不确定",
        )
        remote_preference = st.selectbox("远程偏好", options=["接受", "不接受", "都可以"])
    with preference_right:
        company_types = st.multiselect(
            "公司类型偏好",
            options=["国企", "央企", "外企", "民企", "初创公司", "都可以"],
        )

    profile_submitted = st.form_submit_button(
        "检查求职画像",
        type="primary",
        use_container_width=True,
    )


if profile_submitted:
    try:
        profile = build_profile(
            candidate_type=candidate_type,
            skills=skills,
            school=school,
            major=major,
            degree=degree,
            graduation_year=graduation_year,
            experience_type=experience_type,
            experience_organization=experience_organization,
            experience_description=experience_description,
            experience_start_date=experience_start_date,
            experience_end_date=experience_end_date,
            project_name=project_name,
            project_description=project_description,
            project_source_type=project_source_type,
            project_source_locator=project_source_locator,
            project_is_team=project_is_team,
            project_platform_username=project_platform_username,
            project_contribution=project_contribution,
            competition_name=competition_name,
            competition_result=competition_result,
            competition_description=competition_description,
            target_roles=target_roles,
            target_work_content=target_work_content,
            target_cities=target_cities,
            salary_expectation=salary_expectation,
            remote_preference=remote_preference,
            company_types=company_types,
        )
        validation = validate_profile(profile)
        st.session_state["candidate_profile"] = profile
        st.session_state["profile_validation"] = validation
    except ValueError as error:
        st.session_state.pop("candidate_profile", None)
        st.session_state["profile_validation"] = None
        st.error(str(error))


validation = st.session_state.get("profile_validation")
profile = st.session_state.get("candidate_profile")

if validation is None or profile is None:
    st.info("填写并提交求职画像后，系统会检查你是否可以进入岗位搜索。")
    st.stop()

if validation.can_search:
    st.success("画像信息足够完整，可以进入岗位搜索阶段。")
    st.write(f"当前身份：{PERSONA_LABELS[profile.candidate_type.value]}")
else:
    st.error("画像信息还不完整，请先补充以下内容：")
    for missing_field in validation.missing_fields:
        st.write(f"- {missing_field}")

for recommendation in validation.recommendations:
    st.warning(recommendation)

if not validation.can_search:
    st.stop()

st.header("第二步：职位匹配分析演示")
st.caption("当前仍使用本地规则分析；岗位搜索工具和 Agent 编排将在后续阶段接入。")

resume_text = st.text_area(
    "你的简历文本",
    height=220,
    placeholder="请粘贴简历文本，后续会改为从求职画像和上传文件自动生成。",
)
job_description = st.text_area(
    "目标职位描述",
    height=220,
    placeholder="请粘贴职位描述，后续会改为由岗位搜索工具提供。",
)

analyze_clicked = st.button("开始匹配分析", type="primary", use_container_width=True)

if analyze_clicked:
    if not resume_text.strip():
        st.error("请先输入简历内容。")
    elif not job_description.strip():
        st.error("请先输入目标职位描述。")
    else:
        with st.spinner("正在分析职位和简历……"):
            result = analyze(
                candidate_type=profile.candidate_type.value,
                resume_text=resume_text,
                job_description=job_description,
            )

        st.success("分析完成！")
        st.header("分析报告")
        st.write(result.role_summary)

        left, right = st.columns(2)
        with left:
            st.subheader("匹配优势")
            for strength in result.matched_strengths:
                st.success(strength)
        with right:
            st.subheader("能力缺口或证据不足")
            for gap in result.gaps:
                st.warning(gap)

        st.subheader("为什么这样判断？")
        for evidence in result.evidence:
            st.write(f"- {evidence}")
        st.subheader("简历改进建议")
        for advice in result.resume_advice:
            st.write(f"- {advice}")
        st.subheader("面试准备问题")
        for question in result.interview_questions:
            st.write(f"- {question}")

