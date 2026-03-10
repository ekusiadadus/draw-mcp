# Presets Specification

## Purpose

Presets are **validation profiles**, not generation inputs.

A preset defines constraints that a diagram must satisfy for a given
diagram family (flowchart, architecture, etc.). Presets are applied
as an additional validation layer, not as a code generation template.

## Application Points

### 1. Validation Profile (Current)

```bash
draw-mcp-validate diagram.drawio --preset flowchart
```

When `--preset` is specified, `validate_against_preset()` checks:

- **Font family**: All text cells must use the preset's `default_font_family`
- **Font size**: All text cells must have `fontSize >= default_font_size`
- **Allowed shapes**: If the preset defines `allowed_shapes`, only those
  shapes are permitted

Preset validation findings are WARNING severity.

### 2. PRODUCTION Mode Integration (Planned)

In PRODUCTION mode, presets can be auto-detected from example metadata
or specified explicitly. Preset compliance becomes a hard requirement.

### 3. Generator Input (Future)

A future generator could read preset defaults to produce conformant XML.
This is NOT the current scope. The repo has no generator implementation.

## Preset Schema

```yaml
name: flowchart                    # Required: preset identifier
default_font_family: "Noto Sans JP"  # Font policy
default_font_size: 18              # Minimum font size
min_node_spacing: 60               # Minimum gap between nodes (px)
default_vertex_style: "rounded=1;" # Template vertex style
default_edge_style: "edgeStyle=orthogonalEdgeStyle;"
allowed_shapes:                    # Empty = no shape restriction
  - rounded
  - ellipse
  - rhombus
```

## Available Presets

| Preset | Font | Min Size | Shapes |
|--------|------|----------|--------|
| `flowchart` | Noto Sans JP | 18 | ellipse, rounded, rhombus, rectangle |
| `architecture` | Noto Sans JP | 18 | rounded, rectangle, cylinder3, cloud, hexagon |

## Non-Goals

- Presets do NOT generate XML
- Presets do NOT auto-apply styles to existing diagrams
- Presets do NOT override mode-level rules
