#!/usr/bin/env python3
"""
Test suite for draw.io skill validation.

This module validates that draw.io XML files conform to the skill's best practices:
- Font family settings
- Arrow placement
- Text element sizing
- XML structure
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple

import pytest


class DrawioValidator:
    """Validator for draw.io XML files following skill best practices."""

    MINIMUM_FONT_SIZE = 14
    RECOMMENDED_FONT_SIZE = 18
    MIN_LABEL_ARROW_DISTANCE = 20
    JAPANESE_CHAR_WIDTH = 30

    def __init__(self, xml_content: str):
        """Initialize validator with XML content."""
        self.xml_content = xml_content
        self.root = ET.fromstring(xml_content)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[List[str], List[str]]:
        """Run all validations and return errors and warnings."""
        self.validate_font_family()
        self.validate_font_size()
        self.validate_arrow_placement()
        self.validate_text_width()
        self.validate_page_setting()
        return self.errors, self.warnings

    def validate_font_family(self) -> None:
        """Validate that all text elements have fontFamily specified."""
        mxcells = self.root.findall(".//mxCell")

        for cell in mxcells:
            style = cell.get("style", "")
            value = cell.get("value", "")

            # Skip if no text content
            if not value:
                continue

            # Check if it's a text element
            if "text" in style or value:
                if "fontFamily=" not in style:
                    cell_id = cell.get("id", "unknown")
                    self.errors.append(
                        f"Cell '{cell_id}' has text but missing fontFamily in style"
                    )

    def validate_font_size(self) -> None:
        """Validate font sizes are adequate for readability."""
        mxcells = self.root.findall(".//mxCell")

        for cell in mxcells:
            style = cell.get("style", "")
            value = cell.get("value", "")

            if not value:
                continue

            # Extract fontSize from style
            font_size_match = re.search(r"fontSize=(\d+)", style)
            if font_size_match:
                font_size = int(font_size_match.group(1))
                cell_id = cell.get("id", "unknown")

                if font_size < self.MINIMUM_FONT_SIZE:
                    self.errors.append(
                        f"Cell '{cell_id}' has fontSize={font_size}, "
                        f"minimum is {self.MINIMUM_FONT_SIZE}"
                    )
                elif font_size < self.RECOMMENDED_FONT_SIZE:
                    self.warnings.append(
                        f"Cell '{cell_id}' has fontSize={font_size}, "
                        f"recommended is {self.RECOMMENDED_FONT_SIZE}"
                    )

    def validate_arrow_placement(self) -> None:
        """Validate that arrows (edges) come before other elements."""
        mxcells = self.root.findall(".//mxCell")

        first_vertex_idx = -1
        last_edge_idx = -1

        for idx, cell in enumerate(mxcells):
            is_edge = cell.get("edge") == "1"
            is_vertex = cell.get("vertex") == "1"

            if is_vertex and first_vertex_idx == -1:
                first_vertex_idx = idx
            if is_edge:
                last_edge_idx = idx

        if first_vertex_idx != -1 and last_edge_idx != -1:
            if last_edge_idx > first_vertex_idx:
                self.warnings.append(
                    "Edges (arrows) should be placed before vertices (boxes) "
                    "in XML to render behind other elements"
                )

    def validate_text_width(self) -> None:
        """Validate text elements have sufficient width for Japanese text."""
        mxcells = self.root.findall(".//mxCell")

        for cell in mxcells:
            value = cell.get("value", "")

            if not value:
                continue

            # Count Japanese characters (Hiragana, Katakana, Kanji)
            japanese_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', value))

            if japanese_chars == 0:
                continue

            geometry = cell.find("mxGeometry")
            if geometry is not None:
                width = float(geometry.get("width", 0))
                recommended_width = japanese_chars * self.JAPANESE_CHAR_WIDTH

                if width < recommended_width:
                    cell_id = cell.get("id", "unknown")
                    self.warnings.append(
                        f"Cell '{cell_id}' has {japanese_chars} Japanese chars "
                        f"with width={width}, recommended width is {recommended_width}"
                    )

    def validate_page_setting(self) -> None:
        """Validate page setting for transparency."""
        mxgraph_model = self.root.find(".//mxGraphModel")
        if mxgraph_model is not None:
            page = mxgraph_model.get("page", "1")
            if page != "0":
                self.warnings.append(
                    'mxGraphModel should have page="0" for transparent background'
                )


# Test fixtures
@pytest.fixture
def valid_drawio_xml() -> str:
    """Return a valid draw.io XML for testing."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="200" as="sourcePoint"/>
            <mxPoint x="300" y="200" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="box1" value="テスト"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="120" height="60" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''


@pytest.fixture
def invalid_drawio_xml() -> str:
    """Return an invalid draw.io XML for testing."""
    return '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="box1" value="テスト"
          style="rounded=1;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="40" height="60" />
        </mxCell>
        <mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="100" y="200" as="sourcePoint"/>
            <mxPoint x="300" y="200" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''


class TestDrawioValidator:
    """Test cases for DrawioValidator."""

    def test_valid_xml_passes(self, valid_drawio_xml: str) -> None:
        """Test that valid XML passes validation."""
        validator = DrawioValidator(valid_drawio_xml)
        errors, warnings = validator.validate_all()

        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_missing_font_family_detected(self, invalid_drawio_xml: str) -> None:
        """Test that missing fontFamily is detected."""
        validator = DrawioValidator(invalid_drawio_xml)
        errors, warnings = validator.validate_all()

        font_errors = [e for e in errors if "fontFamily" in e]
        assert len(font_errors) > 0, "Should detect missing fontFamily"

    def test_small_font_size_detected(self, invalid_drawio_xml: str) -> None:
        """Test that small font size is detected."""
        validator = DrawioValidator(invalid_drawio_xml)
        errors, warnings = validator.validate_all()

        font_errors = [e for e in errors if "fontSize" in e]
        assert len(font_errors) > 0, "Should detect small fontSize"

    def test_arrow_placement_warning(self, invalid_drawio_xml: str) -> None:
        """Test that incorrect arrow placement is warned."""
        validator = DrawioValidator(invalid_drawio_xml)
        errors, warnings = validator.validate_all()

        arrow_warnings = [w for w in warnings if "Edges" in w]
        assert len(arrow_warnings) > 0, "Should warn about arrow placement"

    def test_narrow_text_width_warning(self, invalid_drawio_xml: str) -> None:
        """Test that narrow text width for Japanese is warned."""
        validator = DrawioValidator(invalid_drawio_xml)
        errors, warnings = validator.validate_all()

        width_warnings = [w for w in warnings if "width" in w.lower()]
        assert len(width_warnings) > 0, "Should warn about narrow text width"

    def test_page_setting_warning(self, invalid_drawio_xml: str) -> None:
        """Test that missing page=0 is warned."""
        validator = DrawioValidator(invalid_drawio_xml)
        errors, warnings = validator.validate_all()

        page_warnings = [w for w in warnings if "page" in w.lower()]
        assert len(page_warnings) > 0, "Should warn about page setting"


class TestSkillFilesExist:
    """Test that all required skill files exist."""

    SKILL_ROOT = Path(__file__).parent.parent / "skills" / "draw-io"

    def test_skill_md_exists(self) -> None:
        """Test that SKILL.md exists."""
        skill_file = self.SKILL_ROOT / "SKILL.md"
        assert skill_file.exists(), f"SKILL.md not found at {skill_file}"

    def test_reference_md_exists(self) -> None:
        """Test that reference.md exists."""
        ref_file = self.SKILL_ROOT / "reference.md"
        assert ref_file.exists(), f"reference.md not found at {ref_file}"

    def test_examples_md_exists(self) -> None:
        """Test that examples.md exists."""
        examples_file = self.SKILL_ROOT / "examples.md"
        assert examples_file.exists(), f"examples.md not found at {examples_file}"

    def test_checklist_md_exists(self) -> None:
        """Test that checklist.md exists."""
        checklist_file = self.SKILL_ROOT / "checklist.md"
        assert checklist_file.exists(), f"checklist.md not found at {checklist_file}"


class TestSkillMdFormat:
    """Test SKILL.md format and content."""

    SKILL_ROOT = Path(__file__).parent.parent / "skills" / "draw-io"

    def test_skill_md_has_frontmatter(self) -> None:
        """Test that SKILL.md has valid YAML frontmatter."""
        skill_file = self.SKILL_ROOT / "SKILL.md"
        if not skill_file.exists():
            pytest.skip("SKILL.md not yet created")

        content = skill_file.read_text()

        # Check frontmatter delimiters
        assert content.startswith("---"), "SKILL.md must start with ---"
        assert content.count("---") >= 2, "SKILL.md must have closing ---"

        # Extract frontmatter
        parts = content.split("---", 2)
        frontmatter = parts[1]

        # Check required fields
        assert "name:" in frontmatter, "Missing 'name' field in frontmatter"
        assert "description:" in frontmatter, "Missing 'description' field in frontmatter"

    def test_skill_md_name_format(self) -> None:
        """Test that skill name follows naming convention."""
        skill_file = self.SKILL_ROOT / "SKILL.md"
        if not skill_file.exists():
            pytest.skip("SKILL.md not yet created")

        content = skill_file.read_text()
        parts = content.split("---", 2)
        frontmatter = parts[1]

        # Extract name
        name_match = re.search(r"name:\s*(.+)", frontmatter)
        assert name_match, "Could not find name in frontmatter"

        name = name_match.group(1).strip()

        # Name should be lowercase with hyphens only
        assert re.match(r'^[a-z0-9-]+$', name), \
            f"Name '{name}' should only contain lowercase letters, numbers, and hyphens"


class TestPluginFiles:
    """Test plugin configuration files."""

    PLUGIN_ROOT = Path(__file__).parent.parent / ".claude-plugin"

    def test_plugin_json_exists(self) -> None:
        """Test that plugin.json exists."""
        plugin_file = self.PLUGIN_ROOT / "plugin.json"
        assert plugin_file.exists(), f"plugin.json not found at {plugin_file}"

    def test_marketplace_json_exists(self) -> None:
        """Test that marketplace.json exists."""
        marketplace_file = self.PLUGIN_ROOT / "marketplace.json"
        assert marketplace_file.exists(), f"marketplace.json not found at {marketplace_file}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
