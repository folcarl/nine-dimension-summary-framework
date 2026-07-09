---
name: transcribe-video
description: Optional local transcription adapter for authorized audio or video content. Use only when the user explicitly asks to transcribe a local media file or user-authorized media URL into text before another workflow. Do not use for ordinary summarization when the user already provided text or a transcript.
---

# Transcribe Video

Use this optional adapter only when the user needs a transcript from media they are authorized to process. The main framework expects direct text or transcripts; this skill is just a local input pipeline.

## Workflow

1. Confirm the user supplied either a local media file or an authorized media URL.
2. Read `references/authorized-media-policy.md`.
3. If troubleshooting is needed, read `references/troubleshooting.md`.
4. Install dependencies from `scripts/requirements-transcribe.txt` in a local environment if needed.
5. Run `scripts/transcribe_media.py` for simple local media files.
6. Use `scripts/transcribe_worker.py` only when a caller needs worker-style JSON progress events.
7. Produce a `.txt` transcript and tell the user where it was saved.

## Guardrails

- Do not present this project as a media acquisition or downloader product.
- Do not process private, copyrighted, or platform-restricted content unless the user states they are authorized to process it.
- Do not commit media files, cookies, logs, generated transcripts, or job state.
- If transcript cleanup is requested, distinguish obvious recognition errors from uncertain claims.
