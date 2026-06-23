# Architecture View Generation — Portable Agent Instructions

Evidence-based instructions for building better software architecture views with any LLM or agent framework.

**Source study:** [*LLM-based Automated Architecture View Generation: Where Are We Now?*](https://arxiv.org/html/2603.21178)  
**Replication package:** [CodeToDiagram on Zenodo](https://zenodo.org/records/18772573)

## What this is

A framework-agnostic instruction set derived from the **ArchView** approach and empirical evaluation across 340 repositories and 4,137 generated views. Use it with any orchestrator: LangChain, LangGraph, CrewAI, AutoGen, Semantic Kernel, custom pipelines, or direct API calls.

## Files

| File | Purpose | Typical use |
|------|---------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Get a view in minutes | Start here |
| [INSTRUCTIONS.md](INSTRUCTIONS.md) | Complete agent instruction | System prompt or agent goal |
| [METADATA_SCHEMA.md](METADATA_SCHEMA.md) | View specification schema (human-readable) | Reference, field definitions |
| [view_spec.schema.json](view_spec.schema.json) | View specification (JSON Schema 2020-12) | Strict validation, tool/function-calling args |
| [PROMPT_TEMPLATES.md](PROMPT_TEMPLATES.md) | Copy-paste prompts per stage | Per-agent or per-step prompts |
| [EVALUATION_RUBRIC.md](EVALUATION_RUBRIC.md) | Quality self-check criteria | Critic/validator agent or post-processing |

## Built for robustness

The instructions are designed so an agent works across messy, incomplete inputs:

- **Asks only when it matters** — one batched clarification round for high-impact unknowns; sensible defaults for everything else.
- **Never gives up** — always returns a usable artifact via a fallback ladder (render → diagram-as-code → textual structure).
- **Self-repairs** — diagnoses render errors, simplifies, and switches diagram libraries automatically (max 3 tries).
- **Stays explicit** — every assumption, simplification, and limitation is reported.

## Integration patterns

New here? Read [QUICKSTART.md](QUICKSTART.md) first.

### Pattern A — Single agent

Load `INSTRUCTIONS.md` as the system prompt. Pass user request + optional repo context. Agent follows all 7 steps internally.

```
system: <contents of INSTRUCTIONS.md>
user:   Generate a deployment view for this repo. Concern=deployment, notation=icons_and_arrows.
        <repo summary or file tree>
```

### Pattern B — Multi-agent pipeline

Map stages to agents or nodes. Each agent gets one section from `PROMPT_TEMPLATES.md`.

```
[Knowledge Extractor] → summary JSON
        ↓
[Metadata Assembler]  → view_spec JSON (validate against METADATA_SCHEMA.md)
        ↓
[Prompt Builder]      → generation_prompt string
        ↓
[View Generator]      → diagram-as-code
        ↓
[Renderer]            → PNG/SVG (tool: plantuml / dot / python)
        ↓ (on error, loop back to View Generator, max 3)
[Quality Checker]     → pass/fail using EVALUATION_RUBRIC.md
```

Your framework handles routing, state, and tool calls. These files define **what** each stage does, not **how** to wire it.

### Pattern C — Tool-augmented agent

Give the agent `INSTRUCTIONS.md` plus tools:

- `extract_repo_summary(repo_path)` — runs knowledge extraction
- `render_diagram(code, format)` — compiles PlantUML/Graphviz/diagrams
- `validate_view(image, view_spec)` — optional LLM-as-judge using rubric

The compile-verify loop (Step 6) should be a **deterministic tool**, not left to the LLM.

### Pattern D — RAG / context injection

Index `METADATA_SCHEMA.md` and concern-specific sections from `INSTRUCTIONS.md`. Retrieve relevant chunks when the user specifies a concern or notation.

## Minimum viable input

```json
{
  "summary": "<architectural knowledge from repo>",
  "Concern": "control_flow",
  "Behavior": "dynamic",
  "Granularity": "medium",
  "Architecture Scope": "entire",
  "Architectural Notation": "icons_and_arrows"
}
```

Full schema in [METADATA_SCHEMA.md](METADATA_SCHEMA.md). More fields → better results (empirically validated).

## Key empirical findings (TL;DR)

1. **Full view metadata beats summary-only prompts** — ArchView outperformed zero-shot, few-shot, and general-purpose agents.
2. **Over-detailing is the #1 failure mode** — enforce granularity explicitly.
3. **Notation-aware library selection matters** — map notation to PlantUML / Graphviz / `diagrams`.
4. **Compile-verify loops are essential** — render, catch errors, retry with stderr (max 3).
5. **Repo exploration alone is insufficient** — structured metadata conditioning beats open-ended agentic browsing.
6. **Start with `control_flow` + `functional_suitability`** — highest empirical success rates.

## Citation

If you use these instructions in research or tools, cite the paper and replication package (see links above).
