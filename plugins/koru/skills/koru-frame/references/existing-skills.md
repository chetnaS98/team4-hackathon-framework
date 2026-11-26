# Existing third-party skills

Twenty-one community skills were reviewed against the AI-led and AI-assisted steps. They are not Koru's own, so the user should read each one before installing it. A skill's output still follows the Frame rules: claim lines, naming and status. Never let a third-party skill override those. If a listed skill is not installed, do the step from `steps.md` yourself; do not claim to have used it.

## Used in the workflow (fully cover a step's task)

| Skill | Step | Why it fits |
|---|---|---|
| affinity-diagram (Owl-Listener/designer-skills, design-research) | 11 Synthesis, 12 Insights and themes | Clusters observations bottom-up into themes and writes an insight statement with a "so what" for each. Tags every observation with a participant ID and flags single-source patterns, matching the confidence rule |
| competitive-analysis (Owl-Listener/designer-skills, ux-strategy) | 14a Competitive scan | Identifies direct, indirect and aspirational competitors, compares them, lists strengths and gaps, and produces profiles and annotated references |

Both leave out the 3 to 5 product limit and the claim line format. Those come from this skill.

## Cover part of a step only

| Skill | Covers | What is missing |
|---|---|---|
| jobs-to-be-done (Owl-Listener) | The JTBD part of step 15, in "When, I want, so I can" form | Journeys, workflows, pain points, constraints, problem statement |
| experience-map and service-blueprint (Owl-Listener, ux-strategy) | Journey, workflow and pain point part of step 15 | JTBDs, constraints, problem statement |
| assumption-mapper (mohitagw15856/pm-claude-skills, pm-discovery) | Extracts and risk-rates assumptions, names the cheapest test. Fits the gap check (step 7) and brief section 4 | Not a whole step; belongs to a separate product-decision chain |
| product-research (alirezarezvani/claude-skills, research-ops) | Steps 11 and 12: refuses to promote a single-source finding to an insight | Needs coded observations as input; runs its own scripts and onboarding |
| competitive-analysis (PM, mohitagw15856) | Step 14a | Built for positioning, pricing and win/loss, not UX comparison |
| user-research (anthropics/knowledge-work-plugins, design) | Steps 11 and 12 | Too general: a short method guide, not a synthesis procedure |
| UXR brain (gist galfa-droid/d6ee0ab8...) | Pattern of step 3: cited retrieval that never fabricates | Queries one specific research brain through its own MCP server, not our knowledge base |

## Not a fit

- synthetic-user-research (mohitagw15856) builds AI personas. That conflicts with the rule that every claim has a real source. Do not use it.
- Outside Frame's steps: ab-test-analyzer, a-b-test-design, design-critique, research-protocol, idea-validation, card-sort-analysis, information-architecture, analytics-strategy, cohort-analysis and storytelling. Most belong to Explore, Harden or Learn. The research protocol belongs to the human-led research phase (step 8).

## Already installed in many Koru environments

The markdown-research-formatter skill handles sources (steps 1 and 10). Use it for every conversion; never convert by retyping.
