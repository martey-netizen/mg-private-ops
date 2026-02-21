"""
CTW: Proverbs 10:9 — “He that walketh uprightly walketh surely”
Intent: Verify config behavior with integrity-focused tests for safe defaults.
Theme: Integrity
"""

from private_ops.config import OpsConfig


def test_default_config_is_valid(monkeypatch):
    for key in [
        "PRIVATE_OPS_ENV",
        "PRIVATE_OPS_PROVIDER",
        "PRIVATE_OPS_MODEL",
        "PRIVATE_OPS_LOG_LEVEL",
    ]:
        monkeypatch.delenv(key, raising=False)

    cfg = OpsConfig.from_env()
    assert cfg.validate() == []


def test_invalid_env_and_provider_rejected():
    cfg = OpsConfig(env="qa", provider="foo", model="x", log_level="INFO")

    errors = cfg.validate()
    assert any("env must be one of" in e for e in errors)
    assert any("provider must be one of" in e for e in errors)
