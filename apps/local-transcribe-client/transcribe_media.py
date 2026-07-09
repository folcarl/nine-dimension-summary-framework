#!/usr/bin/env python
"""Transcribe an MP3/MP4 file to TXT with optional timestamps.

This script uses faster-whisper for local speech recognition. It accepts common
audio/video files supported by PyAV, including .mp3 and .mp4.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS.mmm."""
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transcribe an MP3/MP4 file to TXT with faster-whisper."
    )
    parser.add_argument("input", help="MP3/MP4 file path.")
    parser.add_argument(
        "-o",
        "--output",
        help="Output TXT path. Defaults to <input stem>_transcript.txt.",
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Write segment timestamps before each recognized text segment.",
    )
    parser.add_argument(
        "--model",
        default="small",
        help="Whisper model size/name. Examples: tiny, base, small, medium, large-v3.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Speech language code, such as zh/en/ja. Omit for auto detection.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        help="Inference device: auto, cpu, or cuda.",
    )
    parser.add_argument(
        "--compute-type",
        default="default",
        help="Compute type for faster-whisper, such as default, int8, float16.",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam size. Higher can improve accuracy but is slower.",
    )
    parser.add_argument(
        "--no-vad",
        action="store_true",
        help="Disable voice activity detection filtering.",
    )
    return parser


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def transcribe(args: argparse.Namespace) -> Path:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: faster-whisper\n"
            "Install it with:\n"
            "  python -m pip install -r requirements-transcribe.txt\n"
            "If installation fails on Python 3.14, create a Python 3.10-3.12 "
            "virtual environment and install there."
        ) from exc

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.is_file():
        raise SystemExit(f"Input file not found: {input_path}")

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else input_path.with_name(f"{input_path.stem}_transcript.txt")
    )

    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
    )

    segments, info = model.transcribe(
        str(input_path),
        language=args.language,
        beam_size=args.beam_size,
        vad_filter=not args.no_vad,
    )

    lines: list[str] = []
    if info.language:
        probability = getattr(info, "language_probability", None)
        if probability is None:
            print(f"Detected language: {info.language}")
        else:
            print(f"Detected language: {info.language} ({probability:.2%})")

    for segment in segments:
        text = normalize_text(segment.text)
        if not text:
            continue

        if args.timestamps:
            start = format_time(segment.start)
            end = format_time(segment.end)
            lines.append(f"[{start} --> {end}] {text}")
        else:
            lines.append(text)

    if not lines:
        raise SystemExit("No speech text was recognized.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def main() -> int:
    args = build_parser().parse_args()
    output_path = transcribe(args)
    print(f"Transcript saved to: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
