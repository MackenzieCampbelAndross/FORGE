# FORGE Architecture Export Formats

FORGE v1.0 provides an extensible export subsystem through `forge.reporting.exporters.ReportExporter`.
Every generated `EngineeringReport` or `ArchitectureBlueprint` can be serialized into production-ready documentation and diagramming languages.

---

## 1. Supported Output Formats

| Format | Extension | Target Consumer / Tooling |
| :--- | :---: | :--- |
| **Markdown** | `.md` | GitHub, Confluence, Obsidian, Hugo, PR descriptions |
| **JSON** | `.json` | Programmatic downstream pipelines, REST APIs, databases |
| **Interactive HTML** | `.html` | Standalone browser preview, executive review, client reporting |
| **Graphviz DOT** | `.dot` | `dot -Tsvg`, Graphviz CLI, Doxygen, CI visual pipelines |
| **Structurizr C4 DSL** | `.dsl` | Structurizr CLI, C4 Model visualizer, enterprise architecture repositories |
| **PlantUML** | `.puml` | PlantUML server, IntelliJ / VS Code PlantUML extensions |
| **Terminal ASCII** | text | CI/CD terminal logs, interactive CLI workflows, Docker stdout |

---

## 2. Python API Usage

### Batch Export (All Formats)

```python
from forge.reporting.exporters import ReportExporter

# Export all 6 formats simultaneously into a directory
exported_paths = ReportExporter.export_all(
    report=engineering_report,
    output_dir="./exports/system_blueprint",
    base_name="payment_core"
)
print(exported_paths)
# {
#   "markdown": "./exports/system_blueprint/payment_core.md",
#   "json": "./exports/system_blueprint/payment_core.json",
#   "html": "./exports/system_blueprint/payment_core.html",
#   "dot": "./exports/system_blueprint/payment_core.dot",
#   "c4": "./exports/system_blueprint/payment_core.dsl",
#   "puml": "./exports/system_blueprint/payment_core.puml"
# }
```

### Targeted Single-Format Exporters

```python
# 1. Standalone Interactive HTML
ReportExporter.export_html(engineering_report, "reports/blueprint.html")

# 2. Graphviz DOT
ReportExporter.export_dot(engineering_report, "diagrams/topology.dot")

# 3. Structurizr C4 Model DSL
ReportExporter.export_c4(engineering_report, "architecture/model.dsl")

# 4. PlantUML Component Diagram
ReportExporter.export_puml(engineering_report, "diagrams/components.puml")

# 5. Terminal ASCII Topology
ascii_art = ReportExporter.render_ascii(engineering_report)
print(ascii_art)
```

---

## 3. Format Details & Examples

### Graphviz DOT
Generates orthogonal directed digraphs clustered by components and data flows with distinct visual styles for dependencies vs. active runtime data traffic.

To compile SVG from the DOT file:
```bash
dot -Tsvg diagrams/topology.dot -o diagrams/topology.svg
```

### Structurizr C4 DSL
Implements the C4 model specification defining:
- `person` (External Client / User)
- `softwareSystem` (Target System)
- `container` (Per-component definitions with technology stereotypes)
- `relationships` (Both static structural dependencies and dynamic data flows)
- `views` (System Context and Container views with `autoLayout lr`)

To compile diagrams using Structurizr CLI:
```bash
structurizr-cli export -w architecture/model.dsl -f mermaid
```

### PlantUML
Produces clean component diagrams encapsulated in a deployment package environment, rendering component aliases and labeled interface protocols.

To render PNG locally:
```bash
plantuml diagrams/components.puml
```

### Interactive HTML5
The generated `.html` file is 100% self-contained with no local build dependencies. It embeds Mermaid.js via CDN for responsive interactive vector diagram rendering alongside structured tables for:
- Executive Summary & Readiness Scores
- Component Catalog with Interface & Technology breakdown
- STRIDE Threat Model & Mitigations
- Acceptance Criteria & Requirements Mapping
