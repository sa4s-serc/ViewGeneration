# Evaluation Rubric

Quality criteria for architecture views. Use for human review, LLM-as-judge validation, or automated critic agents.

Derived from human evaluation and LLM-as-judge protocols in the CodeToDiagram replication package.

---

## Instructions

Compare the generated diagram against:
1. The view specification (metadata)
2. The architectural summary (source knowledge)

For each criterion, assign one rating and provide a brief justification.

---

## Ratings

| Rating | Meaning |
|--------|---------|
| **Meets Expectations** | No significant issues |
| **Partially Meets Expectations** | Minor issues; small improvements needed |
| **Does Not Meet Expectations** | Major issues; incorrect or missing elements |

---

## Criteria

### 1. Clarity

The diagram should be understandable to technical and non-technical stakeholders.

- Symbols, icons, labels, and information are clear and unambiguous
- Each component has a descriptive name reflecting its purpose
- Components are arranged in a logical, readable layout

### 2. Consistency

Symbols, icons, styles, notations, connectors, and components are used uniformly.

- Notation matches the specified `Architectural Notation`
- Connector styles are consistent throughout
- Structural style aligns with specified `Architectural Styles`

### 3. Completeness

The diagram includes necessary information for the stated scope and concern.

- No missing primary components from the summary
- No missing primary relationships for the concern
- No unjustified extra components outside scope

### 4. Accuracy

The diagram reflects the system architecture described in the summary.

- Component relationships are correct
- Flow direction matches `Behavior` and `Connectors Direction`
- Concern emphasis is visually apparent

### 5. Level of Detail

Detail matches `Granularity` and concern alignment.

- Not too vague for the intended audience
- Not too detailed (no class/file-level explosion)
- Concern focus is appropriate

---

## Known failure modes (check explicitly)

| Mode | Signal | Action |
|------|--------|--------|
| Over-detailing | Individual classes, files, or helpers shown | Remove; raise abstraction |
| Too many components | Node count exceeds granularity budget | Merge or reduce scope |
| Missing components | Primary actor from summary absent | Add missing node |
| Extra components | Elements not in summary or scope | Remove |
| Granularity mismatch | Detail level contradicts metadata | Adjust abstraction |
| Notation mismatch | Wrong visual style for specification | Regenerate with correct library |

Empirical frequencies from human qualitative analysis (4,137 views):

| Failure theme | Occurrences |
|---------------|-------------|
| too_detailed | 57 |
| too_many_components | 22 |
| missing_components | 14 |
| extra_components | 9 |
| matching_structure (success) | 24 |

---

## LLM-as-judge output format (3Cs)

For automated comparison against a reference diagram:

```json
{
  "Clarity": {
    "rating": "Meets Expectations | Partially Meets Expectations | Does Not Meet Expectations",
    "justification": ""
  },
  "Completeness": {
    "rating": "",
    "justification": ""
  },
  "Consistency": {
    "rating": "",
    "justification": ""
  }
}
```

---

## Pass/fail heuristic for agents

**Pass** if all five criteria are "Meets" or "Partially Meets" AND no failure mode is critical.

**Fail** (trigger revision) if:
- Accuracy or Completeness is "Does Not Meet"
- Over-detailing or too_many_components detected
- Notation does not match specification

Maximum revision loops: 3 (then deliver best attempt with documented limitations).

---

## Interpreting automated metrics

| Metric | What it measures | Limitation |
|--------|------------------|------------|
| SSIM | Pixel/structural similarity to reference | Can be high despite semantic failure |
| LLM 3Cs | Clarity, completeness, consistency | May reject valid abstractions (~26% strict) |
| Human accuracy | Ground-truth alignment | Only 9.5% "Meets" across all methods — set expectations |

Optimize for **concern alignment and stakeholder comprehensibility**, not pixel similarity alone.
