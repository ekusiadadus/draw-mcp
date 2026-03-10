"""Edge rules: Z-order, relative=1, arrowhead segment, node spacing."""

import math
import xml.etree.ElementTree as ET
from typing import List

from drawio_validator.rules import register
from drawio_validator.severity import Finding, Severity

MIN_NODE_SPACING = 60
MIN_ARROWHEAD_SEGMENT = 20


@register
def check_z_order(root: ET.Element) -> List[Finding]:
    """Verify edges are declared before vertices for correct Z-order."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")

    first_vertex_idx = -1
    last_edge_idx = -1

    for idx, cell in enumerate(cells):
        is_edge = cell.get("edge") == "1"
        is_vertex = cell.get("vertex") == "1"
        if is_vertex and first_vertex_idx == -1:
            first_vertex_idx = idx
        if is_edge:
            last_edge_idx = idx

    if first_vertex_idx != -1 and last_edge_idx != -1:
        if last_edge_idx > first_vertex_idx:
            findings.append(
                Finding(
                    rule_id="edge/z-order",
                    severity=Severity.WARNING,
                    message="Edges should be placed before vertices in XML for correct Z-order",
                    suggestion="Move all edge elements before vertex elements in the XML",
                )
            )
    return findings


@register
def check_edge_relative(root: ET.Element) -> List[Finding]:
    """Verify edge geometries have relative=1."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        if cell.get("edge") != "1":
            continue
        cell_id = cell.get("id", "unknown")
        geom = cell.find("mxGeometry")
        if geom is not None and geom.get("relative") != "1":
            findings.append(
                Finding(
                    rule_id="edge/relative",
                    severity=Severity.ERROR,
                    message='Edge geometry missing relative="1"',
                    cell_id=cell_id,
                    suggestion='Add relative="1" to the mxGeometry element',
                )
            )
    return findings


@register
def check_arrowhead_segment(root: ET.Element) -> List[Finding]:
    """Verify edges with explicit points have sufficient final segment length."""
    findings: List[Finding] = []
    for cell in root.findall(".//mxCell"):
        if cell.get("edge") != "1":
            continue

        # Only check edges with explicit source/target points
        geom = cell.find("mxGeometry")
        if geom is None:
            continue

        source_pt = None
        target_pt = None
        for pt in geom.findall("mxPoint"):
            if pt.get("as") == "sourcePoint":
                source_pt = pt
            elif pt.get("as") == "targetPoint":
                target_pt = pt

        if source_pt is None or target_pt is None:
            continue

        sx = float(source_pt.get("x", "0"))
        sy = float(source_pt.get("y", "0"))
        tx = float(target_pt.get("x", "0"))
        ty = float(target_pt.get("y", "0"))

        distance = math.sqrt((tx - sx) ** 2 + (ty - sy) ** 2)
        if distance < MIN_ARROWHEAD_SEGMENT:
            cell_id = cell.get("id", "unknown")
            findings.append(
                Finding(
                    rule_id="edge/arrowhead-segment",
                    severity=Severity.WARNING,
                    message=(
                        f"Edge segment length {distance:.0f}px is less "
                        f"than {MIN_ARROWHEAD_SEGMENT}px minimum"
                    ),
                    cell_id=cell_id,
                    suggestion="Increase spacing between source and target points",
                )
            )
    return findings


@register
def check_node_spacing(root: ET.Element) -> List[Finding]:
    """Verify nodes have sufficient spacing between them."""
    findings: List[Finding] = []
    cells = root.findall(".//mxCell")
    vertices = []

    for cell in cells:
        if cell.get("vertex") != "1":
            continue
        geometry = cell.find("mxGeometry")
        if geometry is None:
            continue
        parent = cell.get("parent", "1")
        if parent != "1":
            continue
        x = float(geometry.get("x", "0"))
        y = float(geometry.get("y", "0"))
        w = float(geometry.get("width", "0"))
        h = float(geometry.get("height", "0"))
        cell_id = cell.get("id", "unknown")
        vertices.append({"id": cell_id, "x": x, "y": y, "w": w, "h": h})

    for i, v1 in enumerate(vertices):
        for v2 in vertices[i + 1 :]:
            cx1 = v1["x"] + v1["w"] / 2
            cy1 = v1["y"] + v1["h"] / 2
            cx2 = v2["x"] + v2["w"] / 2
            cy2 = v2["y"] + v2["h"] / 2

            gap_x = abs(cx1 - cx2) - (v1["w"] + v2["w"]) / 2
            gap_y = abs(cy1 - cy2) - (v1["h"] + v2["h"]) / 2

            if gap_x > 0 and gap_y > 0:
                continue
            gap = max(gap_x, gap_y)
            if gap < MIN_NODE_SPACING:
                findings.append(
                    Finding(
                        rule_id="edge/node-spacing",
                        severity=Severity.WARNING,
                        message=(
                            f"Nodes '{v1['id']}' and '{v2['id']}' are only "
                            f"{gap:.0f}px apart, minimum is {MIN_NODE_SPACING}px"
                        ),
                    )
                )
    return findings
