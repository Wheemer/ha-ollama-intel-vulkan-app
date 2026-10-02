#!/usr/bin/env python3
"""Update the pinned Ollama runtime when upstream publishes a release."""

from __future__ import annotations

import json
import os
import pathlib
import re
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "ollama_intel_vulkan" / "config.yaml"
DOCKERFILE = ROOT / "ollama_intel_vulkan" / "Dockerfile"
CHANGELOG = ROOT / "ollama_intel_vulkan" / "CHANGELOG.md"
RELEASE_URL = "https://api.github.com/repos/ollama/ollama/releases/latest"


def replace_once(text: str, pattern: str, replacement: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Expected one match for {pattern!r}, found {count}")
    return updated


def bump_patch(version: str) -> str:
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def main() -> None:
    request = urllib.request.Request(RELEASE_URL, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        latest = json.load(response)["tag_name"].removeprefix("v")

    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    current_match = re.search(r"^ARG OLLAMA_VERSION=([^\s]+)$", dockerfile, re.MULTILINE)
    if current_match is None:
        raise RuntimeError("Pinned Ollama version was not found")
    current = current_match.group(1)

    changed = current != latest
    if changed:
        config = CONFIG.read_text(encoding="utf-8")
        version_match = re.search(r"^version:\s*([^\s]+)$", config, re.MULTILINE)
        if version_match is None:
            raise RuntimeError("App version was not found")
        app_version = bump_patch(version_match.group(1))

        DOCKERFILE.write_text(
            replace_once(dockerfile, r"^ARG OLLAMA_VERSION=[^\s]+$", f"ARG OLLAMA_VERSION={latest}"),
            encoding="utf-8",
        )
        CONFIG.write_text(
            replace_once(config, r"^version:\s*[^\s]+$", f"version: {app_version}"),
            encoding="utf-8",
        )
        CHANGELOG.write_text(
            f"# Changelog\n\n## {app_version}\n\n- Update Ollama to {latest}.\n\n" + CHANGELOG.read_text(encoding="utf-8").removeprefix("# Changelog\n\n"),
            encoding="utf-8",
        )
    else:
        app_version = re.search(r"^version:\s*([^\s]+)$", CONFIG.read_text(encoding="utf-8"), re.MULTILINE).group(1)

    output = pathlib.Path(os.environ["GITHUB_OUTPUT"])
    with output.open("a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changed else 'false'}\n")
        handle.write(f"version={app_version}\n")


if __name__ == "__main__":
    main()
