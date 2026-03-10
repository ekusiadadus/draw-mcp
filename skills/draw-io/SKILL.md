---
name: draw-io
description: Generate and validate draw.io diagrams in XML format. Strict quality rules for font settings, edge routing, containers, layers, and Japanese text. 23-rule validator with CLI. Use for flowcharts, architecture diagrams, sequence diagrams in .drawio format.
---

# draw.io XML Generation Specification v2.0

## 1. Scope

This specification defines the rules for AI-generated draw.io XML files. It ensures consistent, high-quality output that renders correctly in draw.io desktop, web, and PNG export. Rules are categorized as:

- **MUST** (Severity: ERROR) — Violations break rendering or structure
- **SHOULD** (Severity: WARNING) — Violations degrade quality
- **INFORMATIONAL** (Severity: INFO) — Suggestions for best practices

All rules are enforced by the `draw-mcp-validate` CLI tool with 23 validation rules.

## 2. Structural Rules (MUST)

### 2.1 File Hierarchy

```
mxfile > diagram > mxGraphModel > root > mxCell...
```

Every file MUST follow this hierarchy. The `mxfile` element is the root.

### 2.2 Root Cells

Two root cells MUST always be present:

```xml
<mxCell id="0"/>
<mxCell id="1" parent="0"/>
```

Cell `id="0"` is the invisible root. Cell `id="1"` is the default layer with `parent="0"`.

### 2.3 Parent References

Every `mxCell` with a `parent` attribute MUST reference an existing cell id. Orphaned references cause rendering failures.

### 2.4 Vertex/Edge Exclusivity

A cell MUST NOT have both `vertex="1"` and `edge="1"`. It is either a shape or a connection, never both.

### 2.5 Edge Geometry

Edge `mxGeometry` MUST have `relative="1"`:

```xml
<mxCell id="e1" edge="1" parent="1" source="a" target="b"
  style="edgeStyle=orthogonalEdgeStyle;">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 2.6 Unique IDs

All `mxCell` elements MUST have unique `id` attributes.

### 2.7 XML Well-Formedness

- MUST NOT use `--` inside XML comments (illegal per XML spec)
- MUST escape special characters in attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`

## 3. Style String Rules (MUST)

### 3.1 Format

Style strings use `key=value;` pairs with a trailing semicolon:

```
style="rounded=1;whiteSpace=wrap;html=1;fontFamily=Noto Sans JP;fontSize=18;"
```

### 3.2 Boolean Values

Boolean style keys MUST use `0` or `1`, never `true` or `false`:

```xml
<!-- CORRECT -->
style="rounded=1;html=1;"

<!-- WRONG -->
style="rounded=true;html=false;"
```

### 3.3 fontFamily on All Text

Every cell with a `value` attribute MUST include `fontFamily=FontName;` in its style:

```xml
<mxCell id="a" value="Label"
  style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
  vertex="1" parent="1"/>
```

### 3.4 Font Size

Minimum font size is **14px** (MUST). Recommended size is **18px** (SHOULD).

### 3.5 Known Keys

Use only valid draw.io style keys. Common typos (e.g., `storkeColor` for `strokeColor`) are detected and flagged.

## 4. Layout Rules (SHOULD)

### 4.1 Grid Alignment

Align node positions to a 10px grid (multiples of 10).

### 4.2 Node Spacing

- Minimum spacing: **60px** between nodes
- Recommended: **200px horizontal**, **120px vertical**

### 4.3 Edge Final Segment

The final straight segment of an edge MUST be at least **20px** for arrowheads to render cleanly.

## 5. Edge Routing (SHOULD)

### 5.1 Z-Order

Edges SHOULD be declared before vertices in XML for correct Z-order (arrows behind shapes):

```xml
<root>
  <mxCell id="0"/><mxCell id="1" parent="0"/>
  <!-- EDGES FIRST -->
  <mxCell id="e1" edge="1" .../>
  <!-- VERTICES AFTER -->
  <mxCell id="a" vertex="1" .../>
</root>
```

### 5.2 Orthogonal Style

Use `edgeStyle=orthogonalEdgeStyle` for right-angle connectors. Add `rounded=1` for cleaner bends.

### 5.3 jettySize

Use `jettySize=auto` for better port spacing on orthogonal edges.

### 5.4 jumpStyle

For crossing edges, use `jumpStyle=arc` or `jumpStyle=gap` to show crossings clearly.

### 5.5 Waypoints

Add explicit waypoints when edges would overlap:

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points">
    <mxPoint x="300" y="150"/>
  </Array>
</mxGeometry>
```

### 5.6 Connection Points

Use `exitX`/`exitY` and `entryX`/`entryY` (values 0-1) to control which side of a node an edge connects to. Spread connections across different sides to prevent overlap.

## 6. Containers (SHOULD)

### 6.1 Group Container

Invisible grouping with no visual border:

```xml
<mxCell id="grp1" style="group;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>
```

### 6.2 Swimlane Container

Visible title bar, ideal for service boundaries:

```xml
<mxCell id="svc1" value="User Service"
  style="swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontFamily=Noto Sans JP;fontSize=16;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>
```

Swimlanes SHOULD specify `startSize` for the title bar height.

### 6.3 Custom Container

Any shape acting as a container:

```xml
style="rounded=1;container=1;pointerEvents=0;"
```

Containers (except swimlanes) SHOULD include `pointerEvents=0;` to prevent connection capture.

### 6.4 Children Coordinates

Children MUST use **relative coordinates** within their parent container:

```xml
<!-- Child at (20, 40) relative to container origin -->
<mxCell id="child" vertex="1" parent="svc1">
  <mxGeometry x="20" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

Children SHOULD not extend beyond parent container bounds.

### 6.5 Collapsible

Consider adding `collapsible=1` for interactive containers (INFO).

## 7. Layers (SUPPORTED)

Layers are additional cells with `parent="0"` (like cell `id="1"`):

```xml
<mxCell id="0"/>
<mxCell id="1" parent="0"/>                    <!-- Default layer -->
<mxCell id="layer-bg" value="Background" parent="0"/>  <!-- Custom layer -->
<mxCell id="layer-fg" value="Foreground" parent="0"/>  <!-- Custom layer -->
```

Assign elements to layers via `parent="layerId"`. Layer cells do not require `fontFamily`.

## 8. Export Modes (INFORMATIONAL)

### 8.1 Transparent Background

Set `page="0"` on `mxGraphModel` for transparent background in PNG export.

### 8.2 PNG Verification

Always verify diagrams with PNG export:

```bash
drawio -x -f png -s 2 -t -o output.png input.drawio
```

### 8.3 Embed Diagram

For portable files, consider `type="embed"` on `mxfile`.

## 9. Japanese Text (SHOULD)

- Allocate **30-40px width** per Japanese character
- Use `Noto Sans JP` as default font for cross-platform compatibility
- Set `defaultFontFamily="Noto Sans JP"` on `mxGraphModel`

## 10. Validation

### CLI Usage

```bash
# Validate a file (text output, warning+ severity)
draw-mcp-validate diagram.drawio

# JSON output
draw-mcp-validate diagram.drawio --format json

# Errors only
draw-mcp-validate diagram.drawio --severity error

# Multiple files
draw-mcp-validate *.drawio
```

### Rule Summary (23 rules)

| Module | Rules | Severity |
|--------|-------|----------|
| structure | root-cells, hierarchy, vertex-edge-exclusivity, parent-reference, unique-ids | ERROR |
| style | trailing-semicolon (W), boolean-values (E), typo (W), font-family (E) | Mixed |
| edge | z-order (W), relative (E), arrowhead-segment (W), node-spacing (W) | Mixed |
| container | pointer-events (W), children-bounds (W), swimlane-start-size (W), collapsible (I) | Mixed |
| text | japanese-width (W), html-escape (W), font-size (E/W) | Mixed |
| export | page-setting (W), embed-diagram (I) | Mixed |

### Quick Decision Guide

| Need | Approach |
|------|----------|
| Custom styling, precise positioning, Japanese text | **XML** (this skill) |
| Simple flowchart, sequence, ER diagram | **Mermaid.js** via MCP |
| Inline preview in chat | **MCP App Server** (`mcp.draw.io/mcp`) |

## Supporting Files

- [reference.md](reference.md) — Complete XML structure reference
- [examples.md](examples.md) — 8 production-ready examples
- [checklist.md](checklist.md) — Pre-commit validation checklist
