"""Preset loading and schema for diagram family defaults."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


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
