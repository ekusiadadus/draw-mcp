"""Preset loading, schema, and validation profile for diagram families."""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml

from drawio_validator.severity import Finding, Severity


@dataclass(frozen=True)
class Preset:
    """Defines safe defaults for a specific diagram family."""

    name: str
    default_font_family: str = "Noto Sans JP"
    default_font_size: int = 18
    min_node_spacing: int = 60
    default_vertex_style: str = "rounded=1;"
    default_edge_style: str = "edgeStyle=orthogonalEdgeStyle;"
    allowed_shapes: List[str] = field(default_factory=list)


def load_preset(filepath: Path) -> Preset:
    """Load a preset from a YAML file.

    Raises FileNotFoundError if the file does not exist.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Preset file not found: {filepath}")

    with open(filepath, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return Preset(
        name=data.get("name", filepath.stem),
        default_font_family=data.get("default_font_family", "Noto Sans JP"),
        default_font_size=data.get("default_font_size", 18),
        min_node_spacing=data.get("min_node_spacing", 60),
        default_vertex_style=data.get("default_vertex_style", "rounded=1;"),
        default_edge_style=data.get("default_edge_style", "edgeStyle=orthogonalEdgeStyle;"),
        allowed_shapes=data.get("allowed_shapes", []),
    )


def validate_against_preset(root: ET.Element, preset: Preset) -> List[Finding]:
    """Check cells against preset constraints (validation profile).

    This is the preset-as-validation-profile entry point.
    Intended for PRODUCTION mode or explicit --preset CLI usage.
    """
    findings: List[Finding] = []

    for cell in root.findall(".//mxCell"):
        value = cell.get("value", "")
        if not value:
            continue
        # Skip structural cells
        if cell.get("parent") == "0" and cell.get("vertex") != "1":
            continue

        style = cell.get("style", "")
        cell_id = cell.get("id", "unknown")

        # Check font family matches preset
        match = re.search(r"fontFamily=([^;]+)", style)
        if match:
            actual_font = match.group(1).strip()
            if actual_font != preset.default_font_family:
                findings.append(
                    Finding(
                        rule_id="preset/font-family",
                        severity=Severity.WARNING,
                        message=(
                            f"fontFamily='{actual_font}' does not match "
                            f"preset default '{preset.default_font_family}'"
                        ),
                        cell_id=cell_id,
                        suggestion=f"Use fontFamily={preset.default_font_family};",
                    )
                )

        # Check font size meets preset minimum
        size_match = re.search(r"fontSize=(\d+)", style)
        if size_match:
            actual_size = int(size_match.group(1))
            if actual_size < preset.default_font_size:
                findings.append(
                    Finding(
                        rule_id="preset/font-size",
                        severity=Severity.WARNING,
                        message=(
                            f"fontSize={actual_size} is below preset "
                            f"default {preset.default_font_size}"
                        ),
                        cell_id=cell_id,
                        suggestion=f"Use fontSize={preset.default_font_size};",
                    )
                )

        # Check allowed shapes (only if preset defines them)
        if preset.allowed_shapes:
            shape_match = re.search(r"shape=([^;]+)", style)
            if shape_match:
                actual_shape = shape_match.group(1).strip()
                if actual_shape not in preset.allowed_shapes:
                    findings.append(
                        Finding(
                            rule_id="preset/allowed-shape",
                            severity=Severity.WARNING,
                            message=(
                                f"shape='{actual_shape}' is not in preset "
                                f"allowed shapes: {preset.allowed_shapes}"
                            ),
                            cell_id=cell_id,
                            suggestion="Use an allowed shape for this preset",
                        )
                    )

    return findings
