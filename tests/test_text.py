"""Tests for text rules: Japanese width, HTML escape, font size."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.text import (
    check_font_size,
    check_html_escape,
    check_japanese_width,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


class TestJapaneseWidth:
    def test_adequate_width(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="テスト" style="rounded=1;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_japanese_width(_parse(xml))
        assert len(findings) == 0

    def test_narrow_width_warned(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="テスト" style="rounded=1;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="40" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_japanese_width(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "a" for f in findings)

    def test_no_japanese_text_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="Hello" style="rounded=1;" vertex="1" parent="1">
              <mxGeometry x="0" y="0" width="40" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_japanese_width(_parse(xml))
        assert len(findings) == 0


class TestHtmlEscape:
    def test_properly_escaped(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A &amp; B" style="html=1;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_html_escape(_parse(xml))
        assert len(findings) == 0

    def test_unescaped_html_tags(self) -> None:
        xml = (
            '<mxfile><diagram name="P" id="d1"><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="a" '
            'value="&lt;script&gt;alert(1)&lt;/script&gt;" '
            'style="html=1;" vertex="1" parent="1"/>'
            "</root></mxGraphModel></diagram></mxfile>"
        )
        findings = check_html_escape(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "a" for f in findings)


class TestFontSize:
    def test_adequate_font_size(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="fontSize=18;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_font_size(_parse(xml))
        assert len(findings) == 0

    def test_small_font_size_error(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="fontSize=10;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_font_size(_parse(xml))
        assert any(f.severity == Severity.ERROR and f.cell_id == "a" for f in findings)

    def test_below_recommended_warning(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="fontSize=15;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_font_size(_parse(xml))
        assert any(f.severity == Severity.WARNING and f.cell_id == "a" for f in findings)
