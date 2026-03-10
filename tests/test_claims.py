"""Tests for claims coverage: verify README claims are backed by rules and tests."""

from pathlib import Path

from drawio_validator.rules import Mode, get_rules_for_mode
from drawio_validator.validator import validate  # noqa: F401 — triggers rule registration

ROOT = Path(__file__).parent.parent


class TestClaimsCoverage:
    """Verify that key claims are backed by validator rules."""

    def test_structure_rules_exist(self) -> None:
        """Claim: structural validation (root cells, hierarchy, IDs)."""
        rules = get_rules_for_mode(Mode.LOOSE)
        rule_names = [r.__name__ for r in rules]
        assert "check_root_cells" in rule_names
        assert "check_hierarchy" in rule_names
        assert "check_unique_ids" in rule_names

    def test_style_rules_exist(self) -> None:
        """Claim: style validation (font, typos, booleans)."""
        rules = get_rules_for_mode(Mode.STANDARD)
        rule_names = [r.__name__ for r in rules]
        assert "check_font_family" in rule_names
        assert "check_style_typos" in rule_names
        assert "check_boolean_values" in rule_names

    def test_edge_rules_exist(self) -> None:
        """Claim: edge routing validation."""
        rules = get_rules_for_mode(Mode.STANDARD)
        rule_names = [r.__name__ for r in rules]
        assert "check_edge_relative" in rule_names
        assert "check_z_order" in rule_names

    def test_container_rules_exist(self) -> None:
        """Claim: container and swimlane validation."""
        rules = get_rules_for_mode(Mode.STANDARD)
        rule_names = [r.__name__ for r in rules]
        assert "check_pointer_events" in rule_names
        assert "check_swimlane_start_size" in rule_names

    def test_text_rules_exist(self) -> None:
        """Claim: Japanese text and font size validation."""
        rules = get_rules_for_mode(Mode.STANDARD)
        rule_names = [r.__name__ for r in rules]
        assert "check_japanese_width" in rule_names
        assert "check_font_size" in rule_names

    def test_endpoint_rules_at_strict(self) -> None:
        """Claim: endpoint semantic validation at STRICT."""
        rules = get_rules_for_mode(Mode.STRICT)
        rule_names = [r.__name__ for r in rules]
        assert "check_endpoint_validity" in rule_names
        assert "check_floating_edges" in rule_names

    def test_escape_rules_at_strict(self) -> None:
        """Claim: escape/security validation at STRICT."""
        rules = get_rules_for_mode(Mode.STRICT)
        rule_names = [r.__name__ for r in rules]
        assert "check_dangerous_tags" in rule_names

    def test_layer_rules_at_strict(self) -> None:
        """Claim: layer validation at STRICT."""
        rules = get_rules_for_mode(Mode.STRICT)
        rule_names = [r.__name__ for r in rules]
        assert "check_layer_structure" in rule_names
        assert "check_cross_layer_edges" in rule_names

    def test_group_rules_at_strict(self) -> None:
        """Claim: group validation at STRICT."""
        rules = get_rules_for_mode(Mode.STRICT)
        rule_names = [r.__name__ for r in rules]
        assert "check_group_detection" in rule_names
        assert "check_group_connectability" in rule_names

    def test_golden_examples_exist(self) -> None:
        """Claim: real .drawio example files exist."""
        examples = list((ROOT / "examples").glob("*.drawio"))
        assert len(examples) >= 4

    def test_mode_hierarchy(self) -> None:
        """Claim: modes form a strict hierarchy."""
        loose = len(get_rules_for_mode(Mode.LOOSE))
        standard = len(get_rules_for_mode(Mode.STANDARD))
        strict = len(get_rules_for_mode(Mode.STRICT))
        production = len(get_rules_for_mode(Mode.PRODUCTION))
        assert loose < standard <= strict <= production
