# Quickstart

The default workflow starts from text or a transcript. You can use the framework manually, inside an AI assistant prompt, or inside an agent workflow.

## Use The Generic Framework

For Chinese output:

```text
Read framework/standard.zh.md. Use framework/material-routing.md to choose full or lightweight mode. Summarize the source according to framework/output-contract.md, score with framework/scoring-rubric.md, and check the result with framework/completion-checklist.md.
```

For English output:

```text
Read framework/standard.en.md. Use framework/material-routing.md to choose full or lightweight mode. Summarize the source according to framework/output-contract.md, score with framework/scoring-rubric.md, and check the result with framework/completion-checklist.md.
```

## Optional Codex Adapter

If you use Codex, you can install or copy:

```text
skills/nine-dimension-summary
```

Then ask:

```text
Use $nine-dimension-summary to summarize this transcript in Chinese.
```

The adapter is optional; the canonical framework lives in `framework/`.

## Typical Inputs

- pasted text;
- `.txt` transcript;
- article draft;
- interview transcript;
- lecture notes;
- research report notes;
- user-provided video-derived text.

## Default Output

The framework returns Markdown. For dense material it defaults to full mode. For short, low-density material it can use lightweight mode.

Media transcription is optional. If you already have text, do not use the transcription adapter.
