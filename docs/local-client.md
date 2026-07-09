# Local Transcription Client

The local client is an optional helper for users who need to create transcripts from authorized media before summarizing.

## Start

From `apps/local-transcribe-client`:

```powershell
.\start_client.bat
```

The client opens locally at:

```text
http://127.0.0.1:7860
```

## Notes

- Keep the service bound to localhost.
- Do not commit generated downloads, uploads, transcripts, logs, or job state.
- Use only content you are authorized to process.
- If you already have a transcript, use the framework directly.
