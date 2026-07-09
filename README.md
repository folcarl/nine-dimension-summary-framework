# Nine-Dimension Summary Framework

Most summaries are too small for the material they summarize.

They compress the surface, keep a few arguments, and miss the harder parts: what problem the source is really dealing with, how it tries to persuade, where the evidence is thin, what the audience may misunderstand, and what judgment the reader can actually make afterward.

The Nine-Dimension Summary Framework is a reusable method for producing structured, critical, high-signal summaries from dense material.

[中文说明](README.zh-CN.md)

## What this is

This repository is mainly a methodology.

Use it for:

- articles;
- transcripts;
- interviews;
- lectures;
- reports;
- podcasts;
- research notes;
- user-provided video-derived text.

The default output is Markdown. The framework works in Chinese or English.

It is not a media downloader. It is not only a Codex skill. Codex adapters and local transcription helpers are included, but the core product is the framework under `framework/`.

## Quick start: give this to an agent

If your agent can read GitHub links, send it this:

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

Then paste your source text or transcript.

## Quick start: use the framework directly

For English output:

```text
Read framework/standard.en.md.
Use framework/material-routing.md to choose full or lightweight mode.
Summarize the source according to framework/output-contract.md.
Score the result with framework/scoring-rubric.md.
Check the result with framework/completion-checklist.md.
```

For Chinese output:

```text
Read framework/standard.zh.md.
Use framework/material-routing.md to choose full or lightweight mode.
Summarize the source according to framework/output-contract.md.
Score the result with framework/scoring-rubric.md.
Check the result with framework/completion-checklist.md.
```

## Codex skill installation

This repo contains optional Codex-compatible skills under `skills/`.

To install the main summary skill:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/folcarl/nine-dimension-summary-framework /tmp/nine-dimension-summary-framework
cp -R /tmp/nine-dimension-summary-framework/skills/nine-dimension-summary ~/.codex/skills/nine-dimension-summary
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.codex\skills | Out-Null
git clone https://github.com/folcarl/nine-dimension-summary-framework $env:TEMP\nine-dimension-summary-framework
Copy-Item -Recurse $env:TEMP\nine-dimension-summary-framework\skills\nine-dimension-summary $env:USERPROFILE\.codex\skills\nine-dimension-summary
```

Then ask Codex:

```text
Use $nine-dimension-summary to summarize this transcript in Chinese:

[paste transcript]
```

Optional skills:

- `skills/nine-dimension-summary`: the main Codex adapter
- `skills/transcribe-video`: local transcription for media you are allowed to process
- `skills/transcribe-and-summarize`: local transcription followed by the framework

If you already have text or a transcript, skip transcription.

## What the framework checks

Full mode usually covers:

- core content and argument;
- the real problem the source is handling;
- form, audience, and viewing logic;
- evidence chain and reasoning;
- critique and limits;
- external verification boundary;
- implications for judgment and action;
- follow-up observation list;
- overall evaluation and scores.

Lightweight mode keeps the essential checks for short or low-density material.

## Repository layout

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

## Good first files

Start here:

- [docs/quickstart.md](docs/quickstart.md)
- [docs/methodology.md](docs/methodology.md)
- [docs/input-output.md](docs/input-output.md)
- [examples/](examples/)

## Compliance note

The default workflow starts from text or transcripts you provide. Only use local transcription for media you have the right to process.

Do not commit cookies, downloaded media, private transcripts, logs, generated job state, or credentials.

For investment, economic, or market material, the output is research support, not investment advice.
