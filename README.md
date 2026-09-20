# Targetjob：受约束的求职 Agent 工作流

Targetjob 是一个面向求职者的受约束 Agent 工作流，目标是帮助用户完成从求职画像、职位搜索、简历匹配到面试准备的一系列任务。

项目不会把所有逻辑都交给大模型，而是采用“程序规则 + 大模型 + 外部工具 + 用户状态”的组合：确定性校验由程序完成，自然语言理解和任务规划交给模型，岗位搜索和项目资料读取通过工具完成。

本项目会在搭建过程中同步记录设计决策、实现过程、测试结果和面试表达要点，最终形成一个可以演示、解释和继续扩展的完整项目。

## 当前状态

项目目前处于第一版 MVP 骨架阶段。基础网页、求职画像模型和完整性校验已经完成，Agent 编排和外部工具接入将在后续阶段逐步加入。项目将以 GitHub 仓库作为主要构建、版本管理和面试展示平台。

当前支持的求职身份包括：应届生、实习生和有工作经验的求职者。转行情况通过当前经历与目标岗位的差异体现。

## GitHub

- GitHub 账号：`kangyi996`
- 仓库地址：[github.com/kangyi996/Targetjob](https://github.com/kangyi996/Targetjob)
- 仓库名称：`Targetjob`
- 可见性：公开
- 默认分支：`main`

## 文档

- [项目搭建记录](PROJECT_BUILD_LOG.md)
- [MVP 需求说明](docs/MVP_SPEC.md)
- [第一版技术架构](docs/ARCHITECTURE.md)

## 目标架构

```text
用户画像
    ↓
确定性校验器：判断是否具备继续执行的条件
    ↓
CareerAgent：根据当前状态决定下一步
    ↓
岗位搜索工具 / 项目证据工具 / 匹配分析工具 / 面试工具
    ↓
结构化结果和下一步建议
```

## 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

然后在浏览器打开 Streamlit 提供的本地地址即可。

当前版本使用本地规则分析，不需要 API Key，还不是完整的 Agent。后续接入大模型和工具调用时，会继续保留这套本地演示模式作为备用方案。
