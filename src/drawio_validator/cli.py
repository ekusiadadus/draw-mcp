"""CLI entry point: draw-mcp-validate."""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from drawio_validator.output import format_json, format_text
from drawio_validator.preset import load_preset
from drawio_validator.rules import Mode
from drawio_validator.severity import Severity
from drawio_validator.validator import validate


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point. Returns exit code (0=ok, 1=errors found, 2=usage error)."""
    parser = argparse.ArgumentParser(
        prog="draw-mcp-validate",
        description="Validate draw.io XML files against quality rules",
    )
    parser.add_argument("files", nargs="+", type=Path, help="draw.io XML files to validate")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        default="warning",
        help="Minimum severity to report (default: warning)",
    )
    parser.add_argument(
        "--mode",
        choices=["loose", "standard", "strict", "production"],
        default="standard",
        help="Validation mode (default: standard)",
    )
    parser.add_argument(
        "--preset",
        type=Path,
        default=None,
        help="Path to a preset YAML file for validation profile checks",
    )

    args = parser.parse_args(argv)

    severity_map = {
        "error": Severity.ERROR,
        "warning": Severity.WARNING,
        "info": Severity.INFO,
    }
    min_severity = severity_map[args.severity]

    mode_map = {
        "loose": Mode.LOOSE,
        "standard": Mode.STANDARD,
        "strict": Mode.STRICT,
        "production": Mode.PRODUCTION,
    }
    validation_mode = mode_map[args.mode]

    # Load preset if specified
    preset = None
    if args.preset:
        preset = load_preset(args.preset)

    has_errors = False
    all_output: list[str] = []

    for filepath in args.files:
        if not filepath.exists():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            has_errors = True
            continue

        xml_content = filepath.read_text(encoding="utf-8")
        findings = validate(xml_content, mode=validation_mode)

        # Apply preset validation if specified
        if preset:
            from drawio_validator.preset import validate_against_preset

            try:
                root = ET.fromstring(xml_content)
                findings.extend(validate_against_preset(root, preset))
            except ET.ParseError:
                pass  # XML parse errors already captured by validate()

        error_findings = [f for f in findings if f.severity == Severity.ERROR]
        if error_findings:
            has_errors = True

        if args.format == "json":
            all_output.append(format_json(findings, min_severity))
        else:
            header = f"=== {filepath} ==="
            body = format_text(findings, min_severity)
            all_output.append(f"{header}\n{body}")

    print("\n".join(all_output))
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
