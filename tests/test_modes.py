"""Tests for validation modes: loose, standard, strict, production."""

import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from drawio_validator.rules import Mode, get_rule_metadata, get_rules_for_mode
from drawio_validator.severity import Severity
from drawio_validator.validator import validate

CLAIMS_PATH = Path(__file__).parent.parent / "claims.yaml"


VALID_MINIMAL = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="P" id="d1">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="a" value="Test"
          style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
          vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""


class TestMode:
    def test_mode_enum_has_four_levels(self) -> None:
        assert len(Mode) == 4

    def test_mode_values(self) -> None:
        assert Mode.LOOSE.value == "loose"
        assert Mode.STANDARD.value == "standard"
        assert Mode.STRICT.value == "strict"
        assert Mode.PRODUCTION.value == "production"


class TestGetRulesForMode:
    def test_loose_returns_subset(self) -> None:
        loose_rules = get_rules_for_mode(Mode.LOOSE)
        standard_rules = get_rules_for_mode(Mode.STANDARD)
        assert len(loose_rules) > 0
        assert len(loose_rules) <= len(standard_rules)

    def test_standard_returns_more_than_loose(self) -> None:
        loose_rules = get_rules_for_mode(Mode.LOOSE)
        standard_rules = get_rules_for_mode(Mode.STANDARD)
        assert len(standard_rules) >= len(loose_rules)

    def test_strict_returns_more_than_standard(self) -> None:
        standard_rules = get_rules_for_mode(Mode.STANDARD)
        strict_rules = get_rules_for_mode(Mode.STRICT)
        assert len(strict_rules) >= len(standard_rules)

    def test_production_returns_all(self) -> None:
        strict_rules = get_rules_for_mode(Mode.STRICT)
        prod_rules = get_rules_for_mode(Mode.PRODUCTION)
        assert len(prod_rules) >= len(strict_rules)


class TestValidateWithMode:
    def test_validate_loose_valid_file(self) -> None:
        findings = validate(VALID_MINIMAL, mode=Mode.LOOSE)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_validate_standard_valid_file(self) -> None:
        findings = validate(VALID_MINIMAL, mode=Mode.STANDARD)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_validate_default_is_standard(self) -> None:
        default_findings = validate(VALID_MINIMAL)
        standard_findings = validate(VALID_MINIMAL, mode=Mode.STANDARD)
        assert len(default_findings) == len(standard_findings)

    def test_loose_skips_style_checks(self) -> None:
        xml_no_font = """<mxfile><diagram name="P" id="d1"><mxGraphModel><root>
            <mxCell id="0"/><mxCell id="1" parent="0"/>
            <mxCell id="a" value="X" style="rounded=1;" vertex="1" parent="1"/>
        </root></mxGraphModel></diagram></mxfile>"""
        loose = validate(xml_no_font, mode=Mode.LOOSE)
        standard = validate(xml_no_font, mode=Mode.STANDARD)
        loose_errors = [f for f in loose if f.severity == Severity.ERROR]
        standard_errors = [f for f in standard if f.severity == Severity.ERROR]
        # loose should have fewer errors (no fontFamily check)
        assert len(loose_errors) < len(standard_errors)


class TestModeRuleMatrix:
    """Verify the mode-rule matrix is explicit and queryable."""

    def test_get_rule_metadata_returns_all(self) -> None:
        metadata = get_rule_metadata()
        assert len(metadata) == len(get_rules_for_mode(Mode.PRODUCTION))

    def test_metadata_has_required_fields(self) -> None:
        metadata = get_rule_metadata()
        for entry in metadata:
            assert "func_name" in entry
            assert "min_mode" in entry

    def test_metadata_matches_claims_yaml(self) -> None:
        """Every entry in get_rule_metadata must match claims.yaml."""
        with open(CLAIMS_PATH, encoding="utf-8") as f:
            claims = yaml.safe_load(f)
        claims_by_func = {r["func"]: r for r in claims["rules"]}
        metadata = get_rule_metadata()
        for entry in metadata:
            func_name = entry["func_name"]
            assert (
                func_name in claims_by_func
            ), f"Rule '{func_name}' in registry but not in claims.yaml"
            assert entry["min_mode"] == claims_by_func[func_name]["min_mode"], (
                f"Rule '{func_name}' mode mismatch: "
                f"registry={entry['min_mode']}, claims={claims_by_func[func_name]['min_mode']}"
            )

    def test_no_rule_registered_without_explicit_mode_assignment(self) -> None:
        """All rules must have a mode explicitly documented in claims.yaml."""
        with open(CLAIMS_PATH, encoding="utf-8") as f:
            claims = yaml.safe_load(f)
        claimed_funcs = {r["func"] for r in claims["rules"]}
        metadata = get_rule_metadata()
        for entry in metadata:
            assert entry["func_name"] in claimed_funcs
