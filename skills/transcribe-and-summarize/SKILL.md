---
name: transcribe-and-summarize
description: Optional workflow that transcribes user-authorized audio or video content, then applies the nine-dimension summary framework to produce a Markdown summary. Use only when the user explicitly wants a media-to-summary pipeline.
---

# Transcribe And Summarize

Use this workflow when the user explicitly asks to go from authorized media to a nine-dimension summary. If the user already supplied text or a transcript, use `nine-dimension-summary` directly.

## Workflow

1. Read `references/workflow.md`.
2. Use the `transcribe-video` adapter only to create the transcript.
3. Review the transcript for likely recognition errors and uncertain names, numbers, institutions, or terms.
4. Apply `nine-dimension-summary` to the transcript.
5. Output Markdown by default:
   - Transcript path or source note.
   - Summary.
   - Verification boundary and likely transcript issues.
   - Overall evaluation and scores.

## Positioning

This is a convenience workflow, not the core product. The core product is the nine-dimension summary framework for user-provided text and transcripts.
