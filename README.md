# ProcessAssist

[![CI](https://github.com/YOUR_USER/processassist/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USER/processassist/actions/workflows/ci.yml)

An evaluated AI agent for process engineering. It answers questions by combining
process data, public safety documents and engineering calculators.

> **Status:** work in progress (week 1 of 16). This is a stub.

## Planned scope

- **Data:** Tennessee Eastman Process fault-detection dataset (public domain, Rieth et al. 2017)
- **Documents (RAG):** US Chemical Safety Board reports and OSHA PSM material
- **Tools:** SQL queries, engineering calculations, anomaly detection
- **Evals:** golden dataset, deterministic checks, LLM-as-judge, CI quality gate

## Ground rules

- Public data only.
- The agent is read-only and advisory. It never issues control actions.
- Calculations are done by tools, never by the model.

## Quick start

```bash
uv sync --extra dev
uv run processassist-data download   # fetch the TEP files (see docs/DATA.md)
uv run processassist-data convert    # RData -> Parquet
uv run processassist-plots           # 3 exploratory plots into docs/plots/
uv run pytest
```

## Data

See [docs/DATA.md](docs/DATA.md) for source, licence and citation.
