# Defaults register (Open and Proposed items), one section per stage

The source documents leave these undecided or proposed. So the skills can run end to end, they use the defaults below. At kickoff, tell the user once that the defaults exist, show the core section and the sections for the stages being started, and log "defaults accepted" (or any change) in the decisions log with stage `core`. If the team decides differently, edit this file; nothing else needs to change. A phase skill adds its own section here when it is built; it does not keep a separate defaults file.

## Contents
- Core
- Frame
- Explore
- Harden
- Ship

## Core

| Item | Status | Default used |
|---|---|---|
| Engagement size thresholds and review time boxes | Proposed (written for Frame) | Small: one workflow, about 10 or fewer source files, 1 or 2 personas; large: several workflows, more sources, or 3 or more stakeholder groups. Small: async comments within 1 working day, decision the next day; large: 45 to 60 minutes live. Each later phase must check and declare its own thresholds; until then use these and log it |
| How the client confirms | Open | Any of email, meeting or doc comment; always logged with who, date and channel |
| Who owns the AI quality log and who runs the stale-check | Open | The research owner owns the log and the stale-check. Run at session start, before sign-off, after any new source or version and after any send-back |
| `checked_by` field in front matter | Open | Not added. The checker is recorded in the step tracker and the decisions log |
| Who the developer is on a small engagement | Open | Ask at kickoff; record in `00-read-me-first.md` |
| The final-status marker for Figma, Jira and GitHub | Confirmed 25 Nov 2026 by the user | Figma: a section status named `Final`; Jira and GitHub: the label `koru-final` |
| Which later-stage roles each stage requires | Open | Each phase skill declares its required roles in `stage.json`; until then only Frame's are enforced |
| Sign-off signers and re-confirmation triggers for Explore, Harden and Ship | Open | Each phase defines its rows in `governance.md` before it asks for client confirmation of anything |
| Homes for Figma, GitHub and Jira artefacts in the "where things live" map | Proposed | As written in `file-protocol.md`; each phase confirms its own rows |

### Team rules set during use (core)

| Rule | Set | Applies to |
|---|---|---|
| All owners must be named, and `check_roles.py` must pass, before any step runs | 25 Nov 2026 by the user | Kickoff and every step |
| Shared rules, logs, naming, registers and integrity checks live once, in koru-core; phase skills point to it | 25 Nov 2026 by the user | All phases |

## Frame

| Item | Status in the source | Default used |
|---|---|---|
| How TRACES tags (fact, assumption, opinion) map to confidence levels | Open | Do not map. Use tags on calls, confidence levels in files. Never translate silently. The handbook also asks for a layer label per entry (data, finding, insight, belief); use it alongside the confidence level |
| Which file holds the problem space scope and the problem statement between steps 14 and 19 | Open | A single working draft file `[project]-frame-problem-space-v1-draft` (type `insight`, flagged in its description) in `drafts/stage-define/`; its content moves into brief section 1 at step 19 |
| Mode of the gap check (step 7) | Not yet assigned | AI-assisted |
| Does research pack v2 feed the one-page brief | Open (no arrow on the board) | Yes: the brief draws on the final pack |
| HTML summary required or optional | Open | Optional; offered at step 20 |
| How competitive-scan products are chosen | Open | You propose, the researcher confirms |
| What counts as a change to the problem statement or success outcomes (triggers client re-confirmation) | Open | Any change to the meaning of the problem, who it is for, the measure, or an outcome. Wording and layout edits do not count. When unsure, ask the senior |
| Whether a senior reviews every new brief version | Proposed | Yes |
| Formatter skill's `product`, `lifecycle`, `personas` values | Open | Ask the user at setup. If Koru's work is not logistics, agree adapted values before step 1 and note them in `00-read-me-first.md`. The formatter's validator may then need its enum checks ignored; record that |
| Project instructions, templates and remaining skills | To write | Templates are in each skill's `assets/templates/`; the project instructions block is in `references/project-instructions.md` |
| Board drawing of new steps, checkers, review, sign-offs, path decision, Explore return arrow | Open | Out of scope for the skills |

### Team rules set during use (Frame)

| Rule | Set | Applies to |
|---|---|---|
| Candidates graded High or Medium-high at step 3 are relevant and kept at step 4; Medium and lower are dropped unless the user asks | 25 Nov 2026 by the user | Steps 3 and 4 |

### Additions made by the Frame skill (not in the source document)

- A step tracker in the read-me so a later session can resume.
- Multiple sources on one line separated by `; `.
- The engagement folder layout, because the skills cannot write into Claude project knowledge.
- Scripts for engagement setup, linting, the stale-check and the roles gate (now in koru-core).
- Step 14b, Current platform review (team addition, 25 Nov 2026).
- A contradictions register kept from step 5.

## Explore

Context from the Explore source document ("explore-idea-generation") is in `stages.md`. These are inferences, listed so the team can confirm or change them.

| Item | Status | Default used |
|---|---|---|
| Explore's input file `frame.md` | Proposed | An export of the final framed brief and research pack index, generated (not hand-written), naming its versions and listed in `derives_from`; regenerated as a new version when a final Frame artefact changes |
| Required roles | Proposed | Designer, Design lead, second-person checker |
| Who checks Explore artefacts, given the designer confirms checkpoints | Proposed | The design lead (a second person) checks each artefact; the designer's checkpoint confirmation is not the check |
| Sharing Idea A and Idea B for feedback | Proposed | Only at `review` or `final` (core rule 6), after the second-person check |
| Sign-off rows and re-confirmation | Proposed | As in `governance.md`: the client confirms nothing in Explore; a change touching the brief's problem or success outcomes is a send-back to Frame |
| Size thresholds | Open | Not defined; Explore has a fixed shape. Until defined, use core's and log it |
| Number of directions | Proposed | At least two, 2 to 3 unless the designer asks otherwise (Frame's handoff says two direction cards) |
| Final folder number | Proposed | `06-explore/` |
| Artefact types | Proposed | direction, journey, wireframe, rationale, add-ons, insight-decisions, design |
| Design system gap list | Proposed | Recorded in the open-questions register (stage `explore`, blocking Harden) and handed to Harden |
| Who owns theme exploration and creating the design system when there is none (after Design v1) | Open | Not stated in the source document; not started unless the designer asks |
| Wireframe form | Proposed | Self-contained HTML with core front matter in a leading HTML comment |
| Internal "Stage 1 to 4" naming | Proposed | Renamed "Part 1 to 4" so "stage" means only Frame, Explore, Harden, Ship |

## Harden

No defaults yet. The Harden skill adds its section here when it is built. It owns reserved folders `03-rulebook/` and `04-design-library/`.

## Ship

No defaults yet. The Ship skill adds its section here when it is built.
