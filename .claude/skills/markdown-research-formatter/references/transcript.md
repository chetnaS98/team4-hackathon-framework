# Transcript

Source stays line-for-line: speaker labels (incl. real names), filler, typos, timestamps, and product-name misspellings are all untouched. Get plain text via `to_text.py` (`.vtt/.srt/.txt` pass through unchanged; pasted chat text → write once to `src.txt` exactly as received).

- Sections: one topic each, ~300-700 words, starting at a speaker turn. Title in plain words; summary names the participant and topic.
- Overview holds the speaker key (e.g. "'Speaker 2' = office manager (S03)"), duration/format, and 2-3 sentences on coverage. Never guess identity; if unsure, say so and flag it.
- `both` research type: `## Discovery` and `## Design feedback` at level 2, topics at level 3.
- `notes` (optional "Moments of note"): only pain points, workarounds, tool names, exact numbers stated, each citing a timestamp or line. No interpretation.
- Very long transcripts stay one file unless the user asks to split; if so, split at section boundaries by line range.
- Screenshots/slides shared during the session (if provided as images): figure block at the moment they appear, tagged with the nearest timestamp in `title`.
