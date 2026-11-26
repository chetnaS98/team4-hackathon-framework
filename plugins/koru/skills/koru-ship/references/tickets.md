# Tickets: template, splitting, acceptance criteria, delivery

A ticket is a Markdown artefact first. It is the source of truth; whatever lands in Jira or GitHub is a copy of a `final` ticket with the `koru-final` label. This works with no Jira or GitHub access at all.

## Contents
- The template
- How tickets are split
- Acceptance criteria rules
- How states, data, API assumptions and edge cases are described
- Screenshots
- Delivering tickets (no Jira access)
- Labels and the upload rule

## The template

File: `<project>-ship-ticket-<nn>-<slug>-v<n>-<status>.md` (for example `demo-ship-ticket-01-book-room-v1-draft.md`), type `ticket`, from `assets/templates/ticket.md`. The nine fields are level-2 headings, in this order and wording (`lint_ship.py` checks them):

| Field | What goes in |
|---|---|
| Title | Verb plus object ("Book a room from suggestions"). An optional `Priority:` line under it (Highest, High, Medium, Low, Lowest) |
| User story | As a [role], I want [thing], so that [outcome]. Add the story id: "(Story U1)" |
| Context | Three labelled links: `- Framed brief:`, `- Figma frame:`, `- HTML deliverable:` (the deliverable file with a `#step-N` anchor). Then "Relies on (data and API)": claim lines citing `feasibility` or `ship-notes` |
| Acceptance criteria | Given, when, then. One line each. Grouped under bold labels (Happy path, each state, Roles and permissions, AI behaviour, Edge cases, Data and API) |
| States covered | One line per state: `- <State>: <deliverable>.html#step-N-state-<state>`. Empty, Loading, Error and Success always (or `Not applicable: <reason>`), plus Partial, Stale and No permission where Harden has them, and every AI state the screens have |
| Screenshots | Anchors in the HTML deliverable (see "Screenshots") |
| Tokens used | Token names from the design library's `tokens.css` |
| Out of scope | What not to build from this ticket, including Ship notes closed as out of scope; or `None` |
| Open questions | `Q<n>: <question> (owner: <name>)` from the open-questions register; or `None` |

`Figma frame:` may read `not pasted: <reason>` when Harden handed on no Figma frame. Nothing else may be blank.

## How tickets are split

- **One ticket per user story.** The default, from the workbook. A story covers one or two journey steps of the one core flow.
- **3 to 5 tickets for one flow.** Fewer than 3 usually means a story hides two jobs; more than 5 means a second flow. A second flow is a second Ship pass with its own deliverable, logged.
- **A screen may appear in two tickets** (for example a list that a second story filters). Each ticket owns the states it changes; the other ticket links them, and says so under Out of scope.
- **Shared things are not a ticket of their own** unless an engineer asks: tokens and components belong to the ticket that first needs them; later tickets name them under Tokens used.
- **Ticket numbers** (`<nn>`) follow journey order, so `01` is the first thing the user does.

## Acceptance criteria rules

- One line each, in the form `- Given <context>, when <action>, then <result>.` One Given, one When, one Then per line. A criterion that needs "and then" is two criteria.
- Testable: a person or a test can say pass or fail without asking. No "should feel fast"; say the number Harden or the engineer gave, or raise an open question.
- Cover, for every screen in the ticket:
  1. **The happy path** through the story.
  2. **Every state** Harden defined (`states`): Empty, Loading, Error, Success, and Partial, Stale, No permission where they exist. A screen whose scope row has `Data from another system` other than `None` always has Partial (some data arrived, some did not). The state name appears in the criterion or in its bold label.
  3. **Every role permission** (`roles`): who can and cannot see, change, undo and approve; what a role that must not see something gets instead (No permission); what happens if a permission changes mid-flow; and, from "If the person who must act is away", what happens when an approver is away (delegate, or no delegate).
  4. **AI behaviour** (the AI touchpoints block in `states`): the trigger, AI thinking, low confidence, **what happens when the AI is wrong** (who sees it, who fixes it, how it is overridden or undone), and **the audit log line** from "Accepted suggestions audit-logged" (who accepted or changed what, when, where it is stored).
  5. **Edge cases** (`edge-cases`): long text, no data, a lot of data, double submit, slow or no network, concurrent edits, deleted or renamed items, permission removed, approver away with no delegate, session timeout mid-task, and each target viewport (smallest first, from scope's "Target viewports"), where they apply.
  6. **Data and API** (`feasibility`, `ship-notes`, scope's `Data from another system`): which system owns the data, freshness ("shows when it was last updated"), failure and retry, limits the engineer named.
- Only what Harden decided. A missing behaviour is an open question, not a guess.

## How states, data, API assumptions and edge cases are described

- **States** are described once, in the deliverable, and linked by anchor from the ticket. The ticket's criteria say what must be true in that state; the deliverable shows what it looks like. Copy in a criterion is the copy in the deliverable.
- **Data and API assumptions** are claim lines under Context, "Relies on (data and API)", each with a confidence and a `src:` to Harden's `feasibility` or `ship-notes` (core's traceable-line format). An assumption with no source goes in the assumptions register and the ticket names its `A` id.
- **Edge cases** are criteria under their own bold label, with the made-up sample data the deliverable uses (for example "a room name of 80 characters").
- **Accessibility** is covered by the rulebook and Harden's `accessibility` result; a ticket adds a criterion only where a screen needs something specific (focus order after an AI suggestion, for example).

## Screenshots

Tickets do not carry image files made up by the AI. The Screenshots field lists anchors in the HTML deliverable (`<deliverable>.html#step-2-state-error`). Each anchor shows exactly one state, so anyone can capture a screenshot from it: open the deliverable at the anchor in a browser and capture the visible state, or use a headless browser. If a person captures image files, save them as `07-ship/screenshots/<anchor>.png` and link them next to the anchor; `lint_ship.py` fails a ticket that links an image file that does not exist.

## Delivering tickets (no Jira access)

The team has no Jira access and the GitHub CLI may not be logged in, so delivery is a file anyone can carry.

```bash
python scripts/export_tickets.py --engagement <project>                  # finals only, into 07-ship/export/
python scripts/export_tickets.py --engagement <project> --status draft   # preview of drafts, into stages/ship/export-preview/
python scripts/export_tickets.py --engagement <project> --link-base https://host/path/deliverable.html
python scripts/export_tickets.py --engagement <project> --github owner/repo          # dry run
python scripts/export_tickets.py --engagement <project> --github owner/repo --yes    # creates issues (ask first)
```

- **`tickets.csv`** is in Jira's CSV import format: columns `Summary`, `Issue Type`, `Priority`, `Description`, `Labels`, `Labels`. The description is the full ticket body (every field after the title) in Jira wiki markup (`--format plain` keeps Markdown). Jira reads each `Labels` column as one label, so a final ticket carries `koru` and `koru-final`. Anyone with Jira imports all tickets at once: Jira settings, System, External system import, CSV (or a project's "Import issues"); map Summary, Issue Type, Priority, Description and both Labels columns. Ask them to import one ticket first if they have not used the importer before.
- **`tickets.md`** joins all tickets into one file to paste into any tool.
- **Links.** The deliverable is a local file, so its links only work next to it. Attach the HTML to the epic, or host it and pass `--link-base`, which rewrites `<deliverable>.html#anchor` links to `<url>#anchor`.
- **GitHub Issues (optional).** `--github owner/repo` runs `gh issue create` per ticket with the labels `koru` and `koru-final`. Without `--yes` it is a dry run that prints each command and writes the bodies to `export/github/`. It publishes outside the team, so ask the user in chat before ever passing `--yes`, showing the repo and the ticket list. It refuses `--yes` for non-final tickets. If `gh auth status` fails, it says how to log in (`gh auth login`) and the CSV stays the delivery.
- After import, the person gives you the keys or issue numbers; add one registry row per ticket with its `jira:` or `github:` pointer. Never invent one.

## Labels and the upload rule

Core's upload rule (`koru-core/references/integrity.md`): in Jira and GitHub, only items with the `koru-final` label count as source of truth. The export adds `koru-final` only to `final` tickets; drafts get `koru` alone and should not be imported except as a preview in a test project. When a final ticket gets a new version, export again and replace the copy; remove `koru-final` from the old one.
