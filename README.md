# Claude Skill: draw.io Diagram Generator

A Claude Code skill for generating high-quality draw.io diagrams with proper font settings, arrow placement, and Japanese text support.

## Features

- **Font Management**: Ensures `fontFamily` is set on all text elements
- **Arrow Layering**: Correct Z-order placement (arrows behind boxes)
- **Japanese Text Support**: Proper width allocation for CJK characters
- **PNG Validation**: Pre-commit hooks for automatic PNG generation
- **Best Practices**: Comprehensive checklist and examples

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

Create a sequence diagram for user login flow
```

### Manual Trigger

If needed, you can explicitly request the skill:

```
Using the draw-io skill, create a flowchart for the authentication process
```

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
│       ├── reference.md     # XML structure reference
│       ├── examples.md      # Production-ready examples
│       └── checklist.md     # Validation checklist
├── scripts/
│   └── convert-drawio-to-png.sh
├── tests/
│   └── test_drawio_skill.py
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
<!-- In mxGraphModel -->
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>

<!-- In EVERY text element -->
<mxCell style="...fontFamily=Noto Sans JP;fontSize=18;..." />
```

### 2. Arrow Placement

Arrows must be declared FIRST in XML to render behind other elements:

```xml
<root>
  <!-- Arrows first (background) -->
  <mxCell id="arrow1" edge="1" ... />

  <!-- Boxes after (foreground) -->
  <mxCell id="box1" vertex="1" ... />
</root>
```

### 3. Japanese Text Width

Allocate 30-40px per Japanese character:

```xml
<!-- 6 characters × 35px = 210px -->
<mxGeometry width="220" ... />
```

### 4. PNG Verification

Always export to PNG and verify visually:

```bash
drawio -x -f png -s 2 -t -o diagram.png diagram.drawio
```

## Pre-commit Hooks

This project includes pre-commit hooks for:

1. **XML Validation**: Check font settings and structure
2. **PNG Conversion**: Auto-generate PNG on commit
3. **Python Tests**: Run skill validation tests

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
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [draw.io XML Format Reference](https://www.diagrams.net/doc/faq/xml-format)

## Changelog

### v1.0.0 (2025-12-16)

- Initial release
- Core skill with font, arrow, and text handling
- Pre-commit hooks for validation
- Comprehensive documentation and examples
