# Quickstart

Get an architecture view in minutes with any LLM or agent framework. For the full procedure, see [INSTRUCTIONS.md](INSTRUCTIONS.md).

---

## 1. The 60-second version

1. Give the agent **system knowledge** (a repo, code, or a summary).
2. Tell it **what to show** (concern) — or let it default.
3. The agent assembles a view spec, picks a diagram library, generates code, renders it, and self-checks.
4. You get a diagram + the assumptions it made. Ask for changes if needed.

The agent **asks at most one short question round** only when something high-impact is missing, and **never gives up** — it always returns a usable artifact.

---

## 2. Minimal usage (any LLM)

Use [INSTRUCTIONS.md](INSTRUCTIONS.md) as the system prompt, then send your request.

```
SYSTEM: <paste INSTRUCTIONS.md>

USER: Generate an architecture view for this system.
Concern: deployment
Notation: icons_and_arrows

<paste a repo summary, or attach/point to the code>
```

No metadata? This works too — the agent infers defaults and lists them:

```
USER: Draw the architecture of this project.
<paste summary or code>
```

---

## 3. Copy-paste view spec (optional, best results)

Filling more fields improves output. Minimum viable spec:

```json
{
  "summary": "<what the system does and its main parts>",
  "Concern": "control_flow",
  "Behavior": "dynamic",
  "Granularity": "medium",
  "Architecture Scope": "entire",
  "Architectural Notation": "icons_and_arrows"
}
```

Full field list and defaults: [METADATA_SCHEMA.md](METADATA_SCHEMA.md).

---

## 4. Multi-agent / pipeline wiring

Map each stage to an agent or node; prompts are in [PROMPT_TEMPLATES.md](PROMPT_TEMPLATES.md).

```
Stage 0  Intake & Clarification   → ask-or-proceed decision
Stage 1  Knowledge Extractor      → summary
Stage 2  Metadata Assembler       → view spec (+ assumptions, optional questions)
Stage 3/4 View Generator          → diagram-as-code
  (renderer tool)                 → PNG/SVG   [deterministic, not the LLM]
Stage 5  Error correction         → self-repair + fallback ladder (loop, max 3)
Stage 6  Quality Checker          → pass/fail vs EVALUATION_RUBRIC.md
Stage 7  User-facing response     → diagram + assumptions + limitations
```

Prepend the **system preamble** from PROMPT_TEMPLATES.md to every stage for robust behavior.

---

## 5. Notation → library cheat sheet

| You want | Notation | Library | Render with |
|----------|----------|---------|-------------|
| Cloud/infra icons | `icons_and_arrows` | Python `diagrams` | `python script.py` |
| Simple boxes & arrows | `boxes_and_arrows` | Graphviz | `dot -Tpng f.dot -o f.png` |
| UML (component/sequence) | `UML` | PlantUML | `plantuml f.puml` |

Unsure? Default is `boxes_and_arrows` (Graphviz). The agent switches libraries automatically if one fails.

---

## 6. Pick a starting point by goal

| Goal | Concern | Behavior | Notation |
|------|---------|----------|----------|
| "How does a request flow?" | `control_flow` | `dynamic` | `UML` (sequence) |
| "What runs where?" | `deployment` | `static` | `icons_and_arrows` |
| "How does data move?" | `data_flow` | `static` | `boxes_and_arrows` |
| "High-level overview" | `general` | `static` | `boxes_and_arrows` |
| "Where are the trust boundaries?" | `security` | `static` | `boxes_and_arrows` |

`control_flow` + `functional_suitability` give the highest empirical success rates — a safe default when unsure.

---

## 7. What to expect

- A **rendered diagram** (or runnable code / textual structure if no renderer is available).
- An **Assumptions** list — every default the agent chose.
- A **Limitations** note — what was simplified or omitted.
- An **offer to refine** — change concern, scope, notation, or granularity any time.
- Output is a **draft for review**, not ground truth. Verify against the real system.

---

## 8. Troubleshooting

| Symptom | What's happening / what to do |
|---------|-------------------------------|
| Agent asks a question | A high-impact detail is ambiguous. Answer, or say "use defaults". |
| Diagram too detailed | Ask for lower granularity (`low`) or a `part` scope. |
| Diagram too sparse | Ask for `high` granularity or name components to include. |
| Code won't render | The agent self-repairs and switches libraries automatically (max 3 tries). |
| No renderer installed | You'll get diagram-as-code + render instructions. |
| Wrong focus | Restate the concern (e.g., "focus on deployment, not classes"). |
