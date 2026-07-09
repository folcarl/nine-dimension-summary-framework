# Optional Adapters

The framework is designed for direct text and transcripts. Adapters are secondary.

## Generic Use

Any agent or application can load files from `framework/` directly. No Codex-specific format is required.

## Codex-Compatible Adapter

`skills/nine-dimension-summary` wraps the framework as a Codex-compatible skill package. It is useful for Codex users, but it is not the core product.

## Transcription Adapter

`skills/transcribe-video` can create transcripts from local or user-authorized media. It should be used only when the user explicitly needs transcription.

It is not the main project and should not be presented as a downloader.

## Combined Workflow

`skills/transcribe-and-summarize` runs:

```text
authorized media -> transcript -> nine-dimension summary
```

If the user already has text, skip this workflow and use the framework directly.

## Local Client

`apps/local-transcribe-client` is a local interface for transcription workflows. It is useful for personal processing, but it is not required for the summary framework.
