#!/usr/bin/env python3
"""
Test suite for draw.io skill validation.

This module validates that draw.io XML files conform to the skill's best practices:
- Font family settings
- Arrow placement
- Text element sizing
- XML structure
- XML well-formedness
- Container validation
- Edge routing (node spacing)
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
    MIN_NODE_SPACING = 60
    RECOMMENDED_HORIZONTAL_SPACING = 200
    RECOMMENDED_VERTICAL_SPACING = 120
    MIN_ARROWHEAD_SEGMENT = 20

    def __init__(self, xml_content: str):
        """Initialize validator with XML content."""
        self.xml_content = xml_content
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.root = None
        self._parse_xml()

    def _parse_xml(self) -> None:
        """Parse XML content, handling well-formedness errors."""
        self._check_double_hyphens()
        try:
            self.root = ET.fromstring(self.xml_content)
        except ET.ParseError as e:
            self.errors.append(f"XML parse error: {e}")

    def _check_double_hyphens(self) -> None:
        """Check for illegal double hyphens in XML comments before parsing."""
        comment_pattern = re.compile(r"<!--(.*?)-->", re.DOTALL)
        for match in comment_pattern.finditer(self.xml_content):
            comment_body = match.group(1)
            if "--" in comment_body:
                self.errors.append(
                    "XML comment contains '--' which is illegal per XML spec. "
                    "Use single hyphens or rephrase."
                )

    def validate_all(self) -> Tuple[List[str], List[str]]:
        """Run all validations and return errors and warnings."""
        if self.root is None:
            return self.errors, self.warnings
        self.validate_font_family()
        self.validate_font_size()
        self.validate_arrow_placement()
        self.validate_text_width()
        self.validate_page_setting()
        self.validate_node_spacing()
        self.validate_container_rules()
        self.validate_unique_ids()
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

    def validate_node_spacing(self) -> None:
        """Validate that nodes have sufficient spacing between them."""
        mxcells = self.root.findall(".//mxCell")
        vertices = []

        for cell in mxcells:
            if cell.get("vertex") != "1":
                continue
            geometry = cell.find("mxGeometry")
            if geometry is None:
                continue
            parent = cell.get("parent", "1")
            if parent != "1":
                continue
            x = float(geometry.get("x", 0))
            y = float(geometry.get("y", 0))
            w = float(geometry.get("width", 0))
            h = float(geometry.get("height", 0))
            cell_id = cell.get("id", "unknown")
            vertices.append({"id": cell_id, "x": x, "y": y, "w": w, "h": h})

        for i, v1 in enumerate(vertices):
            for v2 in vertices[i + 1:]:
                cx1 = v1["x"] + v1["w"] / 2
                cy1 = v1["y"] + v1["h"] / 2
                cx2 = v2["x"] + v2["w"] / 2
                cy2 = v2["y"] + v2["h"] / 2

                gap_x = abs(cx1 - cx2) - (v1["w"] + v2["w"]) / 2
                gap_y = abs(cy1 - cy2) - (v1["h"] + v2["h"]) / 2

                if gap_x > 0 and gap_y > 0:
                    continue
                gap = max(gap_x, gap_y)
                if gap < self.MIN_NODE_SPACING:
                    self.warnings.append(
                        f"Nodes '{v1['id']}' and '{v2['id']}' are only "
                        f"{gap:.0f}px apart, minimum recommended is "
                        f"{self.MIN_NODE_SPACING}px"
                    )

    def validate_container_rules(self) -> None:
        """Validate container/group best practices."""
        mxcells = self.root.findall(".//mxCell")

        for cell in mxcells:
            style = cell.get("style", "")
            cell_id = cell.get("id", "unknown")

            if "container=1" in style and "pointerEvents=0" not in style:
                if "swimlane" not in style:
                    self.warnings.append(
                        f"Container '{cell_id}' has container=1 but missing "
                        f"pointerEvents=0 (add it to prevent connection capture)"
                    )

    def validate_unique_ids(self) -> None:
        """Validate that all mxCell elements have unique IDs."""
        mxcells = self.root.findall(".//mxCell")
        seen_ids = {}

        for cell in mxcells:
            cell_id = cell.get("id")
            if cell_id is None:
                self.errors.append("Found mxCell without id attribute")
                continue
            if cell_id in seen_ids:
                self.errors.append(
                    f"Duplicate id '{cell_id}' found in mxCell elements"
                )
            seen_ids[cell_id] = True


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

    def test_double_hyphen_in_comment_detected(self) -> None:
        """Test that double hyphens in XML comments are detected."""
        xml_with_double_hyphen = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- Order 1 --- OrderItem -->
        <mxCell id="box1" value="Test"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="120" height="60" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        validator = DrawioValidator(xml_with_double_hyphen)
        errors, warnings = validator.validate_all()

        comment_errors = [e for e in errors if "'--'" in e or "comment" in e.lower()]
        assert len(comment_errors) > 0, "Should detect -- in XML comments"

    def test_valid_comment_passes(self, valid_drawio_xml: str) -> None:
        """Test that valid XML comments pass without errors."""
        validator = DrawioValidator(valid_drawio_xml)
        errors, warnings = validator.validate_all()

        comment_errors = [e for e in errors if "comment" in e.lower()]
        assert len(comment_errors) == 0, "Should not flag valid comments"

    def test_duplicate_ids_detected(self) -> None:
        """Test that duplicate IDs are detected."""
        xml_with_dup_ids = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="box1" value="A"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="120" height="60" />
        </mxCell>
        <mxCell id="box1" value="B"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="250" y="150" width="120" height="60" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        validator = DrawioValidator(xml_with_dup_ids)
        errors, warnings = validator.validate_all()

        dup_errors = [e for e in errors if "Duplicate" in e]
        assert len(dup_errors) > 0, "Should detect duplicate IDs"

    def test_container_missing_pointer_events(self) -> None:
        """Test that containers without pointerEvents=0 are warned."""
        xml_with_container = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="c1" value="Container"
          style="rounded=1;container=1;fontFamily=Noto Sans JP;fontSize=18;"
          vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="300" height="200" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        validator = DrawioValidator(xml_with_container)
        errors, warnings = validator.validate_all()

        container_warnings = [w for w in warnings if "pointerEvents" in w]
        assert len(container_warnings) > 0, "Should warn about missing pointerEvents=0"

    def test_swimlane_allows_no_pointer_events(self) -> None:
        """Test that swimlane containers do not require pointerEvents=0."""
        xml_with_swimlane = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="sw1" value="Service"
          style="swimlane;startSize=30;fontFamily=Noto Sans JP;fontSize=16;"
          vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="300" height="200" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        validator = DrawioValidator(xml_with_swimlane)
        errors, warnings = validator.validate_all()

        container_warnings = [w for w in warnings if "pointerEvents" in w]
        assert len(container_warnings) == 0, "Swimlane should not need pointerEvents=0"

    def test_node_spacing_too_close(self) -> None:
        """Test that nodes placed too close together are warned."""
        xml_close_nodes = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="Page-1" id="test">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="a" value="A"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" />
        </mxCell>
        <mxCell id="b" value="B"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
          <mxGeometry x="130" y="100" width="120" height="60" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
        validator = DrawioValidator(xml_close_nodes)
        errors, warnings = validator.validate_all()

        spacing_warnings = [w for w in warnings if "apart" in w]
        assert len(spacing_warnings) > 0, "Should warn about nodes too close together"


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
