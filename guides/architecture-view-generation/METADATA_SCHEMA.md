# View Specification Schema

IEEE 42010-aligned metadata for architecture view generation. Validate agent inputs and outputs against this schema.

> Machine-readable version: [`view_spec.schema.json`](view_spec.schema.json) (JSON Schema 2020-12). Use it for strict input validation, tool/function-calling argument schemas, or config validation. This document is the human-readable companion.

## JSON structure

```json
{
  "summary": "string (required)",
  "Concern": "string (required)",
  "Behavior": "static | dynamic | both (required)",
  "Granularity": "low | medium | high (required)",
  "Architecture Scope": "entire | part | entire+ (required)",
  "Architectural Notation": "string (required)",
  "Components Nature": "string (recommended)",
  "Connectors Nature": "string (recommended)",
  "QAs": "string (recommended)",
  "Architectural Styles": "string (recommended)",
  "Shapes": "string (optional)",
  "Colored?": "yes | no (optional)",
  "Connectors Direction": "unidirectional | bidirectional | mixed (optional)",
  "Legend?": "yes | no (optional)",
  "Nested Components?": "yes | no (optional)",
  "Explicit Ports/Interfaces?": "yes | no (optional)",
  "Explicit Connectors?": "yes | no (optional)"
}
```

## Field definitions

### summary

Textual description of the system architecture extracted from source code or documentation. Primary guide for diagram structure and relationships.

### Concern

What the view must emphasize.

| Value | Use when | Empirical note |
|-------|----------|----------------|
| `general` | Overall system structure | Hardest to generate; keep abstract |
| `control_flow` | Runtime interactions, call order | Best results (+19–20% SSIM vs general) |
| `data_flow` | Data movement and persistence | Show stores and pipelines |
| `deployment` | Infrastructure topology | Requires full metadata |
| `connectivity` | External integrations | Highlight protocols and boundaries |
| `security` | Auth, trust zones | Use boundaries and labeled channels |
| `performance` | Scaling, bottlenecks | Annotate cache/async/queue paths |
| `scheduling` | Jobs, cron, workflows | Show triggers and execution order |

### Behavior

| Value | Diagram type |
|-------|--------------|
| `static` | Component, deployment, package |
| `dynamic` | Sequence, activity |
| `both` | Component with annotations, or two views |

### Granularity

| Value | Abstraction | Node budget |
|-------|-------------|-------------|
| `low` | System / subsystem | 3–8 blocks |
| `medium` | Modules / services | 5–15 nodes |
| `high` | Components / interfaces | 8–20 nodes |

Human evaluation flagged over-detailing 57 times. Prefer coarser abstraction when uncertain.

### Architecture Scope

| Value | Meaning |
|-------|---------|
| `entire` | Full system |
| `part` | One subsystem or feature |
| `entire+` | Full system plus contextual elements |

### Architectural Notation

| Value | Output library | Empirical SSIM (ArchView) |
|-------|----------------|---------------------------|
| `icons_and_arrows` | Python `diagrams` | 0.754 |
| `UML` | PlantUML | 0.685 |
| `boxes_and_arrows` | Graphviz | 0.610 |
| `boxes` | Graphviz / PlantUML | 0.607 |

Hybrids (e.g., `boxes_and_arrows, icons_and_arrows`) are valid; prefer the dominant style for library selection.

### Components Nature

Types of nodes to show: services, APIs, databases, classes, modules, containers, actors, etc.

### Connectors Nature

Types of edges: REST, gRPC, message queue, function call, SQL, file I/O, etc.

### QAs (Quality Attributes, ISO 25010-inspired)

`maintainability`, `functional_suitability`, `security`, `flexibility`, `performance_efficiency`, `reliability`, `compatibility`, `interaction_capability`

Highest empirical SSIM: `functional_suitability`.

### Architectural Styles

Common values: `layered`, `microservices`, `client-server`, `event-driven`, `SOA`, `hexagonal`, `pipeline`, `peer-to-peer`, `serverless`

Layout mapping:
- `layered` → horizontal tiers
- `microservices` → bounded contexts
- `event-driven` → message buses, async connectors

### Visual fields

| Field | Values | Effect |
|-------|--------|--------|
| `Shapes` | rectangle, circle, etc. | Node shape |
| `Colored?` | yes / no | Color by component type |
| `Connectors Direction` | unidirectional / bidirectional / mixed | Arrow style |
| `Legend?` | yes / no | Include legend |
| `Nested Components?` | yes / no | Use clusters/subgraphs |
| `Explicit Ports/Interfaces?` | yes / no | Show port notation |
| `Explicit Connectors?` | yes / no | Label all connectors |

## Notation → library mapping (for orchestrators)

```python
def select_library(notation: str) -> str:
    if notation == "boxes_and_arrows":
        return "graphviz"
    if notation == "UML":
        return "plantuml"
    return "diagrams"  # default for icons_and_arrows and unknown
```

## Example: deployment view

```json
{
  "summary": "Three-tier web app: React frontend, FastAPI backend, PostgreSQL. Nginx reverse proxy. Redis for session cache.",
  "Concern": "deployment",
  "Behavior": "static",
  "Granularity": "medium",
  "Components Nature": "web server, API service, database, cache",
  "Connectors Nature": "HTTP, SQL, Redis protocol",
  "QAs": "performance_efficiency",
  "Architecture Scope": "entire",
  "Architectural Notation": "icons_and_arrows",
  "Architectural Styles": "layered, client-server",
  "Shapes": "rectangle",
  "Colored?": "yes",
  "Connectors Direction": "unidirectional",
  "Legend?": "no",
  "Nested Components?": "yes",
  "Explicit Ports/Interfaces?": "no",
  "Explicit Connectors?": "yes"
}
```

## Example: control flow view

```json
{
  "summary": "User submits order via API gateway. Order service validates, publishes to Kafka. Payment service processes async. Notification service sends confirmation.",
  "Concern": "control_flow",
  "Behavior": "dynamic",
  "Granularity": "medium",
  "Components Nature": "API gateway, order service, payment service, notification service, message broker",
  "Connectors Nature": "HTTP, Kafka publish/subscribe",
  "QAs": "functional_suitability",
  "Architecture Scope": "part",
  "Architectural Notation": "UML",
  "Architectural Styles": "event-driven, microservices",
  "Connectors Direction": "unidirectional",
  "Nested Components?": "no",
  "Explicit Connectors?": "yes"
}
```
