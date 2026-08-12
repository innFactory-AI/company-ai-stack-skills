---
name: settings-ui-skill
description: Open the companyFILES web UI, view settings, and get help on available tools. Use when asked to show documents, browse files, open the file manager, manage templates, change settings, view branding/colors, or get help on how to use companyFILES tools. Also use when the user wants an interactive embedded view instead of raw JSON.
---

# Settings & UI Skill

Tools for opening the companyFILES web app as an embedded UI, retrieving settings, and getting tool help.

## Tools in This Skill

| Tool | Purpose |
|------|---------|
| `open_companyfiles_ui` | Open the companyFILES web app as an embedded iframe |
| `get_settings` | Get resolved org/user settings (colors, company name, logo) |
| `help` | Get usage examples for any companyFILES tool category |

## Decision Guide

```
User says "show my files" / "open file manager"    → open_companyfiles_ui page="documents"
User says "manage / browse templates"               → open_companyfiles_ui page="templates"
User says "upload a file" (via UI)                  → open_companyfiles_ui page="documents"
User says "open settings" / "change preferences"   → open_companyfiles_ui page="settings"

User asks about settings / colors / logo            → get_settings
User asks how to use a tool / needs examples        → help (with topic)
```

**Always call the tool immediately — never just describe what the user could do.**

## Tool Usage

### open_companyfiles_ui

Renders the companyFILES SPA as an embedded interactive iframe in the chat.

```json
{
  "page": "documents"
}
```

Available pages (enum — only these four values are accepted):
| Page | Shows |
|------|-------|
| `documents` | File list, upload, download, folder navigation |
| `templates` | Template browser, upload personal templates |
| `upload` | File upload view |
| `settings` | Org/user branding, colors, logo, language |

> Note: UI widgets require a chat client that supports MCP UI rendering (e.g. LibreChat). Google Gemini falls back to text.

---

### get_settings

Returns the resolved settings: org defaults merged with user overrides.

```json
{}
```

Example response:
```json
{
  "companyName": "Acme Corp",
  "companyUrl": "https://acme.com",
  "primaryColor": "#336699",
  "secondaryColor": "#66aacc",
  "accentColor": "#ff6600",
  "hasLogo": true,
  "sources": {"companyName": "org", "primaryColor": "user"}
}
```

`logoPath` is intentionally omitted (internal filesystem path). To view or change the logo, use `open_companyfiles_ui page="settings"`.

---

### help

Get detailed usage examples for a specific tool category.

```json
{
  "topic": "excel"
}
```

Available topics: `excel`, `word`, `pdf`, `powerpoint`, `text`, `chart`, `mermaid`, `zip`, `assets`, `upload`, `templates`, `admin`, `settings`, `convert`, `read`, `ui`, `all`

Omitting `topic` (or using `"all"`) returns the full help document and also opens the embedded UI.

## Key Notes

- `open_companyfiles_ui` is the default tool for any request to browse, view, or manage files/templates/settings interactively.
- Settings colors (`primaryColor`, `secondaryColor`, `accentColor`) are automatically used as the theme in all document and chart creation tools. `get_settings` only returns this core subset; the full settings model holds many more org/user-overridable fields that also feed generated documents — extended colors (`headingColor`, `bodyTextColor`, `linkColor`, `tableHeaderBg`, `tableHeaderText`, `codeBg`), typography (`fontHeading`, `fontBody`, `fontCode`, `fontSize*`), and document defaults (`defaultPageSize`, `defaultPageOrientation`, `defaultHeaderText`, `defaultFooterText`, `defaultShowPageNumbers`, `defaultPageNumberPosition`, `defaultPageNumberFormat`, `logoInHeader`, `logoHeaderHeight`).
- To edit settings, use the UI (`open_companyfiles_ui page="settings"`) or, for admins, `PUT /api/ui/admin/settings` (gated by an admin UI session/bearer token — the legacy `X-API-Key` admin routes were removed).
