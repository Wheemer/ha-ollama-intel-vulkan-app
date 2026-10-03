#!/usr/bin/env python3
"""Render concise, user-facing release notes for the app."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request


sys.stdout.reconfigure(encoding="utf-8")


def upstream_highlights(version: str) -> list[str]:
    """Return the meaningful, user-facing bullets from Ollama's release."""
    request = urllib.request.Request(
        f"https://api.github.com/repos/ollama/ollama/releases/tags/v{version}",
        headers={"Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.load(response).get("body", "")

    lines = body.replace("\r\n", "\n").splitlines()
    highlights: list[str] = []
    preface: list[str] = []
    in_changes = False
    in_code_block = False
    for line in lines:
        if re.match(r"^##\s+what's changed\s*$", line, re.IGNORECASE):
            in_changes = True
            continue
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_changes and line.startswith("## "):
            break
        if not in_changes and not in_code_block and line and not line.startswith(("#", "-", "*")):
            preface.append(line.strip())
            continue
        if not in_changes:
            continue
        match = re.match(r"^\s*[*-]\s+(.+)$", line)
        if match and not any(
            excluded in match.group(1).lower()
            for excluded in ("macos", "mlx", "settings now opens")
        ):
            highlights.append(match.group(1).strip())

    intro = " ".join(preface)
    sentences = re.split(r"(?<=[.!?])\s+", intro)
    return [*sentences[:2], *highlights][:5]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--previous-version")
    parser.add_argument("--upstream-url")
    args = parser.parse_args()

    summary = (
        f"This update bundles Ollama v{args.version} for the Home Assistant app."
        if args.previous_version
        else f"This release introduces Ollama v{args.version} for the Home Assistant app."
    )
    highlights = upstream_highlights(args.version) if args.upstream_url else []

    print(f"## 🎉 Ollama for Intel Vulkan v{args.version}\n")
    print(f"{summary}\n")
    if highlights:
        print("### Highlights\n")
        for highlight in highlights:
            print(f"- {highlight}")
        print()
    if args.upstream_url:
        print(f"See the official [Ollama v{args.version} release]({args.upstream_url}) for full details.\n")
    print("No configuration migration is required.")


if __name__ == "__main__":
    main()
