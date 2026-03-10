"""Text rules: Japanese width, HTML escape, font size."""

import re
import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import register
from drawio_validator.severity import Finding, Severity

MINIMUM_FONT_SIZE = 14
RECOMMENDED_FONT_SIZE = 18
JAPANESE_CHAR_WIDTH = 30


@register
def check_japanese_width(root: ET.Element) -> List[Finding]:
    """Verify text elements have sufficient width for Japanese characters."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        value = cell.get("value", "")
        if not value:
            continue

        japanese_chars = len(
            re.findall(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]", value)
        )
        if japanese_chars == 0:
            continue

        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue

        width = float(geometry.get("width", "0"))
        recommended = japanese_chars * JAPANESE_CHAR_WIDTH

        if width < recommended:
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="text/japanese-width",
                    severity=Severity.WARNING,
                    message=(
                        f"Has {japanese_chars} Japanese chars with width={width:.0f}, "
                        f"recommended width is {recommended}"
                    ),
                    cell_id=cell_id,
                    suggestion=f"Increase width to at least {recommended}px",
                )
            )
    return findings


@register
def check_html_escape(root: ET.Element) -> List[Finding]:
    """Check for potentially unsafe HTML in values when html=1."""
    findings: List[Finding] = []
    dangerous_pattern = re.compile(r"<(?:script|iframe|object|embed|form|input)", re.IGNORECASE)

    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        value = cell.get("value", "")
        if not value or "html=1" not in style:
            continue

        if dangerous_pattern.search(value):
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="text/html-escape",
                    severity=Severity.WARNING,
                    message="Value contains potentially dangerous HTML tags",
                    cell_id=cell_id,
                    suggestion="Use HTML entities or remove dangerous tags",
                )
            )
    return findings


@register
def check_font_size(root: ET.Element) -> List[Finding]:
    """Verify font sizes are adequate for readability."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        value = cell.get("value", "")
        if not value:
            continue

        style = cell.get("style", "")
        match = re.search(r"fontSize=(\d+)", style)
        if not match:
            continue

        font_size = int(match.group(1))
        cell_id = cell.get("id", "unknown")

        if font_size < MINIMUM_FONT_SIZE:
            findings.append(
                Finding(
                    rule_id="text/font-size",
                    severity=Severity.ERROR,
                    message=f"fontSize={font_size}, minimum is {MINIMUM_FONT_SIZE}",
                    cell_id=cell_id,
                    suggestion=f"Increase fontSize to at least {MINIMUM_FONT_SIZE}",
                )
            )
        elif font_size < RECOMMENDED_FONT_SIZE:
            findings.append(
                Finding(
                    rule_id="text/font-size",
                    severity=Severity.WARNING,
                    message=f"fontSize={font_size}, recommended is {RECOMMENDED_FONT_SIZE}",
                    cell_id=cell_id,
                    suggestion=f"Consider increasing fontSize to {RECOMMENDED_FONT_SIZE}",
                )
            )
    return findings
