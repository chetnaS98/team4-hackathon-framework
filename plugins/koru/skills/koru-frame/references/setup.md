# Frame setup: once, and at the start of a Frame stage

The shared scaffolding (the engagement folder, the read-me, the logs, the registers, the roles gate) is in `koru-core` (`koru-core/references/engagement.md`). This file is only what is specific to Frame.

## Contents
- Set up once, before the first Frame engagement
- Starting Frame in an engagement
- The two layers in one paragraph

## Set up once, before the first Frame engagement

Walk the user through this as a checklist. Ask which items are already done; do not assume. Items marked (needed at step 1) must exist before step 1 can start.

- [ ] **Knowledge base** (needed at step 1). Cloud storage (SharePoint or Google Drive) with prior research, access restricted to the team, connected to Jira, Confluence and similar tools. Client names are kept here.
- [ ] **Backlog converted.** Existing research converted to `.md` with front matter and naming (`product_workflow_content-type[-qualifier]_vN.md`). Originals kept. Use the markdown-research-formatter skill. Conversion is verbatim; nothing deleted, reworded, reordered or anonymised.
- [ ] **Formatter skill installed**, with its local output folder (and SharePoint folder if used) configured. **Check its `product`, `lifecycle` and `personas` values against Koru's projects**: the defaults are logistics values (rail, truck; plan, tender, execute, track, settle). If Koru's projects are not logistics, the team must decide the adapted values (see the Frame section of core's `defaults.md`).
- [ ] **koru-core installed** (this skill needs it).
- [ ] **Claude project template**: a project with the project-knowledge folders and the shared logs and registers, ready to copy per engagement; its instructions are core's block (`koru-core/references/project-instructions.md`).
- [ ] **Skills.** Existing third-party skills reviewed and installed (`references/existing-skills.md`).
- [ ] **Templates** for each Frame artefact type are in `assets/templates/`.
- [ ] **Shared output folder**: one folder per project with a sub-folder per stage.
- [ ] **Roles**: a pool of people for research owner, senior, developer and second-person checker (needed at step 1).
- [ ] **Reuse check**: find out what already exists at Koru before building anything new: the transcript clean-up skill, the Sense-Shape-Steer problem space and AI opportunity canvases, the shared research repository, and how research teams take in client calls.
- [ ] **Handbook**: the TRACES handbook (v2) is bundled in `references/traces-handbook.md`.

Output of this part: a short list of what is missing and who owns each gap. Offer to put it in a file.

## Starting Frame in an engagement

Ask the user for the inputs in one compact message, then run core's scripts.

1. **Project prefix** for file names (lowercase letters and digits, no hyphens; a code name, not the client's real name).
2. **Engagement size**, small or large (core's `governance.md`). If unsure, ask how many workflows, source files and stakeholder groups, propose a size, and log it.
3. **Named roles**: researcher, research owner, senior, developer, and the second-person checker pool. If two people share a name, record a surname or initial.
4. **Client decision makers** and the **review rhythm** (or "none set so far", which core's gate accepts but the default for a large engagement is a live review per sign-off).
5. **Knowledge base location** and whether Jira and Confluence connectors are reachable.
6. **Where the request material is** (to be converted at step 1).

Then:

```bash
python koru-core/scripts/init_engagement.py --project deskly --out <folder> --size small --client-alias "the client"
python koru-core/scripts/init_stage.py --engagement <folder>/deskly --stage-dir koru-frame
python koru-core/scripts/check_roles.py <folder>/deskly
```

Fill the roles and decision makers with the user, record the size and the "defaults accepted" lines in the decisions log, and re-run the gate. No step starts until it passes. Frame's working area is `stages/frame/` (drafts under `stages/frame/drafts/stage-*`, sources under `stages/frame/sources/`); its final folders are `01-framed-brief/` and `02-research/`.

**Upload rule.** Only `final` files belong in Claude project knowledge. After each sign-off, list exactly which files are ready to upload.

## The two layers in one paragraph

Layer 1 is the knowledge base: raw material converted verbatim to `.md`, no claims, source text only, names kept, restricted to the team. Layer 2 is the insights base: derived artefacts where every claim is a claim line, drafted by AI and checked by a person; drafts live in the output folder, finals in Claude project knowledge. Derived artefacts point back to Layer 1 through `src:` pointers and `derives_from`. That chain is what the stale-check follows.
