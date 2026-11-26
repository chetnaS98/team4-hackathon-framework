# Workflow map (flows, journey maps, FigJam/Miro, whiteboards)

Text exports (e.g. FigJam/Miro CSV, docx descriptions): extract with `to_text.py` and build verbatim like any text source.

Images/diagrams/whiteboards: embed the original **and** transcribe by hand. Run `extract_images.py` (step 4b), copy each image to `<LOCAL_OUT>/assets/<md-stem>_figNN.<ext>`, and put each under `## Source diagram` as a figure block (`![alt](assets/...)` + `**Transcription:**`) before the step-by-step table. Transcribe every node, label, arrow direction, swimlane, annotation, sticky, and colour legend exactly as written; nothing summarised or omitted. Multi-image boards: one figure block per image, in board order, each with its own transcription.

```
# <title>
*<context line>*
## Overview            who, trigger, outcome, systems (only what the source shows)
## Source diagram      figure block(s): embedded image + **Transcription:**
## Step-by-step        | # | Actor | System/tool | Action | Pain point / workaround |
## Decision points and exceptions
## Flow diagram        optional mermaid, convenience only; the table is the source of truth
```

- Keep source numbering; if absent, number in flow order and say so.
- Sticky exports: one H3 per cluster (title as given), one bullet per sticky, text unchanged.
- Unreadable → `[illegible: <where>]` and flag it. Never guess.
- Tell the user the content was read visually and needs a spot-check; the embedded image is the ground truth for it.
