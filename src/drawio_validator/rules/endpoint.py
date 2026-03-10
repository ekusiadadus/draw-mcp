"""Endpoint rules: source/target validity, floating edges, orphan edges."""

import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import Mode, register
from drawio_validator.severity import Finding, Severity


@register(mode=Mode.STRICT)
def check_endpoint_validity(root: ET.Element) -> List[Finding]:
    """Verify edge source and target attributes reference existing cells."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")
    all_ids = {cell.get("id") for cell in cells if cell.get("id") is not None}

    for cell in cells:
        if cell.get("edge") != "1":
            continue
        cell_id = cell.get("id", "unknown")
        source = cell.get("source")
        target = cell.get("target")

        if source is not None and source not in all_ids:
            findings.append(
                Finding(
                    rule_id="endpoint/source-validity",
                    severity=Severity.ERROR,
                    message=f"Edge source '{source}' does not exist",
                    cell_id=cell_id,
                    suggestion="Ensure source references a valid vertex id",
                )
            )
        if target is not None and target not in all_ids:
            findings.append(
                Finding(
                    rule_id="endpoint/target-validity",
                    severity=Severity.ERROR,
                    message=f"Edge target '{target}' does not exist",
                    cell_id=cell_id,
                    suggestion="Ensure target references a valid vertex id",
                )
            )
    return findings


@register(mode=Mode.STRICT)
def check_floating_edges(root: ET.Element) -> List[Finding]:
    """Detect edges with neither source nor target (fully floating)."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        if cell.get("edge") != "1":
            continue
        source = cell.get("source")
        target = cell.get("target")
        if source is None and target is None:
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="endpoint/floating-edge",
                    severity=Severity.WARNING,
                    message="Edge has neither source nor target (floating)",
                    cell_id=cell_id,
                    suggestion="Connect the edge to source and target vertices",
                )
            )
    return findings


@register(mode=Mode.STRICT)
def check_orphan_edges(root: ET.Element) -> List[Finding]:
    """Detect edges with only one endpoint (partially connected)."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        if cell.get("edge") != "1":
            continue
        source = cell.get("source")
        target = cell.get("target")
        # Only flag if exactly one is missing (not both — that's floating)
        has_source = source is not None
        has_target = target is not None
        if has_source != has_target:
            cell_id = cell.get("id", "unknown")
            missing = "target" if has_source else "source"
            findings.append(
                Finding(
                    rule_id="endpoint/orphan-edge",
                    severity=Severity.WARNING,
                    message=f"Edge is missing {missing} endpoint",
                    cell_id=cell_id,
                    suggestion=f"Add a {missing} attribute to connect the edge",
                )
            )
    return findings
