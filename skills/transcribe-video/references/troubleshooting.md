# Transcription Troubleshooting

## Dependencies

Install the transcription dependency:

```powershell
python -m pip install -r scripts/requirements-transcribe.txt
```

Python 3.10-3.12 is recommended for broad package compatibility.

## Local Files

Basic transcription:

```powershell
python scripts/transcribe_media.py "D:\path\audio.mp3" -o "D:\path\transcript.txt"
```

With timestamps:

```powershell
python scripts/transcribe_media.py "D:\path\video.mp4" --timestamps
```

## GPU

CPU mode is the most portable. CUDA requires a compatible NVIDIA driver and runtime DLLs. If CUDA fails, retry with CPU or `int8` compute.

## Transcript Quality

Common weak points:

- proper nouns;
- numbers and dates;
- foreign-language terms;
- organizations and product names;
- speech with background noise;
- charts or visuals not present in audio.

Mark uncertain recognition instead of fabricating certainty.
