---
name: powerpoint-skill
description: 'Build and refine PowerPoint (.pptx) presentations with companyFILES MCP tools. Use when asked to create a presentation, build a deck, add or fix slides, or use a corporate slide master / Folienmaster. Covers all three build paths: from scratch (create_powerpoint), from a {{placeholder}} template (create_powerpoint_from_template), and from a corporate master WITHOUT any placeholders via its native slide layouts (describe_pptx_template, create_powerpoint_from_layouts, set_powerpoint_slide_fields). Also covers iterative editing (append_slides_to_powerpoint, update_powerpoint_slide, read_powerpoint_slides), clone-and-refill of template slides, styled tables, speaker notes, images and charts.'
---

# PowerPoint Skill

Everything needed to build, extend and repair `.pptx` decks.

## Tool map

| Tool                              | Purpose                                                             |
| --------------------------------- | ------------------------------------------------------------------- |
| `create_powerpoint`               | New deck from Markdown or a typed `slides` array (built-in design)  |
| `create_powerpoint_from_template` | New deck from a POTX/PPTX template that contains `{{placeholders}}` |
| `describe_pptx_template`          | Read a deck's **native slide layouts** — no `{{}}` needed           |
| `create_powerpoint_from_layouts`  | New deck by instantiating those native layouts (corporate design)   |
| `set_powerpoint_slide_fields`     | Patch one slide's native placeholder text, in place                 |
| `append_slides_to_powerpoint`     | Append slides to an existing deck, in place                         |
| `update_powerpoint_slide`         | Replace one slide of an existing deck, in place                     |
| `read_powerpoint_slides`          | Read back slide numbers, titles and text lines                      |
| `list_templates`                  | Find available templates (`type: "potx"`) before building           |
| `embed_chart_in_document`         | Render a Chart.js chart into a one-slide deck                       |

---

## 1. Work iteratively — do not one-shot a deck

**A deck of more than ~6 slides must be built in several tool calls.** One giant
`create_powerpoint` call is the most common failure mode: the arguments get truncated, layout
choices cannot be corrected, and a single bad slide means regenerating everything.

The loop:

```
PLAN   → write the outline in your reply first (slide number, role/layout, headline, content sketch)
PROBE  → describe_pptx_template / list_templates / read_powerpoint_slides — learn what exists
SEED   → create_powerpoint* with the FIRST 3–5 slides only → keep the returned document_id
EXTEND → append_slides_to_powerpoint in chunks of 3–5 slides, repeatedly
REFINE → set_powerpoint_slide_fields or update_powerpoint_slide for individual fixes
VERIFY → read_powerpoint_slides to confirm slide count, order and titles
```

### PLAN before the first tool call

For anything beyond a couple of slides, show the user a plan and let them react. It costs one
message and prevents rebuilding a 20-slide deck.

```
Plan — "Digitalstrategie 2027" (12 slides, corporate master `folienmaster`)

 #  Layout / role      Headline                      Content
 1  title              Digitalisierungsstrategie 2027 Author + date
 2  section            1. Ausgangslage
 3  content            Kernbefunde                   3 bullets, 1 nested
 4  two-content        Handlungsoptionen             Option A | Option B
 5  section            2. Zielbild
 …
12  closing            —                             Contact block

I'll build 1–5 first, then append 6–12 in two chunks. Say if the structure should change.
```

### Rules of thumb

- **Chunk size 3–5 slides** per call. Long bullet text or `htmlTable` content → 2–3.
- **Keep the `document_id`.** Every create/append/update/patch call returns the _same_
  `document_id` for that deck. Reuse it; never build a second deck to fix the first.
- **One bad slide → patch that slide.** `set_powerpoint_slide_fields` (layout-native) or
  `update_powerpoint_slide` (built-in / clone mode). Both preserve slide count and position.
- **`read_powerpoint_slides` between chunks** when you have appended several times, to confirm
  you are numbering slides from the right base.
- **Report progress**, e.g. "slides 1–5 done, appending 6–9 next", and render the returned
  `markdownLink` so the user can open the intermediate state.
- **Never re-create to append.** `drop_template_slides: false` / `append_slides_to_powerpoint`
  exist precisely so a deck can grow across turns.

Every slide in a `slides` array **requires a `title`** (it is a mandatory field, including for `section` slides) — a slide without a `title` fails validation.

---

## 2. Pick the build path

Decide once, at the start. Mixing paths in one deck produces inconsistent design.

| Situation                                                   | Path                                    |
| ----------------------------------------------------------- | --------------------------------------- |
| No template mentioned, companyFILES design is fine          | **A** `create_powerpoint`               |
| A template exists **and** contains `{{key}}` markup         | **B** `create_powerpoint_from_template` |
| A corporate master / Folienmaster with **no** `{{}}` markup | **C** `create_powerpoint_from_layouts`  |

**How to tell B from C:** run `describe_pptx_template` on the template and read
`hasLegacyPlaceholders`.

- `true` → the deck uses `{{}}` → path **B** (see also **templates-skill**)
- `false` → path **C**

`list_templates` (`type: "potx"`) lists candidates and, for `{{}}` decks, a per-slide placeholder
breakdown. It does **not** return the layout catalog — use `describe_pptx_template` for that.

---

## 3. Path A — from scratch (`create_powerpoint`)

### Markdown mode (fast, text-heavy decks)

`#` or `##` starts a new slide. All slides get the `default` layout. A line of exactly `???`
starts speaker notes, which run until the next `#`/`##` heading.

> **`title` adds a slide.** Passing the top-level `title` argument to `create_powerpoint`
> prepends a generated dark title slide (title, author, today's date). So `n` content slides plus
> `title` = `n + 1` slides, and every later `slide_number` shifts by one. Omit `title` when you
> want to author the opening slide yourself. `append_slides_to_powerpoint` never adds one.

```json
{
  "markdown": "# Quarterly Results\n\n- Revenue: €1.2M\n- Growth: 15%\n\n???\nOpen with the revenue number.\n\n## Key Highlights\n\n- Launched new product\n- Expanded to 3 markets",
  "filename": "q4_results",
  "title": "Q4 2025 Results",
  "author": "Strategy Team",
  "folder": "presentations"
}
```

Inline images use `doc:<documentId>` or `lc:<file_id>`:

```markdown
![Chart](doc:abc12345-...)
![Attachment](lc:xyz-librechat-file-id)
```

### Typed slides mode (layout control)

Pass `slides` instead of `markdown`. When both are given, `slides` wins.

| `type`         | Visual                                                 | Fields                                                               |
| -------------- | ------------------------------------------------------ | -------------------------------------------------------------------- |
| `"default"`    | Accent bar + title + stacked content                   | `title`, `content`, `bullets`, `code`, `table`, `htmlTable`, `image` |
| `"section"`    | Dark background, large centred title — chapter divider | `title`, `subtitle`                                                  |
| `"text-image"` | Title on top, text/bullets left, image right           | `title`, `content`, `bullets`, `htmlTable`, `image`, `imageAlt`      |

Every type also accepts `notes` (speaker notes). Unknown `type` values fall back to `"default"`.
Omitting `image` on a `text-image` slide draws a skeleton placeholder box — useful for drafts.

```json
{
  "slides": [
    { "type": "section", "title": "Q4 2025 Results", "subtitle": "Strategy Team" },
    {
      "type": "default",
      "title": "Key Metrics",
      "bullets": ["Revenue: €1.2M", "Growth: 15%", "NPS: 72"],
      "notes": "Lead with revenue; growth is YoY, not QoQ — expect that question."
    },
    {
      "type": "text-image",
      "title": "System Architecture",
      "bullets": ["Microservices", "Auto-scaling", "99.9% uptime"],
      "image": "lc:xyz-file-id",
      "imageAlt": "Architecture diagram"
    }
  ],
  "title": "Q4 2025 Results",
  "filename": "q4_results",
  "folder": "presentations"
}
```

`bullets` is a flat `string[]` here — for nested bullets use path C (`level`) or a template.

### Styled tables — `htmlTable`

Use `htmlTable` instead of `table` when cells need colour, bold or alignment. Supported on
`default` and `text-image`; it takes precedence over `table`.

| Inline CSS                        | Effect      |
| --------------------------------- | ----------- |
| `background-color: #hex`          | Cell fill   |
| `color: #hex`                     | Text colour |
| `font-weight: bold`               | Bold        |
| `font-style: italic`              | Italic      |
| `text-align: left\|center\|right` | Alignment   |

`<th>` cells get the theme's header fill/text automatically unless overridden.

```json
{
  "type": "default",
  "title": "Revenue by Region",
  "htmlTable": "<table><tr><th>Region</th><th>Q1</th><th>vs PY</th></tr><tr><td style=\"font-weight:bold\">DACH</td><td>€1.2M</td><td style=\"color:#16A34A\">+18%</td></tr><tr><td style=\"font-weight:bold\">US</td><td>€0.8M</td><td style=\"color:#DC2626\">-3%</td></tr></table>"
}
```

For a plain grid, `table: string[][]` (first row = header) is enough.

---

## 4. Path C — corporate master without `{{}}` (layout-native)

This is the path for a deck the design team shipped: `Folienmaster_LMU.pptx` and friends. Such
decks carry **no `{{}}` markup**, only named slide layouts with OOXML's own placeholders.
Content is bound to those placeholders and **no formatting is written**, so fonts, colours,
logos and geometry come from the master. ("Reset layout" in PowerPoint changes nothing — that is
the proof.)

Upload such a master as a template with `type: potx` (also correct for a `.pptx` file).

### Step 1 — `describe_pptx_template`

```json
{ "template_name": "folienmaster" }
```

Returns:

```json
{
  "hasLegacyPlaceholders": false,
  "slideSize": { "widthEmu": 12192000, "heightEmu": 6858000 },
  "roleMap": { "title": "slideLayout5.xml", "section": "slideLayout8.xml", "content": "slideLayout9.xml" },
  "layouts": [
    {
      "layoutId": "slideLayout11.xml",
      "name": "Titel_mit_Inhalt",
      "masterId": "slideMaster3.xml",
      "role": "content",
      "exampleSlides": [4],
      "slots": [
        { "key": "title", "type": "title" },
        { "key": "body:10", "type": "body", "hint": "Mastertextformat bearbeiten" }
      ]
    },
    {
      "layoutId": "slideLayout9.xml",
      "name": "Inhalt",
      "role": "content",
      "exampleSlides": [],
      "slots": [{ "key": "title" }, { "key": "body:12" }, { "key": "body:13" }]
    }
  ]
}
```

Reading it:

- **`layoutId` is the stable identifier.** Layout **names repeat** across slide masters
  (a real deck had `Präsentationstitel` 3× across 5 masters). Prefer `layoutId`.
- **Slot keys are `type` or `type:idx`.** The `idx` matters: `body:12` + `body:13` on the same
  layout means a two-column layout — fill both to use both columns.
- **`role`** is inferred from the layout name (German + English keywords) and its slot
  composition. Roles: `title`, `title-image`, `section`, `content`, `two-content`,
  `title-only`, `closing`, `reference`. `roleMap` picks one layout per role.
- **`hint`** is the layout's own prompt text and is only a hint — real masters often say
  "Mastertextformat bearbeiten" or lorem ipsum. Judge by name + slot shape, not by hint.
- **`isImage` slots (`pic:*`) cannot be filled yet.** They stay empty and are reported back as
  `imageSlotsNotFilled`. Do not promise the user an image in such a slot.

### Step 2 — `create_powerpoint_from_layouts`

Each slide picks its layout by `layoutId`, layout name, or role — mix freely.

```json
{
  "template_name": "folienmaster",
  "filename": "strategie-2027",
  "folder": "presentations",
  "slides": [
    {
      "layout": "title",
      "fields": { "title": "Digitalisierungsstrategie 2027", "body:11": "Dr. Max Mustermann\n27.07.2026" },
      "notes": "Begrüßung, 2 Minuten."
    },
    { "layout": "Kapiteltrenner", "fields": { "title": "1. Ausgangslage" } },
    {
      "layout": "slideLayout11.xml",
      "fields": {
        "title": "Kernbefunde",
        "body:10": [
          "Drei Systeme decken 80 % ab",
          { "text": "Redundante Datenhaltung", "level": 1 },
          "Betriebskosten +9 % p. a."
        ]
      }
    },
    {
      "layout": "Inhalt",
      "fields": {
        "title": "Handlungsoptionen",
        "body:12": ["Option A: Konsolidierung", "Aufwand: hoch"],
        "body:13": ["Option B: Schnittstellen", "Aufwand: mittel"]
      }
    },
    { "layout": "closing", "fields": { "body:11": "Institut XY\n80539 München" } }
  ]
}
```

**Slot values** accept three shapes:

| Value                             | Result                                           |
| --------------------------------- | ------------------------------------------------ |
| `"one line"`                      | One paragraph; `\n` splits into paragraphs       |
| `["a", "b"]`                      | One bullet per item, all at level 0              |
| `[{ "text": "sub", "level": 1 }]` | Nested bullet, `level` 0–8, styled by the master |

Omitted slots stay empty and show the layout prompt in PowerPoint.

**Base deck options:**

- `drop_template_slides` (default `true`) removes the source deck's own slides. Slide masters,
  layouts, themes and media are **always** kept.
- `drop_template_slides: false` **appends** the new slides after the existing ones.
- Instead of `template_name`, pass `document_id` (a stored `.pptx`) or `librechat_file_id` (an
  attachment) to use that deck as the base. Because layouts survive, a deck built this way can be
  appended to again — that is the iterative path for path C.
- `role_map` overrides inference: `{ "content": "slideLayout4.xml" }`.

**Response** reports per slide: `layoutId`, `layoutName`, `filledSlots`, `unknownFields`,
`emptySlots`. Always check `unknownFields` — a typo'd slot key is reported, not silently dropped.

### Step 3 — `set_powerpoint_slide_fields` (iterative editing)

Patches **one** slide in place. Only the slots you pass change; every other slot, shape, image
and the slide's position stay untouched. Slots the layout offers but the slide does not yet carry
are added.

```json
{
  "document_id": "<id>",
  "slide_number": 3,
  "fields": { "title": "Kernbefunde (überarbeitet)", "body:10": ["Neuer Punkt 1", "Neuer Punkt 2"] }
}
```

This is the tool to call repeatedly across turns while the user reviews the deck. Accepts
`librechat_file_id` too (the attachment is updated on the shared volume when available).

### `slide_type` routing still works

A role resolves in this order: a `{{slide_type:x}}` marker found in a deck slide (unchanged
legacy behaviour, highest priority) → an explicit `role_map` → roles inferred from native
layouts. **Never ask the user to type `{{}}` markers into a corporate master** — that is exactly
what path C removes.

---

## 5. Iterative editing of any deck

All three tools below target the deck with `document_id` **or** `librechat_file_id` (a LibreChat
attachment, updated in place on the shared volume when it is mounted).

### `append_slides_to_powerpoint`

Two mutually exclusive modes.

**(1) Generate** — `markdown` or `slides`, same schema as `create_powerpoint`:

```json
{
  "document_id": "<id>",
  "slides": [
    { "type": "section", "title": "Part 2: Deep Dive" },
    { "type": "default", "title": "Technical Details", "bullets": ["Detail A", "Detail B"] }
  ]
}
```

**(2) Clone-and-refill** — `reference_slide` copies an **existing slide of this same deck**
(its design, layout, fonts, background) and refills its `{{placeholders}}`. This is how a
`{{}}`-template deck is extended so the new slide looks identical to the template:

```json
{
  "document_id": "<id>",
  "reference_slide": 4,
  "placeholders": { "region": "APAC", "revenue": "€0.9M" },
  "notes": "APAC is the newest market — numbers are 2 quarters old."
}
```

`reference_slide` cannot be combined with `markdown`/`slides`. In clone mode use the top-level
`notes` field; in generate mode use `slides[].notes`.

Clone-mode limits:

- Structured fields (`bullets`, `code`, `table`) are **not** rendered — the cloned slide only has
  the shapes the template defines. Feed content in through `{{placeholders}}`.
- Only `{{text placeholders}}` are refilled; image (`{%name}`) refill is not supported here — use
  `create_powerpoint_from_template` for that.

### `update_powerpoint_slide`

Replaces one slide, keeping its position and the total slide count. Same two modes:

```json
{
  "document_id": "<id>",
  "slide_number": 3,
  "slides": [{ "type": "section", "title": "Chapter 2", "subtitle": "The Deep Dive" }]
}
```

```json
{ "document_id": "<id>", "slide_number": 3, "reference_slide": 4, "placeholders": { "region": "EMEA" } }
```

Or quick text-only: `{ "document_id": "<id>", "slide_number": 2, "markdown": "## New Title\n\n- Bullet" }`
(`##` sets the title, `???` adds notes).

When `reference_slide` equals `slide_number`, the slide is refilled in place — the way to fix a
slide that still shows raw `{{placeholders}}`.

### `read_powerpoint_slides`

```json
{ "document_id": "<id>" }
```

Returns `{ slide_count, slides: [{ slideNumber, title, textLines }] }`. Use it before editing a
deck you did not just build, and after several appends to confirm numbering.

---

## 6. Charts and images in slides

- **Chart as its own slide:** `embed_chart_in_document` with `document_type: "powerpoint"` renders
  the chart onto its own slide (plus a generated title slide when `title` is given). Use the
  resulting `document_id` as an image source, or keep appending to it.
- **Chart on a content slide:** create the chart image, then reference it via `image` on a
  `text-image` slide (`doc:<id>`), or via a `{%name}` image placeholder in a `{{}}` template.
- **Image sources everywhere:** an https URL, a base64 data URI, `doc:<documentId>` (PVC upload)
  or `lc:<file_id>` (LibreChat attachment — see `list_my_files`).
- See **charts-diagrams-skill** for chart/diagram creation, **templates-skill** for `{%image}`
  placeholders, chart data replacement and `repeat`.

---

## 7. Gotchas

- **Never fall back to path A when a corporate master was requested.** If a layout call is
  rejected, fix the call — do not switch to `create_powerpoint`. Its output uses the built-in
  design, so the one thing that was asked for (the corporate master) is exactly what is lost, and
  a deck named after the master that does not use it reads as success when it is a failure. If you
  cannot get the call through, say so and stop; do not ship a substitute silently.
- **Pass `slides`, `fields` and `role_map` as real JSON, not as a string.** A serialised
  `"[{\"layout\":…}]"` is tolerated by the server, but only as a safety net — send structured
  arguments. A schema rejection means the _shape_ is wrong: re-read this file's example rather than
  retrying the same payload.
- **`slides` beats `markdown`** when both are passed to the same call.
- **`title` on `create_powerpoint` prepends an extra generated title slide** — it shifts every
  `slide_number`. Omit it to author slide 1 yourself.
- **`reference_slide` + `markdown`/`slides` is an error.** Pick one mode.
- **`slide_number` is 1-based**; out of range is an error that reports the real slide count.
- **`unknownFields` / `emptySlots`** in a layout response are the signal that a slot key was
  wrong — re-read `describe_pptx_template` rather than guessing. Common synonyms are accepted
  (`title` for a `ctrTitle` placeholder, `subtitle` for `subTitle`, `content`/`bullets` for
  `body`), but exact slot keys are always safest.
- **A synonym fills one slot, not all matching ones.** On a layout with two body placeholders
  (`body:12`, `body:13`) a single `bullets` fills the **first free** one and reports the other in
  `emptySlots` — it is not duplicated into both. To fill both columns, address them by exact key.
  Exact keys win over synonyms, so `{ "body:13": "right", "content": "left" }` fills both correctly.
- **`subtitle` on a master with no `subTitle` placeholder** (Folienmaster_LMU and similar: the
  subtitle line of a title layout is a plain `body` placeholder) falls back to the first free
  `body` slot instead of landing in `unknownFields`.
- **`create_powerpoint_from_template` refuses a template with no `{{}}` placeholders** and names
  the layout tools in the error. That is path C's cue, not a broken template — do not retry the
  legacy tool and do not add `{{}}` markers to a corporate master.
- **`pic:*` slots are not fillable** in path C yet.
- **Layout names are not unique.** Ambiguous name references resolve to the first match and log a
  warning; use `layoutId`.
- **`list_templates` does not include the layout catalog.** `describe_pptx_template` does.
- **Do not write formatting in path C.** Passing colours/fonts is neither possible nor wanted —
  the master owns the design.
- **Downloads:** every create/append/update/patch call returns
  `{ id, filename, downloadUrl, markdownLink }`. Always render `markdownLink` in the reply. In
  embedded (iframe) mode downloads are sandboxed — offer "copy link" instead.
- **Theming (path A/B):** the org/user colour theme and logo are applied automatically from
  settings; no theme arguments needed.

---

## 8. End-to-end test drive

A single run that exercises every slide feature. Useful for verifying a deployment.

**Path A — scratch deck, built iteratively**

1. `create_powerpoint` — no `title` argument, 3 slides: `section`, `default` (bullets +
   `htmlTable` with coloured cells), `text-image` **without** `image` → expect a skeleton box.
   → 3 slides, note `document_id`. (Repeat once **with** `title` to confirm the generated title
   slide appears and shifts numbering to 4.)
2. `append_slides_to_powerpoint` — `slides`: a `default` with a `code` block and a `table`, plus
   a `text-image` **with** `image: "lc:<file_id>"`. → same `document_id`, 5 slides.
3. `append_slides_to_powerpoint` — `markdown` with two `##` headings and a `???` notes block.
   → 7 slides, notes visible in the presenter view.
4. `update_powerpoint_slide` — `slide_number: 2`, a single-element `slides` array of type
   `section`. → still 7 slides, slide 2 is now a divider.
5. `read_powerpoint_slides` → `slide_count: 7`, titles in the expected order.

**Path C — corporate master, built iteratively**

6. Upload the master as a `potx` template → log line
   `Auto-extracted N slide layout(s) from PPTX template …`, `placeholders` empty.
7. `describe_pptx_template` → `hasLegacyPlaceholders: false`, layouts with `layoutId`, `name`,
   `masterId`, `role`, slot keys including at least one `body:idx` pair and one `pic:*`.
8. `create_powerpoint_from_layouts` — 5 slides addressed by **role**, **name** and **layoutId**
   mixed; include multi-level bullets, a two-column layout filling `body:12` + `body:13`, a `\n`
   inside a value, and `notes` on slide 1.
   → open in PowerPoint: corporate fonts/colours/logos, real master bullets, and **"Reset
   layout" changes nothing**.
9. `set_powerpoint_slide_fields` — patch only the `title` of slide 2 → same `document_id`, same
   slide count, other slots untouched.
10. `create_powerpoint_from_layouts` with `document_id` (not `template_name`) and
    `drop_template_slides: false` → 6 slides, appended slide in the same corporate design.

**Error paths**

11. `"layout": "GibtsNicht"` → error listing all layouts **and** roles.
12. `fields: { "untertitel": "x" }` on a layout without that slot → `unknownFields: ["untertitel"]`.
13. `slide_number: 99` on `set_powerpoint_slide_fields` → error naming the real slide count.
14. `reference_slide` together with `slides` → error.
15. A deck **with** `{{}}` markup through `describe_pptx_template` →
    `hasLegacyPlaceholders: true` → switch to `create_powerpoint_from_template`.
