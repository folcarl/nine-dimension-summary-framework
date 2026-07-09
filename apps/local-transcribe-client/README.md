# Local Transcription Client

This is an optional local adapter for creating transcripts from user-authorized media. It is secondary to the nine-dimension summary framework.

## Start

```powershell
.\start_client.bat
```

The client runs on localhost:

```text
http://127.0.0.1:7860
```

## Use

- Upload a local authorized audio/video file.
- Create a transcript.
- Pass the transcript to the generic framework in `framework/`, or to the optional Codex adapter in `skills/nine-dimension-summary`.

Do not commit downloads, uploads, logs, job state, cookies, or generated transcripts.
