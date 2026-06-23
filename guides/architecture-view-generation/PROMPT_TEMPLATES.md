# Prompt Templates

Copy-paste prompts for each pipeline stage. Replace `{placeholders}` with runtime values. Works with any LLM API (OpenAI, Anthropic, Gemini, local models).

Every generation prompt below is written to be **robust**: the model infers sensible defaults, asks only high-impact questions, self-repairs on failure, and never returns nothing.

---

## System preamble (prepend to any stage)

Use this as the system message for any agent running these stages.

```
You are an expert software architect that generates architecture views from code knowledge.

Operating rules:
- Never give up: always return the best valid artifact you can. A simpler correct diagram beats broken code or refusal.
- Default, don't stall: when an input is missing and low-impact, choose a sensible default and record it as an assumption.
- Ask sparingly: request user input only when a missing detail is high-impact and would change the output meaningfully. Batch questions into one short round and offer defaults so the user can say "use defaults".
- Self-repair: on any error, diagnose and fix automatically before reporting a problem.
- Degrade gracefully: if rendering is impossible, fall back to diagram-as-code, then to a clear textual structure.
- Be explicit: list every assumption, simplification, and limitation in your output.
```

---

## Stage 0: Intake & Clarification

Use when the request is informal or input completeness is unknown. Decides whether to ask or proceed.

```
Assess this request for architecture view generation.

User request:
{user_request}

Available inputs (any of: repo path, source access, summary, system description):
{available_inputs}

Decide:
1. Is there enough to generate a view (any system knowledge at all)? 
2. Are any MISSING details high-impact (would change the diagram fundamentally) AND not safely defaultable?

If yes to (1) and no high-impact gaps: respond exactly with "PROCEED" and a JSON of inferred defaults.
If high-impact gaps exist: output ONE batched clarification block, offering defaults, in this form:

I can generate this now with defaults, or tailor it. Optionally confirm:
1. <question> [options]  (default: <X>)
2. <question> [options]  (default: <Y>)
Reply with choices, or say "use defaults".

If there is NO system knowledge at all: ask the user to paste a summary or describe the system.

Never ask about purely visual/optional fields (colors, shapes, legend) — default those silently.
```

---

## Stage 1: Knowledge Extractor

### Per-chunk summary

```
You are analyzing part {chunk_index} of {total_chunks} of a software repository.

Repository structure:
{repo_structure}

Source contents (this chunk):
{chunk_content}

Summarize this chunk. Include:
- Key functionalities and components
- Important files and their roles
- Architectural insights
- Notable design patterns

If the chunk is unreadable, truncated, or low-signal, summarize whatever is present and note the gap rather than failing.
Keep the response modular so it can be merged with other chunks.
Do not generate diagrams. Output prose only.
```

### Final merge

```
Merge these partial repository summaries into one cohesive architectural report.

Partial summaries:
{partial_summaries}

Requirements:
- Remove repetition
- Logical flow from overview to components to integrations
- Cohesive picture of functionality and architecture
- Maximum 4000 tokens; prioritize the most critical architectural information

Do not generate diagrams. Output prose only.
```

---

## Stage 2: Metadata Assembler

Use when the user request is informal and metadata must be inferred.

```
Given this architectural summary and user request, produce a complete view specification as JSON.

Summary:
{summary}

User request:
{user_request}

Output a JSON object with all fields from the view specification schema:
summary, Concern, Behavior, Granularity, Architecture Scope, Architectural Notation,
Components Nature, Connectors Nature, QAs, Architectural Styles,
Shapes, Colored?, Connectors Direction, Legend?, Nested Components?,
Explicit Ports/Interfaces?, Explicit Connectors?

Rules:
- Infer EVERY missing field; never leave one blank. Use these defaults when unsure:
  Concern=inferred-from-summary-else-general, Behavior=static, Granularity=medium,
  Architecture Scope=entire, Architectural Notation=boxes_and_arrows.
- Prefer medium granularity unless user specifies otherwise.
- Match notation to user preference; default to boxes_and_arrows.
- For dynamic behavior, set Behavior to "dynamic".
- List every inferred value in a separate "assumptions" array.
- If a HIGH-IMPACT field is genuinely ambiguous (e.g., concern changes the diagram fundamentally and intent is unclear), add a "questions" array with at most 2 batched questions. Still output a complete best-guess spec so generation can proceed if the user does not answer.

Output valid JSON only, with keys: all spec fields, "assumptions", and optional "questions".
```

---

## Stage 3: Prompt Builder

Produces the generation prompt from view specification. This is the core ArchView pattern.

```
You are an expert software architect. Generate valid Python code that produces an architecture diagram.

## Architectural knowledge
{summary}

## View specification
- Concern: {Concern} — the diagram must visually emphasize this
- Behavior: {Behavior}
- Granularity: {Granularity} — respect this abstraction level; do NOT over-detail
- Components: {Components Nature}
- Connectors: {Connectors Nature}
- Quality attributes: {QAs}
- Scope: {Architecture Scope}
- Notation: {Architectural Notation}
- Styles: {Architectural Styles}
- Visual: shapes={Shapes}, colored={Colored?}, connector direction={Connectors Direction}
- Layout: legend={Legend?}, nested={Nested Components?}, ports={Explicit Ports/Interfaces?}, explicit connectors={Explicit Connectors?}

## Output requirements
1. Use the {library} library as the ONLY representation mechanism
2. Output ONLY executable code — no markdown fences, no explanations
3. The summary is the primary guide for structure and relationships
4. Show architectural abstractions, not individual classes or files
5. Include all primary components and relationships for the stated scope
6. If scope is "part", show only the relevant subsystem
7. Clear component names; readable left-to-right or top-to-bottom layout
{if diagrams}
8. For diagrams library: use ONLY imports from this whitelist: {import_whitelist}
9. Refer to https://diagrams.mingrammer.com/docs/nodes/ for valid node classes
10. If an exact icon/node does not exist, use the closest valid generic node rather than inventing one
{endif}

## Robustness
- The summary may be incomplete. Generate the best diagram from what is given; do not stall on gaps.
- For any element you are unsure about, still include it with a clear label rather than omitting key structure.
- The code MUST be self-contained and runnable as-is. Avoid features that commonly fail (exotic imports, unsupported styling).
- Prefer correctness and renderability over visual flourish.

Generate the diagram code now.
```

**Library selection:**

| Architectural Notation | `{library}` value |
|------------------------|-------------------|
| `icons_and_arrows` | `diagrams` |
| `boxes_and_arrows` | `graphviz` |
| `UML` | `plantuml` |
| `boxes` | `graphviz` |

---

## Stage 4: View Generator (PlantUML variant)

Use when notation is UML and you want PlantUML text directly (no Python wrapper).

### Static (component diagram)

```
You are an expert software architect. Generate a PlantUML component diagram.

Repository summary:
{summary}

Concern: {Concern}
Granularity: {Granularity}
Scope: {Architecture Scope}
Styles: {Architectural Styles}

Requirements:
- Show components and their relationships
- Emphasize the specified concern
- Respect granularity — no class-level explosion
- Valid PlantUML only: @startuml ... @enduml
- No explanations, only code
```

### Dynamic (sequence diagram)

```
You are an expert software architect. Generate a PlantUML sequence diagram.

Repository summary:
{summary}

Concern: {Concern}
Behavior: dynamic

Requirements:
- Show runtime message flow between components
- Label messages clearly
- Match the described system behavior
- Valid PlantUML only: @startuml ... @enduml
- No explanations, only code
```

---

## Stage 5: Error correction & fallback ladder

Inject when rendering fails. The `{attempt}` and `{max_attempts}` values let the model escalate automatically.

```
A previous diagram generation attempt failed. Fix it and return runnable code.

Error:
{error_message}

Previous code:
{previous_code}

Original view specification:
{view_spec_json}

This is attempt {attempt} of {max_attempts}. Escalate your strategy as attempts increase:
- Attempts 1: fix the specific error directly (bad import, syntax, undefined element).
  - Invalid `diagrams` import → closest valid node or a generic node
  - Unknown PlantUML element → standard element (component, rectangle)
- Attempt 2: also SIMPLIFY — fewer nodes, remove optional styling/colors/ports/nesting that may cause errors.
- Attempt 3: if this library keeps failing, SWITCH to a more forgiving library
  ({current_library} → graphviz → plantuml → mermaid) and regenerate the same view.

Requirements:
- Keep the same architectural intent and concern focus
- Output ONLY corrected executable code (or code for the new library)
- The result MUST run as-is
- No markdown fences, no explanations
```

### Last-resort fallback (no renderer available)

Use when no rendering tool exists in the environment, after code attempts.

```
No diagram renderer is available. Produce a clear, copy-pasteable result instead of failing.

View specification:
{view_spec_json}

Output, in this order:
1. Valid diagram-as-code (PlantUML preferred for portability) in a code block
2. One line of render instructions (e.g., paste into plantuml.com or run `plantuml file.puml`)
3. A compact textual/ASCII structure of components and their relationships, so the architecture is understandable even without rendering

Label this clearly as a fallback and offer to adapt the notation on request.
```

---

## Stage 6: Quality Checker

Use as a separate critic agent or self-reflection pass.

```
You are evaluating an architecture diagram against its specification.

View specification:
{view_spec_json}

Diagram (code or description):
{diagram_output}

Evaluate each criterion with rating (Meets / Partially Meets / Does Not Meet) and one-sentence justification:

1. Clarity — readable labels, logical layout, descriptive names
2. Consistency — uniform notation and connector styles
3. Completeness — primary components and relationships present for scope
4. Accuracy — relationships match summary and concern
5. Level of Detail — matches granularity, not too vague or too detailed

Also check for known failure modes:
- Over-detailing (too many low-level elements)
- Too many components for stated granularity
- Missing primary components from summary
- Extra components outside scope

Output JSON:
{
  "clarity": {"rating": "", "justification": ""},
  "consistency": {"rating": "", "justification": ""},
  "completeness": {"rating": "", "justification": ""},
  "accuracy": {"rating": "", "justification": ""},
  "level_of_detail": {"rating": "", "justification": ""},
  "overall_pass": true/false,
  "revision_needed": "specific instructions if overall_pass is false"
}
```

---

## Stage 7: User-facing response

Template for final agent output (any framework).

```
## Architecture View

[Rendered diagram or diagram-as-code]

## View Specification
| Field | Value |
|-------|-------|
| Concern | {Concern} |
| Behavior | {Behavior} |
| Granularity | {Granularity} |
| Notation | {Architectural Notation} |
| Scope | {Architecture Scope} |

## Assumptions
{assumptions_list}

## Limitations
{limitations_list}

## Fallback note (include only if not a rendered diagram)
{fallback_note}

---
Want changes? I can adjust the concern, scope, notation, or granularity — just say so.
```
