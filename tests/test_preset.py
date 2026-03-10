"""Tests for preset loading and validation."""

from pathlib import Path

import pytest

from drawio_validator.preset import Preset, load_preset

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
