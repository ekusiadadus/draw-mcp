"""Container rules: pointerEvents, children bounds, swimlane startSize, collapsible."""

import xml.etree.ElementTree as ET
from typing import Dict, List

from drawio_validator.rules import register
from drawio_validator.severity import Finding, Severity


def _is_container(style: str) -> bool:
    """Check if a cell is a container (has container=1 or swimlane style)."""
    return "container=1" in style or style.startswith("swimlane") or ";swimlane" in style


def _is_swimlane(style: str) -> bool:
    return style.startswith("swimlane") or ";swimlane" in style


@register
def check_pointer_events(root: ET.Element) -> List[Finding]:
    """Verify containers have pointerEvents=0 unless swimlane."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        cell_id = cell.get("id", "unknown")
        if "container=1" in style and "pointerEvents=0" not in style:
            if not _is_swimlane(style):
                findings.append(
                    Finding(
                        rule_id="container/pointer-events",
                        severity=Severity.WARNING,
                        message="Container missing pointerEvents=0",
                        cell_id=cell_id,
                        suggestion="Add pointerEvents=0; to prevent connection capture",
                    )
                )
    return findings


@register
def check_children_bounds(root: ET.Element) -> List[Finding]:
    """Verify children are within parent container bounds."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")

    # Build container geometry map
    containers: Dict[str, Dict[str, float]] = {}
    for cell in cells:
        style = cell.get("style", "")
        if not _is_container(style):
            continue
        geom = cell.find("mxGeometry")
        if geom is None:
            continue
        cell_id = cell.get("id")
        if cell_id is None:
            continue
        containers[cell_id] = {
            "w": float(geom.get("width", "0")),
            "h": float(geom.get("height", "0")),
        }

    # Check children
    for cell in cells:
        parent_id = cell.get("parent")
        if parent_id not in containers:
            continue
        if cell.get("vertex") != "1":
            continue

        geom = cell.find("mxGeometry")
        if geom is None:
            continue

        cell_id = cell.get("id", "unknown")
        cx = float(geom.get("x", "0"))
        cy = float(geom.get("y", "0"))
        cw = float(geom.get("width", "0"))
        ch = float(geom.get("height", "0"))
        pw = containers[parent_id]["w"]
        ph = containers[parent_id]["h"]

        if cx + cw > pw or cy + ch > ph:
            findings.append(
                Finding(
                    rule_id="container/children-bounds",
                    severity=Severity.WARNING,
                    message="Child extends beyond parent container bounds",
                    cell_id=cell_id,
                    suggestion="Adjust child position/size or enlarge the container",
                )
            )
    return findings


@register
def check_swimlane_start_size(root: ET.Element) -> List[Finding]:
    """Verify swimlane containers have startSize defined."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        if not _is_swimlane(style):
            continue
        cell_id = cell.get("id", "unknown")
        if "startSize=" not in style:
            findings.append(
                Finding(
                    rule_id="container/swimlane-start-size",
                    severity=Severity.WARNING,
                    message="Swimlane missing startSize",
                    cell_id=cell_id,
                    suggestion="Add startSize=30; for proper title bar height",
                )
            )
    return findings


@register
def check_collapsible(root: ET.Element) -> List[Finding]:
    """Suggest collapsible=1 for containers."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        if not _is_container(style):
            continue
        cell_id = cell.get("id", "unknown")
        if "collapsible=" not in style:
            findings.append(
                Finding(
                    rule_id="container/collapsible",
                    severity=Severity.INFO,
                    message="Container does not specify collapsible attribute",
                    cell_id=cell_id,
                    suggestion="Consider adding collapsible=1; for interactive containers",
                )
            )
    return findings
