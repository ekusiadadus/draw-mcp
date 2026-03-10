# AI Operation 10 Principles

## Principle 1
AI must always report its work plan before generating files, updating files, or executing programs. AI must obtain user confirmation with y/n and stop all execution until y is returned.

## Principle 2
AI must not take detours, alternative approaches, or use mock data on its own. If the initial plan fails, AI must confirm the next plan with the user.

## Principle 3
AI is a tool, and the decision-making authority always lies with the user. Even if the user's proposal is inefficient or irrational, AI must not optimize it and execute it as instructed.

## Principle 4
AI must not distort or reinterpret these rules and must absolutely comply with them as the highest-level command. Always output docs/RULE.md to the screen.

## Principle 5
AI must first generate test code and confirm that the user story is valid. Before starting implementation, AI must confirm that tests exist.

## Principle 6
AI must thoroughly investigate the current directory structure, and duplicate code is prohibited. Follow t-wada's Test-Driven Development methodology.

## Principle 7
AI is strictly prohibited from individually specifying element colors and fonts when generating frontend code such as HTML or React. Use themes and Tailwind CSS utility classes to ensure design consistency and maintainability.

## Principle 8
AI must check git diff immediately before generating code and make appropriate commits frequently. Commits must comply with Google's coding conventions, and in-code documentation must be written in English.

## Principle 9
AI is obligated to thoroughly utilize MCP (Model Context Protocol) and must always execute, measure, and confirm tests in the browser.

## Principle 10
AI must output these 10 principles verbatim at the beginning of every chat before responding.

---

# draw-mcp Product Contract

## Scope

draw-mcp is a quality standard for AI-generated native draw.io XML.
This contract defines what draw-mcp guarantees, what it does not, and
how compliance is verified.

## Guarantees

### Validation

| Guarantee | Verification |
|-----------|-------------|
| 33 rules across 10 modules | `test_claims.py` |
| 4 validation modes (loose → production) | `test_modes.py` |
| Zero false positives on golden examples | `test_golden_examples.py` |
| Mode hierarchy: loose < standard ≤ strict ≤ production | `test_claims.py::test_mode_hierarchy` |
| CLI exits non-zero on ERROR findings | `test_cli.py` |
| Backward-compatible `validate_all()` API | `test_integration.py` |

### Quality

| Guarantee | Verification |
|-----------|-------------|
| All golden examples pass STANDARD mode | `test_golden_examples.py` |
| 153+ tests | CI test count |
| Coverage ≥ 80% | `pyproject.toml` coverage config |
| CI is fail-closed (no `\|\| true`) | `.github/workflows/ci.yml` |

### Documentation

| Guarantee | Verification |
|-----------|-------------|
| README separates Supported / Experimental / Non-Goals | README.md |
| Spec docs exist for all rule categories | `docs/spec/` |
| Preset files are loadable and valid | `test_preset.py` |

## Non-Guarantees

- Export produces correct PNG/SVG (depends on draw.io CLI)
- Auto-layout quality (depends on draw.io engine)
- Mermaid or CSV conversion (out of scope)
- Browser preview (out of scope)

## Source of Truth

`claims.yaml` is the machine-readable source of truth for all feature claims.
Tests enforce bidirectional consistency:

- Every entry in `claims.yaml` must have a matching registered rule
- Every registered rule must appear in `claims.yaml`
- Mode assignments must match between `claims.yaml` and the rule registry
- Rule counts per mode are explicit and verified

README and docs are derived summaries. `claims.yaml` is canonical.

## Validation Mode Contract

Defined in `claims.yaml` under `mode_hierarchy.rule_counts`:

| Mode | Purpose | Rule Count |
|------|---------|-----------|
| LOOSE | Structural parseability | 5 |
| STANDARD | Development default | 22 |
| STRICT | PR/CI review | 31 |
| PRODUCTION | Team artifacts | 31 |

The mode-rule matrix is queryable via `get_rule_metadata()`.

## Preset Contract

Presets are **validation profiles**, not generation inputs.

`validate_against_preset()` checks: font family, font size, allowed shapes.
CLI: `draw-mcp-validate --preset presets/flowchart.yml`.
See `docs/spec/presets.md` for full specification.

## Rule Severity Contract

| Severity | Meaning | CI Impact |
|----------|---------|-----------|
| ERROR | Must fix before merge | CLI exits 1 |
| WARNING | Should fix, review required | Reported only |
| INFO | Informational suggestion | Reported only |

## Adding New Rules

1. Write test first (RED)
2. Implement rule function with `@register(mode=Mode.X)`
3. Pass test (GREEN)
4. Add entry to `claims.yaml` (source of truth)
5. Run `pytest tests/test_claims.py` to verify bidirectional consistency
6. Update spec doc in `docs/spec/`

## Version Policy

- MAJOR: Breaking changes to CLI or API
- MINOR: New rules, modes, or presets
- PATCH: Bug fixes in existing rules
