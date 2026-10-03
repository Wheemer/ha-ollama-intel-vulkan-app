<div align="center">

<img src="ollama_intel_vulkan/logo.png" width="112" alt="Ollama logo">

# Ollama for Intel Vulkan

### Local Ollama models for Home Assistant, accelerated by Intel Vulkan

[![Home Assistant App](https://img.shields.io/badge/HOME%20ASSISTANT-APP-41BDF5?style=for-the-badge&logo=home-assistant&logoColor=white&labelColor=555555)](https://www.home-assistant.io/apps/)
[![Intel Vulkan](https://img.shields.io/badge/INTEL-VULKAN-0071C5?style=for-the-badge&logo=intel&logoColor=white&labelColor=555555)](https://www.vulkan.org/)
[![AMD64](https://img.shields.io/badge/AMD64-SUPPORTED-22C55E?style=for-the-badge&labelColor=555555)](https://github.com/Wheemer/ha-ollama-intel-vulkan-app)
[![Latest release](https://img.shields.io/github/v/release/Wheemer/ha-ollama-intel-vulkan-app?style=for-the-badge&logo=github&logoColor=white&label=RELEASE&labelColor=555555&color=22C55E)](https://github.com/Wheemer/ha-ollama-intel-vulkan-app/releases/latest)
[![Build](https://img.shields.io/github/actions/workflow/status/Wheemer/ha-ollama-intel-vulkan-app/quality.yml?branch=main&style=for-the-badge&label=BUILD&labelColor=555555)](https://github.com/Wheemer/ha-ollama-intel-vulkan-app/actions/workflows/quality.yml)

</div>

Run [Ollama](https://ollama.com/) locally on Home Assistant OS with Intel Vulkan acceleration. This app is for amd64 Home Assistant systems where an Intel GPU is available through `/dev/dri`.

Intel Vulkan is required. The app checks the GPU at startup and stops instead of silently falling back to CPU inference.

## Installation

[![Open this repository in your Home Assistant App Store](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWheemer%2Fha-ollama-intel-vulkan-app)

1. Add this repository under **Settings > Apps > App store > Repositories**.
2. Install **Ollama for Intel Vulkan**.
3. Start the app.
4. Check the app log to confirm that Vulkan detected the Intel GPU.

## Connect Home Assistant

Add the Ollama integration under **Settings > Devices & services > Add integration**. Use your Home Assistant IP address and the app's standard port:

```text
http://<home-assistant-ip>:11434
```

For example, if Home Assistant is at `192.168.1.40`, use `http://192.168.1.40:11434`.

## Models

Ollama starts without any models. Open the app terminal and pull the model you want to run:

```sh
ollama pull <model>
```

Model files remain available across app restarts. They are deliberately excluded from Home Assistant backups, so large model downloads do not inflate routine backups.

## App Options

| Option | Default | Purpose |
| --- | ---: | --- |
| Context length | `2048` | Maximum context window for each model request. |
| Parallel requests | `1` | Number of requests Ollama may process concurrently. |
| Loaded models | `1` | Maximum number of models Ollama keeps in memory. |

Start with the defaults. Increase these only when the Intel GPU and available memory can support the additional workload.

## Updates

The repository checks for upstream Ollama releases once each day and publishes an app update when one is available. Enable automatic app updates in Home Assistant to install those releases automatically.

## Troubleshooting

If the app stops during startup, open its log and check the Vulkan device check. The host must expose a working Intel GPU under `/dev/dri`; this app does not offer a CPU fallback.

## Credits

Uses the official [Ollama](https://ollama.com/) runtime. This Home Assistant app is independently maintained for Intel Vulkan use. The Ollama logo artwork is from the [official Ollama repository](https://github.com/ollama/ollama) under its MIT license.
