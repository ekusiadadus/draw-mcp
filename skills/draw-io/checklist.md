# draw.io Diagram Checklist

Use this checklist to validate draw.io diagrams before committing.

## Pre-Commit Validation

### 1. Font Settings

- [ ] `mxGraphModel` has `defaultFontFamily` attribute
- [ ] ALL text elements have `fontFamily=FontName;` in style
- [ ] Font size is 14px or larger (18px recommended)
- [ ] Japanese text uses appropriate font (Noto Sans JP, etc.)

### 2. Arrow Placement (Z-Order)

- [ ] All `edge="1"` elements (arrows) appear BEFORE `vertex="1"` elements (boxes) in XML
- [ ] Arrow labels are at least 20px away from arrow lines
- [ ] Explicit coordinates used for text element connections (avoid `exitY`/`entryY` on text)

### 3. Edge Routing

- [ ] Nodes spaced at least 60px apart (prefer 200px horizontal / 120px vertical)
- [ ] `exitX`/`exitY` and `entryX`/`entryY` used to control connection sides
- [ ] At least 20px straight segment before target for arrowheads
- [ ] Explicit waypoints added where edges would overlap
- [ ] `rounded=1` on edges for cleaner bends
- [ ] `jettySize=auto` for orthogonal edges

### 4. Text Element Sizing

- [ ] Japanese text width: 30-40px per character minimum
- [ ] Text does not overflow geometry bounds
- [ ] No unintended line breaks in labels

### 5. Containers and Groups

- [ ] Containers have `pointerEvents=0;` unless using `swimlane` style
- [ ] Children set `parent="containerId"` and use relative coordinates
- [ ] `swimlane` used for titled containers, `group` for invisible grouping

### 6. XML Well-Formedness

- [ ] No `--` inside XML comments (illegal per XML spec)
- [ ] Special characters properly escaped (`&amp;`, `&lt;`, `&gt;`, `&quot;`)
- [ ] All `mxCell` elements have unique `id` attributes

### 7. Page Settings

- [ ] `page="0"` is set in `mxGraphModel` (for transparent background)
- [ ] Appropriate canvas size (`dx`, `dy`)

### 8. Element IDs

- [ ] All `mxCell` elements have unique `id` attributes
- [ ] IDs are descriptive (e.g., `box1`, `arrow1`, `label-process`)
- [ ] Root cells `id="0"` and `id="1"` are present

### 9. Visual Verification

- [ ] PNG export generated successfully
- [ ] All text is readable at intended display size
- [ ] Arrows do not overlap with labels
- [ ] Edges do not cross unnecessarily
- [ ] Colors are consistent with design guidelines
- [ ] Layout is balanced and professional
- [ ] Container boundaries properly enclose child elements

## Automated Validation Script

Run the Python validator:

```bash
python tests/test_drawio_skill.py
```

Or use pytest:

```bash
pytest tests/test_drawio_skill.py -v
```

## PNG Export Verification

```bash
# Export to PNG
drawio -x -f png -s 2 -t -o diagram.png diagram.drawio

# Open for visual inspection
open diagram.png  # macOS
xdg-open diagram.png  # Linux
```

## Common Issues and Fixes

### Issue: Font not rendering correctly in PNG

**Cause**: `fontFamily` missing from individual elements

**Fix**: Add `fontFamily=FontName;` to every text element's style

```xml
<!-- Before -->
<mxCell style="text;html=1;fontSize=18;" />

<!-- After -->
<mxCell style="text;html=1;fontSize=18;fontFamily=Noto Sans JP;" />
```

### Issue: Arrow appears in front of boxes

**Cause**: Edge element declared after vertex elements

**Fix**: Move all edge elements to appear before vertex elements in XML

### Issue: Label overlaps with arrow

**Cause**: Label positioned too close to arrow line

**Fix**: Adjust label Y coordinate to be at least 20px away from arrow Y

```xml
<!-- Arrow at Y=200 -->
<mxPoint y="200" as="sourcePoint"/>

<!-- Label should be at Y=170 or less (above), or Y=230 or more (below) -->
<mxGeometry y="170" />
```

### Issue: Japanese text wraps unexpectedly

**Cause**: Geometry width too narrow for text content

**Fix**: Increase width (30-40px per Japanese character)

```xml
<!-- 6 Japanese characters = 180-240px minimum -->
<mxGeometry width="220" />
```

### Issue: Background not transparent in PNG

**Cause**: `page` attribute not set to `"0"`

**Fix**: Add `page="0"` to `mxGraphModel`

```xml
<mxGraphModel page="0" ... />
```

### Issue: XML parse error "not well-formed"

**Cause**: `--` used inside XML comments

**Fix**: Remove double hyphens from comments. Use words or single hyphens.

```xml
<!-- WRONG -->
<!-- Order 1 --- OrderItem -->

<!-- CORRECT -->
<!-- Order 1 to OrderItem -->
```

### Issue: Arrowhead overlaps with bend

**Cause**: Final edge segment too short for arrowhead

**Fix**: Ensure at least 20px of straight segment before target. Increase node spacing or add explicit waypoints.

### Issue: Connections captured by container

**Cause**: Container missing `pointerEvents=0` in style

**Fix**: Add `pointerEvents=0;` to container style (not needed for `swimlane`)

```xml
<mxCell style="rounded=1;container=1;pointerEvents=0;" ... />
```

## Quick Reference: Style String Format

```
style="property1=value1;property2=value2;property3=value3;"
```

### Essential Properties

| Property | Required | Example |
|----------|----------|---------|
| `fontFamily` | Yes (text) | `fontFamily=Noto Sans JP;` |
| `fontSize` | Recommended | `fontSize=18;` |
| `html` | Yes (text) | `html=1;` |
| `whiteSpace` | Recommended | `whiteSpace=wrap;` |
| `rounded` | Optional | `rounded=1;` |
| `fillColor` | Optional | `fillColor=#dae8fc;` |
| `strokeColor` | Optional | `strokeColor=#6c8ebf;` |

## Pre-Commit Hook Integration

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-drawio
        name: Validate draw.io files
        entry: python tests/test_drawio_skill.py
        language: python
        files: \.drawio$
        additional_dependencies: [pytest]

      - id: convert-drawio-to-png
        name: Convert draw.io to PNG
        entry: bash scripts/convert-drawio-to-png.sh
        language: system
        files: \.drawio$
        pass_filenames: true
```

## Review Questions

Before submitting a diagram, ask yourself:

1. Can I read all text clearly at the intended display size?
2. Are the arrows clearly showing the flow direction?
3. Do labels clearly associate with their respective arrows/elements?
4. Is the color scheme consistent and accessible?
5. Does the PNG export look the same as the draw.io preview?
6. Are nodes spaced generously enough (200px horizontal / 120px vertical)?
7. Do any edges overlap or cross unnecessarily?
8. Are containers properly enclosing their child elements?
9. Is the XML free of `--` in comments?
