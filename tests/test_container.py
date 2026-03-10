"""Tests for container rules: pointerEvents, children coords, swimlane, collapsible."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.container import (
    check_children_bounds,
    check_collapsible,
    check_pointer_events,
    check_swimlane_start_size,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


class TestPointerEvents:
    def test_container_with_pointer_events(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="c1" value="C" style="rounded=1;container=1;pointerEvents=0;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_pointer_events(_parse(xml))
        assert len(findings) == 0

    def test_container_missing_pointer_events(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="c1" value="C" style="rounded=1;container=1;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_pointer_events(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "c1" for f in findings)

    def test_swimlane_exempt(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="sw" value="Service" style="swimlane;startSize=30;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_pointer_events(_parse(xml))
        assert len(findings) == 0


class TestChildrenBounds:
    def test_children_within_bounds(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="c1" style="container=1;pointerEvents=0;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
            <mxCell id="ch" value="Child" style="rounded=1;" vertex="1" parent="c1">
              <mxGeometry x="10" y="10" width="100" height="50" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_children_bounds(_parse(xml))
        assert len(findings) == 0

    def test_child_outside_bounds(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="c1" style="container=1;pointerEvents=0;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
            <mxCell id="ch" value="Child" style="rounded=1;" vertex="1" parent="c1">
              <mxGeometry x="250" y="10" width="100" height="50" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_children_bounds(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "ch" for f in findings)


class TestSwimlaneStartSize:
    def test_swimlane_with_start_size(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="sw" style="swimlane;startSize=30;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_swimlane_start_size(_parse(xml))
        assert len(findings) == 0

    def test_swimlane_missing_start_size(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="sw" style="swimlane;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_swimlane_start_size(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "sw" for f in findings)


class TestCollapsible:
    def test_collapsible_container(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="c1" style="container=1;collapsible=1;pointerEvents=0;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_collapsible(_parse(xml))
        assert len(findings) == 0

    def test_collapsible_info(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="c1" style="container=1;pointerEvents=0;"
              vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="300" height="200" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_collapsible(_parse(xml))
        assert any(f.severity == Severity.INFO for f in findings)
