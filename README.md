# draw-mcp — AI-Generated draw.io XML Quality Standard

A Claude Code skill and CLI validator for generating high-quality draw.io diagrams. 23 validation rules, strict specification, and CI-ready tooling.

## Positioning

| Feature | draw-mcp | draw.io MCP Server | Mermaid.js |
|---------|----------|-------------------|-----------|
| Output | Native XML | Image/JSON | Text DSL |
| Layout control | Pixel-perfect | Auto-layout | Auto-layout |
| Japanese text | Full support | Limited | No control |
| Validation | 23 rules, CI-ready | None | Syntax only |
| Offline | Yes | Optional | Yes |
| Best for | Production diagrams | Quick previews | Simple flows |

**draw-mcp** is a Claude Code XML generation skill with strict validator and style guide. The official draw.io MCP server is complementary (use it for previews, Mermaid, CSV). draw-mcp focuses on **quality** for production diagrams.

## Features

- **23 Validation Rules** across 6 categories (structure, style, edge, container, text, export)
- **CLI Tool**: `draw-mcp-validate` with text/JSON output and severity filtering
- **SKILL.md Specification v2.0**: Formal MUST/SHOULD/INFO rules
- **Font Management**: Enforces `fontFamily` on all text elements
- **Edge Routing**: Z-order, waypoints, connection points, arrowhead spacing
- **Containers/Layers**: Swimlane, group, custom containers, multi-layer support
- **Japanese Text**: Width allocation for CJK characters
- **CI Integration**: GitHub Actions, pre-commit hooks, 96%+ test coverage
- **8 Production Examples**: Flowcharts, architecture, containers, layers, edge routing

## Quick Start

### Plugin Installation

```bash
# Via Claude Code marketplace
/plugin marketplace add ekusiadadus/draw-mcp

# Or install directly
/plugin add https://github.com/ekusiadadus/draw-mcp
```

### Manual Installation

```bash
git clone https://github.com/ekusiadadus/draw-mcp ~/.claude/skills/draw-io
```

### CLI Validator

```bash
pip install -e ".[dev]"

# Validate a file
draw-mcp-validate diagram.drawio

# JSON output
draw-mcp-validate diagram.drawio --format json

# Errors only
draw-mcp-validate diagram.drawio --severity error
```

## Usage

Once installed, Claude Code uses this skill automatically for draw.io diagrams.

```
Create a simple flowchart showing: Start -> Process -> End
Draw an architecture diagram with swimlane containers
Create a layered diagram with infrastructure and application layers
```

## Validation Rules (23)

| Module | Rules | Default Severity |
|--------|-------|-----------------|
| **structure** | root-cells, hierarchy, vertex-edge-exclusivity, parent-reference, unique-ids | ERROR |
| **style** | trailing-semicolon, boolean-values, typo, font-family | Mixed |
| **edge** | z-order, relative, arrowhead-segment, node-spacing | Mixed |
| **container** | pointer-events, children-bounds, swimlane-start-size, collapsible | Mixed |
| **text** | japanese-width, html-escape, font-size | Mixed |
| **export** | page-setting, embed-diagram | Mixed |

## Project Structure

```
draw-mcp/
├── src/drawio_validator/          # Validator package
│   ├── __init__.py                # Version constant
│   ├── severity.py                # Severity enum, Finding dataclass
│   ├── validator.py               # Orchestrator
│   ├── output.py                  # Text/JSON formatters
│   ├── cli.py                     # CLI entry point
│   └── rules/                     # 6 rule modules
│       ├── structure.py           # 5 rules
│       ├── style.py               # 4 rules
│       ├── edge.py                # 4 rules
│       ├── container.py           # 4 rules
│       ├── text.py                # 3 rules
│       └── export.py              # 2 rules
├── skills/draw-io/                # Skill definition
│   ├── SKILL.md                   # Formal specification v2.0
│   ├── reference.md               # XML reference (layers, routing, containers)
│   ├── examples.md                # 8 production-ready examples
│   └── checklist.md               # Validation checklist (10 categories)
├── tests/                         # 93 tests, 96%+ coverage
│   ├── fixtures/                  # 9 XML fixture files
│   ├── test_structure.py
│   ├── test_style.py
│   ├── test_edge.py
│   ├── test_container.py
│   ├── test_text.py
│   ├── test_cli.py
│   ├── test_integration.py
│   ├── test_severity.py
│   └── test_drawio_skill.py       # Legacy tests (backward compatible)
├── .github/workflows/ci.yml       # GitHub Actions CI
├── pyproject.toml                  # Build config (hatchling)
├── .pre-commit-config.yaml         # Pre-commit hooks
└── examples/
    └── sample-flowchart.drawio
```

## MCP Integration (Optional)

| Method | Best For | Setup |
|--------|----------|-------|
| **MCP App Server** | Inline previews | `https://mcp.draw.io/mcp` |
| **MCP Tool Server** | Desktop workflows | `npx @drawio/mcp` |
| **This Skill** | Production diagrams with full control | See Installation |

## Requirements

- Python 3.10+
- pytest (for tests)
- draw.io CLI (for PNG export, optional)

```bash
# macOS
brew install --cask drawio

# Development setup
pip install -e ".[dev]"
pre-commit install
```

## Running Tests

```bash
# All tests with coverage
pytest tests/ -v --cov=drawio_validator --cov-report=term-missing

# Specific module
pytest tests/test_structure.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests first (TDD)
4. Implement to pass tests
5. Run: `pytest tests/ -v --cov=drawio_validator`
6. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE)

## Related Resources

- [draw.io Desktop](https://github.com/jgraph/drawio-desktop)
- [draw.io MCP Server (Official)](https://github.com/jgraph/drawio-mcp)
- [draw.io Style Reference](https://www.drawio.com/doc/faq/drawio-style-reference.html)
- [draw.io XSD Schema](https://www.drawio.com/assets/mxfile.xsd)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)

## Changelog

### v2.0.0 (2026-03-10)

- **Validator overhaul**: 23 modular rules in 6 categories (structure, style, edge, container, text, export)
- **CLI tool**: `draw-mcp-validate` with text/JSON output and severity filtering
- **Package**: `pyproject.toml` with hatchling build, `pip install -e ".[dev]"`
- **SKILL.md v2.0**: Formal specification with MUST/SHOULD/INFO levels
- **Layers**: Full layer support in reference, examples, and checklist
- **Test suite**: 93 tests at 96%+ coverage (up from 20 tests)
- **CI**: GitHub Actions with Python 3.10-3.13 matrix, linting, coverage
- **Pre-commit**: CLI-based validator replaces inline Python
- **8 examples**: Added layer diagram example
- **Positioning**: Clear complementary relationship with official MCP server

### v1.1.0 (2026-03-10)

- Edge routing best practices
- Container/group support
- XML well-formedness validation
- Mermaid.js integration guide
- 20 test cases

### v1.0.0 (2025-12-16)

- Initial release
