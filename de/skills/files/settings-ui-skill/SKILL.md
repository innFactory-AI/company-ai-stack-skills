---
name: settings-ui-skill
description: 'Die companyFILES-Web-UI öffnen, Einstellungen anzeigen und Hilfe zu den verfügbaren Tools erhalten. Verwenden, wenn Dokumente angezeigt, Dateien durchsucht, der Dateimanager geöffnet, Vorlagen verwaltet, Einstellungen geändert, Branding/Farben angezeigt oder Hilfe zur Nutzung der companyFILES-Tools gewünscht werden. Auch verwenden, wenn der Benutzer statt rohem JSON eine interaktive eingebettete Ansicht möchte.'
---

# Einstellungen & UI Skill

Tools, um die companyFILES-Web-App als eingebettete UI zu öffnen, Einstellungen abzurufen und Hilfe zu den Tools zu erhalten.

## Tools in diesem Skill

| Tool                   | Zweck                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `open_companyfiles_ui` | Die companyFILES-Web-App als eingebetteten iframe öffnen                           |
| `get_settings`         | Aufgelöste Organisations-/Benutzereinstellungen abrufen (Farben, Firmenname, Logo) |
| `help`                 | Anwendungsbeispiele für jede companyFILES-Tool-Kategorie abrufen                   |

## Entscheidungshilfe

```
Benutzer sagt „zeig meine Dateien“ / „Dateimanager öffnen“  → open_companyfiles_ui page="documents"
Benutzer sagt „Vorlagen verwalten / durchsuchen“            → open_companyfiles_ui page="templates"
Benutzer sagt „eine Datei hochladen“ (über die UI)          → open_companyfiles_ui page="documents"
Benutzer sagt „eine Vorlage hochladen“ (über die UI)        → open_companyfiles_ui page="upload"
Benutzer sagt „Einstellungen öffnen“ / „Präferenzen ändern“ → open_companyfiles_ui page="settings"

Benutzer fragt nach Einstellungen / Farben / Logo           → get_settings
Benutzer fragt, wie ein Tool funktioniert / braucht Beispiele → help (mit topic)
```

**Rufe das Tool immer sofort auf – beschreibe nie nur, was der Benutzer tun könnte.**

## Tool-Verwendung

### open_companyfiles_ui

Rendert die companyFILES-SPA als eingebetteten interaktiven iframe im Chat.

```json
{
  "page": "documents"
}
```

Verfügbare Seiten (Enum – nur diese vier Werte werden akzeptiert):
| Seite | Zeigt |
|------|-------|
| `documents` | Dokumentliste (einschließlich Chat-Uploads), Datei-Upload, Vorschau, Download |
| `templates` | Vorlagen-Browser, Hochladen persönlicher Vorlagen |
| `upload` | Formular zum Hochladen einer neuen Vorlage |
| `settings` | Reiter **Meine Einstellungen** (persönliche Farben, Typografie, Dokument-Standards, Logo) und **Organisation** (Firmendaten, Organisationsfarben und -logo – ohne Admin-Berechtigung nur lesbar; Admins bearbeiten zusätzlich Typografie und Dokument-Standards der Organisation) |

Die Einstellungsseite enthält keine Spracheinstellung – die Sprache wird im Kontomenü der companyFILES-Web-App umgestellt. Die Seite **Visualisierungen** der Web-App (Diagramme, Schaubilder und Karten aus dem Chat) ist kein `page`-Wert und kann nicht mit `open_companyfiles_ui` geöffnet werden.

> Hinweis: UI-Widgets erfordern einen Chat-Client, der MCP-UI-Rendering unterstützt (z. B. LibreChat). Google Gemini fällt auf Text zurück.

---

### get_settings

Liefert die aufgelösten Einstellungen: Organisations-Standards zusammengeführt mit Benutzer-Überschreibungen.

```json
{}
```

Beispielantwort:

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

`logoPath` wird absichtlich weggelassen (interner Dateisystempfad). Um das Logo anzusehen oder zu ändern, verwende `open_companyfiles_ui page="settings"`.

---

### help

Liefert ausführliche Anwendungsbeispiele für eine bestimmte Tool-Kategorie.

```json
{
  "topic": "excel"
}
```

Verfügbare Themen: `excel`, `word`, `pdf`, `powerpoint`, `text`, `chart`, `mermaid`, `map`, `zip`, `upload`, `templates`, `admin`, `convert`, `read`, `settings`, `assets`, `ui`, `provenance` (KI-Kennzeichnung in den Datei-Metadaten), `all` – sowie `cad` und `docs`, wo diese Erweiterungen verfügbar sind. Ein unbekanntes Thema liefert die Liste der verfügbaren Themen.

Ohne `topic` (oder mit `"all"`) wird das vollständige Hilfedokument zurückgegeben und zusätzlich die eingebettete UI geöffnet.

## Wichtige Hinweise

- `open_companyfiles_ui` ist das Standard-Tool für jede Anfrage, Dateien/Vorlagen/Einstellungen interaktiv zu durchsuchen, anzuzeigen oder zu verwalten.
- Die Farben aus den Einstellungen (`primaryColor`, `secondaryColor`, `accentColor`) werden automatisch als Theme in allen Tools zur Dokument- und Diagrammerstellung verwendet. `get_settings` liefert nur diese Kernauswahl; das vollständige Einstellungsmodell enthält viele weitere, auf Organisations- oder Benutzerebene überschreibbare Felder, die ebenfalls in erzeugte Dokumente einfließen – erweiterte Farben (`headingColor`, `bodyTextColor`, `linkColor`, `tableHeaderBg`, `tableHeaderText`, `codeBg`), Typografie (`fontHeading`, `fontBody`, `fontCode`, `fontSize*`) und Dokument-Standards (`defaultPageSize`, `defaultPageOrientation`, `defaultHeaderText`, `defaultFooterText`, `defaultShowPageNumbers`, `defaultPageNumberPosition`, `defaultPageNumberFormat`, `logoInHeader`, `logoHeaderHeight`).
- Zum Bearbeiten der Einstellungen verwende die UI (`open_companyfiles_ui page="settings"`): persönliche Werte unter **Meine Einstellungen**, Organisationswerte unter **Organisation**. Das Ändern von Organisationseinstellungen und Branding erfordert die companyFILES-Admin-Berechtigung (`ext:files:admin`); das Hochladen oder Hochstufen globaler Vorlagen erfordert die Vorlagen-Berechtigung (`ext:files:templates`). Benutzer ohne diese Berechtigungen verwalten nur ihre persönlichen Einstellungen und Vorlagen.
