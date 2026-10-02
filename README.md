# Ollama for Intel Vulkan

[![Home Assistant App](https://img.shields.io/badge/HOME%20ASSISTANT-APP-41BDF5?style=for-the-badge&logo=home-assistant&logoColor=white&labelColor=555555)](https://www.home-assistant.io/apps/)
[![AMD64](https://img.shields.io/badge/AMD64-SUPPORTED-22C55E?style=for-the-badge&labelColor=555555)](https://github.com/Wheemer/ha-ollama-intel-vulkan-app)
[![Latest release](https://img.shields.io/github/v/release/Wheemer/ha-ollama-intel-vulkan-app?style=for-the-badge&logo=github&logoColor=white&label=RELEASE&labelColor=555555&color=22C55E)](https://github.com/Wheemer/ha-ollama-intel-vulkan-app/releases/latest)
[![Build](https://img.shields.io/github/actions/workflow/status/Wheemer/ha-ollama-intel-vulkan-app/quality.yml?branch=main&style=for-the-badge&label=BUILD&labelColor=555555)](https://github.com/Wheemer/ha-ollama-intel-vulkan-app/actions/workflows/quality.yml)
[![Add app repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWheemer%2Fha-ollama-intel-vulkan-app)

Ollama for Intel Vulkan runs local Ollama models on Home Assistant OS using the Intel GPU through Vulkan. It targets amd64 systems with an Intel GPU available at `/dev/dri/renderD128`.

## Install

1. Add this repository in **Settings > Apps > App store > Repositories**:
   `https://github.com/Wheemer/ha-ollama-intel-vulkan-app`
2. Install **Ollama for Intel Vulkan**.
3. Keep **Vulkan** and **Require GPU** enabled, then start the app.
4. In the app log, confirm that `vulkaninfo` lists the Intel GPU and Ollama reports an inference compute device other than CPU.
5. Use `http://192.168.1.40:11434` for the Ollama integration.

Models persist under the app data directory and are excluded from Home Assistant backups. Pull models with `ollama pull <model>` through the app container after installation.

## Updates

The repository checks the official Ollama release once daily. When a release changes, it builds, scans, publishes, releases, and Home Assistant installs the app update automatically.

## Credits

Uses the official [Ollama](https://ollama.com/) container runtime. This app is independently maintained for Intel Vulkan use on Home Assistant.
