# Step playbook: the 24 steps

Read the entry for the current step before running it. Every entry gives: mode, what to do, output, checker, exit test. The general loop (announce, do, write, hand to checker, record, move on) is core's (`koru-core/SKILL.md`). Every AI output starts as `draft`. Every claim is a claim line (core's `file-protocol.md`, "Traceable lines"). Add each new assumption to core's assumptions register and each question for the client to the open-questions register.

Modes: **AI-led** (AI does, a person checks), **Human-led** (a person does), **AI-assisted** (AI drafts, a person judges).

## Contents
- Steps 1 to 7: intake, first brief, related material, TRACES, pack v1, gap check
- Steps 8 to 10: research and conversion
- Steps 11 to 13: synthesis, insights, personas
- Steps 14 to 15a: problem space, competitive scan, current platform review (14b), workflows and JTBDs, constraints
- Steps 16 to 18a: pack v2, opportunities, success
- Steps 19 to 20: brief and HTML summary

---

## 1. Request, brief or transcript arrives (human-led)

- **Human does:** receives the client material and gets it converted to source `.md` (the formatter skill does the conversion straight away; invoke it, do not retype text).
- **You do:** confirm what arrived, point to the formatter skill, and check the result has front matter, the right filename, and that the original is kept. Offer the formatter's validator output as evidence.
- **Request material list.** Ask the user which converted sources are "the request": everything the client handed over or said to open the work. That means the written brief, any requirements doc **and any kickoff or client call transcripts**. Everything else (other calls with client staff about specifics, interviews, analytics, tickets, architecture, earlier synthesis) is related material for steps 3 and 5. Propose the split, get a yes, and record the list in the progress tracker (row 1) and in `00-read-me-first`. If a transcript's status is unclear, treat it as request material and ask.
- **Output:** source `.md` in the knowledge base (and a copy in `sources/`).
- **Checker:** the person doing it. **Exit:** every item has a source `.md` and an untouched original, and the request material list is recorded.

## 2. Client-based brief v1 (AI-led)

- **You do, before drafting:** read **every** source on the request material list in full, start to finish, including transcripts. Reading only the written documents is the mistake that was made on the first Meridian run (the kickoff call transcript was skipped). Keep a coverage list (file, read yes/no, used in which sections) and show it to the user with the draft. After drafting, run `koru-core/scripts/lint_lines.py --must-cite <name>` for each request source; it fails if any source is never cited.
- **Then:** draft brief v1 from the request material only, using `assets/templates/brief.md`. Transcripts give stakeholder positions, quotes and disagreements: attribute them by role (not by name), and record disagreements between stakeholders as claim lines and open questions, not as a resolved fact. Reproduce every enumerated list in the sources in full (see `brief.md`). Put nothing between the title and section 1.
- Give the request a provisional path label from its wording (roadmap or discovery) and write the hypothesis or question as one sentence. Fill each section only from the source. Write every fact as a claim line. Move anything without a source to What we're assuming. List open questions for the client. A section the request cannot fill says "not yet known". Do not search the knowledge base (step 3), do not draft success outcomes (step 18a), do not invent numbers.
- **Output:** `[project]-frame-brief-v1-draft` in `drafts/stage-brief/`.
- **Checker:** a researcher who did not run it. **Log:** the provisional path in the decisions log. **Exit:** checker passes; lint clean.
- Note: the spec calls for a skill named `frame-client-brief-v1`. Until it exists, this step is that skill's spec, run inline.

## 3. Identify what in the knowledge base relates (AI-led)

- **You do:** search the `.md` knowledge base (and connected tools if reachable) for material related to the brief: same product, workflow, persona, customer, problem. Return a candidate list: file, why it might be related, and what it would answer. Do not judge relevance beyond a first guess; step 4 does that.
- **Grade every candidate** High, Medium-high, Medium or Low (first guess, with a one-line reason and what it could answer). Grade by how directly the file bears on the brief's claims, assumptions, constraints and open questions. Transcripts, data exports (with their column notes), support tickets, constraints notes, architecture maps and earlier synthesis that touch the request are High or Medium-high; design-system assets and process documents are Low. **The current product of the thing being replaced or changed** (a clickable mock, screenshots, a demo, a walkthrough) is High: it is the only direct evidence of what exists today (TRACES clue +2). Do not grade it Medium because it is not research. List the lower-graded files too, so nothing is hidden.
- **Output:** candidate related files list. **Checker:** step 4 (the human validation is the check). **Exit:** list handed to step 4.
- If the knowledge base is not reachable, say so and ask the user to paste or point to files; never pretend to have searched.

## 4. Validate relevance and confirm the path (human-led)

- **Human does:** validates that each candidate is relevant to this problem, and answers: does validated research exist on this exact problem?
- **Standing team rule (set 25 Nov 2026):** treat every candidate graded **High or Medium-high** as relevant and keep it, without asking one by one. Medium and Low are dropped unless the user says otherwise; still list them and say they were dropped by the rule, so the user can pull one back in. Companion files count with their main file (for example an export and its column notes).
- **You do:** show the kept and dropped lists, record them, and ask the path question plainly (the user still decides it). Roadmap if yes, discovery if no or only other modules.
- **Output:** validated set and confirmed path. **Log:** path confirmed (or switched) in the decisions log, with who and the alternative. **Exit:** path logged.

## 5. Pull related material and answer TRACES (AI-led)

- **You do:** pull the validated material (storage, Jira, Confluence where connected) and answer TRACES for both sides: the request and the workflow underneath it. Every answer is claim lines. An unanswered letter becomes a question or a stated assumption, never filler.
- **Count sources honestly.** Two files from the same interviews are one source; documents written by the same person (for example an engineering lead's notes, architecture file and call) are one source. A claim is high only with two independent sources or direct data tagged `(data)`/`(observed)`. Recompute every number you quote (totals, shares) from the source rows, and re-open the source for any claim you are unsure of before handing over. Put a section called "Where the sources disagree" and one called "What TRACES could not answer" at the end. Also start the contradictions register (see `file-specs.md`, "The contradictions register"), including the requirements document against the evidence, and compare numbers and definitions, not only opinions.
- **Use the bundled TRACES handbook (`references/traces-handbook.md`)**: read sections 2 to 4b and 16 before answering. Fill each letter twice, once for the request and once for the workflow (section 3), and weight the side the handbook says to for the path (discovery = fresh start = weight the workflow). For each letter, test it against the handbook's "You have X when you can write" sentence (section 4b); where you cannot write it, that is an open question, not a gap to fill. Add the three extras: constraints, existing product and design system, and what has been tried (section 5). Label what layer each entry came from, data, finding, insight or stakeholder belief (section 16); only insights can carry a design direction. Ask "can we talk to them?" under Audience and record the answer or the gap. Check the red flags per letter.
- **Name:** `[project]-frame-insight-traces-v1-draft` (type `insight`), in `drafts/stage-research/`. Step 6 folds it into the pack as links, it does not copy it.
- **Independent audit.** Before handing to the checker, launch the `koru:evidence-auditor` agent on the engagement folder. It reads the sources and your drafts cold and writes an evidence-audit insight. Fold what it finds into the TRACES answers and the contradictions register (a new version), log anything it caught in the AI quality log, and give the research owner both files.
- **Output:** TRACES answers (they live in research pack v1). **Checker:** research owner. **Exit:** checker passes; lint clean; no claim without a source in a "known" position.

## 6. Research pack v1 (AI-led)

- **You do:** assemble everything that fills TRACES into `assets/templates/research-pack.md`: TRACES answers, links to the files used (pinned by version), open questions, a count of high, medium and low claims (compute with `koru-core/scripts/lint_lines.py --count`). The pack is a thin index, not a copy.
- **Output:** research pack v1 `draft`. **Checker:** research owner. **Exit:** checker passes.

## 7. Gap check: what is left to know and validate (mode not yet assigned)

- Default used here: AI-assisted (see the Frame section of `koru-core/references/defaults.md`). Tell the user this is an open decision and that you are using that default.
- **You do:** compare the pack against the requirement and the TRACES checklist. List the unknowns: assumptions to test and open questions for the client. Re-check the path (it may switch; log it).
- **Re-audit.** Run the `koru:evidence-auditor` agent again on the pack draft; its "People missing from the personas" and "Claims the data doesn't support" lists feed the gap list.
- **Ask the client.** Collect the open questions only the client can answer into one short list, most important first, each with the role that should answer and why it matters. A person asks them (on the hackathon an organiser answers as the client). Save the answers verbatim as a new source, `stages/frame/sources/<project>_client-answers_vN.md` (who answered, date), never paraphrased into the brief directly. Then run the stale-check: the brief and pack items the answers touch get a new version. Unanswered questions stay in the open-questions register.
- **Output:** list of unknowns, the client questions and the answers source. **Checker:** research owner. **Decision:** roadmap path: fill only these gaps or skip step 8; discovery path: full loop. **Exit:** the gap list is agreed, the client questions are asked or logged as open, and the step 8 plan is chosen.

## 8. Research phase (human-led)

- **Human does:** new primary research, scaled to the path. Offer a short plan only if asked (the research-protocol skill is not part of Frame's table; see `existing-skills.md`). Do not invent research.
- **Output:** new research material. **Exit:** the user confirms what was gathered and what was not (and why).

## 9. Transcripts and secondary research files (human-led)

- **Human does:** gathers the raw files. **You do:** list what is expected from the step 7 gap list and track what has arrived. **Exit:** all expected files in hand, or the missing ones recorded as open questions.

## 10. Clean and convert to .md (AI-led)

- **You do:** convert verbatim with the formatter skill (front matter and file name). Never retype source text. Run its validator with the source text so unaltered content is proven, not assumed.
- **Output:** source `.md` in the knowledge base. **Checker:** a second person confirms front matter and sections; the validator proves the text is unaltered. **Log:** any mistake caught goes in the AI quality log (for example a dropped speaker label). **Exit:** after any new source, run the stale-check.

## 11. Synthesis (AI-assisted)

- **You do:** draft a synthesis across the sources (use `affinity-diagram` thinking: cluster observations bottom-up into themes, tag each observation with its participant or source, flag single-source patterns). Every statement a claim line. Roadmap path: short; does the evidence support or contradict what the client arrives with? Discovery path: full.
- **Output:** synthesis `draft`. **Checker:** researcher. **Exit:** checker passes.

## 12. Insights and themes (AI-assisted)

- **Use the handbook** (`traces-handbook.md` sections 11 to 14): data, finding and insight are different layers; an insight is what happened plus why plus so what, with an opportunity; one person's comment is a hypothesis. State which layer each line is.
- **You do:** turn the synthesis into an insight file: one insight per line, each explaining what happened, why, and so what, each a claim line with confidence. Do not promote a single-source finding to `high`. Design directions live here and only here.
- **Output:** `[project]-frame-insight-[topic]-v1-draft`. **Checker:** researcher. **Exit:** checker passes; lint clean.

## 13. Personas (AI-assisted)

- **You do:** draft 1 or 2 personas (limit): who they are, needs, known pain points and friction, work conditions. Derive from sources and insights; every statement a claim line. No invented demographics or quotes; a persona built on thin evidence says so and is marked `low`.
- **Output:** persona files. **Checker:** researcher. **Exit:** checker passes.

## 14. Define the problem space (AI-assisted)

- **You do:** draft the problem space scope from insights, themes, personas and research pack v1: who, where, and which workflows. This step only scopes; the problem statement is written after the JTBDs in step 15. On the roadmap path this may reframe the request. Explain any reframing.
- **Output:** problem space scope. **Checker:** research owner. **Note:** which file holds it until step 19 is open; default in the Frame section of `koru-core/references/defaults.md`.

## 14a. Competitive scan of 3 to 5 products (AI-led)

- **You do:** gather 3 to 5 products: what each does well, what it misses, annotated screenshots. Never invent a product or a feature; cite where each came from. Roadmap: how others solved this specific solution; discovery: wider, including adjacent categories. A researcher picks or confirms the products (selection method is open; default in the Frame section of `koru-core/references/defaults.md`: you propose, the researcher confirms). Use the `competitive-analysis` skill if installed.
- **Output:** competitive-scan file. **Checker:** research owner. If you cannot browse, say so and ask the user for the products and material rather than writing from memory.

## 14b. Current platform review (AI-assisted) - added by the team, 25 Nov 2026

Frame as written has no step that looks at what the existing tool actually does. The TRACES handbook asks for it as clue +2 ("existing product / design system": what we must reuse, respect or stay consistent with), and workflows (step 15) describe what people do, not what the tool offers. This step closes that gap.

- **Input:** the current platform as the client gave it to us: a clickable mock, screenshots, a demo recording, a walkthrough transcript, or live access. Use the mock or screenshots in the validated set. Never describe functionality from memory or from the name of the product.
- **You do:** open the artefact and write a functionality inventory: each screen or area, what a user can do there, the fields and statuses it shows, how approvals, notifications, search, duplicates and errors behave, what it does on a tablet or small screen, and what is missing or broken that the sources mention (tickets, interviews). Every line is a claim line citing the artefact (and, where the artefact is a mock, say that it is a mock, not the live tool). For each area add what the other sources say about it (a ticket, an interview, a metric), so the inventory shows what staff use, avoid or work around. Do not propose solutions.
- **Human does:** a person with access to the live tool (or the developer) confirms the inventory against the real system and corrects anything the mock does not show.
- **Note on order:** this step does not depend on the research phase, so it can run early (as it did on the Meridian engagement) and be revisited at step 15. Log it if it runs out of sequence. If the artefact is a mock, record where the mock disagrees with other sources in the contradictions register, and check the mock's rendering (for example open it at the stated screen size) rather than trusting its own notes.
- **Output:** `[project]-frame-workflow-current-platform-v1-draft` (type `workflow`, topic `current-platform`) in `drafts/stage-define/`. It feeds step 15 (workflows), TRACES clue +2 and the brief's Constraints (section 6).
- **Checker:** research owner. If the researcher and research owner are the same person, the second-person checker checks it. **Exit:** checker passes; a developer or tool-owner has confirmed it against the live system, or the gap is listed as an open question.

## 15. Journey, workflows, pain points, friction, constraints, JTBDs, then the problem statement (AI-assisted)

- **Use the handbook's chain** (`traces-handbook.md` section 14): insight, then JTBD ("When [situation], I want to [motivation], so I can [outcome]", no solution), then problem statement ("[User] needs to [job], but [obstacle], which leads to [impact]. Solved when [measure]."). You can only write a step if the previous one supports it; if you cannot, name what is missing.
- **You do, in this order:** workflow files (steps today, who does what, pain points and friction per step, constraints), then the JTBD file (5 to 8 jobs, each linked to a persona, "When [situation], I want to [motivation], so I can [outcome]"), then the problem statement: one sentence with user, obstacle, impact and measure, no solution in it. The statement becomes the brief's Problem section. All claims as claim lines.
- **Output:** workflow files, JTBD file, problem statement. **Checker:** research owner. **Exit:** checker passes; the problem statement has no solution words.

## 15a. Constraints review (AI-assisted)

- **You do:** draft a constraints list from the knowledge base and existing documentation. Ask the developer (named role) to list tech limits, the existing system and integrations; a researcher adds business, regulatory and time limits.
- **Output:** constraints, written straight into brief section 6 (not a separate file). **Checker:** senior. **Exit:** developer input recorded or the gap listed as an open question.

## 16. Research pack v2 (AI-led)

- **You do:** compile the final pack from the final persona, JTBD, workflow, insight and scan files: TRACES answers, links pinned by version, open questions, claim-confidence count. Run the stale-check first; it must be clean.
- **Output:** research pack v2. **Checker/signer:** research owner signs, then `final`. Log the sign-off. **Exit:** signed, `final`, listed for upload.

## 17. UX opportunity (AI-assisted)

- **You do:** draft UX opportunities as directions to test, drawn from the problem statement and insight lines (never a single quote). HMW is not done here; it belongs to Explore.
- **Output:** opportunity files. **Checker:** senior.

## 18. AI opportunities (AI-assisted)

- **Use the handbook's AI questions** (`traces-handbook.md` section 14, "UX opportunity to AI opportunity"): say first that "no AI here" is a valid answer; then ask: is there real evidence of the user need; does AI add unique value over a simpler approach; automate or augment; what does a wrong answer cost; is there a graceful non-AI fallback.
- **You do:** draft AI opportunities and where AI fits: screen, agent, both or neither, and why. "Neither" is a valid answer. Roadmap path: check the AI idea the client arrived with against the evidence. Discovery path: left open until the problem is clear.
- **Output:** opportunity files; summary into brief section 5. **Checker:** senior.

## 18a. Success looks like: 2 or 3 observable outcomes (AI-assisted)

- **You do:** draft 2 or 3 outcomes someone could observe, for the user and the business, from the evidence and the opportunities. No metrics you cannot source; if a target is needed and unknown, write it as an open question.
- **Output:** brief section 7. **Checker:** senior; the client corrects it at brief confirmation.

## 19. One-page brief (AI-led)

- **You do:** draft the final brief from the opportunities and the pack (`brief.md`). Run the stale-check and the claim lint; resolve all warnings (a file with open warnings cannot be `final`). Put the riskiest three assumptions first in section 4. Section 8 is required.
- **Sign-off:** review (async or live by size), then a **senior signs**, then the **client confirms** (problem, who it is for, success looks like, answers to open questions). Record who, date and channel in the decisions log. Only after the client has confirmed is the brief `final`.
- **Open:** research pack v2 has no arrow into the brief on the team's board. This skill feeds it anyway (the brief draws on the pack); say so to the user once.

## 20. HTML summary (AI-led)

- **You do:** build one self-contained HTML page with key insights, personas, pain points, workflow, opportunities and the problem statement, using only content from the final files. Required or optional is open (default: optional; ask if the client wants it).
- **Output:** HTML file in `drafts/stage-brief/`. **Checker:** a second person who did not generate it. **Exit:** passed; regenerate when the brief changes.

## After step 20

Fill the handoff card (`handoff.md`), run the final stale-check, list the files to upload, and tell the user what Explore will take from here.
