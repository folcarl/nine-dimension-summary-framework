# Nine-Dimension Summary Framework

[中文说明](README.zh-CN.md)

Nine-Dimension Summary Framework is a reusable Codex skill for turning dense source material into structured, critical, high-signal summaries. It works with text, transcripts, articles, interviews, lectures, reports, podcasts, and user-provided video-derived content.

The project is centered on a methodology: summaries are not compression. They are reconstruction of meaning, evidence, limits, form, audience position, and practical judgment.

## What This Is

The main product is `skills/nine-dimension-summary`, a bilingual summary framework for Chinese and English work. It helps an agent:

- restore what the source actually says before evaluating it;
- identify the deeper problem beneath the surface topic;
- analyze form, audience, viewing logic, and possible misreadings;
- separate source claims, inference, and externally unverified claims;
- critique evidence gaps, logic risks, and alternative positions;
- produce a scored Markdown summary.

## What It Produces

Default output is Markdown. Full mode usually includes:

- Core Content / Core Argument
- The Real Problem It Handles
- Form And Viewing Logic
- Evidence Chain And Reasoning
- Critique And Limits
- External Verification Boundary
- Implications For Judgment And Action
- Follow-Up Observation List
- Overall Evaluation And Scores

Lightweight mode compresses the structure for short, low-density material while preserving the essential checks.

## When To Use It

Use the framework for:

- pasted source text;
- transcript files;
- article drafts;
- interviews, lectures, podcasts, and speeches;
- research notes and reports;
- user-provided extracted video content;
- Chinese or English summaries.

## Quick Start

Install or copy the main skill:

```text
skills/nine-dimension-summary
```

Then ask:

```text
Use $nine-dimension-summary to summarize this transcript in Chinese.
```

or:

```text
Use $nine-dimension-summary to produce an English full-mode summary of this article.
```

See `docs/quickstart.md` for more examples.

## Main Skill

`nine-dimension-summary` is the primary skill. It supports direct text and transcript inputs by default. It does not require media URLs.

## Optional Adapters

The repository includes optional local adapters:

- `skills/transcribe-video`: local transcription for user-authorized audio or video content.
- `skills/transcribe-and-summarize`: convenience workflow from authorized media to transcript to summary.
- `apps/local-transcribe-client`: a local web client for transcription workflows.

These adapters are secondary. The framework is not positioned as a media acquisition tool.

## Compliance And User Responsibility

The default workflow expects user-provided text, transcripts, or document content. URL handling is provided only as a convenience path for content the user has rights to process. Do not commit cookies, downloaded media, private transcripts, logs, or generated job state.

For investment or economic material, outputs are judgment support, not investment advice.

## Repository Layout

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

Start with `docs/methodology.md` to understand the framework and `docs/input-output.md` to understand the expected output shape.
