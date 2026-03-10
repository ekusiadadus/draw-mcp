# draw.io XML Reference

## File Structure

### Root Element

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron" version="21.x.x">
  <diagram name="Page-1" id="unique-id">
    <mxGraphModel ...>
      <root>
        <!-- Elements go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### mxGraphModel Attributes

| Attribute | Description | Recommended Value |
|-----------|-------------|-------------------|
| `dx` | Canvas width | 1200 |
| `dy` | Canvas height | 800 |
| `grid` | Show grid | 1 |
| `gridSize` | Grid cell size | 10 |
| `guides` | Show guides | 1 |
| `tooltips` | Enable tooltips | 1 |
| `connect` | Enable connections | 1 |
| `arrows` | Enable arrows | 1 |
| `fold` | Enable folding | 1 |
| `page` | Page mode (0=transparent) | 0 |
| `pageScale` | Page scale | 1 |
| `pageWidth` | Page width | 850 |
| `pageHeight` | Page height | 1100 |
| `math` | Enable math rendering | 0 |
| `shadow` | Enable shadows | 0 |
| `defaultFontFamily` | Default font | Noto Sans JP |

## Element Types

### Root Cells (Required)

```xml
<mxCell id="0" />
<mxCell id="1" parent="0" />
```

These two cells are ALWAYS required as the root of the diagram.

### Vertex (Box/Shape)

```xml
<mxCell id="box1"
  value="Label Text"
  style="rounded=1;whiteSpace=wrap;html=1;fontFamily=Noto Sans JP;fontSize=18;"
  vertex="1"
  parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### Edge (Arrow/Line)

```xml
<mxCell id="arrow1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
  edge="1"
  parent="1"
  source="box1"
  target="box2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Edge with Explicit Points

```xml
<mxCell id="arrow1"
  style="edgeStyle=none;curved=1;"
  edge="1"
  parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="150" as="sourcePoint" />
    <mxPoint x="400" y="150" as="targetPoint" />
    <Array as="points">
      <mxPoint x="300" y="100" />
    </Array>
  </mxGeometry>
</mxCell>
```

### Text Element

```xml
<mxCell id="label1"
  value="Standalone Text"
  style="text;html=1;align=center;verticalAlign=middle;fontFamily=Noto Sans JP;fontSize=18;"
  vertex="1"
  parent="1">
  <mxGeometry x="100" y="50" width="200" height="30" as="geometry" />
</mxCell>
```

## Common Style Properties

### Shape Styles

| Property | Values | Description |
|----------|--------|-------------|
| `rounded` | 0, 1 | Rounded corners |
| `whiteSpace` | wrap, nowrap | Text wrapping |
| `html` | 0, 1 | HTML text support |
| `fillColor` | #RRGGBB, none | Background color |
| `strokeColor` | #RRGGBB, none | Border color |
| `strokeWidth` | number | Border width |
| `dashed` | 0, 1 | Dashed border |
| `opacity` | 0-100 | Transparency |
| `shadow` | 0, 1 | Drop shadow |

### Text Styles

| Property | Values | Description |
|----------|--------|-------------|
| `fontFamily` | font name | Font family (REQUIRED) |
| `fontSize` | number | Font size in px |
| `fontColor` | #RRGGBB | Text color |
| `fontStyle` | 0, 1, 2, 4 | 0=normal, 1=bold, 2=italic, 4=underline |
| `align` | left, center, right | Horizontal alignment |
| `verticalAlign` | top, middle, bottom | Vertical alignment |
| `labelPosition` | left, center, right | Label horizontal position |
| `verticalLabelPosition` | top, middle, bottom | Label vertical position |

### Edge Styles

| Property | Values | Description |
|----------|--------|-------------|
| `edgeStyle` | orthogonalEdgeStyle, entityRelationEdgeStyle, elbowEdgeStyle, none | Edge routing |
| `curved` | 0, 1 | Curved lines |
| `orthogonalLoop` | 0, 1 | Orthogonal loops |
| `jettySize` | auto, number | Connector size |
| `startArrow` | none, classic, block, diamond, oval | Start arrow style |
| `endArrow` | none, classic, block, diamond, oval | End arrow style |
| `startFill` | 0, 1 | Fill start arrow |
| `endFill` | 0, 1 | Fill end arrow |

### Connection Points

| Property | Values | Description |
|----------|--------|-------------|
| `exitX` | 0-1 | Exit point X (0=left, 1=right) |
| `exitY` | 0-1 | Exit point Y (0=top, 1=bottom) |
| `entryX` | 0-1 | Entry point X |
| `entryY` | 0-1 | Entry point Y |
| `exitDx` | number | Exit X offset |
| `exitDy` | number | Exit Y offset |
| `entryDx` | number | Entry X offset |
| `entryDy` | number | Entry Y offset |

## Predefined Shapes

### Basic Shapes

```xml
<!-- Rectangle -->
style="rounded=0;whiteSpace=wrap;html=1;"

<!-- Rounded Rectangle -->
style="rounded=1;whiteSpace=wrap;html=1;"

<!-- Ellipse -->
style="ellipse;whiteSpace=wrap;html=1;"

<!-- Diamond -->
style="rhombus;whiteSpace=wrap;html=1;"

<!-- Triangle -->
style="triangle;whiteSpace=wrap;html=1;"

<!-- Cylinder (Database) -->
style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;"

<!-- Cloud -->
style="ellipse;shape=cloud;whiteSpace=wrap;html=1;"
```

### Flowchart Shapes

```xml
<!-- Process -->
style="rounded=0;whiteSpace=wrap;html=1;"

<!-- Decision -->
style="rhombus;whiteSpace=wrap;html=1;"

<!-- Start/End -->
style="ellipse;whiteSpace=wrap;html=1;"

<!-- Document -->
style="shape=document;whiteSpace=wrap;html=1;"

<!-- Data -->
style="shape=parallelogram;whiteSpace=wrap;html=1;"
```

## Font Recommendations

### Japanese Fonts

| Font Name | Description |
|-----------|-------------|
| `Noto Sans JP` | Google's open source Japanese font |
| `Hiragino Kaku Gothic Pro` | macOS system font |
| `Yu Gothic` | Windows system font |
| `Meiryo` | Windows system font |

### System Fonts

| Font Name | Platform |
|-----------|----------|
| `Arial` | Cross-platform |
| `Helvetica` | macOS |
| `Segoe UI` | Windows |

## Coordinate System

- Origin (0, 0) is at top-left
- X increases to the right
- Y increases downward
- All measurements are in pixels

```
(0,0) ───────────────────> X
  │
  │
  │
  │
  ▼
  Y
```

## Z-Order (Layering)

Elements are drawn in XML order:
1. First element = bottom layer (background)
2. Last element = top layer (foreground)

**Best Practice**: Declare edges before vertices to ensure arrows appear behind shapes.

## mxGeometry Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `x` | number | X position |
| `y` | number | Y position |
| `width` | number | Element width |
| `height` | number | Element height |
| `relative` | 0, 1 | Use relative positioning |
| `as` | "geometry" | Required identifier |

## Special Characters in Values

Use HTML entities for special characters:

| Character | Entity |
|-----------|--------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| `'` | `&apos;` |
| newline | `&#xa;` or `<br>` (with html=1) |

## XML Well-Formedness (CRITICAL)

Generated XML **must** be well-formed:

- **NEVER use `--` inside XML comments.** `--` is illegal inside `<!-- -->` per the XML spec and causes parse errors. Use single hyphens or rephrase.
- Escape special characters in attribute values (`&amp;`, `&lt;`, `&gt;`, `&quot;`).
- All `mxCell` elements must have unique `id` attributes.
- Root cells `id="0"` and `id="1"` are always required.

```xml
<!-- WRONG: Double hyphens in comment -->
<!-- Order 1 --- OrderItem -->

<!-- CORRECT: Use words instead -->
<!-- Order 1 to OrderItem -->
```

## Edge Routing Best Practices

draw.io does **not** have built-in collision detection for edges. Plan layout and routing carefully.

### Node Spacing

- Space nodes at least **60px** apart
- Prefer **200px horizontal** / **120px vertical** gaps
- Align nodes to a grid (multiples of 10)

### Connection Points (exitX/exitY, entryX/entryY)

Use `exitX`/`exitY` and `entryX`/`entryY` (values 0-1) to control which side of a node an edge connects to. Spread connections across different sides to prevent overlap.

```xml
<!-- Connect from right side of source to left side of target -->
<mxCell id="e1"
  style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
  edge="1" parent="1" source="box1" target="box2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### Arrowhead Spacing

The final straight segment of an edge must be long enough to fit the arrowhead (default size: 6px, configurable via `startSize`/`endSize`). Ensure at least **20px** of straight segment before the target and after the source.

### Explicit Waypoints

Add waypoints when edges would overlap:

```xml
<mxCell id="e1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;"
  edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="150"/>
      <mxPoint x="300" y="250"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### Edge Style Tips

- Use `rounded=1` on edges for cleaner bends
- Use `jettySize=auto` for better port spacing on orthogonal edges
- Use `edgeStyle=orthogonalEdgeStyle` for right-angle connectors (most common)

## Containers and Groups

For architecture diagrams or nested elements, use proper parent-child containment.

### How Containment Works

Set `parent="containerId"` on child cells. Children use **relative coordinates** within the container.

### Container Types

| Type | Style | When to Use |
|------|-------|-------------|
| **Group** (invisible) | `group;` | No visual border needed, container has no connections |
| **Swimlane** (titled) | `swimlane;startSize=30;` | Visible title bar/header, or container itself has connections |
| **Custom container** | `container=1;pointerEvents=0;` | Any shape acting as a container without its own connections |

### Key Rules

- **Always add `pointerEvents=0;`** to container styles that should not capture connections being rewired between children
- Only omit `pointerEvents=0` when the container itself needs to be connectable (use `swimlane` style)
- Children must set `parent="containerId"` and use coordinates **relative to the container**

### Swimlane Container Example

```xml
<!-- Swimlane container with title -->
<mxCell id="svc1" value="User Service"
  style="swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;fontFamily=Noto Sans JP;fontSize=16;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<!-- Child inside container (relative coordinates) -->
<mxCell id="api1" value="REST API"
  style="rounded=1;whiteSpace=wrap;fontFamily=Noto Sans JP;fontSize=14;"
  vertex="1" parent="svc1">
  <mxGeometry x="20" y="40" width="120" height="60" as="geometry"/>
</mxCell>

<mxCell id="db1" value="Database"
  style="shape=cylinder3;whiteSpace=wrap;fontFamily=Noto Sans JP;fontSize=14;"
  vertex="1" parent="svc1">
  <mxGeometry x="160" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

### Invisible Group Container Example

```xml
<!-- Invisible group container -->
<mxCell id="grp1" value=""
  style="group;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<mxCell id="c1" value="Component A"
  style="rounded=1;whiteSpace=wrap;fontFamily=Noto Sans JP;fontSize=14;"
  vertex="1" parent="grp1">
  <mxGeometry x="10" y="10" width="120" height="60" as="geometry"/>
</mxCell>
```

## Layers

Layers allow separating diagram elements into independent visibility groups. Each layer is a cell with `parent="0"`.

### Layer Structure

```xml
<root>
  <mxCell id="0"/>                                        <!-- Root -->
  <mxCell id="1" parent="0"/>                             <!-- Default layer -->
  <mxCell id="layer-infra" value="Infrastructure" parent="0"/>  <!-- Custom layer -->
  <mxCell id="layer-app" value="Application" parent="0"/>      <!-- Custom layer -->
</root>
```

### Assigning Elements to Layers

Set `parent` to the layer id:

```xml
<!-- This box belongs to the infrastructure layer -->
<mxCell id="server1" value="Server"
  style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
  vertex="1" parent="layer-infra">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### Layer Visibility

Layers can be toggled in draw.io's Edit > Layers panel. Use layers for:
- Background/foreground separation
- Infrastructure vs application components
- Draft annotations that can be hidden

### Key Rules

- Layer cells have `parent="0"` and are siblings of `id="1"`
- Layer cells do not need `fontFamily` in their style
- Children use absolute coordinates (not relative to layer position)
- The default layer `id="1"` is always present

### Style String Format

Style strings follow a strict `key=value;` format with semicolons:

```
property1=value1;property2=value2;property3=value3;
```

**Rules:**
- Always end with a trailing `;`
- Boolean values use `0` or `1` (never `true`/`false`)
- Use only valid draw.io style keys (typos are flagged by the validator)

## Mermaid.js Integration

For simple diagrams, Mermaid.js syntax can be converted to draw.io format via the official MCP server or draw.io editor.

### Quick Decision Guide

| Need | Format | Reliability |
|------|--------|-------------|
| Flowchart, sequence, ER diagram | Mermaid.js | High |
| Custom styling, precise positioning | XML | High |
| Org chart from data | CSV | Medium |

**Default to Mermaid** for simple diagrams. Use XML when you need precise control over positioning, fonts, or Japanese text.

## Official References

- [draw.io Style Reference](https://www.drawio.com/doc/faq/drawio-style-reference.html) - Complete style properties
- [draw.io XSD Schema](https://www.drawio.com/assets/mxfile.xsd) - XML Schema Definition for validation
- [draw.io XML Format](https://www.drawio.com/doc/faq/diagram-source-edit) - Official XML documentation

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|---------|
| Double hyphen parse error | `--` used inside XML comments | Remove double hyphens from comments |
| Font not rendering in PNG | `fontFamily` missing from elements | Add `fontFamily=FontName;` to every text style |
| Arrow in front of boxes | Edge declared after vertex elements | Move all edges before vertices in XML |
| Label overlaps with arrow | Label too close to arrow line | Adjust label Y to be 20px+ away from arrow |
| Japanese text wraps | Geometry width too narrow | Increase width (30-40px per character) |
| Background not transparent | `page` not set to `"0"` | Add `page="0"` to mxGraphModel |
| Arrowhead overlaps bend | Final segment too short | Ensure 20px+ straight segment before target |
| Connections captured by container | Missing `pointerEvents=0` | Add `pointerEvents=0;` to container style |
