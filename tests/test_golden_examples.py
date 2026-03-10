"""Tests for golden example .drawio files — each must pass validation."""

from pathlib import Path

import pytest

from drawio_validator.rules import Mode
from drawio_validator.severity import Severity
from drawio_validator.validator import validate

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def _example_files():
    """Collect all .drawio files from examples/."""
    return sorted(EXAMPLES_DIR.glob("*.drawio"))


class TestGoldenExamplesLoose:
    """All golden examples must pass LOOSE validation with zero errors."""

    @pytest.mark.parametrize("filepath", _example_files(), ids=lambda p: p.name)
    def test_no_errors_in_loose(self, filepath: Path) -> None:
        xml = filepath.read_text(encoding="utf-8")
        findings = validate(xml, mode=Mode.LOOSE)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0, f"{filepath.name}: {[e.message for e in errors]}"


class TestGoldenExamplesStandard:
    """All golden examples must pass STANDARD validation with zero errors."""

    @pytest.mark.parametrize("filepath", _example_files(), ids=lambda p: p.name)
    def test_no_errors_in_standard(self, filepath: Path) -> None:
        xml = filepath.read_text(encoding="utf-8")
        findings = validate(xml, mode=Mode.STANDARD)
        errors = [f for f in findings if f.severity == Severity.ERROR]
        assert len(errors) == 0, f"{filepath.name}: {[e.message for e in errors]}"


class TestGoldenExamplesCoverage:
    """Verify minimum set of golden examples exists."""

    def test_minimum_example_count(self) -> None:
        files = _example_files()
        assert len(files) >= 4, f"Expected at least 4 examples, found {len(files)}"

    def test_required_examples_exist(self) -> None:
        names = {f.name for f in _example_files()}
        required = {
            "flowchart-basic.drawio",
            "architecture-layered.drawio",
            "swimlane-process.drawio",
            "japanese-labels.drawio",
        }
        missing = required - names
        assert not missing, f"Missing required examples: {missing}"
