# Routing Specification

## Edge Geometry (MUST)

All edge cells must have `<mxGeometry relative="1" as="geometry"/>`.
Missing `relative="1"` causes an ERROR.

## Z-Order (SHOULD)

Edges should be declared before vertices in XML order.
This ensures correct Z-order rendering (edges behind nodes).

## Arrowhead Segment (SHOULD)

The final straight segment of an edge should be at least 20px.
Shorter segments make arrowheads hard to see.

## Node Spacing (SHOULD)

Vertices on the same layer should have at least 60px spacing.
Closer spacing makes the diagram hard to read.

## Recommended Edge Style

```
edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;
```

## Validation Mode

- Edge relative: **STANDARD**
- Z-order: **STANDARD**
- Arrowhead segment: **STANDARD**
- Node spacing: **STANDARD**
