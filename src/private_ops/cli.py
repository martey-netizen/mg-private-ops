"""
CTW: 1 Corinthians 14:40 — “Let all things be done decently and in order.”
Intent: Keep command flow explicit and orderly for predictable operations.
Theme: Order
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from private_ops.config import OpsConfig
from private_ops.adapters.maltego import to_maltego_mapping
from private_ops.protocol.models import GraphPayload, TransformRequest
from private_ops.transforms import dispatch


def _load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def _cmd_run_transform(request_path: str, out_path: str, ndjson_path: str | None) -> int:
    request = TransformRequest.from_dict(_load_json(request_path))
    response = dispatch(request)

    response_payload = response.to_dict()
    response_payload["maltego"] = to_maltego_mapping(response.graph)

    Path(out_path).write_text(
        json.dumps(response_payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    if ndjson_path:
        lines: list[dict[str, Any]] = [
            {"type": "run_meta", "data": response.graph.run_meta.to_dict()},
        ]
        lines.extend({"type": "node", "data": node.to_dict()} for node in response.graph.nodes)
        lines.extend({"type": "edge", "data": edge.to_dict()} for edge in response.graph.edges)
        lines.append({"type": "maltego", "data": to_maltego_mapping(response.graph)})
        lines.append({"type": "errors", "data": response.errors})
        with Path(ndjson_path).open("w", encoding="utf-8") as handle:
            for line in lines:
                handle.write(json.dumps(line, sort_keys=True) + "\n")

    return 0 if response.ok else 1


def _cmd_validate_graph(graph_path: str) -> int:
    raw = _load_json(graph_path)
    graph_data = raw.get("graph", raw)
    graph = GraphPayload.from_dict(graph_data)
    errors = graph.validate()
    if errors:
        print("Graph is invalid:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Graph is valid.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="private_ops",
        description="Maltego GPT Private Ops bootstrap CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-config", help="Validate runtime config")
    subparsers.add_parser("plan", help="Print the incremental roadmap")

    run_transform = subparsers.add_parser(
        "run-transform", help="Execute a transform request JSON",
    )
    run_transform.add_argument("request_json", help="Path to TransformRequest JSON")
    run_transform.add_argument("--out", required=True, help="Path to output JSON")
    run_transform.add_argument("--ndjson", help="Optional streaming NDJSON output path")

    validate_graph = subparsers.add_parser(
        "validate-graph", help="Validate canonical graph JSON",
    )
    validate_graph.add_argument("graph_json", help="Path to graph JSON")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "validate-config":
        return _cmd_validate_config()
    if args.command == "plan":
        return _cmd_plan()
    if args.command == "run-transform":
        return _cmd_run_transform(args.request_json, args.out, args.ndjson)
    if args.command == "validate-graph":
        return _cmd_validate_graph(args.graph_json)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
