# Targetjob 第一版技术架构

## 1. 为什么先选 Streamlit

Streamlit 可以把 Python 函数快速变成网页应用。对于第一版 MVP，它有三个好处：

- 学习成本较低，前端代码量少；
- 可以快速把注意力放在智能体流程和分析结果上；
- 适合面试现场启动和演示。

它不是最终唯一选择。等核心流程稳定后，如果需要更复杂的用户系统、页面交互或多人访问，再考虑拆分前端和后端。

## 2. 当前目录结构

```text
Targetjob/
├── app.py                    # Streamlit 网页入口
├── targetjob/
│   ├── __init__.py
│   ├── analyzer.py           # 第一版本地分析器
│   ├── models.py             # 求职者画像和经历数据结构
│   └── profile_validator.py  # 画像完整性校验
├── tests/
│   └── test_analyzer.py      # 分析器单元测试
├── docs/
│   ├── ARCHITECTURE.md       # 技术架构说明
│   └── MVP_SPEC.md           # MVP 需求说明
├── requirements.txt          # Python 依赖
└── .gitignore                # 忽略本地环境和缓存文件
```

## 3. 数据流

```text
用户选择身份
      ↓
输入简历 + 职位描述
      ↓
画像字段校验
      ↓
分析器提取关键词并做匹配
      ↓
生成结构化分析结果
      ↓
Streamlit 展示报告
```

## 4. 当前分析器的定位

当前 `targetjob/analyzer.py` 使用可解释的本地规则：

1. 从简历和职位描述中识别预先定义的关键词；
2. 计算两边的交集，作为匹配优势；
3. 计算职位有、简历没有的关键词，作为能力缺口；
4. 根据用户身份附加不同的建议重点。

这样做的目的不是模拟最终的大模型效果，而是先验证完整链路：输入、处理、输出、错误处理和测试都能运行。

## 5. 后续模型接入位置

后续接入大模型时，主要替换分析器内部的“关键词提取和报告生成”部分，保留以下稳定接口：

```text
analyze(candidate_type, resume_text, job_description)
        ↓
AnalysisResult
```

这样网页层不需要知道分析过程是规则、模型还是两者结合，便于逐步升级。
