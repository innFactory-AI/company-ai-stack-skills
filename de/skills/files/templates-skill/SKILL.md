---
name: templates-skill
description: 'Create documents from templates using companyFILES MCP tools. Use when asked to fill a template, use a company template, create a document from a predefined layout, fill placeholders, use a letterhead, fill an invoice template, or create from a DOCX/XLSX/POTX/ODT template. Covers Word, Excel, ODT, and PowerPoint template filling, including image placeholders and loop/repeat syntax.'
---

# Vorlagen-Skill

Tools zum Auflisten und Ausfüllen von Dokumentvorlagen (Word, Excel, ODT, PowerPoint).

## Tools in diesem Skill

| Tool                                    | Zweck                                                                                             |
| --------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `list_templates`                        | Alle verfügbaren Vorlagen (persönlich + global) mit Platzhalter-Infos auflisten                   |
| `create_word_from_template`             | DOCX-Vorlage mit `{placeholder}`-Syntax ausfüllen                                                 |
| `create_word_from_template_with_images` | DOCX-Vorlage mit Text- und Bildplatzhaltern ausfüllen                                             |
| `create_excel_from_template`            | XLSX-Vorlage per Zelladresse **oder** `{{placeholder}}`-Name ausfüllen (automatisches Routing)    |
| `fill_excel_template`                   | XLSX-Vorlage mit `{{placeholder}}`-Syntax ausfüllen                                               |
| `create_odt_from_template`              | ODT-Vorlage mit `{{placeholder}}`-Syntax ausfüllen                                                |
| `create_powerpoint_from_template`       | POTX/PPTX-Vorlage mit Text, Bildern, Diagrammen, Sprechernotizen und Folienwiederholung ausfüllen |

## Ablauf

1. **Vorlagen ermitteln:** Rufe `list_templates` auf (optional nach `type` filtern: `docx`, `xlsx`, `potx`, `odt`, `pdf`)
2. **Platzhalternamen** aus der Antwort notieren
3. **Vorlage ausfüllen** mit dem passenden `create_*_from_template`-Tool

## Verwendung der Tools

### list_templates

```json
{
  "type": "potx"
}
```

Liefert pro Vorlage: `name`, `displayName`, `description`, `category`, `tags`, Platzhalterlisten, `loopSources`, `fields` (bei PDF-Formularvorlagen), `size`, `isDefault`, Upload-Daten und den Geltungsbereich (`"user"` persönlich oder `"global"`).

Bei **POTX/PPTX**-Vorlagen enthält die Antwort eine Aufschlüsselung pro Folie (`slideInfo`):

- `slideNumber` — Folienindex, beginnend bei 1
- `layoutName` — Name des PowerPoint-Layouts (z. B. `"Title Slide"`, `"Two Content"`)
- `layoutType` — Wert aus einem `{{slide_type:xxx}}`-Marker auf dieser Folie (z. B. `"section"`, `"default"`, `"text-image"`)
- `textPlaceholders` — `{{key}}`-Platzhalter auf dieser Folie
- `imagePlaceholders` — `{%name}`-Platzhalter auf dieser Folie
- `chartPlaceholders` — `{{name}}`-Platzhalter für Diagrammcontainer auf dieser Folie

Nutze diese Aufschlüsselung, um vor dem Aufruf von `create_powerpoint_from_template` genau zu wissen, welcher Platzhalter auf welche Folie gehört. Filtere mit `type`, um die Ergebnisse einzugrenzen: `"docx"`, `"xlsx"`, `"potx"`, `"odt"`, `"pdf"`.

---

### create_word_from_template

Platzhaltersyntax: `{placeholder}` (einfache geschweifte Klammern). Punktpfade: `{user.name}`.

```json
{
  "template_name": "invoice",
  "data": {
    "customer": "Acme Corp",
    "invoice_number": "INV-2025-042",
    "date": "2025-05-08",
    "total": "€4,200.00"
  },
  "filename": "invoice_acme"
}
```

**Tabellenschleifen-Syntax** (FOR/END-FOR jeweils in eine eigene Tabellenzeile setzen):

```
{FOR item IN items}
{= $item.name} | {= $item.qty} | {= $item.price}
{END-FOR item}
```

Übergib `items` als Array in `data`. Fehlende Schleifenquellen werden stillschweigend mit einer Warnung übersprungen.

**Vorlagenausdrücke sind kein JavaScript.** Innerhalb von `{…}`-Befehlen funktionieren nur Datenpfade (`$item.price`, `rows[0]`), Literale, Operatoren (`+ - * / %`, Vergleiche, `&& || ??`, `cond ? a : b`), die Befehle `FOR`, `IF` und `EXEC` sowie eine kurze Allowlist von Hilfsfunktionen — z. B. `toFixed`, `toUpperCase`, `join`, `toLocaleDateString`, `Math.round`, `parseFloat`, `new Date(…)`. Arrow Functions, `.map`/`.filter`, Schleifen und Template-Literale lassen das Ausfüllen fehlschlagen — berechne solche Werte vorab und übergib sie in `data`.

---

### create_word_from_template_with_images

Unterstützt Textplatzhalter `{name}` und Bildplatzhalter `{%logo}`.

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
  "filename": "letter_acme"
}
```

Bild aus einem gespeicherten Dokument (kein erneuter Upload nötig):

```json
{
  "logo": {
    "document_id": "abc12345-...",
    "width": 4,
    "height": 2
  }
}
```

Das Organisations-/Benutzerlogo wird **automatisch eingefügt**, aber nur in einen Platzhalter, der exakt `logo` heißt (also `{%logo}`) — und nur, wenn es in den Einstellungen konfiguriert ist und kein `logo`-Wert übergeben wird. Anders benannte Bildplatzhalter (z. B. `{%companyLogo}`) werden **nicht** automatisch befüllt.

---

### create_excel_from_template

Akzeptiert in `cell_values` **entweder** Zelladressen (z. B. `"A1"`, `"Sheet2!B3"`) **oder** `{{placeholder}}`-Namen (den reinen Namen ohne `{{ }}` übergeben) — das Tool routet automatisch anhand der übergebenen Schlüssel; bei gemischten Schlüsseln gilt der Platzhaltermodus. Mit `list_templates` siehst du die verfügbaren XLSX-Vorlagen.

```json
{
  "template_name": "budget",
  "cell_values": {
    "A1": "Budget 2025",
    "B5": 125000,
    "Sheet2!C3": "Approved"
  },
  "filename": "budget_2025"
}
```

---

### fill_excel_template

Befüllt Zellen per `{{placeholder}}`-Syntax — Formatierung, Stile, Formeln und Diagramme bleiben erhalten.

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

Befüllt `{{placeholder}}`-Syntax in ODT-Vorlagen.

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

Platzhaltersyntax:

- **Text:** `{{key}}` an beliebiger Stelle in einem Textfeld
- **Bild:** `{%name}` im **Alternativtext** (`descr`-Attribut) einer Bildform
- **Diagramm:** `{{name}}` im **Alternativtext** einer Diagrammcontainer-Form
- **Layout-Marker:** `{{slide_type:default}}`, `{{slide_type:section}}`, `{{slide_type:text-image}}` — unsichtbarer Metadaten-Marker; legt den Layouttyp der Folie für das `repeat`-Routing (Multi-Source) fest. Wird in der Ausgabe automatisch entfernt. Die Layout-nativen Tools (`create_powerpoint_from_layouts`, `add_slides_from_layouts`) ignorieren ihn.

Führe immer zuerst `list_templates` aus — bei POTX/PPTX liefert es eine Aufschlüsselung pro Folie mit `layoutName`, `layoutType` (aus dem `{{slide_type:xxx}}`-Marker) und den Text-/Bild-/Diagrammplatzhaltern, die zu jeder Folie gehören.

> **Enthält die POTX/PPTX-Vorlage KEINE `{{}}`-Platzhalter** und übergibt der Aufruf keine `images`, `charts` oder `speaker_notes`, lehnt dieses Tool den Aufruf ab und nennt stattdessen die Layout-Tools — `list_templates` kennzeichnet solche Vorlagen mit `hasLegacyPlaceholders: false` und einem `nextStep`-Hinweis. Corporate-Design-Folienmaster von Designteams enthalten meist überhaupt kein `{{}}`-Markup — sie bringen stattdessen benannte Folienlayouts mit. Führe `describe_pptx_template { "template_name": "..." }` aus: Ist `hasLegacyPlaceholders` `false`, wechsle zu `create_powerpoint_from_layouts` (siehe **powerpoint-skill**, "corporate master without `{{}}`"). Bitte den Nutzer nie, `{{}}`-Marker in einen Corporate-Master einzutippen.

**Grundlegende Verwendung (Befüllung mit einem Datensatz):**

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
  "filename": "q4_deck"
}
```

Die Schlüssel von `speaker_notes` sind Foliennummern, **beginnend bei 1**.

`charts` benennt nur die Datenreihen des Diagramms um (`datasets[].label`). `labels` und `values` werden **noch nicht** übernommen — der Server protokolliert sie als "not yet implemented", und das Diagramm behält die Daten der Vorlage. Versprich dem Nutzer keine aktualisierten Diagrammwerte.

In PowerPoint-Vorlagen wird kein Logo automatisch platziert: Nur `{{company_name}}` wird automatisch aus den Einstellungen befüllt. Um ein Logo anzuzeigen, übergib es explizit in `images` (z. B. `"logo"` für `{%logo}`).

Das Tool akzeptiert nur `template_name` — kein `document_id` / `librechat_file_id`. Ein im Chat angehängtes `{{}}`-Deck muss zuerst als Vorlage hochgeladen oder im Klonmodus bearbeitet werden (siehe **powerpoint-skill** §2a).

**Single-Source-Wiederholung** (eine Folie pro Datensatz duplizieren):

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

`repeat.slide` ist die zu duplizierende Foliennummer (beginnend bei 1); die Folie wird durch N Kopien ersetzt, eine pro Datensatz. Standardmäßig werden Folien, die **nicht** wiederholt werden, aus der Ausgabe entfernt — setze `repeat.keep_unused_slides: true`, um sie zu behalten. `create_powerpoint_from_template` akzeptiert außerdem `title` und `author` auf oberster Ebene.

**Multi-Source-Wiederholung** (jeden Datensatz an die Folie mit passendem `slide_type` leiten):

Verwende dies, wenn die Vorlage mehrere mit `{{slide_type:xxx}}` markierte Layoutfolien enthält und jeder Datensatz ein anderes Layout nutzen soll.

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

Lass `repeat.slide` beim `slide_type`-Routing weg — die passende Vorlagenfolie wird automatisch über ihren `{{slide_type:xxx}}`-Marker gefunden. Die `slide_type`-Werte (`default`, `section`, `text-image`) entsprechen denselben Layoutnamen wie in `create_powerpoint`.

## Bearbeitung nach dem Ausfüllen (iterative Aktualisierungen)

Jedes Vorlagen-Tool liefert die `id` des neuen Dokuments. Übergib sie als `document_id` an die iterativen Bearbeitungstools aus **word-odt-skill** und **powerpoint-skill**, um das ausgefüllte Dokument weiter anzupassen, ohne es neu zu erzeugen.

### Nach `create_word_from_template` / `create_word_from_template_with_images`

| Ziel                               | Tool                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| Aktuellen Inhalt prüfen            | `read_word_content { "document_id": "<id>" }`                                        |
| Weitere Abschnitte am Ende anfügen | `append_to_word { "document_id": "<id>", "content": "...", "add_page_break": true }` |
| Dokument komplett neu schreiben    | `replace_word_content { "document_id": "<id>", "content": "..." }`                   |

Beispiel — Vorlage ausfüllen und anschließend einen eigenen Anhang anfügen:

```json
// Step 1: fill the template
{ "template_name": "report", "data": { "title": "Annual Report" } }
// → returns id "abc123" (use it as document_id)

// Step 2: append extra content
{ "document_id": "abc123", "content": "## Appendix A\n\nAdditional data...", "add_page_break": true }
```

### Nach `create_powerpoint_from_template`

| Ziel                                          | Tool                                                                                                                |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Vorhandene Folien prüfen                      | `read_powerpoint_slides { "document_id": "<id>" }`                                                                  |
| Neue Folien am Ende anfügen                   | `append_slides_to_powerpoint { "document_id": "<id>", "slides": [...] }`                                            |
| Eine bestimmte Folie ersetzen                 | `update_powerpoint_slide { "document_id": "<id>", "slide_number": 3, "slides": [...] }`                             |
| **Folie im Stil der Vorlage anfügen**         | `append_slides_to_powerpoint { "document_id": "<id>", "reference_slide": 2, "placeholders": {...} }`                |
| **Folie ersetzen, Erscheinungsbild behalten** | `update_powerpoint_slide { "document_id": "<id>", "slide_number": 3, "reference_slide": 2, "placeholders": {...} }` |

> **Erscheinungsbild der Vorlage behalten:** Anfügen/Aktualisieren mit `slides`/`markdown` rendert das generische Theme, das **nicht** zu einem Vorlagen-Deck passt. Verwende stattdessen `reference_slide` + `placeholders` (Klonen und Neubefüllen) — damit wird das Design einer vorhandenen Folie kopiert und ihre `{{placeholders}}` neu befüllt. Details siehe **powerpoint-skill**. (Der Klonmodus befüllt nur Textplatzhalter neu; für Bildplatzhalter führe `create_powerpoint_from_template` erneut aus.)

Beispiel — Vorlage ausfüllen und anschließend eine eigene Abschlussfolie anfügen:

```json
// Step 1: fill the template
{ "template_name": "corporate_deck", "placeholders": { "title": "Q4 Results" } }
// → returns id "def456" (use it as document_id)

// Step 2a: add a generic (non-template-styled) closing slide
{ "document_id": "def456", "slides": [{ "type": "section", "title": "Thank You", "subtitle": "Questions?" }] }

// Step 2b: OR add a slide that matches the template by cloning slide 2 and refilling it
{ "document_id": "def456", "reference_slide": 2, "placeholders": { "title": "Next Steps", "owner": "PMO" } }
```

## Wichtige Hinweise

- Alle Erstellungstools liefern `{id, filename, downloadUrl, markdownLink}` — gib `markdownLink` immer in der Antwort aus.
- Wird `filename` weggelassen, erhält das ausgefüllte Dokument den Namen von `template_name` (`create_word_from_template_with_images`: `document`).
- `create_word_from_template_with_images` greift auf eine globale `default.docx` zurück, wenn die angegebene Vorlage fehlt, `create_word_from_template` dagegen nicht — prüfe mit `list_templates` vorab, ob die Vorlage existiert.
- Vorlagennamen unterscheiden **Groß- und Kleinschreibung** — prüfe sie immer zuerst mit `list_templates`.
- Benutzervorlagen haben Vorrang vor globalen Vorlagen mit demselben Namen.
- `replace_missing: false` (Standard) lässt nicht befüllte `{{placeholder}}`-Tokens unverändert; `true` ersetzt sie durch einen leeren String.
- Warnungen zu fehlenden Platzhaltern sind gegebenenfalls in der Antwort enthalten.
- Nutze nach dem Ausfüllen die iterativen Tools (`append_to_word`, `append_slides_to_powerpoint` usw.), um Inhalte hinzuzufügen oder zu aktualisieren — die `document_id` bleibt dabei durchgehend gleich.
