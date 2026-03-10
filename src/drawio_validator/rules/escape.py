"""Escape rules: XML value escaping, dangerous HTML tag detection."""

import re
import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import Mode, register
from drawio_validator.severity import Finding, Severity

# Pattern for detecting dangerous HTML tags in values
_DANGEROUS_TAGS = re.compile(
    r"<(?:script|iframe|object|embed|form|input|link|meta|base)",
    re.IGNORECASE,
)


@register(mode=Mode.STRICT)
def check_value_escaping(root: ET.Element) -> List[Finding]:
    """Verify values with special characters are properly escaped.

    Note: If XML parsed successfully, attribute values are already
    well-formed. This check looks for common issues in the parsed values.
    """
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        value = cell.get("value", "")
        if not value:
            continue
        # Check for raw control characters (except newline/tab)
        for ch in value:
            if ord(ch) < 32 and ch not in ("\n", "\r", "\t"):
                cell_id = cell.get("id", "unknown")
                findings.append(
                    Finding(
                        rule_id="escape/control-chars",
                        severity=Severity.WARNING,
                        message=(f"Value contains control character U+{ord(ch):04X}"),
                        cell_id=cell_id,
                        suggestion="Remove or escape control characters",
                    )
                )
                break
    return findings


@register(mode=Mode.STRICT)
def check_dangerous_tags(root: ET.Element) -> List[Finding]:
    """Detect dangerous HTML tags in html=1 cell values."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        value = cell.get("value", "")
        if not value or "html=1" not in style:
            continue

        if _DANGEROUS_TAGS.search(value):
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="escape/dangerous-tags",
                    severity=Severity.ERROR,
                    message="Value contains dangerous HTML tags (script, iframe, etc.)",
                    cell_id=cell_id,
                    suggestion="Remove dangerous HTML tags from cell values",
                )
            )
    return findings
