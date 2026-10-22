---
name: word-odt-skill
description: 'Create and read Word (.docx) and ODT (.odt) documents with companyFILES MCP tools. Use when asked to write a report, letter, or document in Word or OpenDocument format, convert Markdown or HTML to Word/ODT, extract text from a Word file, or create a document with headers, footers, table of contents, or page numbers.'
---

# Word & ODT Skill

Tools zum Erstellen von Word- (.docx) und ODT-Dokumenten (.odt) sowie zum Lesen von Word-Dateien.

## Tools in diesem Skill

| Tool                    | Zweck                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| `create_word`           | Word (.docx) aus Markdown oder reinem Text erstellen                                        |
| `create_word_from_html` | Word aus HTML mit optionalem CSS erstellen                                                  |
| `create_word_from_json` | JSON-Daten als einfache Schlüssel/Wert-Auflistung in Word ausgeben                          |
| `create_odt`            | ODT aus Markdown erstellen (LibreOffice/OpenOffice)                                         |
| `create_odt_from_html`  | ODT aus HTML erstellen                                                                      |
| `read_word`             | Word-Datei (.docx) lesen → Text, HTML, Markdown (aus base64 oder LibreChat-Datei)           |
| `read_word_content`     | Inhalt eines gespeicherten Word-Dokuments per document_id lesen → Markdown-ähnlicher String |
| `append_to_word`        | Markdown-Inhalt an ein vorhandenes gespeichertes Word-Dokument direkt anfügen               |
| `replace_word_content`  | Gesamten Inhalt eines vorhandenen gespeicherten Word-Dokuments direkt ersetzen              |

## Entscheidungshilfe

```
Nutzer möchte ein Word-Dokument erstellen aus...
  Markdown / reinem Text    → create_word          (häufigster Fall)
  HTML + CSS                → create_word_from_html
  Rohen JSON-Daten (Dump)   → create_word_from_json  (keine Layoutsteuerung)
  Einer Vorlage             → siehe templates-skill   (create_word_from_template)

Nutzer möchte OpenDocument-Format (LibreOffice)...
  Aus Markdown              → create_odt
  Aus HTML                  → create_odt_from_html
  Aus Vorlage               → siehe templates-skill   (create_odt_from_template)

Nutzer möchte eine Word-Datei LESEN...
  Aus base64 / LibreChat-Anhang           → read_word
  Aus gespeichertem Dokument (document_id) → read_word_content

Nutzer möchte ein vorhandenes gespeichertes Word-Dokument BEARBEITEN...
  Zuerst aktuellen Inhalt prüfen          → read_word_content
  Weiteren Inhalt am Ende anfügen         → append_to_word    (behält vorhandenen Inhalt)
  Gesamtes Dokument neu schreiben         → replace_word_content
```

## Verwendung der Tools

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

`format` kann `"markdown"` (Standard) oder `"plain"` sein. Hinweis: `create_word` hat **kein `author`-Feld** — nur `create_word_from_html`, `create_odt` und `create_odt_from_html` akzeptieren `author`.

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

Unterstützt Inline-Bilder über die URI `doc:<documentId>` (gespeichertes companyFILES-Dokument) oder `lc:<file_id>` (LibreChat-Anhang): `<img src="doc:abc123..." />`. Dieselbe Syntax funktioniert in Markdown für `create_word`: `![alt](doc:<uuid>)` oder `![alt](lc:<file_id>)`.

### create_word_from_json

```json
{
  "json_content": "{\"customer\":\"Acme Corp\",\"items\":[{\"name\":\"Widget\",\"qty\":2}]}",
  "filename": "order_data"
}
```

Schreibt das JSON als einfache Auflistung unter der Überschrift "Document Generated from JSON": ein Absatz pro Feld (`key: value`, Schlüssel fett); verschachtelte Objekte und Arrays werden eingerückt, Array-Einträge erscheinen als `[0]`, `[1]`, …. Es gibt kein Element-Schema (keine Überschriften, Tabellen oder Formatierung aus JSON) und keine Optionen für Titel, Autor oder Seite — nur `json_content` und `filename`. Für ein gestaltetes Dokument wandle die Daten in Markdown um und verwende `create_word`.

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

Akzeptiert genau eines von `file_content` (base64), `librechat_file_id` (LibreChat-Anhang) oder `document_id` (gespeichertes companyFILES-Dokument). Liefert `{ text, html, markdown }`.

### read_word_content

Liest den Inhalt eines gespeicherten Word-Dokuments (über companyFILES erstellt oder hochgeladen). Akzeptiert `document_id` **oder** `librechat_file_id`. Liefert einen Markdown-ähnlichen String plus Zeichenanzahl — nutze das vor dem Anfügen oder Ersetzen, um den aktuellen Stand zu kennen.

```json
{
  "document_id": "uuid-of-stored-word-doc"
}
```

Liefert `{ document_id, librechat_file_id, filename, character_count, content }`.

### append_to_word

Fügt Markdown (oder reinen Text) an ein vorhandenes Word-Dokument an. Bestimme das Ziel mit `document_id` **oder** `librechat_file_id`. Standardmäßig wird vor dem neuen Inhalt ein Seitenumbruch eingefügt. Das Dokument wird direkt aktualisiert — gleiche `document_id`.

```json
{
  "document_id": "uuid-of-stored-word-doc",
  "content": "## New Section\n\nAdditional content here...",
  "format": "markdown",
  "add_page_break": true
}
```

`add_page_break` ist standardmäßig `true`. Verwende `false`, um auf derselben Seite weiterzuschreiben.

### replace_word_content

Ersetzt den gesamten Inhalt eines vorhandenen Word-Dokuments durch neues Markdown. Bestimme das Ziel mit `document_id` **oder** `librechat_file_id`. Alle Seitenlayout-Optionen (`page_size`, `header_text` usw.) funktionieren wie bei `create_word`. Das Dokument wird direkt aktualisiert — gleiche `document_id`.

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

## Gemeinsame Seitenoptionen (alle Erstellungstools außer `create_word_from_json`)

| Parameter               | Werte                               | Standard           |
| ----------------------- | ----------------------------------- | ------------------ |
| `page_size`             | `A4`, `Letter`, `Legal`, `A3`, `A5` | `A4`               |
| `page_orientation`      | `portrait`, `landscape`             | `portrait`         |
| `page_number_position`  | `header`, `footer`                  | `footer`           |
| `page_number_alignment` | `left`, `center`, `right`           | `center`           |
| `page_number_format`    | String mit `{page}` und `{pages}`   | `{page} / {pages}` |

## Muster für die iterative Dokumentbearbeitung

Lange Dokumente, die ein einzelnes Kontextfenster übersteigen, baust du abschnittsweise auf:

1. `create_word` — Dokument mit dem ersten Abschnitt erstellen; die zurückgegebene `id` notieren (als `document_id` übergeben)
2. `append_to_word` — für jeden weiteren Abschnitt erneut aufrufen
3. Optional `read_word_content`, um vor dem Weitermachen den aktuellen Stand zu prüfen
4. `replace_word_content` — falls ein Abschnitt komplett neu geschrieben werden muss

Alle drei direkt arbeitenden Tools (`read_word_content`, `append_to_word`, `replace_word_content`) arbeiten mit vorhandenen Dokumenten, die per `document_id` **oder** `librechat_file_id` (ein LibreChat-Anhang, der direkt auf dem gemeinsamen Volume aktualisiert wird) identifiziert werden, nicht mit base64-Dateiinhalt.

## Wichtige Hinweise

- Alle Erstellungstools liefern `{id, filename, downloadUrl, markdownLink}` (plus `librechat_file_id`, wenn das Dokument zusätzlich als Chat-Datei gespeichert wird) — gib `markdownLink` immer in der Antwort aus.
- Die direkt bearbeitenden Tools (`append_to_word`, `replace_word_content`) liefern bei einem companyFILES-Dokument dieselbe `id` und einen aktualisierten `markdownLink`. Bei einem direkt aktualisierten Chat-Anhang (`librechat_file_id`) liefern sie nur `{librechat_file_id, filename, message}` — es gibt keinen Download-Link; teile dem Nutzer mit, dass die angehängte Datei aktualisiert wurde. Lässt sich der Anhang nicht direkt aktualisieren, wird die geänderte Kopie als **neues** Dokument gespeichert und dessen neue `id`/`markdownLink` zurückgegeben — verwende ab dann diese id.
- Inline-Bilder lassen sich über `doc:<documentId>` oder `lc:<file_id>` im Markdown oder HTML der Erstellungstools (`create_word`, `create_word_from_html`, `create_odt`, `create_odt_from_html`) referenzieren — SVG wird für Word automatisch in PNG umgewandelt. `append_to_word` und `replace_word_content` lösen diese Referenzen nicht auf.
- Nicht gesetzte Seiten-/Kopf-/Fußzeilenoptionen greifen auf die Theme-Standards der Organisation bzw. des Benutzers zurück (z. B. `defaultPageSize`, `defaultHeaderText`, `defaultShowPageNumbers`), bevor die dokumentierten festen Standardwerte gelten.
- Für vorlagenbasierte Word-Erstellung (Platzhalter, Schleifen, Bildeinfügung) verwende den **templates-skill**.
- ODT-Dateien lassen sich nativ in LibreOffice und Google Docs öffnen.
- Das Farbschema der Organisation bzw. des Benutzers wird automatisch angewendet, wenn es konfiguriert ist.
