# company-ai-stack-skills: agent instructions

This repo is the **single source** for the ready-made companyGPT agent skills. The docs site
([innFactory-AI/docs](https://github.com/innFactory-AI/docs), docs.company-gpt.com → Tutorials → Skills) does not
keep its own copy: its build runs `scripts/sync-skills.mjs`, which reads this repo (branch `main`) and generates every
skill page, the skills index and the sidebar. Never edit skill pages in the docs repo; they are gitignored there.

## Layout

```text
catalog.json                                   # categories, order, index texts (DE/EN)
<locale>/skills/<category>/<slug>/SKILL.md     # the skill: what users upload in companyGPT under "Skills"
<locale>/skills/<category>/<slug>/references/… # optional bundled files (Markdown recipes; optionally scripts/…)
<locale>/pages/<category>/<slug>.md            # docs wrapper: title, description, sidebar label, intro
```

- **Package = the skill folder.** Put nothing docs-only into it: companyADMIN Library Sync imports every file in a
  folder that has a `SKILL.md`, which is why the docs wrapper lives under `pages/`. Everything in the folder
  (`SKILL.md`, `references/`, `scripts/`, …) is part of the skill package: the docs offer it as a zip (`<name>/SKILL.md` plus
  bundled files) that companyGPT imports under Skills (`.zip`/`.skill`). The agent reads bundled files with the
  built-in `read_file` tool (`<name>/references/x.md`, works without code execution); with code execution they are
  also copied read-only to `/mnt/data/skills/<name>/…` in the sandbox. A skill pasted or uploaded as a single
  `SKILL.md` has no bundled files.

- `<locale>` is `de` and `en`. Every skill exists in **both**, with the same `<category>/<slug>`.
- `<slug>` is the docs URL (`/de/tutorials/skills/<category>/<slug>`). Don't rename a slug once it is live; links
  and bookmarks point at it.
- `catalog.json` lists every category (`id` = folder, `label.de`/`label.en` = sidebar group and index heading) and its
  skills in display order, plus the title, description and intro of the skills index page. A folder that is not in
  `catalog.json` fails the docs build, and so does a catalog entry without both files in both locales.

### SKILL.md

```markdown
---
name: excel-skill
description: One or two sentences; LibreChat uses it to decide when to load the skill.
---

# Excel Skill
…
```

- `name`: English kebab-case ending in `-skill`, identical in DE and EN (technical identifier). LibreChat allows
  `^[a-z0-9][a-z0-9-]*$`, max. 64 characters.
- `description`: max. 1024 characters, in the page's language. It decides when the skill is activated, so say what
  the skill does *and* when to use it.
- Body max. 100,000 characters. The docs wrap it in a fence that is longer than any backtick run inside, so inner
  ```` ``` ```` blocks are fine.

### pages/<category>/<slug>.md

```markdown
---
title: Excel Skill
description: One sentence for search and the page header.
label: Excel
---

Use this skill when … (DE: "Verwende diesen Skill, wenn …", du-form)

:::note
Optional Starlight asides, e.g. placeholders the user must replace.
:::
```

`label` is the sidebar and index entry; `title`/`description` become the page frontmatter. The body is shown above
the skill. The generator adds `## Skill`, the fenced `SKILL.md` and a source link back to this repo.

## Writing rules

- **Language:** DE files are German (du-form), EN files English. Keep the `name:` slug, tool/parameter names, product
  names (companyFILES, companyRAG, MCP, …) and format keywords (PDF, DOCX, XLSX) unchanged. DE and EN must say the
  same thing; change both in one PR.
- **Prompt-first, code optional:** every `SKILL.md` must work as plain instructions without code execution. Code
  execution (sandbox without network; Python/Node/Bash) is on in most tenants, but not everywhere: the tenant, the
  role permission `RUN_CODE` or the user can switch it off. Point to companyFILES for file output (DOCX/XLSX/PPTX/PDF)
  and to companyRAG collections / MCP servers / file upload for data.
  - Code steps go into an optional section that starts with "If code execution is available …" (DE: "Wenn
    Code-Ausführung verfügbar ist …") and always names the fallback without code (usually a companyFILES tool).
  - Check Python packages with `import` before relying on them, and fall back if one is missing.
  - Longer recipes or scripts go into bundled files next to `SKILL.md` (`references/<topic>.md`, optionally
    `scripts/…`), in both locales. Reference them from `SKILL.md` with a note that they only exist when the skill was
    installed as a package (zip / sync), not when only `SKILL.md` was pasted. `SKILL.md` must still be complete
    without them.
- **Tools must be real.** Every tool name, parameter, enum and limit in a skill must exist in the current release of
  the app that provides it. Check the source before changing a skill:
  - companyFILES: `src/mcp/server.ts`, `cad-tools.ts`, `docs-tools.ts`, `ui-tools.ts`, `template-handoff-tools.ts` (repo `innFactory/companyFILES`;
    it also keeps reviewed templates in `.skills/*/SKILL.md`). Some tools only exist when an extension is configured
    (CAD tools, `read_file`/`convert_to_markdown`, Azure-Maps map options); say "if available" for those.
  - companyRAG: `apps/mcp/internal/handlers/` (repo `innFactory/companyRAG`). The MCP server is usually called
    `ai-search`; dataset tools only exist when DuckDB is enabled.
  - companyM365, companyTRANSCRIBE, companyTRANSLATE, companyLEARN: their MCP tool definitions. Only name an app in
    a skill's "Where the data comes from" section if the tool really exists.
- When an app release adds, renames or removes tools, update the affected skills here in the same rollout.

## Workflow

1. Branch, edit `SKILL.md` and/or the page wrapper in both locales, update `catalog.json` and the README table for new
   skills.
2. Preview locally with a docs checkout next to this repo:
   `cd ../docs && SKILLS_DIR=../company-ai-stack-skills npm run dev` (or `npm run build`).
3. Open a PR. CI (`.github/workflows/ci.yml`) builds the docs site against your branch.
4. After merge to `main`, CI sends a `repository_dispatch` (`skills-updated`) to innFactory-AI/docs, which rebuilds
   and deploys the site. That step needs the repo secret `DOCS_DISPATCH_TOKEN` (fine-grained token for
   innFactory-AI/docs with "Contents: read and write").

Conventional commits, feature branches and PRs; never push to `main`.
