# Non-Goals

The following features are explicitly out of scope for draw-mcp:

## Hosted Preview

draw-mcp produces local `.drawio` files. It does not serve or render
diagrams in a browser. Use draw.io desktop or VS Code extension to preview.

## Mermaid or CSV Conversion

draw-mcp generates native draw.io XML only. For Mermaid or CSV-based
diagram generation, use the official `jgraph/drawio-mcp`.

## Dark Mode and Lightbox

Runtime rendering options are not part of the draw-mcp scope.

## Browser Tab or Editor Orchestration

draw-mcp does not open, control, or interact with browser tabs or
desktop applications.

## Auto-Layout

draw-mcp requires explicit coordinates in generated XML.
Auto-layout is delegated to draw.io's built-in layout engines.
