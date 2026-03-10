"""Tests for layer rules: layer structure, cross-layer edges."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.layer import (
    check_cross_layer_edges,
    check_layer_structure,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


class TestLayerStructure:
    def test_default_layer_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;fontFamily=Noto Sans JP;"
              vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_layer_structure(_parse(xml))
        assert len(findings) == 0

    def test_named_layer_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/>
            <mxCell id="1" parent="0"/>
            <mxCell id="layer2" value="Annotations" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;fontFamily=Noto Sans JP;"
              vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_layer_structure(_parse(xml))
        assert len(findings) == 0

    def test_layer_with_vertex_warned(self) -> None:
        """Layers (parent=0) should not have vertex=1."""
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/>
            <mxCell id="1" parent="0"/>
            <mxCell id="bad" value="Not a layer" parent="0" vertex="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_layer_structure(_parse(xml))
        assert any(
            f.severity == Severity.WARNING and f.cell_id == "bad" for f in findings
        )


class TestCrossLayerEdges:
    def test_same_layer_edge_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="b" value="B" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" edge="1" source="a" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_cross_layer_edges(_parse(xml))
        assert len(findings) == 0

    def test_cross_layer_edge_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/>
            <mxCell id="1" parent="0"/>
            <mxCell id="layer2" value="Layer 2" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="b" value="B" style="rounded=1;" vertex="1" parent="layer2"/>
            <mxCell id="e1" edge="1" source="a" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_cross_layer_edges(_parse(xml))
        assert any(
            f.severity == Severity.WARNING and f.cell_id == "e1" for f in findings
        )
