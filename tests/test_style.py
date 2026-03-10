"""Tests for style rules: trailing semicolon, boolean 0/1, typo detection, fontFamily."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.style import (
    check_boolean_values,
    check_font_family,
    check_style_typos,
    check_trailing_semicolon,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


VALID = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
    <mxCell id="0"/><mxCell id="1" parent="0"/>
    <mxCell id="a" value="Test" style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
      vertex="1" parent="1">
      <mxGeometry x="0" y="0" width="100" height="60" as="geometry"/>
    </mxCell>
</root></mxGraphModel></diagram></mxfile>"""


class TestTrailingSemicolon:
    def test_valid_trailing_semicolon(self) -> None:
        findings = check_trailing_semicolon(_parse(VALID))
        assert len(findings) == 0

    def test_missing_trailing_semicolon(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="rounded=1;fontSize=18" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_trailing_semicolon(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "a" for f in findings)


class TestBooleanValues:
    def test_valid_booleans(self) -> None:
        findings = check_boolean_values(_parse(VALID))
        assert len(findings) == 0

    def test_invalid_boolean_true(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="rounded=true;fontFamily=Noto Sans JP;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_boolean_values(_parse(xml))
        assert any(f.severity == Severity.ERROR and f.cell_id == "a" for f in findings)


class TestStyleTypos:
    def test_no_typos(self) -> None:
        findings = check_style_typos(_parse(VALID))
        assert len(findings) == 0

    def test_stroke_color_typo(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="storkeColor=#000;fontFamily=Noto Sans JP;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_style_typos(_parse(xml))
        assert any(f.severity == Severity.WARNING and "storkeColor" in f.message for f in findings)


class TestFontFamily:
    def test_font_family_present(self) -> None:
        findings = check_font_family(_parse(VALID))
        assert len(findings) == 0

    def test_font_family_missing(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="Text" style="rounded=1;fontSize=18;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_font_family(_parse(xml))
        assert any(f.severity == Severity.ERROR and f.cell_id == "a" for f in findings)
