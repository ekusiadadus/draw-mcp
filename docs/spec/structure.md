# Structure Specification

## File Hierarchy (MUST)

All draw.io XML files must follow this hierarchy:

```xml
<mxfile>
  <diagram name="..." id="...">
    <mxGraphModel ...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- content cells -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Root Cells (MUST)

- `id="0"` — the invisible root node
- `id="1" parent="0"` — the default layer

Both cells are required. Missing either causes an ERROR.

## Unique IDs (MUST)

Every `<mxCell>` must have a unique `id` attribute. Duplicate IDs cause an ERROR.

## Parent References (MUST)

Every `parent` attribute must reference an existing cell ID.

## Vertex/Edge Exclusivity (MUST)

A cell must be either `vertex="1"` or `edge="1"`, never both.

## Validation Mode

All structure rules run at **LOOSE** mode (minimum level).
