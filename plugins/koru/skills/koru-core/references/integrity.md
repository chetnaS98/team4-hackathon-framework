# Integrity checks: stale-check, lint, upload rule

## Contents
- The stale-check
- Running it
- The lint split
- The upload rule
- Rebuilding the artefact registry

## The stale-check

Every derived artefact says what it was built from in two ways: `derives_from` in its front matter (artefact names with version) and the `src:` pointer on every traceable line. It also records the date it was last checked (`last_checked`). Because sources and finals are never overwritten, a newer version of anything it points to is enough to show it is stale.

1. An artefact is **stale** when anything it derives from has a newer version, or has gone back to `review` or `draft` while the artefact is `final`.
2. **A pointer that matches nothing** is broken (reported, and treated as stale). A pointer to a non-file source that is not in the artefact registry is reported as unregistered: it cannot be checked.
3. A design system is a source like any other: register it (a Figma row with its pointer and version) and list it in `derives_from` of every artefact built on it, so a change to the design system flags them. Staleness **cascades across stages**, following `derives_from` and `src:`: a new source flags the insights built on it; a new brief version flags the direction cards built on it; a changed direction flags hardening; a changed design flags the tickets. Phases add their own links to the chain; the rule is the same.
4. An artefact **cannot be marked `final`** while it has open warnings.
5. The check lists the changed artefact and every affected one, in the order to revise them (sources first, the latest-stage artefacts last).
6. **Run it** at the start of a session, before any sign-off, after any new source or version, and after any send-back.
7. Claude cannot push alerts by itself, so the check is run by hand. A real push to Slack or Jira would need a scheduled task.

After every call or test round, insights and assertions are re-tagged confirmed, challenged, new or outdated. The new notes become a new source version and the check runs.

Do not clear a warning by editing `last_checked`. Revise the affected artefact (a new version if it was `final`), have it checked, then re-run. Overrides are a human decision, logged in the decisions log with a name and a reason.

## Running it

```bash
python scripts/stale_check.py --engagement <project> [--kb <knowledge-base-folder> ...]
```

- Reads every artefact with a `type:` in the engagement, Markdown and HTML (skipping templates and `superseded/`), the HTML and Markdown sources in `stages/*/sources/`, any `--kb` folders, and the **artefact registry** for things that are not files (a Figma frame, a ticket). Registry rows with a name that matches no file become nodes of their own, with their version, status and `Derives from`.
- Names that differ only in version (`_v2`, `-v2`, `-v2-final`) are one family.
- Exit 0 when clean, 1 when there are warnings. Output: changed or broken artefacts, cascade, and the order to revise.

## The lint split

**Core checks** (`scripts/lint_core.py`, run on every derived artefact in every phase):
- front matter present, with the required fields (`title`, `description`, `type`, `stage`, `status`, `version`, `last_checked`, `owner`);
- the file name matches `[project]-[stage]-[artefact]-v[n]-[status]`, and the stage, version and status in the name agree with the front matter;
- the type is registered for the stage;
- `derives_from` entries are well formed (`name-vN`);
- client names (via `--client-name`) do not appear in the body (source pointers are not checked);
- no leftover `TODO` or `<placeholder>` text when the status is `review` or `final`.

**Phase checks** stay with the phase skill. Frame's are in `koru-frame/scripts/lint_claims.py`: one assertion per line, the confidence and source rules, the `high` rule, `(inferred)` only on `low`, `src: none` not under a "known" heading, `--must-cite` for request sources, and the confidence counts.

Run core first, then the phase checks. Neither lint can judge whether a citation is accurate; the checker spot-checks sources.

## The upload rule

"Only `final` goes to project knowledge" stays. Each other home has an equivalent: a status marker that means final, and a rule that nothing unmarked is treated as source of truth.

| Home | What counts as final | Rule |
|---|---|---|
| Claude project knowledge | `status: final` in front matter and file name | Upload only `final` files |
| Figma | A section status named `Final` on the frame or section | Treat unlabelled frames as drafts; link only labelled frames in the registry as final |
| Jira | The label `koru-final` on the ticket | Build from tickets with the label only |
| GitHub | The label `koru-final` on the issue or PR (or on the release) | Use only labelled items as knowledge |

The Figma, Jira and GitHub markers were confirmed by the user on 25 Nov 2026 (`defaults.md`). After each sign-off, list exactly which artefacts are ready to move to their home and which stay as drafts, and tell the user to do the upload or labelling.

## Rebuilding the artefact registry

```bash
python scripts/build_registry.py --engagement <project>
```

Rewrites `artefact-registry.md` from the front matter of every derived artefact (name, stage, type, version, status, home, `derives_from`), keeps the manual columns (external link, pointer, signer) for rows that already exist, and leaves rows for non-file artefacts exactly as written. Run it after any new artefact or status change, and before the stale-check.
