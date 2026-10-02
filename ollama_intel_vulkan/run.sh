#!/usr/bin/with-contenv bash
set -euo pipefail

vulkan_enabled="$(jq -r '.vulkan' /data/options.json)"
require_gpu="$(jq -r '.require_gpu' /data/options.json)"
context_length="$(jq -r '.context_length' /data/options.json)"
num_parallel="$(jq -r '.num_parallel' /data/options.json)"
max_loaded_models="$(jq -r '.max_loaded_models' /data/options.json)"
export OLLAMA_CONTEXT_LENGTH="$context_length"
export OLLAMA_NUM_PARALLEL="$num_parallel"
export OLLAMA_MAX_LOADED_MODELS="$max_loaded_models"
export OLLAMA_DEBUG=INFO

mkdir -p /data/.ollama/models

if [ "$vulkan_enabled" = "true" ]; then
    export OLLAMA_VULKAN=1
    export OLLAMA_IGPU_ENABLE=1
    if [ ! -e /dev/dri/renderD128 ]; then
        echo "ERROR: Intel render node /dev/dri/renderD128 is unavailable."
        exit 1
    fi

    echo "Checking Intel Vulkan device availability"
    if ! vulkaninfo --summary; then
        if [ "$require_gpu" = "true" ]; then
            echo "ERROR: Vulkan could not initialize the Intel GPU."
            exit 1
        fi
        echo "WARNING: Vulkan unavailable; allowing CPU fallback by configuration."
        export OLLAMA_VULKAN=0
    fi
else
    export OLLAMA_VULKAN=0
fi

echo "Starting Ollama on ${OLLAMA_HOST}"
exec /usr/local/bin/ollama serve
