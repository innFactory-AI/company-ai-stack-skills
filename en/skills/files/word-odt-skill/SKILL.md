---
name: word-odt-skill
description: 'Create and read Word (.docx) and ODT (.odt) documents with companyFILES MCP tools. Use when asked to write a report, letter, or document in Word or OpenDocument format, convert Markdown or HTML to Word/ODT, extract text from a Word file, or create a document with headers, footers, table of contents, or page numbers.'
---

# Word & ODT Skill

Tools for creating Word (.docx) and ODT (.odt) documents, plus reading Word files.

## Tools in This Skill

| Tool                    | Purpose                                                                         |
| ----------------------- | ------------------------------------------------------------------------------- |
| `create_word`           | Create Word (.docx) from Markdown or plain text                                 |
| `create_word_from_html` | Create Word from HTML with optional CSS                                         |
| `create_word_from_json` | Dump JSON data into Word as a plain key/value listing                           |
| `create_odt`            | Create ODT from Markdown (LibreOffice/OpenOffice)                               |
| `create_odt_from_html`  | Create ODT from HTML                                                            |
| `read_word`             | Read a Word (.docx) file → text, HTML, Markdown (from base64 or LibreChat file) |
| `read_word_content`     | Read stored Word document content by document_id → markdown-like string         |
| `append_to_word`        | Append Markdown content to an existing stored Word document in-place            |
| `replace_word_content`  | Replace entire content of an existing stored Word document in-place             |

## Decision Guide

```
User wants to create a Word document from...
  Markdown / plain text  → create_word          (most common)
  HTML + CSS             → create_word_from_html
  Raw JSON data (dump)   → create_word_from_json  (no layout control)
  A template             → see templates-skill   (create_word_from_template)

User wants OpenDocument format (LibreOffice)...
  From Markdown          → create_odt
  From HTML              → create_odt_from_html
  From template          → see templates-skill   (create_odt_from_template)

User wants to READ a Word file...
  From base64 / LibreChat attachment  → read_word
  From stored document (document_id)  → read_word_content

User wants to EDIT an existing stored Word document...
  Inspect current content first       → read_word_content
  Add more content at the end         → append_to_word    (keeps existing content)
  Rewrite the whole document          → replace_word_content
```

## Tool Usage

### create_word

```json
{
  "content": "# Annual Report\n\n## Summary\n\nThis year we achieved...",
  "filename": "annual_report",
  "title": "Annual Report 2025",
  "page_size": "A4",
  "page_orientation": "portrait",
  "header_text": "Confidential",
  "footer_text": "Acme Corp",
  "show_page_numbers": true,
  "page_number_position": "footer",
  "page_number_format": "{page} / {pages}",
  "include_toc": true
}
```

`format` can be `"markdown"` (default) or `"plain"`. Note: `create_word` has **no `author` field** — only `create_word_from_html`, `create_odt` and `create_odt_from_html` accept `author`.

### create_word_from_html

```json
{
  "html": "<h1>Report</h1><p>Content here.</p><table>...</table>",
  "css": "h1 { color: #336699; } body { font-family: Arial; }",
  "filename": "report",
  "title": "My Report",
  "show_page_numbers": true
}
```

Supports inline images via `doc:<documentId>` (stored companyFILES doc) or `lc:<file_id>` (LibreChat attachment) URI: `<img src="doc:abc123..." />`. The same syntax works in Markdown for `create_word`: `![alt](doc:<uuid>)` or `![alt](lc:<file_id>)`.

### create_word_from_json

```json
{
  "json_content": "{\"customer\":\"Acme Corp\",\"items\":[{\"name\":\"Widget\",\"qty\":2}]}",
  "filename": "order_data"
}
```

Writes the JSON as a simple listing under the heading "Document Generated from JSON": one paragraph per field (`key: value`, key in bold); nested objects and arrays are indented, array items appear as `[0]`, `[1]`, …. There is no element schema (no headings, tables or styling from JSON) and no title, author or page options — only `json_content` and `filename`. For a designed document, turn the data into Markdown and use `create_word`.

### create_odt

```json
{
  "content": "# Letter\n\nDear John,\n\nPlease find enclosed...",
  "filename": "letter",
  "title": "Formal Letter",
  "author": "Jane",
  "page_size": "A4",
  "header_text": "Private & Confidential",
  "show_page_numbers": true
}
```

### create_odt_from_html

```json
{
  "html": "<h1>Document</h1><p>Content</p>",
  "filename": "document",
  "page_size": "A4"
}
```

### read_word

```json
{
  "file_content": "<base64-encoded docx>"
}
```

Accepts any one of `file_content` (base64), `librechat_file_id` (LibreChat attachment), or `document_id` (stored companyFILES doc). Returns `{ text, html, markdown }`.

### read_word_content

Read the content of a stored Word document (created or uploaded via companyFILES). Accepts `document_id` **or** `librechat_file_id`. Returns a markdown-like string plus character count — use this before appending or replacing to understand the current state.

```json
{
  "document_id": "uuid-of-stored-word-doc"
}
```

Returns `{ document_id, librechat_file_id, filename, character_count, content }`.

### append_to_word

Append Markdown (or plain text) to an existing Word document. Identify the target with `document_id` **or** `librechat_file_id`. A page break is inserted before the new content by default. The document is updated in-place — same `document_id`.

```json
{
  "document_id": "uuid-of-stored-word-doc",
  "content": "## New Section\n\nAdditional content here...",
  "format": "markdown",
  "add_page_break": true
}
```

`add_page_break` defaults to `true`. Use `false` to continue on the same page.

### replace_word_content

Replace the entire content of an existing Word document with new Markdown. Identify the target with `document_id` **or** `librechat_file_id`. All page layout options (`page_size`, `header_text`, etc.) work the same as `create_word`. The document is updated in-place — same `document_id`.

```json
{
  "document_id": "uuid-of-stored-word-doc",
  "content": "# Updated Report\n\nFully rewritten content...",
  "format": "markdown",
  "page_size": "A4",
  "header_text": "Confidential",
  "show_page_numbers": true
}
```

## Common Page Options (all create tools except `create_word_from_json`)

| Parameter               | Values                              | Default            |
| ----------------------- | ----------------------------------- | ------------------ |
| `page_size`             | `A4`, `Letter`, `Legal`, `A3`, `A5` | `A4`               |
| `page_orientation`      | `portrait`, `landscape`             | `portrait`         |
| `page_number_position`  | `header`, `footer`                  | `footer`           |
| `page_number_alignment` | `left`, `center`, `right`           | `center`           |
| `page_number_format`    | string with `{page}` and `{pages}`  | `{page} / {pages}` |

## Iterative Document Editing Pattern

For long documents that exceed a single context window, build them section by section:

1. `create_word` — create the document with the first section; note the returned `id` (pass it as `document_id`)
2. `append_to_word` — call repeatedly for each additional section
3. Optionally `read_word_content` to inspect the current state before continuing
4. `replace_word_content` — if a section needs to be fully rewritten

All three in-place tools (`read_word_content`, `append_to_word`, `replace_word_content`) operate on existing documents identified by `document_id` **or** `librechat_file_id` (a LibreChat attachment, updated in-place on the shared volume), not on base64 file content.

## Key Notes

- All create tools return `{id, filename, downloadUrl, markdownLink}` (plus `librechat_file_id` when the document is also stored as a chat file) — always render `markdownLink` in the reply.
- In-place edit tools (`append_to_word`, `replace_word_content`) on a companyFILES document return the same `id` and an updated `markdownLink`. On a chat attachment (`librechat_file_id`) that was updated in place, they return only `{librechat_file_id, filename, message}` — there is no download link; tell the user the attached file was updated. If the attachment cannot be updated in place, the modified copy is saved as a **new** document and its new `id`/`markdownLink` is returned — use that id from then on.
- Inline images can be referenced via `doc:<documentId>` or `lc:<file_id>` in the Markdown or HTML of the create tools (`create_word`, `create_word_from_html`, `create_odt`, `create_odt_from_html`) — SVG is auto-converted to PNG for Word. `append_to_word` and `replace_word_content` do not resolve these references.
- Unset page/header/footer options fall back to the org/user theme defaults (e.g. `defaultPageSize`, `defaultHeaderText`, `defaultShowPageNumbers`) before the documented hard defaults apply.
- For template-based Word creation (placeholders, loops, image injection), use the **templates-skill**.
- ODT files open natively in LibreOffice and Google Docs.
- The org/user CI is applied automatically when configured: colours, fonts and sizes, page format, header/footer, page numbers and the logo at the configured position (header or footer, left/center/right). For a document you build yourself with code execution, `get_corporate_ci` returns the same values.
