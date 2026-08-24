"""Validated application configuration and XDG path discovery."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

import yaml  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
from platformdirs import (  # pyright: ignore[reportMissingImports]
    user_config_path,
    user_data_path,
)
from pydantic import (  # pyright: ignore[reportMissingImports]
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class ConfigurationError(ValueError):
    """Raised when a configuration file is missing required valid settings."""


class ProviderConfig(BaseModel):
    """A named provider endpoint without secret material."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["anthropic", "openai", "gemini", "ollama", "openai-compatible"]
    base_url: str | None = None
    api_key_env: str | None = None

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute http(s) URL")
        if parsed.username or parsed.password:
            raise ValueError("base_url must not embed credentials")
        return value.rstrip("/")

    @field_validator("api_key_env")
    @classmethod
    def validate_key_environment_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.isidentifier() or value != value.upper():
            raise ValueError(
                "api_key_env must be an uppercase environment-variable name"
            )
        return value


class ModelConfig(BaseModel):
    """A reusable model alias backed by one configured provider."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str = Field(min_length=1)
    settings: dict[str, Any] = Field(default_factory=dict)


class DefaultsConfig(BaseModel):
    """Defaults shared by CLI commands and experiment suites."""

    model_config = ConfigDict(extra="forbid")

    executor: str | None = None
    grader: str | None = None
    enhancer: str | None = None
    database: Path | None = None
    max_concurrency: int = Field(default=4, ge=1)
    timeout_seconds: int = Field(default=120, ge=1)


class AppConfig(BaseModel):
    """The complete non-secret configuration schema."""

    model_config = ConfigDict(extra="forbid")

    version: Literal[1] = 1
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    providers: dict[str, ProviderConfig] = Field(default_factory=dict)
    models: dict[str, ModelConfig] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_model_provider_references(self) -> AppConfig:
        missing_providers = {
            alias: model.provider
            for alias, model in self.models.items()
            if model.provider not in self.providers
        }
        if missing_providers:
            details = ", ".join(
                f"{alias!r} -> {provider!r}"
                for alias, provider in missing_providers.items()
            )
            raise ValueError(f"models reference unknown providers: {details}")

        missing_roles = {
            role: alias
            for role, alias in {
                "executor": self.defaults.executor,
                "grader": self.defaults.grader,
                "enhancer": self.defaults.enhancer,
            }.items()
            if alias is not None and alias not in self.models
        }
        if missing_roles:
            details = ", ".join(
                f"{role} -> {alias!r}" for role, alias in missing_roles.items()
            )
            raise ValueError(f"default roles reference unknown models: {details}")
        return self


def default_config_path() -> Path:
    """Return the per-user XDG/platform configuration location."""
    return user_config_path("skill-eval") / "config.yaml"


def default_database_path() -> Path:
    """Return the per-user persistent SQLite database location."""
    return user_data_path("skill-eval") / "skill-evals.db"


def _reject_literal_secrets(value: Any, path: str = "") -> None:
    """Reject common secret keys recursively before Pydantic validation."""
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            normalized = str(key).lower().replace("-", "_")
            if normalized in {"api_key", "token", "password", "secret"}:
                raise ConfigurationError(
                    f"{child_path} is not allowed; reference a secret through api_key_env instead"
                )
            _reject_literal_secrets(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_literal_secrets(child, f"{path}[{index}]")


def load_config(path: Path | None = None) -> tuple[AppConfig, Path]:
    """Load an explicit or global YAML configuration, returning defaults if absent."""
    config_path = (path or default_config_path()).expanduser()
    if not config_path.exists():
        return AppConfig(), config_path
    if not config_path.is_file():
        raise ConfigurationError(f"configuration path is not a file: {config_path}")

    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise ConfigurationError(
            f"could not read configuration {config_path}: {error}"
        ) from error

    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ConfigurationError("configuration root must be a YAML mapping")
    _reject_literal_secrets(data)

    try:
        return AppConfig.model_validate(data), config_path
    except Exception as error:
        raise ConfigurationError(
            f"invalid configuration {config_path}: {error}"
        ) from error


def resolve_database_path(config: AppConfig, override: Path | None = None) -> Path:
    """Resolve a command's database, applying a CLI override last."""
    candidate = override or config.defaults.database or default_database_path()
    return candidate.expanduser()


def config_template(database: Path | None = None) -> str:
    """Return a safe, commented starter configuration."""
    database_value = json.dumps(str(database or default_database_path()))
    return f"""# skill-eval global configuration\n# Secrets belong in environment variables, never in this file.\nversion: 1\n\ndefaults:\n  # executor: local-qwen\n  # grader: cloud-judge\n  # enhancer: cloud-editor\n  database: {database_value}\n  max_concurrency: 4\n  timeout_seconds: 120\n\nproviders:\n  ollama-local:\n    kind: ollama\n    # Ollama's Pydantic AI endpoint must include /v1.\n    base_url: http://localhost:11434/v1\n    # api_key_env: OLLAMA_API_KEY\n\n# Add models after adding a provider.\nmodels: {{}}\n"""


def write_config_template(path: Path, *, force: bool = False) -> None:
    """Create a starter config without overwriting an existing user file."""
    path = path.expanduser()
    if path.exists() and not force:
        raise ConfigurationError(
            f"configuration already exists: {path} (use --force to replace it)"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(config_template(), encoding="utf-8")
    if os.name != "nt":
        path.chmod(0o600)
