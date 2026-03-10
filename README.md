# draw-mcp — AI-Generated draw.io XML Quality Standard

A Claude Code skill and CLI validator for generating high-quality draw.io diagrams. 33 validation rules across 10 modules, 4 validation modes, preset system, and CI-ready tooling.

## Positioning

| Feature | draw-mcp | draw.io MCP Server | Mermaid.js |
|---------|----------|-------------------|-----------|
| Output | Native XML | Image/JSON | Text DSL |
| Layout control | Pixel-perfect | Auto-layout | Auto-layout |
| Japanese text | Full support | Limited | No control |
| Validation | 33 rules, 4 modes | None | Syntax only |
| Presets | YAML-based | None | None |
| Offline | Yes | Optional | Yes |
| Best for | Production diagrams | Quick previews | Simple flows |

**draw-mcp** is a Claude Code XML generation skill with strict validator and style guide. The official draw.io MCP server is complementary (use it for previews, Mermaid, CSV). draw-mcp focuses on **quality** for production diagrams.

## Supported Features

Features backed by validator rules, tests, and real examples:

- **33 Validation Rules** across 10 modules
- **4 Validation Modes**: loose, standard, strict, production
- **CLI Tool**: `draw-mcp-validate` with text/JSON output, severity filtering, and mode selection
- **Preset System**: YAML-based presets for flowchart and architecture diagrams
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
- Production mode preset compliance enforcement

## Non-Goals

Features explicitly out of scope:

- Hosted preview (use draw.io desktop or VS Code extension)
- Mermaid or CSV conversion (use official `jgraph/drawio-mcp`)
- Dark mode / lightbox runtime options
- Browser tab or editor orchestration
- Auto-layout (use draw.io's built-in layout engines)

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

# Validate a file (default: standard mode)
draw-mcp-validate diagram.drawio

# Specify validation mode
draw-mcp-validate diagram.drawio --mode strict

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

## Validation Modes

| Mode | Purpose | Rules |
|------|---------|-------|
| `loose` | Minimal parseability check | 5 structure rules |
| `standard` | Default development mode | + 17 style/edge/container/text/export |
| `strict` | PR and CI review | + 10 endpoint/escape/group/layer |
| `production` | Team-shared artifacts | All 33 rules |

## Validation Rules (33)

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

- **33 rules**: Added endpoint, escape, group, layer modules (up from 23)
- **4 validation modes**: loose, standard, strict, production
- **Preset system**: YAML-based presets for flowchart and architecture
- **Golden examples**: 5 real .drawio files with validation tests
- **Spec docs**: Formal specifications in docs/spec/
- **Claims coverage**: Tests verify README claims match implementation
- **CI fail-closed**: Removed `|| true` from validation steps
- **153+ tests** (up from 93)

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
