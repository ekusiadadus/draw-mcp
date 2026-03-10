"""Tests for group rules: group detection, child semantics, connectability."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.group import (
    check_group_connectability,
    check_group_detection,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


class TestGroupDetection:
    def test_proper_group_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="g1" value="Group"
              style="group;container=1;collapsible=0;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="200" height="200" as="geometry"/>
            </mxCell>
            <mxCell id="c1" value="Child" style="rounded=1;fontFamily=Noto Sans JP;"
              vertex="1" parent="g1">
              <mxGeometry x="10" y="10" width="80" height="40" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_group_detection(_parse(xml))
        assert len(findings) == 0

    def test_group_without_container_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="g1" value="Group" style="group;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="200" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_group_detection(_parse(xml))
        assert any(
            f.severity == Severity.WARNING and f.cell_id == "g1" for f in findings
        )


class TestGroupConnectability:
    def test_edge_to_group_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="g1" value="Group" style="group;container=1;"
              vertex="1" parent="1"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" edge="1" source="a" target="g1" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_group_connectability(_parse(xml))
        assert any(
            f.severity == Severity.WARNING and "group" in f.message.lower()
            for f in findings
        )

    def test_edge_to_non_group_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="b" value="B" style="rounded=1;" vertex="1" parent="1"/>
            <mxCell id="e1" edge="1" source="a" target="b" parent="1">
              <mxGeometry relative="1" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_group_connectability(_parse(xml))
        assert len(findings) == 0
