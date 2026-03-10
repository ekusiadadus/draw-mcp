# Export Specification

## Page Setting (SHOULD)

Set `page="0"` on `<mxGraphModel>` for transparent background export.
Default `page="1"` adds a visible page border.

## Embed Diagram (INFO)

When exporting to PNG or SVG, consider using `type="embed"` on
`<mxfile>` to embed the source diagram data in the exported file.
This makes the file portable and re-editable.

## Validation Mode

- Page setting: **STANDARD**
- Embed diagram: **STANDARD**
