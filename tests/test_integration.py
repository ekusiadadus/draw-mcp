"""Integration tests using fixture files and the full validator pipeline."""

from drawio_validator.severity import Severity
from drawio_validator.validator import validate, validate_all


class TestValidFixtures:
    """Test that valid fixtures produce no errors."""

    def test_valid_minimal_no_errors(self, valid_minimal_xml: str) -> None:
        findings = validate(valid_minimal_xml)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_valid_edge_waypoint_no_errors(self, valid_edge_waypoint_xml: str) -> None:
        findings = validate(valid_edge_waypoint_xml)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_valid_swimlane_no_errors(self, valid_swimlane_xml: str) -> None:
        findings = validate(valid_swimlane_xml)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_valid_layer_no_errors(self, valid_layer_xml: str) -> None:
        findings = validate(valid_layer_xml)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0, f"Unexpected errors: {errors}"


class TestInvalidFixtures:
    """Test that invalid fixtures produce expected findings."""

    def test_duplicate_ids_detected(self, invalid_duplicate_ids_xml: str) -> None:
        findings = validate(invalid_duplicate_ids_xml)
        dup_errors = [
            f for f in findings if "duplicate" in f.message.lower() or "Duplicate" in f.message
        ]
        assert len(dup_errors) > 0, "Should detect duplicate IDs"

    def test_unescaped_html_warned(self, invalid_unescaped_html_xml: str) -> None:
        findings = validate(invalid_unescaped_html_xml)
        html_findings = [f for f in findings if f.rule_id == "text/html-escape"]
        assert len(html_findings) > 0, "Should detect dangerous HTML"

    def test_container_parenting_issues(self, invalid_container_parenting_xml: str) -> None:
        findings = validate(invalid_container_parenting_xml)
        container_findings = [f for f in findings if "container" in f.rule_id]
        assert len(container_findings) > 0, "Should detect container issues"

    def test_edge_geometry_missing_relative(self, invalid_edge_geometry_xml: str) -> None:
        findings = validate(invalid_edge_geometry_xml)
        edge_findings = [f for f in findings if f.rule_id == "edge/relative"]
        assert len(edge_findings) > 0, "Should detect missing relative=1"

    def test_style_typo_detected(self, invalid_style_typo_xml: str) -> None:
        findings = validate(invalid_style_typo_xml)
        typo_findings = [f for f in findings if f.rule_id == "style/typo"]
        assert len(typo_findings) > 0, "Should detect style typos"


class TestBackwardCompatibility:
    """Test backward-compatible validate_all() API."""

    def test_validate_all_returns_tuple(self, valid_minimal_xml: str) -> None:
        result = validate_all(valid_minimal_xml)
        assert isinstance(result, tuple)
        assert len(result) == 2
        errors, warnings = result
        assert isinstance(errors, list)
        assert isinstance(warnings, list)

    def test_validate_all_detects_errors(self, invalid_duplicate_ids_xml: str) -> None:
        errors, warnings = validate_all(invalid_duplicate_ids_xml)
        assert len(errors) > 0, "Should have errors for duplicate IDs"

    def test_validate_all_detects_warnings(self, invalid_container_parenting_xml: str) -> None:
        errors, warnings = validate_all(invalid_container_parenting_xml)
        assert len(warnings) > 0, "Should have warnings for container issues"

    def test_malformed_xml_returns_parse_error(self) -> None:
        errors, warnings = validate_all("<not-xml><<<")
        assert any("parse error" in e.lower() for e in errors)
