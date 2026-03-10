"""Orchestrator: runs all registered rules and provides backward-compatible API."""

import re
import xml.etree.ElementTree as ET
from typing import List, Tuple

import drawio_validator.rules.container  # noqa: F401
import drawio_validator.rules.edge  # noqa: F401
import drawio_validator.rules.export  # noqa: F401

# Import all rule modules to trigger registration
import drawio_validator.rules.structure  # noqa: F401
import drawio_validator.rules.style  # noqa: F401
import drawio_validator.rules.text  # noqa: F401
from drawio_validator.rules import get_all_rules
from drawio_validator.severity import Finding, Severity


def _check_double_hyphens(xml_content: str) -> List[Finding]:
    """Check for illegal double hyphens in XML comments before parsing."""
    findings: List[Finding] = []
    comment_pattern = re.compile(r"<!--(.*?)-->", re.DOTALL)
    for match in comment_pattern.finditer(xml_content):
        comment_body = match.group(1)
        if "--" in comment_body:
            findings.append(
                Finding(
                    rule_id="structure/xml-comments",
                    severity=Severity.ERROR,
                    message=(
                        "XML comment contains '--' which is illegal per XML spec. "
                        "Use single hyphens or rephrase."
                    ),
                )
            )
    return findings


def validate(xml_content: str) -> List[Finding]:
    """Run all validation rules and return list of Findings.

    This is the primary API for v2.0.
    """
    findings: List[Finding] = []

    # Pre-parse checks
    findings.extend(_check_double_hyphens(xml_content))

    # Parse XML
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        findings.append(
            Finding(
                rule_id="structure/xml-parse",
                severity=Severity.ERROR,
                message=f"XML parse error: {e}",
            )
        )
        return findings

    # Run all registered rules
    for rule_func in get_all_rules():
        findings.extend(rule_func(root))

    return findings


def validate_all(xml_content: str) -> Tuple[List[str], List[str]]:
    """Backward-compatible API returning (errors, warnings) as string lists.

    Delegates to validate() internally.
    """
    findings = validate(xml_content)
    errors = [f.message for f in findings if f.severity == Severity.ERROR]
    warnings = [f.message for f in findings if f.severity == Severity.WARNING]
    return errors, warnings
