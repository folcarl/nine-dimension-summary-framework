# 九维总结方法论框架

很多总结太小了。

它们只压缩表层内容，保留几个观点，却漏掉更重要的东西：材料真正处理的问题是什么，作者怎样说服读者，证据哪里薄，受众可能怎样误读，读完之后我们到底能做出什么判断。

九维总结方法论框架就是为了解决这个问题。它把高密度材料整理成结构清楚、带批判意识、能辅助判断的 Markdown 总结。

[English README](README.md)

## 这是什么

这个仓库的核心是 `framework/` 里的通用方法论。

它适合处理：

- 文章；
- 转录稿；
- 访谈；
- 讲座；
- 报告；
- 播客；
- 研究笔记；
- 用户已经提取好的视频文本。

它不是媒体下载器，也不只是 Codex skill。仓库里有 Codex 适配器和本地转录辅助工具，但核心产品是九维总结框架本身。

## 直接把这段话给你的 agent

如果你的 agent 能读取 GitHub 链接，可以直接发：

```text
Read https://github.com/folcarl/nine-dimension-summary-framework.
Use the Nine-Dimension Summary Framework to summarize the material I provide.

First read the right standard:
- framework/standard.en.md for English output
- framework/standard.zh.md for Chinese output

Then use:
- framework/material-routing.md to choose full or lightweight mode
- framework/output-contract.md for the Markdown structure
- framework/scoring-rubric.md for scoring
- framework/completion-checklist.md before final output

Do not summarize by compression only. Reconstruct the source's meaning, evidence, limits, form, audience position, and practical judgment.
```

然后粘贴你的原文或转录稿。

## 直接使用框架

中文输出：

```text
Read framework/standard.zh.md.
Use framework/material-routing.md to choose full or lightweight mode.
Summarize the source according to framework/output-contract.md.
Score the result with framework/scoring-rubric.md.
Check the result with framework/completion-checklist.md.
```

英文输出：

```text
Read framework/standard.en.md.
Use framework/material-routing.md to choose full or lightweight mode.
Summarize the source according to framework/output-contract.md.
Score the result with framework/scoring-rubric.md.
Check the result with framework/completion-checklist.md.
```

## 安装 Codex skill

仓库里的 `skills/` 是可选的 Codex 适配器。

安装主总结 skill：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/folcarl/nine-dimension-summary-framework /tmp/nine-dimension-summary-framework
cp -R /tmp/nine-dimension-summary-framework/skills/nine-dimension-summary ~/.codex/skills/nine-dimension-summary
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.codex\skills | Out-Null
git clone https://github.com/folcarl/nine-dimension-summary-framework $env:TEMP\nine-dimension-summary-framework
Copy-Item -Recurse $env:TEMP\nine-dimension-summary-framework\skills\nine-dimension-summary $env:USERPROFILE\.codex\skills\nine-dimension-summary
```

然后对 Codex 说：

```text
Use $nine-dimension-summary to summarize this transcript in Chinese:

[粘贴转录稿]
```

可选 skill：

- `skills/nine-dimension-summary`：主总结适配器
- `skills/transcribe-video`：处理你有权转录的本地音视频
- `skills/transcribe-and-summarize`：先转录，再用九维框架总结

如果你已经有文本或转录稿，不需要走转录流程。

## 它会检查什么

完整模式通常包括：

- 核心内容和核心论点；
- 材料真正处理的问题；
- 形式、受众和观看逻辑；
- 证据链和推理方式；
- 批判与局限；
- 外部核验边界；
- 对判断和行动的启示；
- 后续观察清单；
- 总体评价和评分。

轻量模式适合短材料或低密度材料，但仍保留关键检查。

## 仓库结构

```text
framework/
  standard.zh.md
  standard.en.md
  material-routing.md
  output-contract.md
  scoring-rubric.md
  completion-checklist.md

skills/
  nine-dimension-summary/
  transcribe-video/
  transcribe-and-summarize/

docs/
examples/
apps/local-transcribe-client/
```

## 建议先读

- [docs/quickstart.md](docs/quickstart.md)
- [docs/methodology.md](docs/methodology.md)
- [docs/input-output.md](docs/input-output.md)
- [examples/](examples/)

## 合规提醒

默认工作流从你提供的文本或转录稿开始。只有在你有权处理媒体内容时，才使用本地转录工具。

不要提交 cookies、下载的音视频、私有转录稿、日志、任务状态或凭证。

对于投资、经济或市场材料，输出是研究辅助，不构成投资建议。
