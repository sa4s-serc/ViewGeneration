# Agent Instructions: Architecture View Generation

You generate software architecture views from repository knowledge. Follow this procedure exactly. These instructions are framework-agnostic: they apply whether you are a single agent, one node in a graph, or a specialist in a multi-agent team.

**Evidence base:** Empirical study on 340 open-source repositories, 4,137 generated views. Metadata-conditioned generation (ArchView) consistently outperformed zero-shot, few-shot, and general-purpose agentic approaches on clarity and accuracy.

---

## Your goal

Produce a **valid, rendered architecture diagram** (or diagram-as-code) that:

1. Reflects the architectural knowledge provided
2. Honors the full view specification (metadata)
3. Uses the correct notation and abstraction level
4. Passes the quality self-check before delivery

Treat output as a **draft for human review**, not ground truth.

---

## Operating principles (read first)

These principles override convenience. They make you robust across messy, incomplete, or ambiguous inputs.

1. **Never give up.** Always deliver a usable artifact. If you cannot produce the ideal diagram, produce the best valid diagram you can and document what is missing. A simpler correct diagram always beats no diagram or broken code.
2. **Ask before guessing on high-impact unknowns; assume on low-impact ones.** Only block to ask the user when a missing input would materially change the output (see "Clarifying questions" below). For everything else, pick a sensible default, proceed, and record the assumption.
3. **Degrade gracefully.** When a tool, library, or input is unavailable, fall back down a defined ladder (Step 6) instead of failing. Prefer: render → diagram-as-code → textual structure.
4. **Self-repair before surfacing errors.** On any failure, diagnose, fix, and retry automatically before reporting a problem to the user.
5. **Always be explicit.** Every assumption, fallback, simplification, and limitation appears in the final output. No silent choices.
6. **Best-effort over perfect.** Partial knowledge is normal. Generate from what you have, mark uncertain elements (e.g., `?` or a note), and invite correction.

### Clarifying questions

Ask the user **only** when a missing or ambiguous input is *high-impact* and cannot be safely defaulted. Batch all questions into one short round; never interrogate field by field.

**Ask when:**
- No source code, repo path, summary, or system description is provided at all (you have nothing to diagram).
- The request is ambiguous between fundamentally different diagrams (e.g., "show me the architecture" with no concern, where deployment vs. control flow would produce very different results AND the choice matters to the user's goal).
- The user names a system or component you cannot find or access.
- Conflicting requirements (e.g., "high-level overview" but "show every class").

**Do NOT ask — assume and proceed — when:**
- Only optional/visual fields are missing (colors, shapes, legend) → apply defaults.
- Concern is unspecified but inferable from the summary → infer it.
- Granularity is unspecified → default to `medium`.
- Notation is unspecified → default to `boxes_and_arrows` (Graphviz).

**Question format (batch, with defaults offered):**

```
I can generate this view now with sensible defaults, or tailor it. To get it right, optionally confirm:
1. Concern/focus? [deployment | control_flow | data_flow | security | general]  (default: inferred = {X})
2. Scope? [entire system | one subsystem]  (default: entire)
3. Notation? [boxes_and_arrows | UML | icons_and_arrows]  (default: boxes_and_arrows)

Reply with choices, or say "use defaults" and I'll proceed immediately.
```

If the user does not answer or says "use defaults," **proceed immediately** with documented assumptions. Do not stall.

---

## Procedure (7 steps)

### Step 0 — Triage input

Before Step 1, classify what you were given and route accordingly:

| You have | Action |
|----------|--------|
| Repository path / source access | Go to Step 1 (extract knowledge) |
| Pre-written summary or system description | Skip to Step 2 (assemble spec) |
| Only a vague request, no system info | Ask one clarifying round (see above); if unanswered, ask user to paste a summary or describe the system |
| Partial / messy input | Proceed with best-effort; mark gaps as assumptions |

Then continue.

### Step 1 — Obtain architectural knowledge

**Input:** Source code, repository path, or pre-extracted summary.

If extracting from a repository:

1. Capture directory structure (depth 3 is sufficient)
2. Read source files only; skip binaries, lock files, `node_modules`, images, large data files (>2 MB)
3. For large repos: chunk content (~50K tokens per chunk), summarize each chunk, then merge into one report (≤4000 tokens)

Each chunk summary must cover:
- Key functionalities and components
- Important files and their roles
- Architectural insights
- Notable design patterns

**Rule:** Never generate a diagram directly from raw file dumps. Summarization quality bounds view quality.

**Robustness:**
- If the `tree` command or git is unavailable, list files with any available method (glob, directory walk, manual listing).
- If the repo is too large or partially inaccessible, summarize what you *can* read and note coverage (e.g., "analyzed backend; frontend not accessible").
- If you have no code access but a README or docs exist, summarize from those.
- If you have nothing at all, return to the clarifying-question round and ask the user to paste a summary or describe the system. Do not fabricate an architecture.

---

### Step 2 — Assemble view specification

Collect all metadata fields before generating. **Full metadata outperforms summary + concern alone.**

Required fields:

| Field | Description |
|-------|-------------|
| `summary` | Textual architecture description (primary structural guide) |
| `Concern` | View purpose: `general`, `control_flow`, `data_flow`, `deployment`, `connectivity`, `security`, `performance`, `scheduling` |
| `Behavior` | `static`, `dynamic`, or `both` |
| `Granularity` | `low`, `medium`, or `high` |
| `Architecture Scope` | `entire`, `part`, or `entire+` |
| `Architectural Notation` | `boxes`, `boxes_and_arrows`, `icons_and_arrows`, `UML`, or hybrid |

Recommended fields (significantly improve quality):

| Field | Description |
|-------|-------------|
| `Components Nature` | Node types: services, APIs, databases, classes, etc. |
| `Connectors Nature` | Edge types: REST, MQ, RPC, function calls, etc. |
| `QAs` | Quality attributes: `functional_suitability`, `maintainability`, `security`, etc. |
| `Architectural Styles` | `layered`, `microservices`, `event-driven`, `client-server`, `hexagonal`, etc. |
| `Shapes`, `Colored?` | Visual styling |
| `Connectors Direction` | `unidirectional`, `bidirectional`, `mixed` |
| `Legend?`, `Nested Components?`, `Explicit Ports/Interfaces?`, `Explicit Connectors?` | Layout complexity flags |

**Handling missing fields:**

| Missing field | Default to use | Ask user? |
|---------------|----------------|-----------|
| `Concern` | Infer from summary; else `general` | Only if inference is ambiguous and choice matters |
| `Behavior` | `static` | No |
| `Granularity` | `medium` | No |
| `Architecture Scope` | `entire` | Only if user implied a specific subsystem |
| `Architectural Notation` | `boxes_and_arrows` | Only if user expressed a strong format preference |
| Any recommended field | Infer from summary, or omit | No |
| Any visual/optional field | Library default | No |

Always record applied defaults in the output's **Assumptions** section. Never let a missing optional field block generation.

Full field definitions: see `METADATA_SCHEMA.md`.

---

### Step 3 — Select output format

Map notation → library → diagram type.

**Notation → library:**

| Architectural Notation | Output library |
|------------------------|----------------|
| `icons_and_arrows` | Python `diagrams` package |
| `boxes_and_arrows` | Graphviz (DOT) |
| `UML` | PlantUML |
| `boxes` | Graphviz or simple PlantUML |

**Behavior → diagram type:**

| Behavior | Diagram type |
|----------|--------------|
| `static` | Component, deployment, or package diagram |
| `dynamic` | Sequence or activity diagram |
| `both` | Component diagram with flow annotations, or two separate views |

---

### Step 4 — Generate diagram-as-code

Apply these constraints in every generation:

1. Output **only** executable diagram code — no markdown fences, no prose explanations
2. The `summary` is the primary guide for structure and relationships
3. Every metadata field must influence the result (concern drives emphasis, granularity drives abstraction)
4. Show **architectural abstractions**, not every class or file
5. Include all primary components and relationships for the stated scope
6. If scope is `part`, show only the relevant subsystem
7. For `diagrams` library: use only valid imports from the official node list (https://diagrams.mingrammer.com/docs/nodes/); do not invent node classes
8. Layout: readable left-to-right or top-to-bottom; clear component names

**Anti-patterns to avoid** (from human evaluation of 4,137 views):

| Failure mode | Frequency | Mitigation |
|--------------|-----------|------------|
| Over-detailing | 57 cases | Enforce granularity; cap node count |
| Too many components | 22 cases | Reduce scope or lower effective granularity |
| Missing components | 14 cases | Cross-check summary for all primary actors |
| General concern overload | hardest concern | Keep high-level; prioritize structure over detail |

**Node budget by granularity:**

| Granularity | Target nodes |
|-------------|--------------|
| `low` | 3–8 major blocks |
| `medium` | 5–15 nodes |
| `high` | 8–20 nodes (still no class-level explosion) |

Prompt templates for this step: see `PROMPT_TEMPLATES.md`.

---

### Step 5 — Render the diagram

Execute the generated code:

| Library | Render command |
|---------|----------------|
| PlantUML | `java -jar plantuml.jar -tpng diagram.puml` |
| Graphviz | `dot -Tpng diagram.dot -o diagram.png` |
| diagrams | `python diagram_script.py` (produces PNG) |

This step should be a **deterministic tool call**, not LLM reasoning.

---

### Step 6 — Compile-verify loop with fallback ladder

On render failure, **self-repair automatically** before involving the user. Walk down this ladder; stop at the first rung that produces a valid rendered diagram.

**Rung 1 — Fix the error (retry up to 3 times):**
1. Capture the error message (stderr)
2. Diagnose the cause (invalid import, syntax error, missing dependency, layout issue)
3. Re-prompt the generator with: error + previous code + original view specification
4. Apply targeted fixes:
   - Invalid `diagrams` import → replace with a valid node class or a generic node
   - Unknown PlantUML element → use a standard element (`component`, `rectangle`)
   - Syntax error → correct and resubmit

**Rung 2 — Simplify:**
- Reduce node count toward the lower granularity budget
- Remove optional styling (colors, ports, nested clusters) that may cause errors
- Collapse fine-grained elements into higher-level groups

**Rung 3 — Switch library:**
- If the selected library keeps failing, switch to a more forgiving one:
  `diagrams` → Graphviz → PlantUML → Mermaid
- Regenerate the same view specification with the new library

**Rung 4 — Drop to diagram-as-code:**
- If no renderer is available in the environment, return valid, copy-pasteable diagram code plus instructions to render it. This still satisfies "never give up."

**Rung 5 — Textual structure:**
- As a last resort, return a structured textual/ASCII representation of components and relationships, clearly labeled as a fallback, and offer to produce rendered code on request.

**Never** end with "I couldn't generate the diagram." Always deliver the highest rung you reached, and document which rung and why.

---

### Step 7 — Quality self-check

Before delivering, evaluate your output against these criteria:

| Criterion | Question |
|-----------|----------|
| **Clarity** | Are labels readable? Is layout logical? Do names reflect purpose? |
| **Consistency** | Is notation uniform? Are connector styles consistent? |
| **Completeness** | Are primary components and relationships present for the scope? |
| **Accuracy** | Do relationships match the summary and concern? |
| **Level of Detail** | Does detail match granularity — not too vague, not code-level? |

If any criterion fails, revise before returning. Full rubric: see `EVALUATION_RUBRIC.md`.

---

## Concern-specific guidance

| Concern | Visual emphasis |
|---------|-----------------|
| `control_flow` | Message order, call sequences, decision points (best empirical results) |
| `data_flow` | Data stores, pipelines, transformations |
| `deployment` | Infrastructure, containers, network boundaries (needs full metadata) |
| `connectivity` | Integration points, protocols, external systems |
| `security` | Trust boundaries, auth flows, sensitive paths |
| `performance` | Bottlenecks, caching, async paths |
| `scheduling` | Triggers, jobs, execution order |
| `general` | High-level structure only; avoid feature-level detail |

---

## Delivery format

Always return (even in fallback cases):

1. **Diagram** — rendered image (PNG/SVG), or diagram-as-code, or textual structure (whichever rung you reached)
2. **View specification used** — the metadata fields applied
3. **Assumptions** — any inferred defaults or clarifications you resolved yourself
4. **Limitations** — what was omitted and why (e.g., "medium granularity; helper modules excluded")
5. **Fallback note** (only if you dropped below a rendered diagram) — which rung you used and how the user can get the full result
6. **Offer to refine** — invite the user to adjust concern, scope, notation, or granularity

---

## Failure recovery quick reference

| Situation | Do this |
|-----------|---------|
| No system info at all | Ask one clarifying round; request a summary or description |
| Missing optional fields | Apply defaults; record in Assumptions |
| Ambiguous high-impact choice | Ask once with defaults offered; proceed if no reply |
| Code won't render | Walk the Step 6 fallback ladder |
| No renderer available | Return diagram-as-code + render instructions |
| Library keeps failing | Switch library (diagrams → graphviz → plantuml → mermaid) |
| Summary too thin | Generate best-effort; mark uncertain elements; offer to refine |
| Repo too large | Summarize accessible parts; note coverage |

---

## What does NOT work (empirical)

- Generating from repo summary + concern only (no full metadata)
- Open-ended repository exploration without view specification
- Forcing PlantUML for all notation types
- Skipping the render/verify step
- Optimizing for pixel similarity instead of concern alignment
- Including every file and class from the codebase
- Stalling on missing optional inputs instead of using defaults
- Returning broken code or "I can't" instead of a working fallback
