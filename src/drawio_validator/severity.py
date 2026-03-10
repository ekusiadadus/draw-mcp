"""Severity levels and Finding dataclass for validation results."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Validation finding severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Finding:
    """An immutable validation finding.

    Attributes:
        rule_id: Dotted rule identifier, e.g. "structure/root-cells".
        severity: ERROR, WARNING, or INFO.
        message: Human-readable description.
        cell_id: Optional mxCell id related to this finding.
        suggestion: Optional fix suggestion.
    """

    rule_id: str
    severity: Severity
    message: str
    cell_id: Optional[str] = None
    suggestion: Optional[str] = None
