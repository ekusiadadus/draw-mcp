"""Export rules: page=0, embed-diagram recommendation."""

import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import register
from drawio_validator.severity import Finding, Severity


@register
def check_page_setting(root: ET.Element) -> List[Finding]:
    """Verify page=0 for transparent background."""
    findings: List[Finding] = []
    model = root.find(".//mxGraphModel")
    if model is not None:
        page = model.get("page", "1")
        if page != "0":
            findings.append(
                Finding(
                    rule_id="export/page-setting",
                    severity=Severity.WARNING,
                    message='mxGraphModel should have page="0" for transparent background',
                    suggestion='Add page="0" to mxGraphModel attributes',
                )
            )
    return findings


@register
def check_embed_diagram(root: ET.Element) -> List[Finding]:
    """Recommend embedding diagram data in exported PNG/SVG."""
    findings: List[Finding] = []
    # This is informational only - check if mxfile has embed attribute
    if root.tag == "mxfile" and root.get("type") == "embed":
        return findings

    # Only emit if the file is explicitly typed
    file_type = root.get("type", "")
    if file_type and file_type != "embed":
        findings.append(
            Finding(
                rule_id="export/embed-diagram",
                severity=Severity.INFO,
                message="Consider using embed type for portable diagram files",
                suggestion='Set type="embed" on mxfile for embedded diagram data',
            )
        )
    return findings
