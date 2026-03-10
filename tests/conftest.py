"""Shared fixtures for draw-mcp tests."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


def load_fixture(name: str) -> str:
    """Load a fixture file by name and return its content."""
    filepath = FIXTURES_DIR / name
    return filepath.read_text(encoding="utf-8")


@pytest.fixture
def valid_minimal_xml() -> str:
    return load_fixture("valid_minimal.drawio")


@pytest.fixture
def valid_edge_waypoint_xml() -> str:
    return load_fixture("valid_edge_waypoint.drawio")


@pytest.fixture
def valid_swimlane_xml() -> str:
    return load_fixture("valid_swimlane.drawio")


@pytest.fixture
def valid_layer_xml() -> str:
    return load_fixture("valid_layer.drawio")


@pytest.fixture
def invalid_duplicate_ids_xml() -> str:
    return load_fixture("invalid_duplicate_ids.drawio")


@pytest.fixture
def invalid_unescaped_html_xml() -> str:
    return load_fixture("invalid_unescaped_html.drawio")


@pytest.fixture
def invalid_container_parenting_xml() -> str:
    return load_fixture("invalid_container_parenting.drawio")


@pytest.fixture
def invalid_edge_geometry_xml() -> str:
    return load_fixture("invalid_edge_geometry.drawio")


@pytest.fixture
def invalid_style_typo_xml() -> str:
    return load_fixture("invalid_style_typo.drawio")
