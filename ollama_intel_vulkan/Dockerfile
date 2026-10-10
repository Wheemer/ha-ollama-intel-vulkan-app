ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:trixie
ARG OLLAMA_VERSION=0.40.2

FROM ollama/ollama:${OLLAMA_VERSION} AS ollama

FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Mesa's ANV driver and the Vulkan loader are required for Intel Gen9 iGPU use.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        jq \
        libvulkan1 \
        mesa-vulkan-drivers \
        vulkan-tools \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ollama /bin/ollama /usr/local/bin/ollama
COPY --from=ollama /usr/lib/ollama /usr/local/lib/ollama

ENV HOME=/data
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_MODELS=/data/.ollama/models
ENV OLLAMA_VULKAN=1

RUN mkdir -p /data/.ollama/models

COPY run.sh /run.sh
RUN chmod +x /run.sh

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="Wheemer" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Wheemer" \
    org.opencontainers.image.licenses="Apache-2.0" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.version="${BUILD_VERSION}"

CMD ["/run.sh"]
