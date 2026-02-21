# Maltego GPT — Private Ops Edition

A private-first operations toolkit for combining **Maltego graph workflows** with **LLM-assisted analysis** in controlled environments.

This repository is currently in the **bootstrap phase**. The goal is to build iteratively and safely:

1. Define architecture and operating model.
2. Build a local CLI + config system.
3. Add Maltego integration adapters.
4. Add LLM provider abstraction (local-first).
5. Add repeatable workflows and tests.

---

## 1) Project goals

- Keep sensitive investigation data under your control.
- Make workflows reproducible, auditable, and scriptable.
- Support multiple LLM backends with strict configuration gates.
- Provide progressive adoption: start local, then expand.

## 2) Current milestone (M0)

This commit provides:

- Initial project structure (`src/`, `tests/`).
- Typed configuration model with environment loading.
- CLI entrypoint for bootstrap checks.

## 3) Suggested build order (incremental)

### Step A — Foundation (this phase)
- [x] Repository scaffold
- [x] Config schema + validation
- [x] Basic CLI
- [ ] Logging and telemetry policy

### Step B — Integration primitives
- [ ] Maltego transform adapter interface
- [ ] Entity/edge schema for ingestion and export
- [ ] Workflow context state management

### Step C — LLM orchestration
- [ ] Provider abstraction (`openai`, `ollama`, `azure`, etc.)
- [ ] Prompt templates for graph reasoning tasks
- [ ] Deterministic run settings (seed, temperature, token caps)

### Step D — Private Ops workflows
- [ ] Target profiling workflow
- [ ] Threat intel enrichment workflow
- [ ] Link analysis narrative generator
- [ ] Operator review + approval checkpoints

### Step E — Hardening
- [ ] Integration tests with fixtures
- [ ] Security controls and secrets handling
- [ ] Packaging and release process

## 4) Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
private-ops validate-config
private-ops plan
```

Optional environment variables:

- `PRIVATE_OPS_ENV` (default: `dev`)
- `PRIVATE_OPS_PROVIDER` (default: `ollama`)
- `PRIVATE_OPS_MODEL` (default: `llama3.1`)
- `PRIVATE_OPS_LOG_LEVEL` (default: `INFO`)

## 5) Next implementation target

Implement **Step B** by introducing a stable adapter protocol for Maltego transforms and a canonical graph payload model.
