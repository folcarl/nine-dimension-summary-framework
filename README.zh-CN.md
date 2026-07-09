# 九维总结方法论框架

[English README](README.md)

九维总结方法论框架是一套通用方法论，用来把高密度材料转化为结构清晰、带有批判意识、可用于判断的高质量总结。它适用于文本、转录稿、文章、访谈、讲座、研报、播客，以及用户已经提取好的视频内容文本。

这个项目的核心不是 Codex 专用 skill，也不是下载或转录工具，而是一套可复用的总结框架：好的总结不是压缩字数，而是重建意义、证据、边界、形式、观看位置和现实判断。

本仓库包含通用方法论文件，也包含一个可选的 Codex 兼容适配器。

## 这是什么

主产品是 `framework/` 里的通用九维总结框架。它可以被人直接使用，也可以被 AI agent、写作流程、研究流程或自定义应用调用。

它帮助总结者：

- 先还原原材料真正说了什么，再进行评价；
- 找出表层主题背后真正处理的问题；
- 分析材料的形式、受众、观看逻辑和误读风险；
- 区分原文观点、合理推论和仍需外部核验的内容；
- 批判证据缺口、逻辑风险、不同立场和框架局限；
- 输出带评分的 Markdown 总结。

## 核心框架文件

```text
framework/
  standard.zh.md
  standard.en.md
  material-routing.md
  output-contract.md
  scoring-rubric.md
  completion-checklist.md
```

- `standard.zh.md`：中文版方法论标准。
- `standard.en.md`：英文版方法论标准。
- `material-routing.md`：材料类型路由和完整版/轻量版选择。
- `output-contract.md`：Markdown 输出结构。
- `scoring-rubric.md`：10 分制评分规则。
- `completion-checklist.md`：完成前质量检查清单。

## 能产出什么

默认输出 Markdown。完整版通常包括：

- 核心内容 / 核心结论
- 它真正处理的问题
- 形式分析与观看逻辑
- 证据链与推理方式
- 批判与局限性
- 外部核验边界
- 对判断和行动的启示
- 后续观察清单
- 总体评价与维度评分

对于短、低密度、低复杂度材料，可以使用轻量版。轻量版会压缩结构，但仍保留核心内容、深层问题、形式/观看风险、主要局限和评分。

## 什么时候用

适合处理：

- 用户直接粘贴的文本；
- `.txt` 转录稿；
- 文章草稿；
- 访谈、讲座、播客和演讲稿；
- 研究笔记和报告；
- 用户自行提供的视频内容文本；
- 中文或英文总结任务。

默认路径是：

```text
文本或转录稿 -> 九维总结框架 -> Markdown 总结
```

## 快速开始

中文输出可以这样使用：

```text
阅读 framework/standard.zh.md，用 framework/material-routing.md 判断完整版或轻量版，然后按照 framework/output-contract.md 和 framework/completion-checklist.md 总结材料。
```

英文输出可以这样使用：

```text
Read framework/standard.en.md, choose full or lightweight mode with framework/material-routing.md, then summarize the source according to framework/output-contract.md and framework/completion-checklist.md.
```

更多示例见 `docs/quickstart.md`。

## 可选 Agent 适配器

`skills/` 目录里是 Codex 兼容的 skill 包。它只是适配器，不是项目本体：

- `skills/nine-dimension-summary`：九维框架的 Codex 兼容适配器。

其他 agent 系统可以直接复用 `framework/` 里的文件，不需要使用 Codex skill 格式。

## 合规与用户责任

默认工作流面向用户已经提供的文本、转录稿或文档内容。

不要提交：

- cookies；
- 下载的音视频；
- 私有转录稿；
- 日志；
- 任务状态；
- 临时文件；
- 密钥或账号凭证。

对于投资、经济或市场材料，输出应作为判断框架和研究辅助，不构成投资建议。

## 仓库结构

```text
framework/                  # 通用方法论文件
skills/                     # 可选 Codex 兼容适配器
docs/
examples/
```

建议先读 `docs/methodology.md` 理解方法论，再读 `docs/input-output.md` 理解输入和输出形态。
