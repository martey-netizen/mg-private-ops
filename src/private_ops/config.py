"""
CTW: Proverbs 12:22 — “Lying lips are abomination to the LORD”
Intent: Enforce truthful, valid runtime configuration before execution.
Theme: Truth
"""

from __future__ import annotations

from dataclasses import dataclass
import os

_ALLOWED_ENVS = {"dev", "staging", "prod"}
_ALLOWED_PROVIDERS = {"ollama", "openai", "azure"}
_ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(slots=True)
class OpsConfig:
    env: str = "dev"
    provider: str = "ollama"
    model: str = "llama3.1"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "OpsConfig":
        return cls(
            env=os.getenv("PRIVATE_OPS_ENV", "dev"),
            provider=os.getenv("PRIVATE_OPS_PROVIDER", "ollama"),
            model=os.getenv("PRIVATE_OPS_MODEL", "llama3.1"),
            log_level=os.getenv("PRIVATE_OPS_LOG_LEVEL", "INFO").upper(),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []

        if self.env not in _ALLOWED_ENVS:
            errors.append(
                f"env must be one of {sorted(_ALLOWED_ENVS)}, got '{self.env}'"
            )

        if self.provider not in _ALLOWED_PROVIDERS:
            errors.append(
                "provider must be one of "
                f"{sorted(_ALLOWED_PROVIDERS)}, got '{self.provider}'"
            )

        if not self.model.strip():
            errors.append("model must not be empty")

        if self.log_level not in _ALLOWED_LOG_LEVELS:
            errors.append(
                "log_level must be one of "
                f"{sorted(_ALLOWED_LOG_LEVELS)}, got '{self.log_level}'"
            )

        return errors
