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
