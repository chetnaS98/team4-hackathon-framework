# Spreadsheet (Excel/CSV)

`to_text.py` writes every sheet and row (one H2 per sheet, named as the sheet) as Markdown tables. No rows or columns are omitted or sampled, however large.

- Only mechanical changes: merged cells repeat their value, formulas appear as their stored values, `|` escaped, in-cell newlines as `<br>`. Mention these in the reply.
- Large data: split the extracted text at row boundaries (`head`/`tail`) into several files (~200 rows each, one qualifier per part, e.g. `survey-part2`), repeat the header row at the top of each part, and link parts via `related`. Validate each part against its own chunk as `--source`.
- Optional extras, clearly labelled and computed in code (never by hand): `## Column dictionary`, `## Summary` counts. Put them in `overview` or `notes`, never in place of data.
- Hidden sheets/rows are included; note that they were hidden.
- Embedded charts/images in a workbook: `extract_images.py` (xlsx media) and figure blocks after the sheet's table; chart data stays in the table, the figure transcription adds titles/axes/legend.
