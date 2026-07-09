# 九维总结方法论框架

[English README](README.md)

九维总结方法论框架是一个可复用的 Codex skill / framework，用来把高密度材料转化为结构清晰、带有批判意识、可用于判断的高质量总结。它适用于文本、转录稿、文章、访谈、讲座、研报、播客，以及用户已经提取好的视频内容文本。

这个项目的核心不是下载或转录工具，而是一套总结方法论：好的总结不是压缩字数，而是重建意义、证据、边界、形式、观看位置和现实判断。

## 这是什么

主产品是 `skills/nine-dimension-summary`，一个支持中文和英文的九维总结 skill。它帮助 agent：

- 先还原原材料真正说了什么，再进行评价；
- 找出表层主题背后真正处理的问题；
- 分析材料的形式、受众、观看逻辑和误读风险；
- 区分原文观点、合理推论和仍需外部核验的内容；
- 批判证据缺口、逻辑风险、不同立场和框架局限；
- 输出带评分的 Markdown 总结。

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

默认路径是：**用户提供文本或转录稿 → 使用九维方法论总结 → 输出 Markdown 文档**。

## 快速开始

安装或复制主 skill：

```text
skills/nine-dimension-summary
```

然后可以这样调用：

```text
Use $nine-dimension-summary to summarize this transcript in Chinese.
```

或者：

```text
Use $nine-dimension-summary to produce an English full-mode summary of this article.
```

更多示例见 `docs/quickstart.md`。

## 主 Skill

`nine-dimension-summary` 是这个仓库的主 skill。它默认支持直接文本和转录稿输入，不需要视频链接，也不依赖下载流程。

方法论细节放在：

```text
skills/nine-dimension-summary/references/
```

其中包括中文版标准、英文版标准、材料类型路由、输出契约、评分规则和完成前检查清单。

## 可选适配器

仓库中也包含几个可选辅助模块：

- `skills/transcribe-video`：面向用户授权音视频内容的本地转录适配器。
- `skills/transcribe-and-summarize`：从授权媒体到转录稿再到九维总结的组合 workflow。
- `apps/local-transcribe-client`：用于本地转录流程的网页客户端。

这些都是辅助能力，不是项目主卖点。本项目不应被宣传为媒体下载器或内容获取工具。

## 合规与用户责任

默认工作流面向用户已经提供的文本、转录稿或文档内容。URL 处理只作为用户有权处理内容时的本地辅助路径。

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
skills/
  nine-dimension-summary/
  transcribe-video/
  transcribe-and-summarize/
apps/
  local-transcribe-client/
docs/
examples/
```

建议先读 `docs/methodology.md` 理解方法论，再读 `docs/input-output.md` 理解输入和输出形态。
