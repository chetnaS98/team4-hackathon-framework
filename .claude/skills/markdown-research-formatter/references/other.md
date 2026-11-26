# Guide, deck, notes, persona

All four: extract with `to_text.py` and build verbatim. The source's wording, order, and structure are untouched.

- **Guide** (discussion guide, script, test plan): question wording, numbering, and probes exactly as written. `research_type` = the guide's intent.
- **Deck** (.pptx): `to_text.py` emits `## Slide N: <title>`, slide text, tables, speaker notes. Pictures/charts/diagrams: figure block (embedded image + **Transcription:**) after that slide's last text line, never replacing text; `extract_images.py` gives each image its `slide` number (use `--render-pages` when a chart or diagram is native shapes, not a picture). Mostly findings → `content_type: synthesis` (ask if unclear).
- **Guide/Notes/Persona with images** (screenshots, sketches, photos): same figure-block rule, placed where the image sits in the source.
- **Notes:** keep original phrasing and order; add headings only to mark existing topic shifts. No new claims.
- **Persona:** the persona doc as written; `personas` = this persona's kebab-case name.
