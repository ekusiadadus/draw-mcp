"""Tests for edge rules: Z-order, relative=1, arrowhead segment, connection points, node spacing."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.edge import (
    check_arrowhead_segment,
    check_edge_relative,
    check_node_spacing,
    check_z_order,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


VALID = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
    <mxCell id="0"/><mxCell id="1" parent="0"/>
    <mxCell id="e1" edge="1" parent="1" source="a" target="b"
      style="edgeStyle=orthogonalEdgeStyle;">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="a" value="A" style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
      vertex="1" parent="1">
      <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="b" value="B" style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
      vertex="1" parent="1">
      <mxGeometry x="400" y="100" width="120" height="60" as="geometry"/>
    </mxCell>
</root></mxGraphModel></diagram></mxfile>"""


class TestZOrder:
    def test_valid_z_order(self) -> None:
        findings = check_z_order(_parse(VALID))
        assert len(findings) == 0

    def test_edge_after_vertex_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
            <mxCell id="e1" edge="1" parent="1" style="">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_z_order(_parse(xml))
        assert any(f.severity == Severity.WARNING for f in findings)


class TestEdgeRelative:
    def test_valid_relative(self) -> None:
        findings = check_edge_relative(_parse(VALID))
        assert len(findings) == 0

    def test_missing_relative(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="e1" edge="1" parent="1" style="">
              <mxGeometry as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_edge_relative(_parse(xml))
        assert any(f.severity == Severity.ERROR and f.cell_id == "e1" for f in findings)


class TestArrowheadSegment:
    def test_sufficient_segment(self) -> None:
        findings = check_arrowhead_segment(_parse(VALID))
        assert len(findings) == 0

    def test_short_segment_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="e1" edge="1" parent="1" style="">
              <mxGeometry relative="1" as="geometry">
                <mxPoint x="100" y="100" as="sourcePoint"/>
                <mxPoint x="110" y="105" as="targetPoint"/>
              </mxGeometry>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_arrowhead_segment(_parse(xml))
        assert any(f.severity == Severity.WARNING for f in findings)


class TestNodeSpacing:
    def test_adequate_spacing(self) -> None:
        findings = check_node_spacing(_parse(VALID))
        assert len(findings) == 0

    def test_nodes_too_close(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" vertex="1" parent="1" style="" value="A">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
            <mxCell id="b" vertex="1" parent="1" style="" value="B">
              <mxGeometry x="130" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_node_spacing(_parse(xml))
        assert any(f.severity == Severity.WARNING for f in findings)
