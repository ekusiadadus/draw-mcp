# Layers Specification

## Layer Structure

Layers are cells with `parent="0"`. The default layer is `id="1"`.

Additional layers can be added:

```xml
<mxCell id="layer2" value="Annotations" parent="0" />
```

## Layer Restrictions (SHOULD)

- Layer cells should NOT have `vertex="1"` or `edge="1"`.
- Layer cells are structural; they define grouping, not visual content.

## Cross-Layer Edges (SHOULD)

Edges should connect vertices within the same layer.
Cross-layer edges may cause unexpected behavior when layers are
shown or hidden.

## Validation Mode

- Layer structure: **STRICT**
- Cross-layer edges: **STRICT**
