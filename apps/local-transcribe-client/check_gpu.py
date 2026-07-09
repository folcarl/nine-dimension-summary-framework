#!/usr/bin/env python
"""Check whether faster-whisper can see the CUDA runtime DLLs."""

from __future__ import annotations

import ctypes
import importlib.metadata
from pathlib import Path

from app import configure_cuda_dll_paths


def check_dll(name: str) -> bool:
    try:
        ctypes.WinDLL(name)
    except OSError as exc:
        print(f"[FAIL] {name}: {exc}")
        return False
    print(f"[OK] {name}")
    return True


def main() -> int:
    print("Added DLL search paths:")
    for path in configure_cuda_dll_paths():
        print(f"  {path}")

    print("\nPackage versions:")
    for package in ("faster-whisper", "ctranslate2"):
        try:
            print(f"  {package}: {importlib.metadata.version(package)}")
        except importlib.metadata.PackageNotFoundError:
            print(f"  {package}: not installed")

    print("\nCUDA DLLs:")
    ok = True
    ok = check_dll("cublas64_12.dll") and ok
    ok = check_dll("cudnn64_9.dll") and ok

    if not ok:
        print("\nGPU is not ready. Install CUDA Toolkit 12.x, then restart start_client.bat.")
        print("Expected cublas64_12.dll in a path like:")
        print(r"  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\bin")
        return 1

    print("\nGPU runtime DLLs are visible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
