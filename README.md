# Nine-Dimension Summary Framework

[中文说明](README.zh-CN.md)

Nine-Dimension Summary Framework is a general-purpose methodology for turning dense source material into structured, critical, high-signal summaries. It works with text, transcripts, articles, interviews, lectures, reports, podcasts, and user-provided video-derived content.

The core idea: summaries are not compression. They are reconstruction of meaning, evidence, limits, form, audience position, and practical judgment.

This repository includes the framework itself plus an optional Codex-compatible adapter. It is not tied to Codex, and it should not be positioned as a media downloader.

## What This Is

The main product is the reusable framework in `framework/`. It can be used by humans, AI agents, writing workflows, research pipelines, or custom applications.

It helps a summarizer:

- restore what the source actually says before evaluating it;
- identify the deeper problem beneath the surface topic;
- analyze form, audience, viewing logic, and possible misreadings;
- separate source claims, inference, and externally unverified claims;
- critique evidence gaps, logic risks, and alternative positions;
- produce a scored Markdown summary.

## Core Framework Files

```text
framework/
  standard.zh.md
  standard.en.md
  material-routing.md
  output-contract.md
  scoring-rubric.md
  completion-checklist.md
```

- `standard.zh.md`: canonical Chinese methodology.
- `standard.en.md`: natural English methodology.
- `material-routing.md`: full vs lightweight mode selection.
- `output-contract.md`: expected Markdown output shapes.
- `scoring-rubric.md`: 10-point scoring rules.
- `completion-checklist.md`: pre-final quality gate.

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

The default path is:

```text
text or transcript -> nine-dimension framework -> Markdown summary
```

## Quick Start

For Chinese output, start with:

```text
Read framework/standard.zh.md, choose full or lightweight mode with framework/material-routing.md, then summarize the source according to framework/output-contract.md and framework/completion-checklist.md.
```

For English output, start with:

```text
Read framework/standard.en.md, choose full or lightweight mode with framework/material-routing.md, then summarize the source according to framework/output-contract.md and framework/completion-checklist.md.
```

See `docs/quickstart.md` for examples.

## Optional Agent Adapters

`skills/` contains a Codex-compatible skill package. It is an adapter, not the core product:

- `skills/nine-dimension-summary`: Codex-compatible adapter for the framework.

Other agent systems can reuse the files under `framework/` directly.

## Compliance And User Responsibility

The default workflow expects user-provided text, transcripts, or document content. Do not commit cookies, downloaded media, private transcripts, logs, or generated job state.

For investment or economic material, outputs are judgment support, not investment advice.

## Repository Layout

```text
framework/                  # Generic methodology files
skills/                     # Optional Codex-compatible adapters
docs/
examples/
```

Start with `docs/methodology.md` to understand the framework and `docs/input-output.md` to understand the expected output shape.
