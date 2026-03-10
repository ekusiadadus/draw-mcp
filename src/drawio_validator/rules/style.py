"""Style rules: trailing semicolon, boolean 0/1, typo detection, fontFamily."""

import re
import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import register
from drawio_validator.severity import Finding, Severity

# Known valid style keys (subset of most common)
KNOWN_KEYS = {
    "align",
    "arcSize",
    "arrows",
    "aspect",
    "autosize",
    "bendable",
    "boundedLbl",
    "cloneable",
    "collapsible",
    "connectable",
    "container",
    "curved",
    "dashed",
    "dashPattern",
    "deletable",
    "direction",
    "edgeStyle",
    "editable",
    "endArrow",
    "endFill",
    "endSize",
    "entryDx",
    "entryDy",
    "entryPerimeter",
    "entryX",
    "entryY",
    "exitDx",
    "exitDy",
    "exitPerimeter",
    "exitX",
    "exitY",
    "fillColor",
    "fixedSize",
    "foldable",
    "fontColor",
    "fontFamily",
    "fontSize",
    "fontStyle",
    "glass",
    "gradientColor",
    "gradientDirection",
    "horizontal",
    "html",
    "image",
    "imageAlign",
    "imageHeight",
    "imageVerticalAlign",
    "imageWidth",
    "jettySize",
    "jumpSize",
    "jumpStyle",
    "labelBackgroundColor",
    "labelBorderColor",
    "labelPadding",
    "labelPosition",
    "labelWidth",
    "movable",
    "noEdgeStyle",
    "noLabel",
    "opacity",
    "orthogonal",
    "orthogonalLoop",
    "overflow",
    "perimeter",
    "perimeterSpacing",
    "pointerEvents",
    "portConstraint",
    "portConstraintRotation",
    "resizable",
    "resizeHeight",
    "resizeWidth",
    "rotation",
    "rounded",
    "routingCenterX",
    "routingCenterY",
    "segment",
    "selectable",
    "shadow",
    "shape",
    "size",
    "sourcePerimeterSpacing",
    "spacing",
    "spacingBottom",
    "spacingLeft",
    "spacingRight",
    "spacingTop",
    "startArrow",
    "startFill",
    "startSize",
    "strokeColor",
    "strokeWidth",
    "swimlaneLine",
    "swimlaneHead",
    "targetPerimeterSpacing",
    "text",
    "textDirection",
    "textOpacity",
    "verticalAlign",
    "verticalLabelPosition",
    "whiteSpace",
}

# Common typos mapping
COMMON_TYPOS = {
    "storkeColor": "strokeColor",
    "strokColor": "strokeColor",
    "stokeColor": "strokeColor",
    "fillColour": "fillColor",
    "strokeColour": "strokeColor",
    "fontColour": "fontColor",
    "fontSise": "fontSize",
    "fontsize": "fontSize",
    "fontfamily": "fontFamily",
    "Fontfamily": "fontFamily",
    "edgestyle": "edgeStyle",
    "whiteSpace ": "whiteSpace",
    "whitespace": "whiteSpace",
    "pointerevents": "pointerEvents",
}

# Boolean style keys that should use 0/1
BOOLEAN_KEYS = {
    "rounded",
    "curved",
    "dashed",
    "html",
    "shadow",
    "glass",
    "container",
    "collapsible",
    "connectable",
    "deletable",
    "editable",
    "foldable",
    "movable",
    "resizable",
    "selectable",
    "bendable",
    "cloneable",
    "autosize",
    "fixedSize",
    "noEdgeStyle",
    "noLabel",
    "orthogonal",
    "orthogonalLoop",
    "startFill",
    "endFill",
    "pointerEvents",
    "swimlaneLine",
}


def _parse_style(style_str: str) -> list[tuple[str, str]]:
    """Parse a style string into (key, value) pairs."""
    pairs = []
    for part in style_str.split(";"):
        part = part.strip()
        if "=" in part:
            key, _, value = part.partition("=")
            pairs.append((key.strip(), value.strip()))
    return pairs


@register
def check_trailing_semicolon(root: ET.Element) -> List[Finding]:
    """Verify style strings end with semicolon."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        if not style:
            continue
        if style and not style.rstrip().endswith(";"):
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="style/trailing-semicolon",
                    severity=Severity.WARNING,
                    message="Style string missing trailing semicolon",
                    cell_id=cell_id,
                    suggestion="Add ; at the end of the style string",
                )
            )
    return findings


@register
def check_boolean_values(root: ET.Element) -> List[Finding]:
    """Verify boolean style values use 0/1 not true/false."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        if not style:
            continue
        cell_id = cell.get("id", "unknown")
        for key, value in _parse_style(style):
            if key in BOOLEAN_KEYS and value.lower() in ("true", "false"):
                findings.append(
                    Finding(
                        rule_id="style/boolean-values",
                        severity=Severity.ERROR,
                        message=f"Boolean key '{key}' uses '{value}', must use 0 or 1",
                        cell_id=cell_id,
                        suggestion=f"Change {key}={value} to {key}={'1' if value.lower() == 'true' else '0'}",
                    )
                )
    return findings


@register
def check_style_typos(root: ET.Element) -> List[Finding]:
    """Detect common style key typos."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        if not style:
            continue
        cell_id = cell.get("id", "unknown")
        for key, _ in _parse_style(style):
            if key in COMMON_TYPOS:
                correct = COMMON_TYPOS[key]
                findings.append(
                    Finding(
                        rule_id="style/typo",
                        severity=Severity.WARNING,
                        message=f"Possible typo '{key}', did you mean '{correct}'?",
                        cell_id=cell_id,
                        suggestion=f"Replace '{key}' with '{correct}'",
                    )
                )
    return findings


@register
def check_font_family(root: ET.Element) -> List[Finding]:
    """Verify all text elements have fontFamily specified."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        value = cell.get("value", "")
        if not value:
            continue
        if "fontFamily=" not in style:
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="style/font-family",
                    severity=Severity.ERROR,
                    message="Cell has text but missing fontFamily in style",
                    cell_id=cell_id,
                    suggestion="Add fontFamily=Noto Sans JP; to the style string",
                )
            )
    return findings
