#!/usr/bin/env python
"""Subprocess worker for a single faster-whisper transcription job."""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from transcribe_media import format_time, normalize_text


ROOT = Path(__file__).resolve().parent
MAX_REASONABLE_DURATION_SECONDS = 24 * 60 * 60


def emit(event: dict[str, Any]) -> None:
    print(json.dumps(event, ensure_ascii=True), flush=True)


def reasonable_duration(seconds: float | int | None) -> float | None:
    if seconds is None:
        return None
    try:
        value = float(seconds)
    except (TypeError, ValueError):
        return None
    if 0 < value <= MAX_REASONABLE_DURATION_SECONDS:
        return value
    return None


def configure_cuda_dll_paths() -> None:
    candidates = [
        ROOT / "cuda-dlls",
        ROOT / ".venv-media-client" / "Lib" / "site-packages" / "ctranslate2",
        ROOT / ".venv-media-client" / "Lib" / "site-packages" / "nvidia" / "cublas" / "bin",
        ROOT / ".venv-media-client" / "Lib" / "site-packages" / "nvidia" / "cudnn" / "bin",
    ]
    candidates.extend(Path(path) for path in glob.glob(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.*\bin"))

    for path in candidates:
        if not path.is_dir():
            continue
        text = str(path.resolve())
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(text)
            except OSError:
                pass
        os.environ["PATH"] = text + os.pathsep + os.environ.get("PATH", "")


def media_duration_seconds(path: Path) -> float | None:
    ffprobe_duration = media_duration_from_ffprobe(path)
    if ffprobe_duration:
        return ffprobe_duration

    try:
        import av
    except ImportError:
        return None

    try:
        with av.open(str(path)) as container:
            if container.duration:
                duration = reasonable_duration(container.duration / 1_000_000)
                if duration:
                    return duration
            durations: list[float] = []
            for stream in container.streams:
                if stream.duration and stream.time_base:
                    duration = reasonable_duration(stream.duration * float(stream.time_base))
                    if duration:
                        durations.append(duration)
            return max(durations) if durations else None
    except Exception:
        return None


def media_duration_from_ffprobe(path: Path) -> float | None:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return reasonable_duration(result.stdout.strip())


def progress_from_time(segment_end: float | None, total_duration: float | None) -> float | None:
    if not segment_end or not total_duration or total_duration <= 0:
        return None
    return 12.0 + min(max(segment_end / total_duration, 0.0), 1.0) * 86.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one transcription job.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--options-json", required=True)
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    options = json.loads(args.options_json)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    configure_cuda_dll_paths()
    from faster_whisper import WhisperModel

    model_name = options.get("model") or "small"
    device = options.get("device") or "cpu"
    compute_type = options.get("compute_type") or "int8"
    beam_size = int(options.get("beam_size") or 5)
    language = options.get("language") or None
    timestamps = bool(options.get("timestamps"))
    no_vad = bool(options.get("no_vad"))

    total_duration = media_duration_seconds(input_path)
    if total_duration:
        emit({"type": "log", "message": f"媒体时长：{format_time(total_duration)}"})

    emit({"type": "log", "message": "加载识别模型"})
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    emit({"type": "progress", "progress": 12, "message": f"开始转录（{device} / {compute_type}）"})

    segments, info = model.transcribe(
        str(input_path),
        language=language,
        beam_size=beam_size,
        vad_filter=not no_vad,
    )
    progress_duration = total_duration or reasonable_duration(getattr(info, "duration", None))
    if not total_duration and progress_duration:
        emit({"type": "log", "message": f"媒体时长：{format_time(float(progress_duration))}"})

    if getattr(info, "language", None):
        probability = getattr(info, "language_probability", None)
        if probability is None:
            emit({"type": "log", "message": f"检测语言：{info.language}"})
        else:
            emit({"type": "log", "message": f"检测语言：{info.language} ({probability:.0%})"})

    line_count = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for index, segment in enumerate(segments, start=1):
            text = normalize_text(segment.text)
            if not text:
                continue

            if timestamps:
                line = f"[{format_time(segment.start)} --> {format_time(segment.end)}] {text}"
            else:
                line = text

            line_count += 1
            handle.write(line + "\n")
            handle.flush()

            if index % 5 == 0:
                progress = progress_from_time(getattr(segment, "end", None), progress_duration)
                if progress is None:
                    emit({"type": "log", "message": f"已识别 {index} 段"})
                else:
                    current = format_time(float(getattr(segment, "end", 0.0)))
                    total = format_time(float(progress_duration))
                    emit({
                        "type": "progress",
                        "progress": min(98.0, progress),
                        "message": f"已识别 {index} 段（{current} / {total}，{progress:.0f}%）",
                    })

    if not line_count:
        raise RuntimeError("没有识别出语音文字。")

    emit({"type": "done", "lines": line_count, "file": str(output_path)})
    return 0


def main() -> int:
    try:
        return run()
    except Exception as exc:  # noqa: BLE001 - worker reports errors as JSON.
        emit({"type": "error", "message": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
