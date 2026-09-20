"""Targetjob Streamlit entry point.

Run locally with:
    streamlit run app.py
"""

import streamlit as st

from targetjob.analyzer import PERSONA_LABELS, analyze


st.set_page_config(
    page_title="Targetjob · 智能求职助手",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 Targetjob 智能求职助手")
st.caption("帮助你理解职位要求，发现简历匹配点，并准备下一步求职行动。")

with st.sidebar:
    st.header("第一步：选择你的身份")
    persona_options = list(PERSONA_LABELS)
    selected_persona = st.selectbox(
        "你目前更接近哪种求职身份？",
        options=persona_options,
        format_func=lambda value: PERSONA_LABELS[value],
    )
    st.divider()
    st.info(
        "当前是本地演示模式：分析结果由可解释的关键词规则生成，"
        "后续会接入大模型能力。"
    )

st.subheader("第二步：提供分析材料")
resume_text = st.text_area(
    "你的简历",
    height=260,
    placeholder=(
        "请粘贴简历文本，例如：\n"
        "教育背景、项目经历、实习经历、工作经历、技能和成果……"
    ),
)
job_description = st.text_area(
    "目标职位描述",
    height=260,
    placeholder=(
        "请粘贴职位描述，例如：\n"
        "岗位职责、任职要求、技术栈、经验要求和加分项……"
    ),
)

st.subheader("第三步：生成分析报告")
analyze_clicked = st.button("开始分析", type="primary", use_container_width=True)

if analyze_clicked:
    if not resume_text.strip():
        st.error("请先输入简历内容。")
    elif not job_description.strip():
        st.error("请先输入目标职位描述。")
    else:
        with st.spinner("正在分析职位和简历……"):
            result = analyze(
                candidate_type=selected_persona,
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

