# Tokens and the design library (H11, H12)

The design library lives in `04-design-library/` (finals) and, when the team is ready, in a GitHub repo. Harden owns it; the rulebook owner signs it. Harden does not build a full library: it sets up the tokens file and a skeleton that Claude and Figma can both read, then fills what this flow needs.

## Contents
- With a design system
- Without a design system
- The library skeleton
- How Claude and Figma each read it
- Moving to GitHub

## With a design system

The read-me's design system path says "with DS" and links it; the design system has an artefact-registry row with a version.

1. **Tokens.** Copy the colour, type, spacing and radius tokens this flow uses from the design system into the `tokens` artefact. `Source` for each is the design system's registry pointer with its version (`figma:<key>/<node>@v3`, or the repo file). Do not rename them.
2. **Explore's gaps.** For each design system gap Explore listed (open-questions rows), propose one of: the closest existing component (and how it is used), a variant of an existing component, or a new component (name, purpose, states, which screens need it). The rulebook owner decides each; log the decision and close or update the open question.
3. **Screens (H12).** Use only design system components and tokens. A new component the rulebook owner approved is drawn and listed under "Design system gaps" as "new, approved, not yet in the design system", so Ship knows it must be built.
4. A change to the design system later flags the tokens and the screens through `derives_from`.

## Without a design system

The read-me says "without DS" (the internal wireframes Figma DS is linked). Explore's wireframes used the internal components; Harden must now make the design look like the real product.

1. **Tokens from Design v1.** Read the colours, type sizes, spacing and radii in Design v1's combined wireframe and turn them into named tokens. `Source` for each is the wireframe and the place it is used. If Design v1 has no clear value (for example only one grey), propose the missing ones, mark each `(proposed)` in `Use`, and have the rulebook owner agree them. Never fill a scale with invented values without saying so.
2. **Name by role, not by look:** `color-text`, `color-surface`, `color-primary`, `color-danger`, `space-1` to `space-6`, `radius-1`, `font-size-body`. This keeps the tokens usable when the theme changes.
3. **Contrast pairs.** List every text-on-background and control-on-background pair the screens use, then run `contrast_check.py`.
4. **Skeleton.** Set up the library skeleton below.
5. **Theme exploration** (choosing a visual style) belongs to Explore's tail if the designer started it; if not, Harden uses the tokens as derived and records that the theme is not final in the Ship notes.

## The library skeleton

```
04-design-library/
  <project>-harden-tokens-v<n>-final.md   the tokens artefact (signed)
  tokens.css                               written by export_tokens.py
  tokens.json                              written by export_tokens.py
  README.md                                how Claude and Figma each read it (below)
  components.md                            one line per component the flow uses: name, source, states, notes
```

`tokens.css` and `tokens.json` are generated, never hand-edited. Change the tokens artefact (new version), then re-run:

```bash
python koru-harden/scripts/export_tokens.py <tokens-artefact.md> --out <folder>
```

## How Claude and Figma each read it

Put this in the library's README, adapted:

- **Claude** reads `tokens.css` and links or inlines it in every HTML screen, and uses only the custom properties it defines (`var(--color-text)`). It reads `components.md` before building a screen and lists any component not in it as a gap.
- **Figma** gets the same values as variables: import `tokens.json` with a variables import plugin, or create the variables by hand from it, keeping the same names. When Claude Code pushes screens to Figma through MCP, the frames use those variables.
- **One source:** the tokens artefact. If someone changes a value in Figma, it is not real until the tokens artefact has a new version and the files are regenerated.

## Moving to GitHub

When the project has a repo, the design library moves there: `tokens.css`, `tokens.json`, `components.md` and the README, with the label `koru-final` on the release (core's upload rule). The tokens artefact stays in `04-design-library/` as the signed record and gains an `external_url` to the repo. Record the move in the decisions log.
