---
name: charts-diagrams-skill
description: Create interactive charts and diagrams with companyFILES MCP tools. Use when asked to visualize data, create a bar/line/pie/scatter/bubble chart, draw a flowchart, sequence diagram, ER diagram, Gantt chart, or any Mermaid diagram. Also covers embedding charts or diagrams into Word, PDF, or PowerPoint documents.
---

# Charts & Diagrams Skill

Tools for creating interactive charts (Chart.js) and diagrams (Mermaid), plus embedding them in documents.

## Tools in This Skill

| Tool | Purpose |
|------|---------|
| `show_interactive_chart` | **PREFERRED** — Interactive Chart.js widget (zoom, pan, type switch, export) |
| `show_interactive_diagram` | **PREFERRED** — Interactive Mermaid diagram widget (pan, zoom, export) |
| `create_chart_document` | Embed a chart image in a Word, PDF, or PowerPoint document |
| `embed_chart_in_document` | Render a Chart.js chart and embed it in a document |

## Decision Guide

```
User wants to SEE a chart in chat            → show_interactive_chart   (ALWAYS preferred)
User wants to SEE a diagram in chat          → show_interactive_diagram  (ALWAYS preferred)

User wants to SAVE a chart as a document...
  Chart + optional description text          → create_chart_document
  Chart embedded in a doc (more control)     → embed_chart_in_document

User wants to SAVE a diagram as a document   → see word-odt-skill or pdf-skill
  (render diagram first, then embed manually, or describe in Markdown)
```

## Tool Usage

### show_interactive_chart (PREFERRED for charts)

Supported chart types: `bar`, `line`, `pie`, `doughnut`, `radar`, `scatter`, `bubble`, `polarArea`, `waterfall`, `funnel`, `area`, `stackedBar`, `horizontalBar`

```json
{
  "chart_type": "bar",
  "labels": ["Q1", "Q2", "Q3", "Q4"],
  "datasets": [
    { "label": "Revenue", "data": [100, 150, 120, 180] },
    { "label": "Costs", "data": [80, 110, 90, 140] }
  ],
  "title": "Quarterly Performance",
  "x_axis_label": "Quarter",
  "y_axis_label": "EUR"
}
```

Optional: `x_axis_label`, `y_axis_label`, and `options` (a raw Chart.js options object merged over the defaults). Datasets also accept `borderWidth` and `fill`.

**Scatter chart** (use `{x, y}` data points):

```json
{
  "chart_type": "scatter",
  "labels": [],
  "datasets": [
    {
      "label": "Points",
      "data": [
        { "x": 1, "y": 2 },
        { "x": 3, "y": 4 }
      ]
    }
  ]
}
```

**Bubble chart** (add `r` for radius):

```json
{
  "chart_type": "bubble",
  "labels": [],
  "datasets": [
    {
      "label": "Bubbles",
      "data": [
        { "x": 1, "y": 2, "r": 10 },
        { "x": 3, "y": 4, "r": 5 }
      ]
    }
  ]
}
```

The widget includes: zoom/pan, chart type switcher, export (PNG at 1x/2x/4x, JPG, SVG, CSV), and clipboard copy.

---

### show_interactive_diagram (PREFERRED for diagrams)

Supported diagram types (Mermaid syntax): flowchart, sequence, class, state, ER, Gantt, pie, mindmap, timeline, and more.

```json
{
  "code": "graph TD\n  A[Start] --> B{Decision}\n  B -->|Yes| C[Do this]\n  B -->|No| D[Do that]\n  C --> E[End]\n  D --> E",
  "title": "Decision Flow",
  "theme": "default"
}
```

The Mermaid source goes in the **`code`** parameter (not `mermaid_code`).

**Themes:** `default`, `dark`, `forest`, `neutral`

The widget includes: pan/zoom, SVG export, PNG export (1x/2x/4x), and "Copy Mermaid Code".

---

### create_chart_document

Renders a chart image and embeds it in a document with an optional description below.

Supports extended chart types: `bar`, `line`, `pie`, `doughnut`, `radar`, `scatter`, `bubble`, `polarArea`, `waterfall`, `funnel`, `area`, `stackedBar`, `horizontalBar`

```json
{
  "chart_type": "line",
  "labels": ["Jan","Feb","Mar","Apr","May"],
  "datasets": [{"label": "Sales", "data": [50,70,65,90,110]}],
  "title": "Monthly Sales Trend",
  "description": "Sales grew steadily throughout Q1 and Q2.",
  "output_format": "word",
  "filename": "sales_trend",
  "folder": "reports"
}
```

`output_format` options: `word` (default), `pdf`, `powerpoint`

---

### embed_chart_in_document

More control over chart dimensions when embedding.

Supported types: `bar`, `line`, `pie`, `doughnut`, `radar`, `scatter`, `bubble`, `polarArea`

```json
{
  "chart_type": "bar",
  "labels": ["Q1","Q2","Q3","Q4"],
  "datasets": [{"label": "Revenue", "data": [100,150,120,180]}],
  "document_type": "pdf",
  "title": "Quarterly Revenue",
  "width": 1400,
  "height": 900,
  "filename": "revenue_chart",
  "folder": "finance"
}
```

`document_type` options: `word`, `powerpoint`, `pdf`

## Key Notes

- `show_interactive_chart` and `show_interactive_diagram` return a **widget** (rendered in LibreChat) plus a static image fallback — include the markdown image in your reply.
- Document-embedding tools return `{id, filename, downloadUrl, markdownLink}` — always render `markdownLink`.
- The org/user color palette is automatically applied to chart colors when configured in settings.
- Google Gemini models cannot render interactive widgets — responses fall back to text/JSON data.
- `show_interactive_chart` and `create_chart_document` accept all 13 chart types; `area`, `stackedBar`, `horizontalBar` are mapped to their static equivalents when rendering as images. `embed_chart_in_document` only accepts the 8 base types and rejects the extended ones — use `create_chart_document` for those.
