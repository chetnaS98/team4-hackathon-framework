# Project profile (`research-profile.json`)

The skill knows nothing about any one project. Everything project-specific (product names, lifecycle
stages, personas, known workflows, spellings, search keywords) lives in one JSON file per project.

## Where it lives and how it is found

`scripts/research_profile.py find <start-dir>` walks up from `<start-dir>` and returns the first
`research-profile.json` it meets. So put one profile at the root of a project folder and every
output written under that folder picks it up. `--profile <path>` on any script overrides discovery.

No profile found: ask the user whether to create one. Offer to draft it from the source file
(products, roles and stages the source names), show the draft, and save only after they confirm.
Never invent values silently.

## Fields

```json
{
  "profile_version": 1,
  "project": "deskly",
  "products": {
    "deskly": "Desk and room booking: web app, mobile app, admin console"
  },
  "lifecycle": {
    "plan": "Deciding where and when to work, team days",
    "book": "Finding and reserving a desk or room",
    "arrive": "Check-in, wayfinding, access",
    "manage": "Admin: floor plans, policies, approvals",
    "analyze": "Occupancy reports, dashboards"
  },
  "personas": ["member", "office-manager", "approving-manager"],
  "workflows": ["booking-desk", "approving-booking", "checking-in"],
  "glossary": {"Deskly": ["deskly", "desk-ly", "Deskley"]},
  "search_keywords": ["Deskly", "desk booking"],
  "default_confidentiality": "internal"
}
```

| Field | Required | Meaning |
|---|---|---|
| `profile_version` | yes | Always `1` for now. |
| `project` | yes | Kebab-case project slug. Used in pipeline artefact names. |
| `products` | yes | Allowed values of the `product` front-matter field, each with a one-line description so files can be classified. One-product projects have one key. |
| `lifecycle` | no | Allowed values of `lifecycle`, each with a description (the goal decides the stage). Omitted → any kebab-case value is accepted, and the reply flags new ones. `multi` is always allowed. |
| `personas` | no | Known roles. Values outside the list are allowed but flagged as new in the reply. |
| `workflows` | no | Known workflow names. Reuse them verbatim; new names are flagged. |
| `glossary` | no | Canonical product/feature names → variants seen in sources. Used **only** for text the skill adds (headings, summaries, context line). Source text is never normalised. |
| `search_keywords` | no | Seed keywords for the optional Jira/Confluence search. |
| `default_confidentiality` | no | Default for `confidentiality` when the source does not say. |

The profile is data the team owns. Change it by editing the file (it is versioned in the repo);
`research_profile.py check` validates it.
