---
name: powerpoint-skill
description: 'Build and refine PowerPoint (.pptx) presentations with companyFILES MCP tools. Use when asked to create a presentation, build a deck, add or fix slides, use a corporate slide master / Folienmaster, or work with a .pptx the user attached in the chat ("make a deck in this design", "add slides to this presentation"). Covers all three build paths: from scratch (create_powerpoint), from a {{placeholder}} template (create_powerpoint_from_template), and from a corporate master WITHOUT any placeholders via its native slide layouts (describe_pptx_template, create_powerpoint_from_layouts, add_slides_from_layouts, set_powerpoint_slide_fields). Also covers iterative editing (append_slides_to_powerpoint, update_powerpoint_slide, read_powerpoint_slides), clone-and-refill of template slides, styled tables, speaker notes, images and charts.'
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
| `add_slides_from_layouts`         | Append layout-native slides to an existing deck, **in place**       |
| `set_powerpoint_slide_fields`     | Patch one slide's native placeholders (text + images), in place     |
| `append_slides_to_powerpoint`     | Append slides to an existing deck, in place                         |
| `update_powerpoint_slide`         | Replace one slide of an existing deck, in place                     |
| `read_powerpoint_slides`          | Read slide numbers, titles, text **and each slide's layout/slots**  |
| `list_my_files`                   | Find a deck the user attached in the chat (`file_id`)               |
| `list_templates`                  | Find available templates (`type: "potx"`) before building           |
| `embed_chart_in_document`         | Chart.js chart as a new deck; `title` adds a title slide            |

---

## 1. Work iteratively — do not one-shot a deck

**A deck of more than ~6 slides must be built in several tool calls.** One giant
`create_powerpoint` call is the most common failure mode: the arguments get truncated, layout
choices cannot be corrected, and a single bad slide means regenerating everything.

The loop:

```
PLAN   → write the outline in your reply first (slide number, role/layout, headline, content sketch)
PROBE  → describe_pptx_template / list_templates / read_powerpoint_slides — learn what exists
SEED   → create_powerpoint* with the FIRST 3–5 slides only → keep the returned id (document_id)
EXTEND → append_slides_to_powerpoint (path A/B) or add_slides_from_layouts (path C)
         in chunks of 3–5 slides, repeatedly
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
- **Keep the `document_id`.** The first create call returns the deck's `id`; every
  append/update/patch call on that deck keeps the _same_ id. Reuse it; never build a second deck
  to fix the first.
- **One bad slide → patch that slide.** `set_powerpoint_slide_fields` (layout-native) or
  `update_powerpoint_slide` (built-in / clone mode). Both preserve slide count and position.
- **`read_powerpoint_slides` between chunks** when you have appended several times, to confirm
  you are numbering slides from the right base.
- **Report progress**, e.g. "slides 1–5 done, appending 6–9 next", and render the returned
  `markdownLink` so the user can open the intermediate state.
- **Never re-create to append.** `add_slides_from_layouts` / `append_slides_to_powerpoint`
  exist precisely so a deck can grow across turns.

Every slide in a **typed** `slides` array (`create_powerpoint`, `append_slides_to_powerpoint`,
`update_powerpoint_slide`) **requires a `title`** (it is a mandatory field, including for `section`
slides) — a slide without a `title` fails validation. The layout tools' `slides` have a different
shape — `layout`, `fields`, `images`, `notes` — and no `title` field; a title goes in
`fields.title`.

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

A deck the user attached to the chat needs no template upload for path C — see the next section.
Path B is the exception: `create_powerpoint_from_template` only takes a `template_name`.

---

## 2a. The user attached a `.pptx` in the chat

This is the common case: someone drops their Folienmaster or an existing deck into the
conversation and asks for a presentation "in this design", or asks to extend the deck they just
sent. For a corporate master (no `{{}}`), **do not ask them to upload it as a template** — the
layout tools, `read_powerpoint_slides`, `append_slides_to_powerpoint` and `update_powerpoint_slide`
take the attachment directly. `create_powerpoint_from_template` does not: it has only
`template_name`, no `document_id` / `librechat_file_id`.

```
FIND    file_id from the "Attached files in this message:" block
        (no block: list_my_files → pick the .pptx by filename; list_documents /
        search_documents work too — pass the entry's id)
PROBE   describe_pptx_template { "librechat_file_id": "<file_id>" }
        → hasLegacyPlaceholders decides the path (B vs C)
        read_powerpoint_slides { "librechat_file_id": "<file_id>" } if the deck has content
        you need to see or extend — it reports each slide's layout and slot keys
BUILD   (path C)
        new deck   → create_powerpoint_from_layouts { "librechat_file_id": ..., "slides": [...] }
        extend it  → add_slides_from_layouts     { "librechat_file_id": ..., "slides": [...] }
        fix one    → set_powerpoint_slide_fields { "librechat_file_id": ..., "slide_number": n, ... }
```

**An attached `{{}}` deck (path B)** has two routes:

- To fill it with `create_powerpoint_from_template` (images, charts, `repeat`), it must be
  uploaded as a template first (web UI, `open_companyfiles_ui page="upload"`); then call the tool
  with that `template_name`.
- Or edit the attachment itself in clone mode (§5): `update_powerpoint_slide` with
  `reference_slide` equal to `slide_number` plus `placeholders` fills a slide in place;
  `append_slides_to_powerpoint` with `reference_slide` plus `placeholders` adds a filled copy.

**`librechat_file_id` and `document_id` are interchangeable inputs.** The server resolves either,
PVC first. Pass whichever id the listing gave you.

**New deck or edited deck?** Two different intents, two different tools:

| The user wants                                | Tool                             | Result                                          |
| --------------------------------------------- | -------------------------------- | ----------------------------------------------- |
| A presentation **in the design of** this deck | `create_powerpoint_from_layouts` | A **new** document; the attachment is untouched |
| More slides **in** this deck                  | `add_slides_from_layouts`        | The **same** deck, extended in place            |
| A slide of this deck changed                  | `set_powerpoint_slide_fields`    | The **same** deck, one slide patched            |

For an attachment, "in place" means: the file is rewritten on the shared LibreChat volume when
that volume is mounted (same `file_id`); otherwise the modified copy is saved as a new
companyFILES document. The response `message` says which happened — pass that on rather than
promising the user their original file changed.

**A deck built from Markdown has no fillable layouts.** `add_slides_from_layouts` refuses it and
names `append_slides_to_powerpoint` instead; that refusal is correct, don't work around it.

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
  "author": "Strategy Team"
}
```

Inline images in `create_powerpoint` Markdown use `doc:<documentId>` or `lc:<file_id>`:

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
      "image": "https://www.example.com/architecture.png",
      "imageAlt": "Architecture diagram"
    }
  ],
  "title": "Q4 2025 Results",
  "filename": "q4_results"
}
```

`bullets` is a flat `string[]` here — for nested bullets use path C (`level`) or a template.
The `image` field takes a base64 data URI or a public http(s) URL — not `doc:`/`lc:` (see §6).

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

This is the path for a deck the design team shipped, e.g. a `Corporate-Master.pptx`. Such
decks carry **no `{{}}` markup**, only named slide layouts with OOXML's own placeholders.
Content is bound to those placeholders and **no formatting is written**, so fonts, colours,
logos and geometry come from the master. ("Reset layout" in PowerPoint changes nothing — that is
the proof.)

Upload such a master as a template (a `.pptx` is stored as type `potx`) — or, if the user attached
it in the chat, use its `librechat_file_id` directly (section 2a).

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
        { "key": "body:10", "type": "body", "hint": "Mastertextformat bearbeiten" },
        { "key": "pic:14", "type": "pic", "isImage": true, "aspectRatio": 1.78 }
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
- **`isImage` slots (`pic:*`) take an image through the separate `images` argument**, not through
  `fields`. `aspectRatio` (width ÷ height of the slot frame) tells you what will crop well — the
  image is centre-cropped to that ratio, never stretched. A slot you pass no image for stays empty
  and comes back in `imageSlotsNotFilled`; don't promise the user a picture then.

### Step 2 — `create_powerpoint_from_layouts`

Each slide picks its layout by `layoutId`, layout name, or role — mix freely.

```json
{
  "template_name": "folienmaster",
  "filename": "strategie-2027",
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
    { "layout": "closing", "fields": { "body:11": "Muster GmbH\n12345 Musterstadt" } }
  ]
}
```

**Images** go in a per-slide `images` object, keyed like `fields` (exact slot key, the bare type
`pic`, or the synonyms `image`/`picture`/`photo`). Sources are the usual three:

```json
{
  "layout": "title-image",
  "fields": { "title": "Standort München" },
  "images": { "pic:14": { "librechat_file_id": "abc-attachment-id" } }
}
```

`{ "document_id": "..." }` (a PVC upload) and `{ "base64": "..." }` work the same way. The
picture inherits its position and size from the layout and is cropped to the slot's aspect ratio.

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
- `drop_template_slides: false` keeps them and appends after them — but the result is saved as a
  **new** document. To grow a deck in place use `add_slides_from_layouts` (step 3).
- Instead of `template_name`, pass `document_id` (a stored `.pptx`) or `librechat_file_id` (an
  attachment) to use that deck as the base. Because layouts survive, a deck built this way can be
  extended later — that is the iterative path for path C.
- `role_map` overrides inference: `{ "content": "slideLayout4.xml" }`.

**Response** reports per slide: `layoutId`, `layoutName`, `filledSlots`, `filledImageSlots`,
`unknownFields`, `emptySlots`. Always check `unknownFields` — a typo'd slot key is reported, not
silently dropped. Picture slots that got no image are listed in `imageSlotsNotFilled` (with a
`note`).

### Step 3 — `add_slides_from_layouts` (grow the deck in place)

The in-place sibling of step 2: same `slides` array, but it targets an existing deck by
`document_id` / `librechat_file_id` and **keeps the same document**. This is how a path-C deck
grows across turns — never re-create the deck to add slides to it.

```json
{
  "document_id": "<id>",
  "slides": [
    { "layout": "Kapiteltrenner", "fields": { "title": "2. Zielbild" } },
    { "layout": "slideLayout11.xml", "fields": { "title": "Roadmap", "body:10": ["Q1", "Q2"] } }
  ]
}
```

- `insert_after: n` places the new slides after slide `n` (`0` = before slide 1). Omit to append.
- Returns `slides_before` / `slides_after` / `slides_added` plus the same per-slide report.
- Refuses a deck whose layouts carry no native placeholders (a Markdown-built deck) and names
  `append_slides_to_powerpoint` instead — nothing is written in that case. It also refuses, without
  writing, when no slot gets filled at all (typically: none of the passed keys matches a slot).

### Step 4 — `set_powerpoint_slide_fields` (patch one slide)

Patches **one** slide in place. Only the slots you pass change; every other slot, shape, image
and the slide's position stay untouched. Slots the layout offers but the slide does not yet carry
are added — including picture slots.

```json
{
  "document_id": "<id>",
  "slide_number": 3,
  "fields": { "title": "Kernbefunde (überarbeitet)", "body:10": ["Neuer Punkt 1", "Neuer Punkt 2"] },
  "images": { "pic:14": { "librechat_file_id": "abc-attachment-id" } }
}
```

Either `fields` or `images` is enough — pass both only when you mean to change both. This is the
tool to call repeatedly across turns while the user reviews the deck. Accepts `librechat_file_id`
too (the attachment is updated on the shared volume when available).

### How a `layout` reference resolves

A slide's `layout` is matched in this order: a `layoutId` → a role (an explicit `role_map` entry
overrides the inferred `roleMap`) → a layout name. `{{slide_type:x}}` markers play no part here;
they only route `repeat` records in `create_powerpoint_from_template` (see **templates-skill**).
**Never ask the user to type `{{}}` markers into a corporate master** — that is exactly what
path C removes.

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

Returns `{ slide_count, hasLegacyPlaceholders, layoutsAvailable, slides: [...] }`, each slide with
`{ slideNumber, title, textLines, layoutId, layoutName, role, slots, emptySlots }`. Use it before
editing a deck you did not just build, and after several appends to confirm numbering.

`slideNumber` is the position **PowerPoint shows** (`sldIdLst` order), not an internal file
number — so it is the number to pass to `set_powerpoint_slide_fields` / `update_powerpoint_slide`
even on a deck whose slides were reordered before it reached us.

The layout fields are what make an unfamiliar deck editable: `layoutId` feeds
`add_slides_from_layouts`, `slots` shows what each slide currently says, and `emptySlots` lists
the keys still free. Pass `include_layouts: false` for a text-only read of a very large deck
(`slideNumber`, `title`, `textLines` only).

---

## 6. Charts and images in slides

- **Chart as its own slide:** `embed_chart_in_document` with `document_type: "powerpoint"` renders
  the chart onto its own slide; with `title` set, a generated title slide comes first, so the deck
  has **two** slides. The result is a deck — keep appending to it with
  `append_slides_to_powerpoint`. Its `id` is a `.pptx`, **not an image**: passed as `doc:<id>` or
  as an image `document_id` it is rejected as "not an image".
- **Chart on a content slide:** take a stored chart image (e.g. an uploaded PNG — its document id)
  and reference it as `![chart](doc:<id>)` in `create_powerpoint` Markdown, through a `{%name}`
  image placeholder in a `{{}}` template, or through a layout picture slot (`images`, path C).
- **Image sources** differ by tool:
  - `create_powerpoint` Markdown: `doc:<documentId>` (stored image), `lc:<file_id>` (LibreChat
    attachment — see `list_my_files`), a base64 data URI or a public http(s) URL.
  - `image` fields in `slides[]`, and Markdown in `append_slides_to_powerpoint` /
    `update_powerpoint_slide`: only a base64 data URI (`data:image/…`) or a public http(s) URL. A
    `doc:`/`lc:` reference is not resolved there — the slide shows an `[Image: …]` text instead.
  - http(s) images must come from a **publicly reachable** host; internal or private addresses
    are refused.
  - `{%name}` template images and layout picture slots (`images`) take
    `{ base64 | document_id | librechat_file_id }`.
- See **charts-diagrams-skill** for chart/diagram creation, **templates-skill** for `{%image}`
  placeholders, `charts` (renames series only — the template's chart data stays) and `repeat`.

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
- **`subtitle` on a master with no `subTitle` placeholder** (common on corporate masters: the
  subtitle line of a title layout is a plain `body` placeholder) falls back to the first free
  `body` slot instead of landing in `unknownFields`.
- **`create_powerpoint_from_template` refuses a template with no `{{}}` placeholders** — when
  `images`, `charts` and `speaker_notes` are also absent — and names the layout tools in the error.
  That is path C's cue, not a broken template — do not retry the legacy tool and do not add `{{}}`
  markers to a corporate master.
- **`pic:*` slots take images via `images`, not `fields`.** A `pic` key inside `fields` fills
  nothing — the slot stays empty.
- **Only `add_slides_from_layouts` keeps the document id** when extending a path-C deck.
  `create_powerpoint_from_layouts` with `drop_template_slides: false` produces a _new_ document —
  useful when the user wants a copy, wrong when they asked to extend what they have.
- **`append_slides_to_powerpoint` on a corporate deck gives you companyFILES-styled slides.** Its
  generated slides carry their own design and are remapped onto the deck's first layout, so on a
  design deck they look off. The response says so in `designNote`; use `add_slides_from_layouts`.
- **Layout names are not unique.** Ambiguous name references resolve to the first match and log a
  warning; use `layoutId`.
- **`list_templates` does not include the layout catalog.** `describe_pptx_template` does.
- **Do not write formatting in path C.** Passing colours/fonts is neither possible nor wanted —
  the master owns the design.
- **Downloads:** every create call, and every append/update/patch call on a companyFILES
  document, returns `{ id, filename, downloadUrl, markdownLink }` (plus `librechat_file_id` when the
  deck is also stored as a chat file). Always render `markdownLink` in the reply. On a chat
  attachment updated in place, the response carries `librechat_file_id`, `filename` and `message`
  but **no** download link — tell the user the attached deck was updated. If the attachment could
  not be updated in place, a new document with its own `id` and `markdownLink` is returned.
- **Theming (path A):** `create_powerpoint` applies the CI from the settings automatically: colours,
  theme fonts, link colour, the company name in the file properties and – on content slides – footer
  text, slide number and the logo (when "logo in documents" is on, at the slide edge of the configured
  logo position; title and section slides stay without). No theme arguments needed.
- **Path B (templates):** only `{{company_name}}` is auto-filled (from the company name in settings);
  a logo needs a `{%logo}` image placeholder and an explicit `images` entry. Path C writes no
  formatting; the template defines the look.

---

## 8. End-to-end test drive

A single run that exercises every slide feature. Useful for verifying a deployment.

**Path A — scratch deck, built iteratively**

1. `create_powerpoint` — no `title` argument, 3 slides: `section`, `default` (bullets +
   `htmlTable` with coloured cells), `text-image` **without** `image` → expect a skeleton box.
   → 3 slides, note `document_id`. (Repeat once **with** `title` to confirm the generated title
   slide appears and shifts numbering to 4.)
2. `append_slides_to_powerpoint` — `slides`: a `default` with a `code` block and a `table`, plus
   a `text-image` **with** `image` set to a base64 data URI. → same `document_id`, 5 slides.
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
10. `add_slides_from_layouts` with that `document_id` → **same** `document_id`, 6 slides, the new
    one in the same corporate design. Repeat with `insert_after: 1` → the slide lands at
    position 2.
11. `set_powerpoint_slide_fields` with `images: { "pic:14": { "librechat_file_id": "<png>" } }` on
    a title-image slide → the picture fills the placeholder frame, cropped not stretched, and
    the response's `slide.filledImageSlots` lists `pic:14`.

**Path D — a deck attached in the chat**

12. Attach a `.pptx` to a chat message → `list_my_files` shows it with a `file_id`.
13. `describe_pptx_template { "librechat_file_id": "<file_id>" }` → the same catalog as step 7,
    without any template upload.
14. `read_powerpoint_slides { "librechat_file_id": "<file_id>" }` → slides in the order
    PowerPoint shows them, each with `layoutId` and `slots`.
15. `add_slides_from_layouts` against that `file_id` → the response's `message` says the attachment
    was updated in place (same `file_id`, `librechat_file_id` in the response) or that the modified
    copy was saved as a new document (new `id` and `markdownLink`).

**Error paths**

16. `"layout": "GibtsNicht"` → error listing all layouts **and** roles.
17. `fields: { "untertitel": "x" }` on a layout without that slot → `unknownFields: ["untertitel"]`.
18. `slide_number: 99` on `set_powerpoint_slide_fields` → error naming the real slide count.
19. `reference_slide` together with `slides` → error.
20. A deck **with** `{{}}` markup through `describe_pptx_template` →
    `hasLegacyPlaceholders: true` → switch to `create_powerpoint_from_template`.
21. `add_slides_from_layouts` on a deck built by `create_powerpoint` → error naming
    `append_slides_to_powerpoint`, and the deck's slide count is unchanged.
22. `add_slides_from_layouts` with `insert_after` beyond the slide count → error naming the real
    count.

`MANUAL_TESTS.md` §4.6 (corporate master) and §4.9 (deck attached in the chat) hold these
scenarios as ready-to-run cURL commands.
