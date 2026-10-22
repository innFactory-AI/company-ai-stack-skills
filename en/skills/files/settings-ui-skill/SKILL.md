---
name: settings-ui-skill
description: 'Open the companyFILES web UI, view settings, and get help on available tools. Use when asked to show documents, browse files, open the file manager, manage templates, change settings, view branding/colors, or get help on how to use companyFILES tools. Also use when the user wants an interactive embedded view instead of raw JSON.'
---

# Settings & UI Skill

Tools for opening the companyFILES web app as an embedded UI, retrieving settings, and getting tool help.

## Tools in This Skill

| Tool                   | Purpose                                                     |
| ---------------------- | ----------------------------------------------------------- |
| `open_companyfiles_ui` | Open the companyFILES web app as an embedded iframe         |
| `get_settings`         | Get resolved org/user settings (colors, company name, logo) |
| `help`                 | Get usage examples for any companyFILES tool category       |

## Decision Guide

```
User says "show my files" / "open file manager"    → open_companyfiles_ui page="documents"
User says "manage / browse templates"               → open_companyfiles_ui page="templates"
User says "upload a file" (via UI)                  → open_companyfiles_ui page="documents"
User says "upload a template" (via UI)              → open_companyfiles_ui page="upload"
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
| `documents` | Document list (including chat uploads), file upload, preview, download |
| `templates` | Template browser, upload personal templates |
| `upload` | Template upload form (upload a new template) |
| `settings` | Tabs **My Settings** (Meine Einstellungen: personal colors, typography, document defaults, logo) and **Organization** (Organisation: company info, org colors and logo — read-only without the admin permission; admins also edit org typography and document defaults) |

The settings page has no language setting — the language is switched in the account menu of the companyFILES web app. The web app's **Visualizations** page (charts, diagrams and maps from the chat) is not one of the page values and cannot be opened with `open_companyfiles_ui`.

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
  "sources": { "companyName": "org", "primaryColor": "user" }
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

Available topics: `excel`, `word`, `pdf`, `powerpoint`, `text`, `chart`, `mermaid`, `map`, `zip`, `upload`, `templates`, `admin`, `convert`, `read`, `settings`, `assets`, `ui`, `provenance` (AI marking in file metadata), `all` — plus `cad` and `docs` where those extensions are available. An unknown topic returns the list of available topics.

Omitting `topic` (or using `"all"`) returns the full help document and also opens the embedded UI.

## Key Notes

- `open_companyfiles_ui` is the default tool for any request to browse, view, or manage files/templates/settings interactively.
- Settings colors (`primaryColor`, `secondaryColor`, `accentColor`) are automatically used as the theme in all document and chart creation tools. `get_settings` only returns this core subset; the full settings model holds many more org/user-overridable fields that also feed generated documents — extended colors (`headingColor`, `bodyTextColor`, `linkColor`, `tableHeaderBg`, `tableHeaderText`, `codeBg`), typography (`fontHeading`, `fontBody`, `fontCode`, `fontSize*`), and document defaults (`defaultPageSize`, `defaultPageOrientation`, `defaultHeaderText`, `defaultFooterText`, `defaultShowPageNumbers`, `defaultPageNumberPosition`, `defaultPageNumberFormat`, `logoInHeader`, `logoHeaderHeight`).
- To edit settings, use the UI (`open_companyfiles_ui page="settings"`): personal values on **My Settings**, organization values on **Organization**. Changing organization settings and branding requires the companyFILES admin permission (`ext:files:admin`); uploading or promoting global templates requires the template permission (`ext:files:templates`). Users without these permissions manage only their personal settings and templates.
