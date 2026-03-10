"""Tests for endpoint rules: source/target validity, floating edges, orphan edges."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.endpoint import (
    check_endpoint_validity,
    check_floating_edges,
    check_orphan_edges,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


class TestEndpointValidity:
    def test_valid_endpoints(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;fontFamily=Noto Sans JP;"
              vertex="1" parent="1"/>
            <mxCell id="b" value="B" style="rounded=1;fontFamily=Noto Sans JP;"
              vertex="1" parent="1"/>
            <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;"
              edge="1" source="a" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_endpoint_validity(_parse(xml))
        assert len(findings) == 0

    def test_invalid_source(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="b" value="B" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;"
              edge="1" source="nonexistent" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_endpoint_validity(_parse(xml))
        assert any(
            f.severity == Severity.ERROR and "source" in f.message.lower()
            for f in findings
        )

    def test_invalid_target(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;"
              edge="1" source="a" target="missing" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_endpoint_validity(_parse(xml))
        assert any(
            f.severity == Severity.ERROR and "target" in f.message.lower()
            for f in findings
        )


class TestFloatingEdges:
    def test_connected_edge_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="b" value="B" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" edge="1" source="a" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_floating_edges(_parse(xml))
        assert len(findings) == 0

    def test_floating_edge_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="e1" edge="1" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_floating_edges(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "e1" for f in findings)


class TestOrphanEdges:
    def test_edge_with_both_endpoints(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="b" value="B" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" edge="1" source="a" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_orphan_edges(_parse(xml))
        assert len(findings) == 0

    def test_edge_missing_one_endpoint_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" edge="1" source="a" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_orphan_edges(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "e1" for f in findings)
