# Optional Adapters

The framework is designed for direct text and transcripts. Adapters are secondary.

## Transcription Adapter

`skills/transcribe-video` can create transcripts from local or user-authorized media. It should be used only when the user explicitly needs transcription.

It is not the main project and should not be presented as a downloader.

## Combined Workflow

`skills/transcribe-and-summarize` runs:

```text
authorized media -> transcript -> nine-dimension summary
```

If the user already has text, skip this workflow and use `nine-dimension-summary`.

## Local Client

`apps/local-transcribe-client` is a local interface for transcription workflows. It is useful for personal processing, but it is not required for the summary framework.
