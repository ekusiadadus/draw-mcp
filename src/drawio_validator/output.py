"""Output formatters for validation findings."""

import json
from typing import List

from drawio_validator.severity import Finding, Severity


def format_text(findings: List[Finding], min_severity: Severity = Severity.INFO) -> str:
    """Format findings as human-readable text."""
    severity_order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
    threshold = severity_order.get(min_severity, 2)

    filtered = [f for f in findings if severity_order.get(f.severity, 2) <= threshold]
    if not filtered:
        return "No issues found."

    lines: List[str] = []
    for f in filtered:
        prefix = f.severity.value.upper()
        cell = f" [{f.cell_id}]" if f.cell_id else ""
        lines.append(f"  {prefix}{cell}: {f.message}")
        if f.suggestion:
            lines.append(f"    -> {f.suggestion}")

    error_count = sum(1 for f in filtered if f.severity == Severity.ERROR)
    warn_count = sum(1 for f in filtered if f.severity == Severity.WARNING)
    info_count = sum(1 for f in filtered if f.severity == Severity.INFO)

    summary = (
        f"\n{len(filtered)} issue(s): {error_count} error, {warn_count} warning, {info_count} info"
    )
    return "\n".join(lines) + summary


def format_json(findings: List[Finding], min_severity: Severity = Severity.INFO) -> str:
    """Format findings as JSON."""
    severity_order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
    threshold = severity_order.get(min_severity, 2)

    filtered = [f for f in findings if severity_order.get(f.severity, 2) <= threshold]

    data = {
        "findings": [
            {
                "rule_id": f.rule_id,
                "severity": f.severity.value,
                "message": f.message,
                "cell_id": f.cell_id,
                "suggestion": f.suggestion,
            }
            for f in filtered
        ],
        "summary": {
            "total": len(filtered),
            "errors": sum(1 for f in filtered if f.severity == Severity.ERROR),
            "warnings": sum(1 for f in filtered if f.severity == Severity.WARNING),
            "info": sum(1 for f in filtered if f.severity == Severity.INFO),
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False)
