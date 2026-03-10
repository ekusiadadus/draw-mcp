"""Tests for preset loading and validation profile."""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from drawio_validator.preset import Preset, load_preset, validate_against_preset
from drawio_validator.severity import Severity

PRESETS_DIR = Path(__file__).parent.parent / "presets"


class TestPresetLoading:
    def test_load_flowchart_preset(self) -> None:
        preset = load_preset(PRESETS_DIR / "flowchart.yml")
        assert preset.name == "flowchart"
        assert preset.default_font_family is not None

    def test_load_architecture_preset(self) -> None:
        preset = load_preset(PRESETS_DIR / "architecture.yml")
        assert preset.name == "architecture"

    def test_preset_has_required_fields(self) -> None:
        preset = load_preset(PRESETS_DIR / "flowchart.yml")
        assert preset.default_font_family
        assert preset.default_font_size > 0
        assert preset.min_node_spacing > 0

    def test_nonexistent_preset_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_preset(PRESETS_DIR / "nonexistent.yml")


class TestPresetDataclass:
    def test_preset_creation(self) -> None:
        preset = Preset(
            name="test",
            default_font_family="Noto Sans JP",
            default_font_size=18,
            min_node_spacing=60,
            default_vertex_style="rounded=1;",
            default_edge_style="edgeStyle=orthogonalEdgeStyle;",
        )
        assert preset.name == "test"
        assert preset.default_font_size == 18


class TestPresetValidation:
    """Preset as validation profile — checks cells against preset constraints."""

    def _make_preset(self, **overrides) -> Preset:
        defaults = {
            "name": "test",
            "default_font_family": "Noto Sans JP",
            "default_font_size": 18,
            "min_node_spacing": 60,
            "default_vertex_style": "rounded=1;",
            "default_edge_style": "edgeStyle=orthogonalEdgeStyle;",
            "allowed_shapes": ["rounded", "ellipse"],
        }
        defaults.update(overrides)
        return Preset(**defaults)

    def test_compliant_xml_passes(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A"
              style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
              vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        root = ET.fromstring(xml)
        preset = self._make_preset()
        findings = validate_against_preset(root, preset)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_wrong_font_family_flagged(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A"
              style="rounded=1;fontFamily=Arial;fontSize=18;"
              vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        root = ET.fromstring(xml)
        preset = self._make_preset()
        findings = validate_against_preset(root, preset)
        assert any(
            f.severity == Severity.WARNING and "font" in f.message.lower() and f.cell_id == "a"
            for f in findings
        )

    def test_disallowed_shape_flagged(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A"
              style="shape=hexagon;fontFamily=Noto Sans JP;fontSize=18;"
              vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        root = ET.fromstring(xml)
        preset = self._make_preset(allowed_shapes=["rounded", "ellipse"])
        findings = validate_against_preset(root, preset)
        assert any(
            f.severity == Severity.WARNING and "shape" in f.message.lower() and f.cell_id == "a"
            for f in findings
        )

    def test_empty_allowed_shapes_skips_check(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A"
              style="shape=hexagon;fontFamily=Noto Sans JP;fontSize=18;"
              vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        root = ET.fromstring(xml)
        preset = self._make_preset(allowed_shapes=[])
        findings = validate_against_preset(root, preset)
        shape_findings = [f for f in findings if "shape" in f.message.lower()]
        assert len(shape_findings) == 0

    def test_small_font_size_flagged(self) -> None:
        xml = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="A"
              style="rounded=1;fontFamily=Noto Sans JP;fontSize=12;"
              vertex="1" parent="1">
              <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
            </mxCell>
        </root></mxGraphModel></diagram></mxfile>"""
        root = ET.fromstring(xml)
        preset = self._make_preset(default_font_size=18)
        findings = validate_against_preset(root, preset)
        assert any(
            f.severity == Severity.WARNING and "fontSize" in f.message and f.cell_id == "a"
            for f in findings
        )
