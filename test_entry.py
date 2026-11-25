#!/usr/bin/env python3
"""Tests for the make.fun tagline entry.

Runs main.py into a temporary output directory twice and checks the
artifact: entry.txt exists, holds 1-100 UTF-8 characters, is not only
whitespace, and is byte-identical across runs (determinism).
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run_once(out_dir: str) -> bytes:
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = out_dir
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "main.py")],
        env=env, capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"main.py failed: {r.stderr}"
    with open(os.path.join(out_dir, "entry.txt"), "rb") as f:
        return f.read()


def main() -> None:
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        a = run_once(d1)
        b = run_once(d2)
    text = a.decode("utf-8")
    assert a == b, "output is not deterministic"
    assert 1 <= len(text) <= 100, f"length {len(text)} outside 1-100"
    assert text.strip(), "output is only whitespace"
    assert "\n" not in text, "output must be a single line"
    print(f"OK: {len(text)} chars: {text}")


if __name__ == "__main__":
    main()
