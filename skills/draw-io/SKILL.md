---
name: draw-io
description: Generate and edit draw.io diagrams in XML format with proper font settings, arrow placement, edge routing, containers, and Japanese text support. Use when creating flowcharts, architecture diagrams, sequence diagrams, or any visual diagrams in .drawio format. Supports Mermaid.js integration via official MCP server.
---

# draw.io Diagram Generation Skill

## Overview

This skill enables Claude Code to generate high-quality draw.io diagrams by directly editing XML. It addresses common pitfalls when generating draw.io files programmatically, with support for edge routing, containers/groups, and Mermaid.js integration.

## Quick Decision Guide

| Need | Approach | When to Use |
|------|----------|-------------|
| Custom styling, precise positioning, Japanese text | **XML** (this skill) | Complex diagrams requiring full control |
| Flowchart, sequence, ER diagram | **Mermaid.js** via MCP | Simple diagrams where layout control is not critical |
| Inline preview in chat | **MCP App Server** (`mcp.draw.io/mcp`) | Quick visualization without file generation |

## Quick Start

When creating a draw.io diagram:

1. Set `defaultFontFamily` in `mxGraphModel`
2. Add `fontFamily=FontName;` to ALL text element styles
3. Use `fontSize=18` or larger for readability
4. Place arrows (edges) BEFORE boxes (vertices) in XML
5. Allocate 30-40px width per Japanese character
6. Set `page="0"` for transparent background
7. Space nodes generously (200px horizontal / 120px vertical)
8. **Never use `--` inside XML comments**
9. Use containers (`swimlane`, `group`) for nested architecture diagrams
10. Verify with PNG export

## Core Rules

### Font Settings

```xml
<!-- In mxGraphModel -->
<mxGraphModel defaultFontFamily="Noto Sans JP" page="0" ...>

<!-- In EVERY text element's style -->
<mxCell style="text;fontFamily=Noto Sans JP;fontSize=18;..." />
```

### Arrow Placement (Z-Order)

Arrows must be declared FIRST to render behind other elements:

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />

  <!-- ARROWS FIRST (renders at back) -->
  <mxCell id="arrow1" edge="1" ... />

  <!-- BOXES AFTER (renders in front) -->
  <mxCell id="box1" vertex="1" ... />
</root>
```

### Edge Routing

draw.io has no built-in collision detection for edges. Plan carefully:

- Space nodes at least **60px** apart (prefer 200px horizontal / 120px vertical)
- Use `exitX`/`exitY` and `entryX`/`entryY` (0-1) to control connection sides
- Ensure at least **20px** straight segment before target for arrowheads
- Add explicit **waypoints** when edges would overlap
- Use `rounded=1` on edges for cleaner bends
- Use `jettySize=auto` for better port spacing

### Label-Arrow Spacing

Labels must be at least 20px away from arrow lines:

```xml
<!-- Arrow at Y=220, Label at Y=180 (40px above) - CORRECT -->
<mxCell id="label" value="Process">
  <mxGeometry y="180" width="60" height="20" />
</mxCell>
```

### Containers and Groups

For architecture diagrams, use proper parent-child containment:

```xml
<!-- Swimlane container with title -->
<mxCell id="svc1" value="Service"
  style="swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<!-- Child uses RELATIVE coordinates -->
<mxCell id="api1" value="API"
  style="rounded=1;whiteSpace=wrap;"
  vertex="1" parent="svc1">
  <mxGeometry x="20" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

- Always add `pointerEvents=0;` to containers that should not capture connections
- Use `swimlane` when the container needs a visible title bar
- Use `group` for invisible grouping

### Japanese Text Width

Allocate sufficient width to prevent unwanted line breaks:

```xml
<!-- 8 Japanese characters x 35px = 280px minimum -->
<mxCell id="title" value="シンプルなフロー図">
  <mxGeometry width="300" height="40" />
</mxCell>
```

### XML Well-Formedness (CRITICAL)

- **NEVER use `--` inside XML comments** (causes parse errors)
- Escape special characters: `&amp;`, `&lt;`, `&gt;`, `&quot;`
- All `id` attributes must be unique

## Instruction Template

When asked to create a draw.io diagram:

1. Understand the diagram requirements
2. Choose approach (XML for precision, Mermaid for simplicity)
3. Plan the layout (positions, connections, containers)
4. Generate XML with all rules applied
5. Suggest PNG verification command

## PNG Verification

Always recommend PNG export for visual verification:

```bash
# macOS
drawio -x -f png -s 2 -t -o output.png input.drawio
open output.png

# Linux
drawio -x -f png -s 2 -t -o output.png input.drawio
xdg-open output.png
```

## MCP Integration (Optional)

For inline previews or Mermaid.js support, use the official draw.io MCP server:

- **MCP App Server**: `https://mcp.draw.io/mcp` (hosted, no install required)
- **MCP Tool Server**: `npx @drawio/mcp` (stdio-based, opens browser)

## Supporting Files

- [reference.md](reference.md) - Complete XML structure reference with edge routing and containers
- [examples.md](examples.md) - Production-ready diagram examples
- [checklist.md](checklist.md) - Pre-commit validation checklist
