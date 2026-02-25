from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceRef:
    source_id: str
    title: str
    url: str = ""
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "title": self.title,
            "url": self.url,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceRef":
        return cls(
            source_id=str(data["source_id"]),
            title=str(data["title"]),
            url=str(data.get("url", "")),
            confidence=float(data.get("confidence", 1.0)),
        )


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    canonical_key: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)
    sources: list[SourceRef] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "canonical_key": self.canonical_key,
            "label": self.label,
            "properties": self.properties,
            "sources": [s.to_dict() for s in self.sources],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        return cls(
            id=str(data["id"]),
            type=str(data["type"]),
            canonical_key=str(data["canonical_key"]),
            label=str(data["label"]),
            properties=dict(data.get("properties", {})),
            sources=[SourceRef.from_dict(s) for s in data.get("sources", [])],
        )


@dataclass(frozen=True)
class Edge:
    id: str
    type: str
    from_id: str
    to_id: str
    canonical_key: str
    properties: dict[str, Any] = field(default_factory=dict)
    sources: list[SourceRef] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "from": self.from_id,
            "to": self.to_id,
            "canonical_key": self.canonical_key,
            "properties": self.properties,
            "sources": [s.to_dict() for s in self.sources],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Edge":
        return cls(
            id=str(data["id"]),
            type=str(data["type"]),
            from_id=str(data["from"]),
            to_id=str(data["to"]),
            canonical_key=str(data["canonical_key"]),
            properties=dict(data.get("properties", {})),
            sources=[SourceRef.from_dict(s) for s in data.get("sources", [])],
        )


@dataclass(frozen=True)
class RunMeta:
    run_id: str
    transform: str
    request_id: str = ""
    generated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "transform": self.transform,
            "request_id": self.request_id,
            "generated_at": self.generated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunMeta":
        return cls(
            run_id=str(data["run_id"]),
            transform=str(data["transform"]),
            request_id=str(data.get("request_id", "")),
            generated_at=str(data.get("generated_at", "")),
        )


@dataclass(frozen=True)
class GraphPayload:
    run_meta: RunMeta
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        node_ids = {node.id for node in self.nodes}
        if len(node_ids) != len(self.nodes):
            errors.append("node ids must be unique")

        edge_ids = {edge.id for edge in self.edges}
        if len(edge_ids) != len(self.edges):
            errors.append("edge ids must be unique")

        for edge in self.edges:
            if edge.from_id not in node_ids:
                errors.append(f"edge {edge.id} has unknown from node {edge.from_id}")
            if edge.to_id not in node_ids:
                errors.append(f"edge {edge.id} has unknown to node {edge.to_id}")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_meta": self.run_meta.to_dict(),
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GraphPayload":
        return cls(
            run_meta=RunMeta.from_dict(data["run_meta"]),
            nodes=[Node.from_dict(n) for n in data.get("nodes", [])],
            edges=[Edge.from_dict(e) for e in data.get("edges", [])],
        )


@dataclass(frozen=True)
class TransformRequest:
    transform: str
    inputs: dict[str, Any] = field(default_factory=dict)
    run_meta: RunMeta | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "transform": self.transform,
            "inputs": self.inputs,
        }
        if self.run_meta is not None:
            payload["run_meta"] = self.run_meta.to_dict()
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TransformRequest":
        run_meta_raw = data.get("run_meta")
        return cls(
            transform=str(data["transform"]),
            inputs=dict(data.get("inputs", {})),
            run_meta=RunMeta.from_dict(run_meta_raw) if run_meta_raw else None,
        )


@dataclass(frozen=True)
class TransformResponse:
    ok: bool
    status: str
    graph: GraphPayload
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "status": self.status,
            "graph": self.graph.to_dict(),
            "errors": self.errors,
        }
