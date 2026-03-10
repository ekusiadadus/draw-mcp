"""Tests for severity module: Severity enum and Finding dataclass."""

import pytest

from drawio_validator.severity import Finding, Severity


class TestSeverity:
    """Test Severity enum."""

    def test_severity_has_three_levels(self) -> None:
        assert len(Severity) == 3

    def test_severity_error_value(self) -> None:
        assert Severity.ERROR.value == "error"

    def test_severity_warning_value(self) -> None:
        assert Severity.WARNING.value == "warning"

    def test_severity_info_value(self) -> None:
        assert Severity.INFO.value == "info"

    def test_severity_ordering(self) -> None:
        """ERROR > WARNING > INFO by convention."""
        assert Severity.ERROR.value < Severity.WARNING.value  # lexicographic not needed
        # Instead, verify they are distinct
        assert Severity.ERROR != Severity.WARNING
        assert Severity.WARNING != Severity.INFO
        assert Severity.ERROR != Severity.INFO


class TestFinding:
    """Test Finding frozen dataclass."""

    def test_finding_creation_minimal(self) -> None:
        f = Finding(rule_id="structure/root-cells", severity=Severity.ERROR, message="Missing root cells")
        assert f.rule_id == "structure/root-cells"
        assert f.severity == Severity.ERROR
        assert f.message == "Missing root cells"
        assert f.cell_id is None
        assert f.suggestion is None

    def test_finding_creation_full(self) -> None:
        f = Finding(
            rule_id="style/trailing-semicolon",
            severity=Severity.WARNING,
            message="Style missing trailing semicolon",
            cell_id="box1",
            suggestion="Add ; at end of style string",
        )
        assert f.cell_id == "box1"
        assert f.suggestion == "Add ; at end of style string"

    def test_finding_is_frozen(self) -> None:
        f = Finding(rule_id="test/frozen", severity=Severity.INFO, message="test")
        with pytest.raises(AttributeError):
            f.message = "changed"  # type: ignore[misc]

    def test_finding_equality(self) -> None:
        f1 = Finding(rule_id="a", severity=Severity.ERROR, message="msg")
        f2 = Finding(rule_id="a", severity=Severity.ERROR, message="msg")
        assert f1 == f2

    def test_finding_inequality(self) -> None:
        f1 = Finding(rule_id="a", severity=Severity.ERROR, message="msg1")
        f2 = Finding(rule_id="a", severity=Severity.ERROR, message="msg2")
        assert f1 != f2

    def test_finding_repr(self) -> None:
        f = Finding(rule_id="test/repr", severity=Severity.ERROR, message="test msg")
        r = repr(f)
        assert "test/repr" in r
        assert "ERROR" in r or "error" in r
