"""Tests for structure rules: root cells, hierarchy, vertex/edge, parent refs, unique IDs."""

import xml.etree.ElementTree as ET

from drawio_validator.rules.structure import (
    check_hierarchy,
    check_parent_references,
    check_root_cells,
    check_unique_ids,
    check_vertex_edge_exclusivity,
)
from drawio_validator.severity import Severity


def _parse(xml_str: str) -> ET.Element:
    return ET.fromstring(xml_str)


VALID_ROOT = """<mxfile>
  <diagram name="P" id="d1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="a" vertex="1" parent="1" style="" value="A">
          <mxGeometry x="0" y="0" width="100" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""


class TestCheckRootCells:
    def test_valid_root_cells(self) -> None:
        root = _parse(VALID_ROOT)
        findings = check_root_cells(root)
        assert len(findings) == 0

    def test_missing_cell_0(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="1" parent="0"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_root_cells(_parse(xml))
        assert any(f.severity == Severity.ERROR and "id=0" in f.message.lower() for f in findings)

    def test_missing_cell_1(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_root_cells(_parse(xml))
        assert any(f.severity == Severity.ERROR and "id=1" in f.message.lower() for f in findings)


class TestCheckHierarchy:
    def test_valid_hierarchy(self) -> None:
        findings = check_hierarchy(_parse(VALID_ROOT))
        assert len(findings) == 0

    def test_missing_mxgraphmodel(self) -> None:
        xml = "<mxfile><diagram name='P' id='d1'><root><mxCell id='0'/></root></diagram></mxfile>"
        findings = check_hierarchy(_parse(xml))
        assert any(f.severity == Severity.ERROR for f in findings)


class TestCheckVertexEdgeExclusivity:
    def test_vertex_only_passes(self) -> None:
        findings = check_vertex_edge_exclusivity(_parse(VALID_ROOT))
        assert len(findings) == 0

    def test_both_vertex_and_edge_flagged(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="bad" vertex="1" edge="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_vertex_edge_exclusivity(_parse(xml))
        assert any(f.severity == Severity.ERROR and f.cell_id == "bad" for f in findings)


class TestCheckParentReferences:
    def test_valid_parents(self) -> None:
        findings = check_parent_references(_parse(VALID_ROOT))
        assert len(findings) == 0

    def test_invalid_parent(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="x" parent="nonexistent" vertex="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_parent_references(_parse(xml))
        assert any(f.severity == Severity.ERROR and f.cell_id == "x" for f in findings)


class TestCheckUniqueIds:
    def test_unique_ids_pass(self) -> None:
        findings = check_unique_ids(_parse(VALID_ROOT))
        assert len(findings) == 0

    def test_duplicate_ids_detected(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="dup" vertex="1" parent="1"/>
            <mxCell id="dup" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_unique_ids(_parse(xml))
        assert any(f.severity == Severity.ERROR and "dup" in f.message for f in findings)

    def test_missing_id_detected(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        findings = check_unique_ids(_parse(xml))
        assert any(
            f.severity == Severity.ERROR and "without id" in f.message.lower() for f in findings
        )
