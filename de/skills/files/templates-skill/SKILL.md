---
name: templates-skill
description: 'Create documents from templates using companyFILES MCP tools. Use when asked to fill a template, use a company template, create a document from a predefined layout, fill placeholders, use a letterhead, fill an invoice template, or create from a DOCX/XLSX/POTX/ODT template. Covers Word, Excel, ODT, and PowerPoint template filling, including image placeholders and loop/repeat syntax.'
---

# Templates Skill

Tools for listing and filling document templates (Word, Excel, ODT, PowerPoint).

## Tools in This Skill

| Tool                                    | Purpose                                                                           |
| --------------------------------------- | --------------------------------------------------------------------------------- |
| `list_templates`                        | List all available templates (personal + global) with placeholder info            |
| `create_word_from_template`             | Fill a DOCX template with `{placeholder}` syntax                                  |
| `create_word_from_template_with_images` | Fill a DOCX template with text and image placeholders                             |
| `create_excel_from_template`            | Fill an XLSX template by cell address **or** `{{placeholder}}` name (auto-routed) |
| `fill_excel_template`                   | Fill an XLSX template using `{{placeholder}}` syntax                              |
| `create_odt_from_template`              | Fill an ODT template with `{{placeholder}}` syntax                                |
| `create_powerpoint_from_template`       | Fill a POTX/PPTX template with text, images, charts, speaker notes, slide repeat  |

## Workflow

1. **Discover templates:** Call `list_templates` (optionally filter by `type`: `docx`, `xlsx`, `potx`, `odt`, `pdf`)
2. **Note placeholder names** from the response
3. **Fill the template** with the matching `create_*_from_template` tool

## Tool Usage

### list_templates

```json
{
  "type": "potx"
}
```

Returns per template: `name`, `displayName`, `description`, `category`, `tags`, placeholder lists, `loopSources`, `fields` (for PDF form templates), `size`, `isDefault`, upload dates, and scope (`"user"` personal or `"global"`).

For **POTX/PPTX** templates the response includes a per-slide breakdown:

- `slideNumber` — 1-based slide index
- `layoutName` — PowerPoint layout name (e.g. `"Title Slide"`, `"Two Content"`)
- `layoutType` — value from a `{{slide_type:xxx}}` marker on that slide (e.g. `"section"`, `"default"`, `"text-image"`)
- `textPlaceholders` — `{{key}}` placeholders on this slide
- `imagePlaceholders` — `{%name}` placeholders on this slide
- `chartPlaceholders` — `{{name}}` chart container placeholders on this slide

Use this breakdown to know exactly which placeholder goes on which slide before calling `create_powerpoint_from_template`. Filter by `type` to narrow results: `"docx"`, `"xlsx"`, `"potx"`, `"odt"`, `"pdf"`.

---

### create_word_from_template

Placeholder syntax: `{placeholder}` (single curly braces). Dotted paths: `{user.name}`.

```json
{
  "template_name": "invoice",
  "data": {
    "customer": "Acme Corp",
    "invoice_number": "INV-2025-042",
    "date": "2025-05-08",
    "total": "€4,200.00"
  },
  "filename": "invoice_acme",
  "folder": "invoices"
}
```

**Table loop syntax** (place FOR/END-FOR in their own table rows):

```
{FOR item IN items}
{= $item.name} | {= $item.qty} | {= $item.price}
{END-FOR item}
```

Pass `items` as an array in `data`. Missing loop sources are silently skipped with a warning.

---

### create_word_from_template_with_images

Supports text placeholders `{name}` and image placeholders `{%logo}`.

```json
{
  "template_name": "letterhead",
  "placeholders": {
    "company": "Acme Corp",
    "date": "2025-05-08",
    "logo": {
      "data": "<base64-encoded image>",
      "width": 4,
      "height": 2,
      "extension": "png"
    }
  },
  "filename": "letter_acme",
  "folder": "letters"
}
```

Image via stored document (no re-upload needed):

```json
{
  "logo": {
    "document_id": "abc12345-...",
    "width": 4,
    "height": 2
  }
}
```

The org/user logo is **auto-injected** only into a placeholder named exactly `logo` (i.e. `{%logo}`) — and only when configured in settings and no `logo` value is passed. Differently-named image placeholders (e.g. `{%companyLogo}`) are **not** auto-filled.

---

### create_excel_from_template

Accepts **either** cell addresses (e.g. `"A1"`, `"Sheet2!B3"`) **or** `{{placeholder}}` names (pass the bare name without `{{ }}`) in `cell_values` — it auto-routes based on the keys you pass; mixed keys default to placeholder mode. Use `list_templates` to see available XLSX templates.

```json
{
  "template_name": "budget",
  "cell_values": {
    "A1": "Budget 2025",
    "B5": 125000,
    "Sheet2!C3": "Approved"
  },
  "filename": "budget_2025",
  "folder": "finance"
}
```

---

### fill_excel_template

Fills cells using `{{placeholder}}` syntax — preserves formatting, styles, formulas, and charts.

```json
{
  "template_name": "monthly_report",
  "data": {
    "company": "Acme Corp",
    "month": "May 2025",
    "total": 42000
  },
  "replace_missing": false,
  "filename": "report_may"
}
```

---

### create_odt_from_template

Fills `{{placeholder}}` syntax in ODT templates.

```json
{
  "template_name": "letter",
  "data": {
    "recipient": "John Doe",
    "date": "2025-05-08",
    "subject": "Offer Letter"
  },
  "replace_missing": false,
  "filename": "offer_letter_john"
}
```

---

### create_powerpoint_from_template

Placeholder syntax:

- **Text:** `{{key}}` anywhere in a text box
- **Image:** `{%name}` in the **alt text** (`descr` attribute) of an image shape
- **Chart:** `{{name}}` in the **alt text** of a chart container shape
- **Layout marker:** `{{slide_type:default}}`, `{{slide_type:section}}`, `{{slide_type:text-image}}` — invisible metadata marker; declares the slide's role. Cleared automatically from the output.

Always run `list_templates` first — for POTX/PPTX it returns a per-slide breakdown including `layoutName`, `layoutType` (from the `{{slide_type:xxx}}` marker), and which text/image/chart placeholders belong to each slide.

> **If the POTX/PPTX template has NO placeholders**, this tool refuses the call and names the layout tools instead — `list_templates` flags such templates with `hasLegacyPlaceholders: false` and a `nextStep` hint. Corporate-design slide masters (Folienmaster) shipped by design teams usually contain no `{{}}` markup at all — they carry named slide layouts instead. Run `describe_pptx_template { "template_name": "..." }`: when `hasLegacyPlaceholders` is `false`, switch to `create_powerpoint_from_layouts` (see **powerpoint-skill**, "corporate master without `{{}}`"). Never ask the user to type `{{}}` markers into a corporate master.

**Basic usage (single-record fill):**

```json
{
  "template_name": "corporate_deck",
  "placeholders": {
    "title": "Q4 Results",
    "subtitle": "Finance Team",
    "date": "May 2025"
  },
  "images": {
    "logo": { "base64": "<base64-png>" },
    "chart_screenshot": { "document_id": "abc123..." }
  },
  "speaker_notes": {
    "1": "Welcome everyone to the Q4 review",
    "3": "These are the key takeaways"
  },
  "charts": {
    "revenue_chart": {
      "labels": ["Q1", "Q2", "Q3", "Q4"],
      "datasets": [{ "label": "Revenue", "values": [100, 150, 120, 180] }]
    }
  },
  "filename": "q4_deck",
  "folder": "presentations"
}
```

`speaker_notes` keys are **1-based** slide numbers.

**Single-source repeat** (duplicate one slide per data record):

```json
{
  "template_name": "team_deck",
  "repeat": {
    "slide": 3,
    "data": [
      { "name": "Alice", "role": "Engineer" },
      { "name": "Bob", "role": "Designer" }
    ]
  }
}
```

`repeat.slide` is the 1-based slide number to duplicate; the slide is replaced by N copies, one per data record. By default, slides that are **not** repeated are removed from the output — set `repeat.keep_unused_slides: true` to keep them. `create_powerpoint_from_template` also accepts top-level `title` and `author`.

**Multi-source repeat** (route each record to the slide matching its `slide_type`):

Use this when the template has multiple layout slides marked with `{{slide_type:xxx}}` and each data record should use a different layout.

```json
{
  "template_name": "dynamic_deck",
  "repeat": {
    "data": [
      { "slide_type": "section", "title": "Chapter 1" },
      { "slide_type": "default", "title": "Results", "content": "Revenue up 15%" },
      { "slide_type": "text-image", "title": "Architecture", "bullets": "Fast\nScalable" }
    ]
  }
}
```

Omit `repeat.slide` when using `slide_type` routing — the matching template slide is found automatically from its `{{slide_type:xxx}}` marker. The `slide_type` values (`default`, `section`, `text-image`) correspond to the same layout names used in `create_powerpoint`.

## Post-Template Editing (Iterative Updates)

Every template tool returns a `document_id`. That ID can be passed directly to the iterative editing tools from **word-odt-skill** and **powerpoint-skill** to further modify the filled document without regenerating from scratch.

### After `create_word_from_template` / `create_word_from_template_with_images`

| Goal                         | Tool                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------ |
| Inspect current content      | `read_word_content { "document_id": "<id>" }`                                        |
| Add more sections at the end | `append_to_word { "document_id": "<id>", "content": "...", "add_page_break": true }` |
| Fully rewrite the document   | `replace_word_content { "document_id": "<id>", "content": "..." }`                   |

Example — fill a template then append a custom appendix:

```json
// Step 1: fill the template
{ "template_name": "report", "data": { "title": "Annual Report" } }
// → returns document_id "abc123"

// Step 2: append extra content
{ "document_id": "abc123", "content": "## Appendix A\n\nAdditional data...", "add_page_break": true }
```

### After `create_powerpoint_from_template`

| Goal                                  | Tool                                                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Inspect existing slides               | `read_powerpoint_slides { "document_id": "<id>" }`                                                                  |
| Add new slides at the end             | `append_slides_to_powerpoint { "document_id": "<id>", "slides": [...] }`                                            |
| Replace a specific slide              | `update_powerpoint_slide { "document_id": "<id>", "slide_number": 3, "slides": [...] }`                             |
| **Add a slide matching the template** | `append_slides_to_powerpoint { "document_id": "<id>", "reference_slide": 2, "placeholders": {...} }`                |
| **Replace a slide, keep the look**    | `update_powerpoint_slide { "document_id": "<id>", "slide_number": 3, "reference_slide": 2, "placeholders": {...} }` |

> **Keep the template look:** appending/updating with `slides`/`markdown` renders the generic theme, which will **not** match a template deck. Use `reference_slide` + `placeholders` (clone-and-refill) instead — it copies an existing slide's design and refills its `{{placeholders}}`. See **powerpoint-skill** for full details. (Clone mode refills text placeholders only; for image placeholders re-run `create_powerpoint_from_template`.)

Example — fill a template then append a custom closing slide:

```json
// Step 1: fill the template
{ "template_name": "corporate_deck", "placeholders": { "title": "Q4 Results" } }
// → returns document_id "def456"

// Step 2a: add a generic (non-template-styled) closing slide
{ "document_id": "def456", "slides": [{ "type": "section", "title": "Thank You", "subtitle": "Questions?" }] }

// Step 2b: OR add a slide that matches the template by cloning slide 2 and refilling it
{ "document_id": "def456", "reference_slide": 2, "placeholders": { "title": "Next Steps", "owner": "PMO" } }
```

## Key Notes

- All create tools return `{id, filename, downloadUrl, markdownLink}` — always render `markdownLink` in the reply.
- When `folder` is omitted, the filled document is filed under a folder named after `template_name`.
- `create_word_from_template_with_images` falls back to a global `default.docx` if the named template is missing, whereas `create_word_from_template` does not — verify the template exists with `list_templates` first.
- Template names are **case-sensitive** — always verify with `list_templates` first.
- User templates take priority over global templates with the same name.
- `replace_missing: false` (default) leaves unfilled `{{placeholder}}` tokens intact; `true` replaces them with empty string.
- Warnings about missing placeholders are included in the response when applicable.
- After filling a template, use the iterative tools (`append_to_word`, `append_slides_to_powerpoint`, etc.) to add or update content — the `document_id` stays the same throughout.
