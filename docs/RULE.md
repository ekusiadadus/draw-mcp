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

# draw.io Skill Specific Rules

## XML Structure Rules

1. **Font Settings**
   - Set `defaultFontFamily` in `mxGraphModel`
   - Add `fontFamily=FontName;` to all text element styles
   - Recommended font size: 1.5x standard (18px)

2. **Arrow Placement**
   - Arrows must be placed at the back (first in XML order)
   - Labels must be at least 20px away from arrows
   - Use explicit coordinates for text element connections

3. **Text Element Sizing**
   - Allocate approximately 30-40px per Japanese character
   - Ensure sufficient width to prevent unintended line breaks

4. **PNG Conversion**
   - Always verify with PNG output
   - Use pre-commit hooks for automatic conversion
   - Scale factor: 2x for high resolution

## Commit Message Format

Follow Google's commit message style:
- Use present tense ("Add feature" not "Added feature")
- First line: summary under 50 characters
- Body: detailed description of what and why
