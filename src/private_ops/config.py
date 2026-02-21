"""
CTW: Proverbs 12:22 — “Lying lips are abomination to the LORD”
Intent: Enforce truthful, valid runtime configuration before execution.
Theme: Truth
"""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
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
            log_level=os.getenv("PRIVATE_OPS_LOG_LEVEL", "INFO"),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []

        if self.env not in {"dev", "staging", "prod"}:
            errors.append(
                f"env must be one of dev/staging/prod, got '{self.env}'"
            )

        if self.provider not in {"ollama", "openai", "azure"}:
            errors.append(
                f"provider must be one of ollama/openai/azure, got '{self.provider}'"
            )

        if not self.model.strip():
            errors.append("model must not be empty")

        if self.log_level.upper() not in {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }:
            errors.append("log_level must be a standard logging level")

        return errors
