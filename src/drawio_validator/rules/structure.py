"""Structure rules: root cells, hierarchy, vertex/edge exclusivity, parent refs, unique IDs."""

import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import Mode, register
from drawio_validator.severity import Finding, Severity


@register(mode=Mode.LOOSE)
def check_root_cells(root: ET.Element) -> List[Finding]:
    """Verify that root cells id=0 and id=1 (parent=0) exist."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")
    ids = {cell.get("id") for cell in cells}

    if "0" not in ids:
        findings.append(
            Finding(
                rule_id="structure/root-cells",
                severity=Severity.ERROR,
                message="Missing required root cell with id=0",
                suggestion='Add <mxCell id="0"/> as first child of <root>',
            )
        )
    if "1" not in ids:
        findings.append(
            Finding(
                rule_id="structure/root-cells",
                severity=Severity.ERROR,
                message="Missing required root cell with id=1 (parent=0)",
                suggestion='Add <mxCell id="1" parent="0"/> after cell id=0',
            )
        )
    return findings


@register(mode=Mode.LOOSE)
def check_hierarchy(root: ET.Element) -> List[Finding]:
    """Verify mxfile > diagram > mxGraphModel > root hierarchy."""
    findings: List[Finding] = []

    if root.tag != "mxfile":
        findings.append(
            Finding(
                rule_id="structure/hierarchy",
                severity=Severity.ERROR,
                message=f"Root element must be <mxfile>, got <{root.tag}>",
            )
        )
        return findings

    diagram = root.find("diagram")
    if diagram is None:
        findings.append(
            Finding(
                rule_id="structure/hierarchy",
                severity=Severity.ERROR,
                message="Missing <diagram> element under <mxfile>",
            )
        )
        return findings

    model = diagram.find("mxGraphModel")
    if model is None:
        findings.append(
            Finding(
                rule_id="structure/hierarchy",
                severity=Severity.ERROR,
                message="Missing <mxGraphModel> element under <diagram>",
            )
        )
        return findings

    root_elem = model.find("root")
    if root_elem is None:
        findings.append(
            Finding(
                rule_id="structure/hierarchy",
                severity=Severity.ERROR,
                message="Missing <root> element under <mxGraphModel>",
            )
        )

    return findings


@register(mode=Mode.LOOSE)
def check_vertex_edge_exclusivity(root: ET.Element) -> List[Finding]:
    """Verify no cell has both vertex=1 and edge=1."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        is_vertex = cell.get("vertex") == "1"
        is_edge = cell.get("edge") == "1"
        if is_vertex and is_edge:
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="structure/vertex-edge-exclusivity",
                    severity=Severity.ERROR,
                    message="Cell has both vertex=1 and edge=1",
                    cell_id=cell_id,
                    suggestion="A cell must be either a vertex or an edge, not both",
                )
            )
    return findings


@register(mode=Mode.LOOSE)
def check_parent_references(root: ET.Element) -> List[Finding]:
    """Verify all parent references point to existing cells."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")
    all_ids = {cell.get("id") for cell in cells if cell.get("id") is not None}

    for cell in cells:
        parent = cell.get("parent")
        cell_id = cell.get("id", "unknown")
        if parent is not None and parent not in all_ids:
            findings.append(
                Finding(
                    rule_id="structure/parent-reference",
                    severity=Severity.ERROR,
                    message=f"Parent '{parent}' does not exist",
                    cell_id=cell_id,
                )
            )
    return findings


@register(mode=Mode.LOOSE)
def check_unique_ids(root: ET.Element) -> List[Finding]:
    """Verify all mxCell elements have unique IDs."""
    findings: List[Finding] = []
    seen: dict[str, bool] = {}

    for cell in root.findall(".//mxCell"):
        cell_id = cell.get("id")
        if cell_id is None:
            findings.append(
                Finding(
                    rule_id="structure/unique-ids",
                    severity=Severity.ERROR,
                    message="Found mxCell without id attribute",
                )
            )
            continue
        if cell_id in seen:
            findings.append(
                Finding(
                    rule_id="structure/unique-ids",
                    severity=Severity.ERROR,
                    message=f"Duplicate id '{cell_id}' found in mxCell elements",
                    cell_id=cell_id,
                )
            )
        seen[cell_id] = True

    return findings
