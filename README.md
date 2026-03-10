# Claude Skill: draw.io Diagram Generator

A Claude Code skill for generating high-quality draw.io diagrams with proper font settings, arrow placement, edge routing, containers, and Japanese text support.

## Features

- **Font Management**: Ensures `fontFamily` is set on all text elements
- **Arrow Layering**: Correct Z-order placement (arrows behind boxes)
- **Edge Routing**: Node spacing, waypoints, connection point control, arrowhead spacing
- **Containers/Groups**: Swimlane, group, and custom container support with proper parent-child containment
- **Japanese Text Support**: Proper width allocation for CJK characters
- **XML Well-Formedness**: Validates `--` in comments, unique IDs, escape characters
- **PNG Validation**: Pre-commit hooks for automatic PNG generation
- **MCP Integration**: Compatible with official [draw.io MCP server](https://github.com/jgraph/drawio-mcp)
- **Best Practices**: Comprehensive checklist, 7 production-ready examples

## Installation

### Plugin Installation (Recommended)

```bash
# Via Claude Code marketplace
/plugin marketplace add ekusiadadus/draw-mcp

# Or install directly
/plugin add https://github.com/ekusiadadus/draw-mcp
```

### Manual Installation

Clone to your Claude Code skills directory:

```bash
# Global (personal use)
git clone https://github.com/ekusiadadus/draw-mcp ~/.claude/skills/draw-io

# Project-specific
git clone https://github.com/ekusiadadus/draw-mcp .claude/skills/draw-io
```

## Usage

Once installed, Claude Code will automatically use this skill when you ask to create draw.io diagrams.

### Example Prompts

```
Create a simple flowchart showing: Start -> Process -> End

Draw an architecture diagram with Web Server, API, and Database

Create a microservices diagram with swimlane containers

Create a sequence diagram for user login flow
```

### Manual Trigger

If needed, you can explicitly request the skill:

```
Using the draw-io skill, create a flowchart for the authentication process
```

## MCP Integration (Optional)

For inline previews or Mermaid.js support, use the official draw.io MCP server:

| Method | Best For | Setup |
|--------|----------|-------|
| **MCP App Server** | Inline previews in chat | Add `https://mcp.draw.io/mcp` as remote MCP server |
| **MCP Tool Server** | Desktop workflows | `npx @drawio/mcp` |
| **This Skill** | Code-based workflows with full control | See Installation above |

### Quick Decision Guide

| Need | Approach |
|------|----------|
| Custom styling, precise positioning, Japanese text | XML (this skill) |
| Flowchart, sequence, ER diagram | Mermaid.js via MCP |
| Inline preview in chat | MCP App Server |

## Requirements

### draw.io CLI (for PNG export)

**macOS:**
```bash
brew install --cask drawio
```

**Linux:**
Download from [draw.io Desktop Releases](https://github.com/jgraph/drawio-desktop/releases)

### Python (for tests and validation)

```bash
pip install pytest
```

## Project Structure

```
draw-mcp/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace configuration
├── skills/
│   └── draw-io/
│       ├── SKILL.md         # Main skill definition
│       ├── reference.md     # XML reference (edge routing, containers, etc.)
│       ├── examples.md      # 7 production-ready examples
│       └── checklist.md     # Validation checklist (9 categories)
├── scripts/
│   └── convert-drawio-to-png.sh
├── tests/
│   └── test_drawio_skill.py # 20 test cases
├── examples/
│   └── sample-flowchart.drawio
├── docs/
│   └── RULE.md
├── .pre-commit-config.yaml
├── .gitignore
├── LICENSE
└── README.md
```

## Key Rules

### 1. Font Settings

```xml
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
<mxCell style="...fontFamily=Noto Sans JP;fontSize=18;..." />
```

### 2. Arrow Placement (Z-Order)

Arrows must be declared FIRST in XML to render behind other elements.

### 3. Edge Routing

- Space nodes at least 60px apart (prefer 200px horizontal / 120px vertical)
- Use `exitX`/`exitY` and `entryX`/`entryY` to control connection sides
- Ensure 20px+ straight segment before target for arrowheads
- Add explicit waypoints where edges would overlap

### 4. Containers

```xml
<!-- Swimlane (titled container) -->
<mxCell style="swimlane;startSize=30;" vertex="1" parent="1">

<!-- Children use RELATIVE coordinates -->
<mxCell style="rounded=1;" vertex="1" parent="svc1">
```

### 5. Japanese Text Width

Allocate 30-40px per Japanese character.

### 6. XML Well-Formedness

- Never use `--` inside XML comments
- Escape special characters
- All IDs must be unique

### 7. PNG Verification

```bash
drawio -x -f png -s 2 -t -o diagram.png diagram.drawio
```

## Pre-commit Hooks

This project includes pre-commit hooks for:

1. **XML Validation**: Check font settings, structure, and well-formedness
2. **PNG Conversion**: Auto-generate PNG on commit
3. **Python Tests**: Run 20 skill validation tests

Setup:

```bash
pip install pre-commit
pre-commit install
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_drawio_skill.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE)

## Related Resources

- [draw.io Desktop](https://github.com/jgraph/drawio-desktop)
- [draw.io MCP Server (Official)](https://github.com/jgraph/drawio-mcp)
- [@drawio/mcp (npm)](https://www.npmjs.com/package/@drawio/mcp)
- [draw.io Style Reference](https://www.drawio.com/doc/faq/drawio-style-reference.html)
- [draw.io XSD Schema](https://www.drawio.com/assets/mxfile.xsd)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)

## Changelog

### v1.1.0 (2026-03-10)

- Edge routing best practices (node spacing, waypoints, connection points, arrowhead spacing)
- Container/group support (swimlane, group, custom containers with pointerEvents)
- XML well-formedness validation (double hyphens, unique IDs)
- Mermaid.js integration guide via official MCP server
- 2 new production-ready examples (container architecture, edge routing)
- 8 new test cases (20 total)
- Updated checklist with 9 validation categories
- Official draw.io style reference and XSD schema links
- Expanded troubleshooting table

### v1.0.0 (2025-12-16)

- Initial release
- Core skill with font, arrow, and text handling
- Pre-commit hooks for validation
- Comprehensive documentation and examples
