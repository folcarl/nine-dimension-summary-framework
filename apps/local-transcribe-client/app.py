#!/usr/bin/env python
"""Local web client for downloading media and transcribing audio/video files."""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from transcribe_media import format_time, normalize_text


ROOT = Path(__file__).resolve().parent
DOWNLOAD_DIR = ROOT / "downloads"
UPLOAD_DIR = ROOT / "uploads"
TRANSCRIPT_DIR = ROOT / "transcripts"
LOG_DIR = ROOT / "logs"
STATE_DIR = ROOT / "job_state"
ALLOWED_FILE_DIRS = (DOWNLOAD_DIR, UPLOAD_DIR, TRANSCRIPT_DIR)
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
APP_VERSION = "2026-06-18-one-click-transcribe-v1"
DESKTOP_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

SUPPORTED_DOMAINS = (
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "bilibili.com",
    "www.bilibili.com",
    "m.bilibili.com",
    "b23.tv",
)


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024 * 1024


@dataclass
class Job:
    id: str
    kind: str
    title: str
    status: str = "queued"
    progress: float = 0.0
    message: str = "Waiting to start"
    logs: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def log(self, message: str) -> None:
        message = ANSI_RE.sub("", message)
        self.message = message
        self.updated_at = time.time()
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"
        self.logs.append(line)
        self.logs = self.logs[-80:]
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            with (LOG_DIR / f"{self.id}.log").open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except OSError:
            pass
        persist_job(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "title": self.title,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "logs": self.logs,
            "files": self.files,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


jobs: dict[str, Job] = {}
jobs_lock = threading.Lock()
transcribe_semaphore = threading.Semaphore(1)


def ensure_dirs() -> None:
    for directory in (DOWNLOAD_DIR, UPLOAD_DIR, TRANSCRIPT_DIR, LOG_DIR, STATE_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def persist_job(job: Job) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        state_path = STATE_DIR / f"{job.id}.json"
        temp_path = state_path.with_suffix(".tmp")
        temp_path.write_text(
            json.dumps(job.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(state_path)
    except OSError:
        pass


def load_jobs_from_disk() -> None:
    ensure_dirs()
    with jobs_lock:
        jobs.clear()
        for state_path in STATE_DIR.glob("*.json"):
            try:
                data = json.loads(state_path.read_text(encoding="utf-8"))
                job = Job(
                    id=data["id"],
                    kind=data.get("kind", "job"),
                    title=data.get("title", "任务"),
                    status=data.get("status", "failed"),
                    progress=float(data.get("progress") or 0),
                    message=data.get("message") or "",
                    logs=list(data.get("logs") or []),
                    files=list(data.get("files") or []),
                    error=data.get("error"),
                    created_at=float(data.get("created_at") or time.time()),
                    updated_at=float(data.get("updated_at") or time.time()),
                )
                if job.status in {"queued", "running"}:
                    job.status = "failed"
                    job.error = "服务已重启或被关闭，任务中断。请重新开始转录。"
                    job.message = job.error
                    job.progress = 0.0
                    job.logs.append(f"[{time.strftime('%H:%M:%S')}] {job.error}")
                    job.logs = job.logs[-80:]
                    job.updated_at = time.time()
                    persist_job(job)
                jobs[job.id] = job
            except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError):
                continue


def create_job(kind: str, title: str) -> Job:
    job = Job(id=uuid.uuid4().hex[:12], kind=kind, title=title)
    with jobs_lock:
        jobs[job.id] = job
    persist_job(job)
    return job


def get_job(job_id: str) -> Job | None:
    with jobs_lock:
        return jobs.get(job_id)


def clean_error_message(exc: BaseException) -> str:
    return ANSI_RE.sub("", str(exc))


def set_failed(job: Job, exc: BaseException) -> None:
    message = clean_error_message(exc)
    job.status = "failed"
    job.progress = 0.0
    job.error = message
    job.log(message)


def is_cuda_runtime_error(exc: BaseException) -> bool:
    message = str(exc).lower()
    return (
        "cuda driver version is insufficient" in message
        or "cuda failed" in message
        or "cuda_error_insufficient_driver" in message
        or "cublas" in message
        or "cudnn" in message
        or "cuda runtime" in message
        or "library cuda" in message
    )


def is_cuda_driver_error(exc: BaseException) -> bool:
    return is_cuda_runtime_error(exc)


def cuda_setup_error(exc: BaseException) -> RuntimeError:
    return RuntimeError(
        "CUDA 运行库没有配置完整，无法使用显卡转录。"
        f"原始错误：{ANSI_RE.sub('', str(exc))}\n"
        "请安装 NVIDIA CUDA Toolkit 12.x，并确认 cublas64_12.dll 在 PATH 中；"
        "当前新版 faster-whisper / CTranslate2 需要 CUDA 12 cuBLAS 和 cuDNN 9。"
    )


def configure_cuda_dll_paths() -> list[str]:
    candidates: list[str] = [
        str(ROOT / "cuda-dlls"),
        str(ROOT / ".venv-media-client" / "Lib" / "site-packages" / "ctranslate2"),
        str(ROOT / ".venv-media-client" / "Lib" / "site-packages" / "nvidia" / "cublas" / "bin"),
        str(ROOT / ".venv-media-client" / "Lib" / "site-packages" / "nvidia" / "cudnn" / "bin"),
    ]
    candidates.extend(glob.glob(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.*\bin"))

    added: list[str] = []
    for directory in candidates:
        path = Path(directory)
        if not path.is_dir():
            continue
        text = str(path.resolve())
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(text)
            except OSError:
                pass
        os.environ["PATH"] = text + os.pathsep + os.environ.get("PATH", "")
        added.append(text)
    return added


def load_whisper_model(
    whisper_model_class: Any,
    model_name: str,
    device: str,
    compute_type: str,
) -> Any:
    return whisper_model_class(
        model_name,
        device=device,
        compute_type=compute_type,
    )


def media_duration_seconds(path: Path) -> float | None:
    try:
        import av
    except ImportError:
        return None

    try:
        with av.open(str(path)) as container:
            if container.duration:
                return float(container.duration * av.time_base)
            durations: list[float] = []
            for stream in container.streams:
                if stream.duration and stream.time_base:
                    durations.append(float(stream.duration * stream.time_base))
            return max(durations) if durations else None
    except Exception:
        return None


def update_transcribe_progress(job: Job, segment_end: float | None, total_duration: float | None) -> None:
    if not segment_end or not total_duration or total_duration <= 0:
        return
    percent = 12.0 + min(max(segment_end / total_duration, 0.0), 1.0) * 86.0
    job.progress = max(job.progress, min(98.0, percent))


def resolve_for_download(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def is_allowed_output(path: Path) -> bool:
    try:
        resolved = path.resolve()
        return any(resolved.is_relative_to(directory.resolve()) for directory in ALLOWED_FILE_DIRS)
    except OSError:
        return False


def public_path(path: Path) -> str:
    return str(path.resolve())


def validate_media_url(url: str) -> None:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("请输入完整的 http/https 视频链接。")
    host = parsed.netloc.lower().split(":")[0]
    if not any(host == domain or host.endswith(f".{domain}") for domain in SUPPORTED_DOMAINS):
        raise ValueError("目前只开放 YouTube 和 Bilibili 链接下载。")


def start_thread(target: Any, *args: Any) -> None:
    thread = threading.Thread(target=target, args=args, daemon=True)
    thread.start()


def build_bilibili_headers(url: str) -> dict[str, str]:
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else "https://www.bilibili.com"
    return {
        "User-Agent": DESKTOP_USER_AGENT,
        "Referer": url if "bilibili" in parsed.netloc.lower() else "https://www.bilibili.com/",
        "Origin": origin,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }


def run_download(
    job: Job,
    url: str,
    mode: str,
    quality: str,
    auth: dict[str, str] | None = None,
    pipeline: bool = False,
) -> list[Path]:
    try:
        from yt_dlp import YoutubeDL
    except ImportError as exc:
        set_failed(job, RuntimeError("缺少 yt-dlp，请先运行 requirements-app.txt 里的依赖安装。"))
        return []

    ensure_dirs()
    job_output_dir = DOWNLOAD_DIR / job.id
    job_temp_dir = job_output_dir / ".tmp"
    job_output_dir.mkdir(parents=True, exist_ok=True)
    job_temp_dir.mkdir(parents=True, exist_ok=True)

    job.status = "running"
    job.progress = 2
    job.log("开始解析链接")
    start_time = time.time()

    def hook(info: dict[str, Any]) -> None:
        status = info.get("status")
        if status == "downloading":
            total = info.get("total_bytes") or info.get("total_bytes_estimate") or 0
            downloaded = info.get("downloaded_bytes") or 0
            if total:
                raw_progress = min(95.0, downloaded * 100 / total)
                visible_progress = 2.0 + raw_progress * 0.28 if pipeline else raw_progress
                job.progress = max(job.progress, visible_progress)
            speed = info.get("speed")
            speed_text = f"，速度 {speed / 1024 / 1024:.1f} MB/s" if speed else ""
            display_progress = downloaded * 100 / total if total else 0
            job.log(f"下载中 {display_progress:.0f}%{speed_text}")
        elif status == "finished":
            job.progress = 29 if pipeline else 96
            filename = info.get("filename")
            if filename:
                job.log(f"下载完成，正在整理文件：{Path(filename).name}")

    if mode == "audio":
        format_selector = "bestaudio/best"
        job_title = "音频源下载"
    elif quality == "compatible":
        format_selector = "best[ext=mp4]/best"
        job_title = "兼容视频下载"
    else:
        format_selector = "bv*+ba/best"
        job_title = "视频源下载"

    outtmpl = "%(title).120B [%(id)s].%(ext)s"
    ydl_opts: dict[str, Any] = {
        "format": format_selector,
        "paths": {
            "home": str(job_output_dir),
            "temp": str(job_temp_dir),
        },
        "outtmpl": outtmpl,
        "noplaylist": True,
        "progress_hooks": [hook],
        "continuedl": True,
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 5,
        "file_access_retries": 12,
        "socket_timeout": 120,
        "ignoreerrors": False,
        "windowsfilenames": True,
        "merge_output_format": "mp4",
        "trim_file_name": 120,
        "http_headers": build_bilibili_headers(url),
        "quiet": True,
        "no_warnings": True,
    }

    auth = auth or {}
    cookie_source = (auth.get("cookie_source") or "none").strip().lower()
    cookie_file = (auth.get("cookie_file") or "").strip()
    if cookie_source in {"chrome", "edge", "firefox"}:
        ydl_opts["cookiesfrombrowser"] = (cookie_source, None, None, None)
        job.log(f"使用 {cookie_source} 浏览器 Cookie")
    if cookie_file:
        cookie_path = resolve_for_download(cookie_file)
        if not cookie_path.is_file():
            set_failed(job, RuntimeError(f"cookies.txt 文件不存在：{cookie_path}"))
            return []
        ydl_opts["cookiefile"] = str(cookie_path)
        job.log(f"使用 cookies.txt：{cookie_path}")

    try:
        job.log(job_title)
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        created_files = [
            path
            for path in job_output_dir.rglob("*")
            if path.is_file()
            and job_temp_dir not in path.parents
            and path.stat().st_mtime >= start_time - 2
            and not path.name.endswith((".part", ".ytdl", ".temp", ".frag"))
        ]
        created_files.sort(key=lambda item: item.stat().st_mtime, reverse=True)
        if not created_files:
            raise RuntimeError("下载结束了，但没有找到输出文件。")

        job.files = [public_path(path) for path in created_files]
        if pipeline:
            job.status = "running"
            job.progress = 30
            job.log("音频下载完成，准备进入转录队列")
        else:
            job.status = "done"
            job.progress = 100
            job.log("完成")
        return created_files
    except Exception as exc:  # noqa: BLE001 - surface downloader errors to the UI.
        message = clean_error_message(exc)
        lower = message.lower()
        if "http error 412" in lower or "precondition failed" in lower:
            set_failed(
                job,
                RuntimeError(
                    "Bilibili 返回 412，通常是反爬或登录态问题。"
                    "请在下载页把 Cookie 来源选为 Chrome/Edge，确保浏览器里已登录 B 站，"
                    "然后重新下载；如果仍失败，导出 B 站 cookies.txt 后填入路径。"
                ),
            )
        elif "winerror 10060" in lower or "timed out" in lower or "timeout" in lower:
            set_failed(
                job,
                RuntimeError(
                    "连接 Bilibili 超时。请稍后重试，或切换网络/关闭代理后再试；"
                    "如果是 B 站视频，建议同时使用浏览器 Cookie。"
                ),
            )
        else:
            set_failed(job, exc)
        return []


def run_transcribe(
    job: Job,
    input_path: Path,
    options: dict[str, Any],
    pipeline: bool = False,
) -> None:
    acquired = False
    try:
        job.status = "queued"
        job.progress = max(job.progress, 30 if pipeline else 1)
        job.log("等待转录队列空闲")
        transcribe_semaphore.acquire()
        acquired = True

        if not input_path.is_file():
            raise FileNotFoundError(f"找不到文件：{input_path}")

        ensure_dirs()
        job.status = "running"
        job.progress = max(job.progress, 32 if pipeline else 3)
        output_path = TRANSCRIPT_DIR / f"{input_path.stem}_transcript.txt"
        prior_files = list(job.files) if pipeline else []
        job.files = prior_files + [public_path(output_path)]
        persist_job(job)

        configure_cuda_dll_paths()
        command = [
            sys.executable,
            str(ROOT / "transcribe_worker.py"),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--options-json",
            json.dumps(options, ensure_ascii=False),
        ]
        job.log("启动独立转录进程")
        worker_env = os.environ.copy()
        worker_env["PYTHONIOENCODING"] = "utf-8"
        worker_env["PYTHONUTF8"] = "1"
        process = subprocess.Popen(
            command,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=worker_env,
        )

        worker_error = ""
        assert process.stdout is not None
        for raw_line in process.stdout:
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                job.log(line)
                continue

            event_type = event.get("type")
            message = str(event.get("message") or "")
            if event_type == "log":
                job.log(message)
            elif event_type == "progress":
                try:
                    worker_progress = min(98.0, float(event.get("progress") or 0))
                    visible_progress = 30.0 + worker_progress * 0.7 if pipeline else worker_progress
                    job.progress = max(job.progress, min(98.6, visible_progress))
                except (TypeError, ValueError):
                    pass
                job.log(message or f"转录中 {job.progress:.0f}%")
            elif event_type == "done":
                job.files = prior_files + [public_path(output_path)]
                job.status = "done"
                job.progress = 100
                job.log(f"转录完成，共 {event.get('lines', 0)} 行")
            elif event_type == "error":
                worker_error = message
                job.log(message)

        return_code = process.wait()
        if return_code != 0 and job.status != "done":
            detail = worker_error or f"转录进程异常退出，退出码 {return_code}"
            set_failed(job, RuntimeError(detail))
        elif job.status != "done":
            set_failed(job, RuntimeError("转录进程结束，但没有返回完成状态。"))
    except Exception as exc:  # noqa: BLE001 - surface transcription errors to the UI.
        set_failed(job, exc)
    finally:
        if acquired:
            transcribe_semaphore.release()


def run_one_click_transcribe(job: Job, url: str, auth: dict[str, str] | None = None) -> None:
    audio_files = run_download(
        job,
        url,
        mode="audio",
        quality="source",
        auth=auth,
        pipeline=True,
    )
    if job.status == "failed" or not audio_files:
        return

    options: dict[str, Any] = {
        "model": "small",
        "language": "",
        "device": "cuda",
        "compute_type": "int8",
        "beam_size": "5",
        "timestamps": False,
        "no_vad": False,
    }
    job.log("开始一键转录：small / cuda / int8 / beam size 5")
    run_transcribe(job, audio_files[0], options, pipeline=True)


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/api/jobs")
def list_jobs() -> Any:
    with jobs_lock:
        ordered = sorted(jobs.values(), key=lambda item: item.created_at, reverse=True)
        return jsonify([job.to_dict() for job in ordered])


@app.get("/api/health")
def health() -> Any:
    return jsonify({"version": APP_VERSION, "root": str(ROOT)})


@app.get("/api/jobs/<job_id>")
def job_detail(job_id: str) -> Any:
    job = get_job(job_id)
    if job is None:
        return jsonify({"error": "job not found"}), 404
    return jsonify(job.to_dict())


@app.post("/api/download")
def download() -> Any:
    data = request.get_json(silent=True) or {}
    url = str(data.get("url") or "").strip()
    mode = str(data.get("mode") or "video")
    quality = str(data.get("quality") or "source")
    auth = {
        "cookie_source": str(data.get("cookie_source") or "none"),
        "cookie_file": str(data.get("cookie_file") or ""),
    }
    try:
        validate_media_url(url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if mode not in {"video", "audio"}:
        return jsonify({"error": "下载类型只能是 video 或 audio。"}), 400

    job = create_job("download", "下载媒体")
    start_thread(run_download, job, url, mode, quality, auth)
    return jsonify(job.to_dict()), 202


@app.post("/api/one-click-transcribe")
def one_click_transcribe() -> Any:
    data = request.get_json(silent=True) or {}
    url = str(data.get("url") or "").strip()
    auth = {
        "cookie_source": str(data.get("cookie_source") or "none"),
        "cookie_file": str(data.get("cookie_file") or ""),
    }
    try:
        validate_media_url(url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    job = create_job("one_click", "一键下载并转录")
    start_thread(run_one_click_transcribe, job, url, auth)
    return jsonify(job.to_dict()), 202


@app.post("/api/transcribe")
def transcribe() -> Any:
    ensure_dirs()
    options: dict[str, Any] = {
        "model": request.form.get("model", "small"),
        "language": request.form.get("language", ""),
        "device": request.form.get("device", "cpu"),
        "compute_type": request.form.get("compute_type", "int8"),
        "beam_size": request.form.get("beam_size", "5"),
        "timestamps": request.form.get("timestamps") == "true",
        "no_vad": request.form.get("no_vad") == "true",
    }

    file = request.files.get("file")
    path_text = request.form.get("path", "")
    if file and file.filename:
        filename = secure_filename(file.filename) or f"upload-{uuid.uuid4().hex}"
        input_path = UPLOAD_DIR / f"{int(time.time())}-{filename}"
        file.save(input_path)
    elif path_text:
        input_path = resolve_for_download(path_text)
    else:
        return jsonify({"error": "请选择上传文件，或传入已下载文件路径。"}), 400

    job = create_job("transcribe", f"转录 {input_path.name}")
    start_thread(run_transcribe, job, input_path, options)
    return jsonify(job.to_dict()), 202


@app.get("/api/file")
def download_file() -> Any:
    path_text = request.args.get("path", "")
    if not path_text:
        return jsonify({"error": "missing path"}), 400
    path = resolve_for_download(path_text)
    if not path.is_file() or not is_allowed_output(path):
        return jsonify({"error": "file not found"}), 404
    return send_file(path, as_attachment=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the local media client.")
    parser.add_argument("--host", default=os.environ.get("MEDIA_CLIENT_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("MEDIA_CLIENT_PORT", "7860")))
    return parser.parse_args()


def main() -> int:
    ensure_dirs()
    load_jobs_from_disk()
    configure_cuda_dll_paths()
    args = parse_args()
    app.run(host=args.host, port=args.port, debug=False, threaded=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
