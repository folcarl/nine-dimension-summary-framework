# Transcribe And Summarize Workflow

This workflow is a convenience path for authorized media. It is not the default path. If the user provides text or a transcript, skip transcription and use `nine-dimension-summary` directly.

## Steps

1. Confirm the media is user-authorized.
2. Use `transcribe-video` to create a transcript.
3. Inspect the transcript for obvious recognition issues:
   - names;
   - numbers;
   - institutions;
   - technical terms;
   - places;
   - missing visual evidence.
4. Apply `nine-dimension-summary`.
5. Produce Markdown output.

## Output

Include:

- source note or transcript path;
- summary body;
- likely transcript issues;
- external verification boundary;
- scores.

Do not claim external verification unless it was actually performed.
