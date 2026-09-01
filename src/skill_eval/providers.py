"""Create Pydantic AI models from validated non-secret configuration."""

# pyright: reportMissingImports=false
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import urlparse

from pydantic_ai.models import Model  # pyright: ignore[reportMissingImports]
from pydantic_ai.models.anthropic import (
    AnthropicModel,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.models.google import (
    GoogleModel,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.models.ollama import (
    OllamaModel,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.models.openai import (
    OpenAIChatModel,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.providers.anthropic import (
    AnthropicProvider,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.providers.google import (
    GoogleProvider,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.providers.ollama import (
    OllamaProvider,  # pyright: ignore[reportMissingImports]
)
from pydantic_ai.providers.openai import (
    OpenAIProvider,  # pyright: ignore[reportMissingImports]
)

from .config import (  # pyright: ignore[reportMissingImports]
    AppConfig,
    ModelConfig,
    ProviderConfig,
)


class ProviderConfigurationError(ValueError):
    """Raised when a selected provider lacks required runtime configuration."""


@dataclass(frozen=True)
class ResolvedModel:
    """A configured model alias and its provider-neutral Pydantic AI model."""

    alias: str
    provider_alias: str
    provider_kind: str
    model_name: str
    model: Model


def create_model(config: AppConfig, alias: str) -> ResolvedModel:
    """Create a Pydantic AI model from a configured model alias.

    This operation does not send a network request. It only resolves the model,
    endpoint, environment-backed credential, and default model settings.
    """
    try:
        model_config = config.models[alias]
    except KeyError as error:
        raise ProviderConfigurationError(f"unknown model alias: {alias}") from error
    provider_config = config.providers[model_config.provider]
    api_key = _resolve_api_key(provider_config)
    model = _create_pydantic_model(model_config, provider_config, api_key)
    return ResolvedModel(
        alias=alias,
        provider_alias=model_config.provider,
        provider_kind=provider_config.kind,
        model_name=model_config.model,
        model=model,
    )


def _resolve_api_key(provider: ProviderConfig) -> str | None:
    if provider.api_key_env is None:
        return None
    value = os.environ.get(provider.api_key_env)
    if value:
        return value
    if provider.kind == "ollama" and _is_local_endpoint(provider.base_url):
        return None
    raise ProviderConfigurationError(
        f"provider {provider.kind!r} requires environment variable {provider.api_key_env}"
    )


def _is_local_endpoint(base_url: str | None) -> bool:
    if base_url is None:
        return True
    return urlparse(base_url).hostname in {"localhost", "127.0.0.1", "::1"}


def _create_pydantic_model(
    model_config: ModelConfig,
    provider_config: ProviderConfig,
    api_key: str | None,
) -> Model:
    settings = cast(Any, model_config.settings)
    model_name = cast(Any, model_config.model)

    if provider_config.kind == "anthropic":
        return AnthropicModel(
            model_name,
            provider=AnthropicProvider(
                api_key=api_key, base_url=provider_config.base_url
            ),
            settings=settings,
        )
    if provider_config.kind in {"openai", "openai-compatible"}:
        return OpenAIChatModel(
            model_name,
            provider=OpenAIProvider(api_key=api_key, base_url=provider_config.base_url),
            settings=settings,
        )
    if provider_config.kind == "ollama":
        return OllamaModel(
            model_name,
            provider=OllamaProvider(api_key=api_key, base_url=provider_config.base_url),
            settings=settings,
        )
    if provider_config.kind == "gemini":
        return GoogleModel(
            model_name,
            provider=GoogleProvider(api_key=api_key, base_url=provider_config.base_url),
            settings=settings,
        )
    raise ProviderConfigurationError(
        f"unsupported provider kind: {provider_config.kind}"
    )
