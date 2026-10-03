#!/usr/bin/env python3
"""Render concise, user-facing release notes for the app."""

from __future__ import annotations

import argparse
import sys


sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--previous-version")
    parser.add_argument("--upstream-url")
    args = parser.parse_args()

    if args.previous_version:
        summary = (
            f"This update moves the embedded Ollama runtime from v{args.previous_version} "
            f"to v{args.version}, while keeping the Home Assistant app configuration intact."
        )
    else:
        summary = (
            f"This release packages Ollama v{args.version} for Home Assistant with required "
            "Intel Vulkan acceleration."
        )

    highlights = [
        f"⬆️ Updates Ollama to v{args.version}.",
        "⚡ Keeps Intel Vulkan acceleration required, with no CPU fallback.",
        "🏠 Keeps the existing Home Assistant app configuration and standard port 11434.",
    ]
    if args.upstream_url:
        highlights.append(
            f"📖 Includes the official [Ollama v{args.version} release]({args.upstream_url})."
        )

    print(f"## 🎉 Ollama for Intel Vulkan v{args.version}\n")
    print(f"{summary}\n")
    print("### Highlights\n")
    for highlight in highlights:
        print(f"- {highlight}")
    print("\nNo configuration migration is required.")


if __name__ == "__main__":
    main()
