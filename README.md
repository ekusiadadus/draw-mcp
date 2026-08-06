# draw-mcp

**Generate and validate production-quality draw.io XML with Claude Code.**

draw-mcp combines a Claude Code skill with a CLI validator: 31 rules across 10 modules, four validation modes, reusable presets, and CI-ready output. It focuses on the structural and visual defects that syntax-only checks miss.

[Quick start](#quick-start) · [Validation rules](#validation-rules-31) · [Examples](./examples) · [Specifications](./docs/spec)

## Why draw-mcp?

AI can generate valid draw.io XML that is still difficult to edit or review: disconnected edges, invalid hierarchy, unsafe HTML, missing fonts, broken containers, and unreadable Japanese labels. draw-mcp turns those quality requirements into executable checks.

| Capability | draw-mcp | draw.io MCP Server | Mermaid.js |
|---|---|---|---|
| Output | Native draw.io XML | Image/JSON | Text DSL |
| Layout control | Explicit and editable | Auto-layout | Auto-layout |
| Validation | 31 structural and visual rules | None | Syntax only |
| CJK text checks | Yes | Limited | No layout control |
| Offline validation | Yes | Optional | Yes |
| Best fit | Production diagrams and CI | Fast previews | Simple diagrams |

The official draw.io MCP server remains complementary for previews, Mermaid, and CSV workflows. draw-mcp is the quality gate for diagrams that must remain editable and consistent.

## Quick start

### Install the Claude Code plugin

```text
/plugin marketplace add ekusiadadus/draw-mcp
/plugin add https://github.com/ekusiadadus/draw-mcp
```

Then ask Claude Code to create a diagram:

```text
Create an architecture diagram with application and infrastructure layers.
Validate it in strict mode before finishing.
```

### Install the CLI from GitHub

```bash
python -m pip install "git+https://github.com/ekusiadadus/draw-mcp.git"
draw-mcp-validate diagram.drawio --mode strict
```

For local development:

```bash
git clone https://github.com/ekusiadadus/draw-mcp.git
cd draw-mcp
python -m pip install -e ".[dev]"
pytest
```

The validator can also emit JSON for CI and automation:

```bash
draw-mcp-validate diagram.drawio --mode production --format json
```

## Supported Features

Features backed by validator rules, tests, and real examples:

- **31 Validation Rules** across 10 modules (defined in `claims.yaml`)
- **4 Validation Modes**: loose, standard, strict, production
- **CLI Tool**: `draw-mcp-validate` with text/JSON output, severity filtering, and mode selection
- **Preset System**: YAML-based presets as validation profiles (`--preset`)
- **Font Management**: Enforces `fontFamily` on all text elements
- **Edge Routing**: Z-order, relative geometry, arrowhead spacing, node spacing
- **Containers**: Swimlane, group, custom containers with pointer events
- **Layers**: Layer structure validation, cross-layer edge detection
- **Endpoint Semantics**: Source/target validity, floating/orphan edge detection
- **Security**: Dangerous HTML tag detection, control character validation
- **Japanese Text**: Width allocation for CJK characters
- **CI Integration**: GitHub Actions, pre-commit hooks, 153+ tests

## Experimental Features

Features documented but not deeply validated:

- Advanced routing heuristics (crossing density, edit tolerance)
- Custom connection-point presets
- PRODUCTION mode auto-detection of preset from example metadata

## Non-Goals

Features explicitly out of scope:

- Hosted preview (use draw.io desktop or VS Code extension)
- Mermaid or CSV conversion (use official `jgraph/drawio-mcp`)
- Dark mode / lightbox runtime options
- Browser tab or editor orchestration
- Auto-layout (use draw.io's built-in layout engines)

## Usage

Once installed, Claude Code uses this skill automatically for draw.io diagrams.

```
Create a simple flowchart showing: Start -> Process -> End
Draw an architecture diagram with swimlane containers
Create a layered diagram with infrastructure and application layers
```

## Validation Modes

| Mode | Purpose | Rule Count |
|------|---------|-----------|
| `loose` | Minimal parseability check | 5 |
| `standard` | Default development mode | 22 |
| `strict` | PR and CI review | 31 |
| `production` | Team-shared artifacts + preset compliance | 31 |

Rule counts are defined in `claims.yaml` and verified by CI.

## Validation Rules (31)

| Module | Rules | Mode | Default Severity |
|--------|-------|------|-----------------|
| **structure** | root-cells, hierarchy, vertex-edge-exclusivity, parent-reference, unique-ids | LOOSE | ERROR |
| **style** | trailing-semicolon, boolean-values, typo, font-family | STANDARD | Mixed |
| **edge** | z-order, relative, arrowhead-segment, node-spacing | STANDARD | Mixed |
| **container** | pointer-events, children-bounds, swimlane-start-size, collapsible | STANDARD | Mixed |
| **text** | japanese-width, html-escape, font-size | STANDARD | Mixed |
| **export** | page-setting, embed-diagram | STANDARD | Mixed |
| **endpoint** | source-validity, target-validity, floating-edge, orphan-edge | STRICT | Mixed |
| **escape** | control-chars, dangerous-tags | STRICT | Mixed |
| **group** | missing-container, connectability | STRICT | WARNING |
| **layer** | structure, cross-layer-edge | STRICT | WARNING |

## Project Structure

```
draw-mcp/
├── src/drawio_validator/          # Validator package
│   ├── __init__.py                # Version constant
│   ├── severity.py                # Severity enum, Finding dataclass
│   ├── validator.py               # Orchestrator with mode support
│   ├── output.py                  # Text/JSON formatters
│   ├── cli.py                     # CLI entry point
│   ├── preset.py                  # Preset loader
│   └── rules/                     # 10 rule modules
│       ├── __init__.py            # Mode enum, rule registry
│       ├── structure.py           # 5 rules (LOOSE)
│       ├── style.py               # 4 rules (STANDARD)
│       ├── edge.py                # 4 rules (STANDARD)
│       ├── container.py           # 4 rules (STANDARD)
│       ├── text.py                # 3 rules (STANDARD)
│       ├── export.py              # 2 rules (STANDARD)
│       ├── endpoint.py            # 3 rules (STRICT)
│       ├── escape.py              # 2 rules (STRICT)
│       ├── group.py               # 2 rules (STRICT)
│       └── layer.py               # 2 rules (STRICT)
├── skills/draw-io/                # Skill definition
│   ├── SKILL.md                   # Formal specification v2.0
│   ├── reference.md               # XML reference
│   ├── examples.md                # Production-ready examples
│   └── checklist.md               # Validation checklist
├── presets/                       # YAML preset definitions
│   ├── flowchart.yml
│   └── architecture.yml
├── docs/spec/                     # Formal specifications
│   ├── structure.md
│   ├── routing.md
│   ├── containers.md
│   ├── layers.md
│   ├── text.md
│   ├── export.md
│   └── non-goals.md
├── tests/                         # 153+ tests
│   ├── fixtures/                  # 9 XML fixture files
│   ├── test_structure.py
│   ├── test_style.py
│   ├── test_edge.py
│   ├── test_container.py
│   ├── test_text.py
│   ├── test_endpoint.py
│   ├── test_escape.py
│   ├── test_group.py
│   ├── test_layer.py
│   ├── test_modes.py
│   ├── test_preset.py
│   ├── test_golden_examples.py
│   ├── test_claims.py
│   ├── test_cli.py
│   ├── test_integration.py
│   ├── test_severity.py
│   └── test_drawio_skill.py       # Legacy tests
├── examples/                      # Golden .drawio files
│   ├── sample-flowchart.drawio
│   ├── flowchart-basic.drawio
│   ├── architecture-layered.drawio
│   ├── swimlane-process.drawio
│   └── japanese-labels.drawio
├── .github/workflows/ci.yml       # CI (fail-closed)
├── pyproject.toml                  # Build config (hatchling)
└── .pre-commit-config.yaml         # Pre-commit hooks
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

### v2.1.0 (2026-03-10)

- **31 rules**: Added endpoint, escape, group, layer modules (up from 23)
- **4 validation modes**: loose, standard, strict, production
- **claims.yaml**: Machine-readable source of truth for all feature claims
- **Mode-rule matrix**: Explicit rule counts per mode, verified by CI
- **Preset as validation profile**: `validate_against_preset()` + `--preset` CLI flag
- **Golden examples**: 5 real .drawio files with validation tests
- **Spec docs**: Formal specifications in docs/spec/ (incl. presets.md)
- **Bidirectional claims tests**: Registry ↔ claims.yaml consistency
- **CI fail-closed**: Removed `|| true` from validation steps
- **162+ tests** (up from 93)

### v2.0.0 (2026-03-10)

- **Validator overhaul**: 23 modular rules in 6 categories
- **CLI tool**: `draw-mcp-validate` with text/JSON output
- **Package**: `pyproject.toml` with hatchling build
- **SKILL.md v2.0**: Formal specification with MUST/SHOULD/INFO levels
- **Layers**: Full layer support
- **Test suite**: 93 tests at 96%+ coverage (up from 20 tests)
- **CI**: GitHub Actions with Python 3.10-3.13 matrix

### v1.1.0 (2026-03-10)

- Edge routing best practices
- Container/group support
- XML well-formedness validation

### v1.0.0 (2025-12-16)

- Initial release
