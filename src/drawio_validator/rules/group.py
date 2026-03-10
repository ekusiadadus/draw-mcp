"""Group rules: group detection, child semantics, connectability."""

import xml.etree.ElementTree as ET
from typing import List, Set

from drawio_validator.rules import Mode, register
from drawio_validator.severity import Finding, Severity


def _is_group(style: str) -> bool:
    """Check if a cell has group style."""
    return style.startswith("group") or ";group" in style or "group;" in style


@register(mode=Mode.STRICT)
def check_group_detection(root: ET.Element) -> List[Finding]:
    """Verify group cells have container=1 for proper behavior."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        style = cell.get("style", "")
        if not _is_group(style):
            continue
        cell_id = cell.get("id", "unknown")
        if "container=1" not in style:
            findings.append(
                Finding(
                    rule_id="group/missing-container",
                    severity=Severity.WARNING,
                    message="Group cell missing container=1",
                    cell_id=cell_id,
                    suggestion="Add container=1; to group style for proper semantics",
                )
            )
    return findings


@register(mode=Mode.STRICT)
def check_group_connectability(root: ET.Element) -> List[Finding]:
    """Warn when edges connect directly to group cells."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")

    # Find group cell IDs
    group_ids: Set[str] = set()
    for cell in cells:
        style = cell.get("style", "")
        if _is_group(style):
            cell_id = cell.get("id")
            if cell_id:
                group_ids.add(cell_id)

    if not group_ids:
        return findings

    # Check edges targeting groups
    for cell in cells:
        if cell.get("edge") != "1":
            continue
        cell_id = cell.get("id", "unknown")
        source = cell.get("source", "")
        target = cell.get("target", "")

        if source in group_ids:
            findings.append(
                Finding(
                    rule_id="group/connectability",
                    severity=Severity.WARNING,
                    message=f"Edge source connects to group cell '{source}'",
                    cell_id=cell_id,
                    suggestion="Connect to a child within the group instead",
                )
            )
        if target in group_ids:
            findings.append(
                Finding(
                    rule_id="group/connectability",
                    severity=Severity.WARNING,
                    message=f"Edge target connects to group cell '{target}'",
                    cell_id=cell_id,
                    suggestion="Connect to a child within the group instead",
                )
            )
    return findings
