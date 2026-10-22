---
name: excel-skill
description: 'Erstelle, lies und bearbeite Excel-Tabellen (.xlsx) mit companyFILES MCP-Tools. Verwende diesen Skill, wenn eine Tabelle erstellt, Daten nach Excel exportiert, eine Excel-Datei gelesen oder ausgewertet, Zellen bearbeitet, Blätter hinzugefügt oder Formeln, bedingte Formatierung oder Autofilter angewendet werden sollen. Deckt CSV-zu-Excel, JSON-zu-Excel, 2D-Array-Eingaben, komplexe Mehrblatt-Arbeitsmappen und das direkte Bearbeiten bestehender Dateien ab.'
---

# Excel Skill

Tools zum Erstellen, Lesen und Bearbeiten von Excel-Tabellen (.xlsx) über companyFILES.

## Tools in diesem Skill

| Tool                     | Zweck                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `create_excel_from_csv`  | Excel aus CSV-Text erstellen                                                                |
| `create_excel`           | Excel aus einem 2D-Array erstellen                                                          |
| `create_excel_from_json` | Excel aus JSON (Array von Objekten) erstellen                                               |
| `create_excel_advanced`  | Mehrblatt-Arbeitsmappen mit Formeln, Datenvalidierung und bedingter Formatierung erstellen  |
| `modify_excel`           | Eine bestehende Excel-Datei anhand der Dokument-ID direkt bearbeiten                        |
| `read_excel`             | Excel als JSON lesen (nur Werte)                                                            |
| `read_excel_detailed`    | Excel mit Formeln, Kommentaren, Hyperlinks, benannten Bereichen und Metadaten lesen         |

## Entscheidungshilfe

```
Benutzer will Excel erstellen aus...
  CSV-Text              → create_excel_from_csv
  JSON-Array            → create_excel_from_json
  2D-Array / Tabelle    → create_excel
  Komplexe Arbeitsmappe → create_excel_advanced  (Formeln, mehrere Blätter, Formatierung)

Benutzer will eine bestehende Excel-Datei bearbeiten → modify_excel  (benötigt document_id oder librechat_file_id)

Benutzer will Excel-Inhalte lesen / auswerten...
  Nur Werte             → read_excel
  Formeln & Metadaten   → read_excel_detailed
  .xls / .xlsb / .ods   → read_file  (file-management-skill, falls verfügbar)
```

## Tool-Verwendung

### create_excel_from_csv

```json
{
  "csv_content": "Name,Alter\nAlice,30\nBob,25",
  "filename": "people",
  "sheet_name": "Sheet1"
}
```

### create_excel

```json
{
  "data": [
    ["Name", "Alter"],
    ["Alice", "30"],
    ["Bob", "25"]
  ],
  "has_headers": true,
  "filename": "people"
}
```

### create_excel_from_json

```json
{
  "json_content": "[{\"name\":\"Alice\",\"age\":30},{\"name\":\"Bob\",\"age\":25}]",
  "filename": "people"
}
```

### create_excel_advanced

```json
{
  "sheets": [
    {
      "name": "Sales",
      "data": [
        ["Produkt", "Q1", "Q2", "Summe"],
        ["Widget A", 100, 150, { "formula": "SUM(B2:C2)" }],
        ["Widget B", 200, 180, { "formula": "SUM(B3:C3)" }]
      ],
      "has_headers": true,
      "auto_filter": true,
      "conditional_formatting": [
        {
          "range": "B2:C3",
          "type": "greaterThan",
          "values": [150],
          "style": { "backgroundColor": "00FF00" }
        }
      ]
    }
  ],
  "filename": "sales_report"
}
```

**Formelsyntax:** Verwende ein Objekt `{"formula": "SUM(A1:A10)"}` – ohne führendes `=`.

**Typen der bedingten Formatierung:** `greaterThan`, `lessThan`, `equal`, `between`, `containsText`, `duplicateValues`

**Weitere Optionen pro Blatt:** `column_widths` (Zahlen-Array), `protected` (Boolean). Auf oberster Ebene: `named_ranges` und `properties` (`{title, subject, author, company}`). Einzelne Zellen können auch erweiterte Objekte sein: `{"value": ..., "comment": ..., "validation": ..., "style": ..., "numberFormat": ...}`. Ein solches Objekt braucht `value` (plus mindestens einen der anderen Schlüssel); eine Formel gehört **in** `value`, nicht daneben: `{"value": {"formula": "SUM(A1:A3)"}, "comment": "Summe"}`. Ein `formula`-Schlüssel neben `value` und `comment` wird ignoriert; ein Objekt ohne `value` (z. B. `{"formula": …, "comment": …}`) wird als reine Formel geschrieben, seine übrigen Schlüssel entfallen.

### modify_excel

Bearbeitet eine bestehende Excel-Datei. Gib das Ziel mit `document_id` an (wird **direkt** aktualisiert – gleiche ID) **oder** mit `librechat_file_id` (ein LibreChat-Anhang; ist das Volume nicht beschreibbar, wird die geänderte Kopie als **neues** Dokument gespeichert).

```json
{
  "document_id": "<id aus upload_file oder einem create_excel*-Aufruf>",
  "set_cells": {
    "A1": "Aktualisierter Titel",
    "Sheet2!B5": { "formula": "SUM(B2:B4)" }
  },
  "append_rows": {
    "Sheet1": [["Neue Zeile", 100, 200]]
  },
  "number_formats": { "B2:B100": "#,##0.00" },
  "auto_filter": { "Sheet1": true },
  "add_sheets": [{ "name": "Summary", "data": [["Summe", 500]], "has_headers": false }],
  "delete_sheets": ["OldSheet"],
  "rename_sheets": { "OldName": "NewName" }
}
```

### read_excel

```json
{
  "file_content": "<base64-kodierte xlsx>",
  "include_headers": true,
  "sheet_name": "Sheet1"
}
```

Akzeptiert genau eines von `file_content` (base64), `librechat_file_id` oder `document_id` (am häufigsten – zum Lesen einer zuvor erstellten/gespeicherten Datei). `sheet_name` ist optional.

`read_excel` und `read_excel_detailed` lesen `.xlsx`-Arbeitsmappen. Für `.xls`, `.xlsb` oder `.ods` verwende `read_file` aus dem **file-management-skill** (nur wo verfügbar) – es liefert den Inhalt als Markdown.

### read_excel_detailed

```json
{
  "document_id": "<id der gespeicherten xlsx>",
  "include_headers": true,
  "sheet_name": "Sheet1"
}
```

Dieselben Eingabeoptionen wie `read_excel` (`file_content` / `librechat_file_id` / `document_id`, optional `sheet_name`). Liefert Werte, Formeln, Kommentare, Validierungsregeln, Hyperlinks, benannte Bereiche, verbundene Zellen und Eigenschaften der Arbeitsmappe.

## Wichtige Hinweise

- Alle Erstell-Tools liefern `{id, filename, downloadUrl, markdownLink}` (plus `librechat_file_id`, wenn das Dokument zusätzlich als Chat-Datei gespeichert wird) – gib in der Antwort immer `markdownLink` aus.
- `modify_excel` benötigt eine `document_id` oder `librechat_file_id`, die auf eine `.xlsx`-Datei zeigt; ist der Dokumenttyp nicht Excel, gibt es einen Fehler. Ein Chat-Anhang (`librechat_file_id`) wird nach Möglichkeit direkt aktualisiert – die Antwort enthält dann `librechat_file_id`, `filename`, `modifications` und `message`, aber keinen Download-Link. Andernfalls wird die geänderte Kopie als neues Dokument mit neuer `id` und `markdownLink` gespeichert.
- Blattnamen müssen zur Arbeitsmappe passen – rufe zuerst `read_excel` auf, um sie zu sehen; ein unbekannter Name führt zu einem Fehler, der die vorhandenen Blätter auflistet.
- Zelladressen unterstützen ein Blatt-Präfix: `"Sheet2!B3"`.
- Das Farbschema der Organisation bzw. des Benutzers wird automatisch angewendet, wenn es in den Einstellungen konfiguriert ist.
- Um eine Vorlage mit `{{placeholder}}`-Syntax auszufüllen, verwende stattdessen `fill_excel_template` aus dem **templates-skill**.
