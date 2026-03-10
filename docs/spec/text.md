# Text Specification

## Font Family (MUST)

All cells with text content must specify `fontFamily` in their style.
Recommended: `fontFamily=Noto Sans JP;`

Missing `fontFamily` causes an ERROR at STANDARD mode.

## Font Size

| Level | Size | Severity |
|-------|------|----------|
| Minimum | 14px | ERROR if below |
| Recommended | 18px | WARNING if below |

## Japanese Text Width (SHOULD)

For Japanese (CJK) characters, allocate approximately 30px per character.
Cells with insufficient width receive a WARNING.

## HTML Escape Safety (STRICT)

When `html=1` is set, values are rendered as HTML.
Dangerous tags (`<script>`, `<iframe>`, `<object>`, `<embed>`, etc.)
are flagged as ERROR.

## Control Characters (STRICT)

Values should not contain raw control characters (except newline/tab).

## Validation Mode

- Font family: **STANDARD**
- Font size: **STANDARD**
- Japanese width: **STANDARD**
- HTML escape: **STANDARD** (text module) / **STRICT** (escape module)
- Dangerous tags: **STRICT**
- Control characters: **STRICT**
