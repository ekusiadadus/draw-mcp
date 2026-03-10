"""Tests for escape rules: XML attribute escaping, html=1 value safety."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.escape import (
    check_dangerous_tags,
    check_value_escaping,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


class TestValueEscaping:
    def test_properly_escaped_ampersand(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A &amp; B" style="rounded=1;"
              vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_value_escaping(_parse(xml))
        assert len(findings) == 0

    def test_multiline_value_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="Line 1&#10;Line 2" style="rounded=1;"
              vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_value_escaping(_parse(xml))
        assert len(findings) == 0


class TestDangerousTags:
    def test_clean_html_value(self) -> None:
        xml = (
            '<mxfile><diagram name="P" id="d1"><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="a" value="&lt;b&gt;Bold&lt;/b&gt;" '
            'style="html=1;" vertex="1" parent="1"/>'
            "</root></mxGraphModel></diagram></mxfile>"
        )
        findings = check_dangerous_tags(_parse(xml))
        assert len(findings) == 0

    def test_script_tag_warned(self) -> None:
        xml = (
            '<mxfile><diagram name="P" id="d1"><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="a" '
            'value="&lt;script&gt;alert(1)&lt;/script&gt;" '
            'style="html=1;" vertex="1" parent="1"/>'
            "</root></mxGraphModel></diagram></mxfile>"
        )
        findings = check_dangerous_tags(_parse(xml))
        assert any(
            f.severity == Severity.ERROR and f.cell_id == "a" for f in findings
        )

    def test_iframe_tag_warned(self) -> None:
        xml = (
            '<mxfile><diagram name="P" id="d1"><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="a" '
            'value="&lt;iframe src=x&gt;&lt;/iframe&gt;" '
            'style="html=1;" vertex="1" parent="1"/>'
            "</root></mxGraphModel></diagram></mxfile>"
        )
        findings = check_dangerous_tags(_parse(xml))
        assert any(
            f.severity == Severity.ERROR and f.cell_id == "a" for f in findings
        )

    def test_no_html_mode_skips(self) -> None:
        xml = (
            '<mxfile><diagram name="P" id="d1"><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="a" '
            'value="&lt;script&gt;alert(1)&lt;/script&gt;" '
            'style="rounded=1;" vertex="1" parent="1"/>'
            "</root></mxGraphModel></diagram></mxfile>"
        )
        findings = check_dangerous_tags(_parse(xml))
        assert len(findings) == 0
