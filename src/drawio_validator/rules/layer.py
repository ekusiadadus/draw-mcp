"""Layer rules: layer structure, cross-layer edge detection."""

import xml.etree.ElementTree as ET
from typing import Dict, List, Set

from drawio_validator.rules import Mode, register
from drawio_validator.severity import Finding, Severity


@register(mode=Mode.STRICT)
def check_layer_structure(root: ET.Element) -> List[Finding]:
    """Verify layer cells (parent=0) have proper structure.

    Layer cells should not have vertex=1 or edge=1 attributes.
    """
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        if cell.get("parent") != "0":
            continue
        cell_id = cell.get("id", "unknown")
        # Skip the root cell itself
        if cell_id == "0":
            continue

        if cell.get("vertex") == "1":
            findings.append(
                Finding(
                    rule_id="layer/structure",
                    severity=Severity.WARNING,
                    message="Layer cell should not have vertex=1",
                    cell_id=cell_id,
                    suggestion="Remove vertex=1 from layer cell",
                )
            )
        if cell.get("edge") == "1":
            findings.append(
                Finding(
                    rule_id="layer/structure",
                    severity=Severity.WARNING,
                    message="Layer cell should not have edge=1",
                    cell_id=cell_id,
                    suggestion="Remove edge=1 from layer cell",
                )
            )
    return findings


@register(mode=Mode.STRICT)
def check_cross_layer_edges(root: ET.Element) -> List[Finding]:
    """Detect edges connecting vertices across different layers."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")

    # Build layer map: cell_id -> layer_id (parent of the cell)
    # Layers are cells with parent="0"
    layer_ids: Set[str] = set()
    for cell in cells:
        if cell.get("parent") == "0":
            cell_id = cell.get("id")
            if cell_id and cell_id != "0":
                layer_ids.add(cell_id)

    if len(layer_ids) <= 1:
        return findings

    # Map each cell to its layer
    cell_layer: Dict[str, str] = {}
    for cell in cells:
        cell_id = cell.get("id")
        parent = cell.get("parent")
        if cell_id and parent:
            if parent in layer_ids:
                cell_layer[cell_id] = parent
            elif parent == "0":
                cell_layer[cell_id] = cell_id

    # Check edges
    for cell in cells:
        if cell.get("edge") != "1":
            continue
        cell_id = cell.get("id", "unknown")
        source = cell.get("source")
        target = cell.get("target")

        if source and target:
            source_layer = cell_layer.get(source)
            target_layer = cell_layer.get(target)
            if source_layer and target_layer and source_layer != target_layer:
                findings.append(
                    Finding(
                        rule_id="layer/cross-layer-edge",
                        severity=Severity.WARNING,
                        message=(
                            f"Edge connects vertices across layers "
                            f"({source_layer} -> {target_layer})"
                        ),
                        cell_id=cell_id,
                        suggestion="Keep connected vertices in the same layer",
                    )
                )
    return findings
