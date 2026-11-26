# Team 4 Koru playbook: getting started

This repo holds our Koru delivery playbook as one Claude Code plugin, **koru**. It runs a client engagement through **Frame → Explore → Harden → Ship**. Claude drafts; named people check and sign off; only signed-off files become project knowledge.

## 1. Install (once, about 2 minutes)

You need Claude Code (desktop app Code tab, or the `claude` CLI) and Python 3.9+.

1. Get the repo and the plugin branch:
   ```bash
   git clone https://github.com/chetnaS98/team4-hackathon-framework.git
   cd team4-hackathon-framework
   git checkout koru/meridian-frame-setup
   ```
2. Open Claude Code in that folder and run:
   ```
   /plugin marketplace add ./
   /plugin install koru@team4-koru
   ```
3. Restart Claude Code. Type `/koru` and you should see `/koru:next`, `/koru:status`, `/koru:break`, `/koru:change`.

## 2. Run an engagement

Type **`/koru:next`**. That is the only command you need.

- **First time:** it asks four quick questions (design system: with, partial or without; existing research; size; where the client material is), then one message of names (team lead, context keeper, researcher, research owner, senior, developer, checkers). It sets the project up in `projects/<code name>/`, copies the material in unchanged and checks everyone is named.
- **Every time after:** it works out the next step, runs it with the right stage skill, and stops wherever a person has to check, decide or sign.
- **End of a stage:** it checks the handoff (all steps passed, sign-offs logged, nothing stale, handoff card filled) and asks the team lead to confirm by name before the next stage starts.

Other commands: `/koru:status` (where are we, changes nothing), `/koru:break` (log something that broke or needed a workaround), `/koru:change` (log a change to the playbook, with the reason).

## 3. Who does what

| Stage | Claude | People | Signs off |
|---|---|---|---|
| Frame | Converts the material, drafts the brief, TRACES, contradictions, research pack | Validate the path, answer as the client, check each draft | Senior (brief), research owner (pack) |
| Explore | Directions, 2 journeys, wireframes for Idea A and B, add-ons, Design v1 | Designer decides at 3 checkpoints, runs concept tests, pastes into Figma | Team lead (an organiser plays the client) |
| Harden | States, roles, edge cases, accessibility, tokens, hardened screens, rulebook checks | Engineer answers feasibility; fix, note or send back at checkpoint 2 | Engineer, rulebook owner, design lead |
| Ship | HTML deliverable, 3 to 5 tickets, handoff note | Engineer reviews and lists open questions | Engineer |

Reviewer agents give an independent read at four points: `evidence-auditor` (Frame 5 and 7), `feasibility-engineer` (Harden H3), `hardening-critic` (after H7), `handoff-reviewer` (Ship S6). They report; a person decides.

Interactive map of every step and who does it: ask Chetna for the "Koru Delivery Flow" page link.

## 4. Rules you'll bump into (they're enforced)

- **A step is passed only by a named checker** from the Roles table, never by the person who ran it.
- **Sources are never edited and finals are never overwritten.** Make the next version. A hook blocks it if you try.
- **Only `-final` files signed off in the decisions log go into the numbered final folders**, and only those go into Claude project knowledge. The **context keeper** uploads them.
- **The stale-check** flags anything built on an older version; a flagged file can't be signed off.
- **Frame's short route:** the team lead can skip or fold the slow Frame steps (new research, separate synthesis, the HTML summary). Each skip is logged with a reason.

## 5. No Jira access?

Ship writes each ticket as markdown in the workbook template, plus `tickets.csv` in Jira's import format (anyone with Jira imports it in one step) and a combined `tickets.md`. GitHub Issues are optional after `gh auth login`, and only created after you confirm.

## 6. Where things are

- `plugins/koru/`: the plugin (skills, agents, scripts, hooks, commands). Its `README.md` explains each part.
- `projects/<code name>/`: an engagement (kept out of git, because real projects hold client material).
- `framework/` and `.claude/skills/`: the team's earlier Frame pipeline and the markdown-research-formatter skill, which Frame uses to convert files.

Questions: ask in the team channel, or log a break with `/koru:break` so we fix the playbook.
