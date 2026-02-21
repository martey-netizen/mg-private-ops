"""
CTW: 1 Corinthians 14:40 — “Let all things be done decently and in order.”
Intent: Keep command flow explicit and orderly for predictable operations.
Theme: Order
"""

from __future__ import annotations

import argparse
import json

from private_ops.config import OpsConfig


def _cmd_validate_config() -> int:
    cfg = OpsConfig.from_env()
    errors = cfg.validate()
    if errors:
        print("Configuration is invalid:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Configuration is valid.")
    print(json.dumps(cfg.__dict__, indent=2))
    return 0


def _cmd_plan() -> int:
    steps = [
        "A: Foundation (config/cli/logging)",
        "B: Integration primitives (Maltego adapters/schema)",
        "C: LLM orchestration (providers/prompts/runs)",
        "D: Private ops workflows",
        "E: Hardening and release",
    ]
    print("Incremental build plan:")
    for step in steps:
        print(f"- {step}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="private-ops",
        description="Maltego GPT Private Ops bootstrap CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-config", help="Validate runtime config")
    subparsers.add_parser("plan", help="Print the incremental roadmap")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate-config":
        return _cmd_validate_config()
    if args.command == "plan":
        return _cmd_plan()

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
