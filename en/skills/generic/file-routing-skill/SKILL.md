---
name: file-routing-skill
description: Decides which tool or app handles a file task in companyGPT. Use whenever the user attached a file or asks for a file as output, e.g. read, analyse, calculate on, chart, edit, convert, translate or transcribe a file, fill a template, or create a Word, Excel, PowerPoint or PDF document. Picks between companyFILES, code execution, companyRAG, companyTRANSCRIBE, companyTRANSLATE and companyM365 and names the fallback when an app or capability is missing.
---

# File Routing Skill

You decide which tool handles a file task. You do not guess file IDs and you do not promise capabilities you have not seen in your tool list.

## Step 1: Find the File

Files the user attached appear in the message context in a block like this:

```
Attached files in this message:
- file_id: 6f1c…, filename: sales_2025.xlsx, type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, size: 48211 bytes
- file_id: a93e…, filename: meeting.m4a, type: audio/mp4, size: 18734112 bytes, stored only
```

- Take the `file_id` from there and pass it on unchanged: companyFILES tools as `librechat_file_id`, companyTRANSCRIBE and companyTRANSLATE as `file_id`.
- `stored only` means the content is not in your context. You only get at it through a tool that takes the `file_id` (or through code execution).
- No block, or the file is from an earlier chat: call `list_my_files` (companyFILES) and pick the file by name. Never invent a `file_id`.

## Step 2: Check What Is Available

Check your tool list before you choose a route. Apps (companyFILES, companyRAG, companyTRANSCRIBE, companyTRANSLATE, companyM365) are only there if they are enabled for this tenant and agent. Code execution is only there if it is enabled for the chat or agent and allowed for the user's role. If a route is missing, use the fallback in the table, or tell the user what is missing.

## Step 3: Pick the Route

| Task | Route | Fallback / condition |
| --- | --- | --- |
| Create a native Word, Excel, PowerPoint or PDF document | companyFILES `create_*` tools (see the Word, Excel, PowerPoint, PDF skills) | Without companyFILES: deliver the content as Markdown in the chat |
| Read an attached DOCX, XLSX, PDF or PPTX | companyFILES `read_word`, `read_excel`, `read_pdf`, `read_powerpoint_slides` with `librechat_file_id` | Short text files are often already in your context |
| Calculations, filters, pivots or statistics on an attached CSV/XLSX | Code execution (pandas on `/mnt/data/<filename>`), see below | Without code execution: companyFILES `read_excel` (CSV: `read_file` if available) and reason over the values; for large files say that the result is based on what you could read |
| Chart from attached data | Code execution (matplotlib/plotly) **or** companyFILES `show_interactive_chart` (in the chat) / `create_chart_document` (in a document) | Without code execution: read the values with `read_excel`, then the companyFILES chart tools |
| Fill a company template | companyFILES `list_templates` + `create_*_from_template` (templates skill) | — |
| Bulk or free-form edits in a template's layout | companyFILES `attach_template_to_chat`, then code execution from the user's **next** message (templates skill) | Needs code execution and LibreChat file storage for companyFILES; otherwise `create_*_from_template` plus the iterative edit tools |
| Edit an attached Excel/Word/PowerPoint file | companyFILES `modify_excel`, `append_to_word`/`replace_word_content`, PowerPoint edit tools with `librechat_file_id` | With code execution also possible in the sandbox (save as a new file) |
| E-mails (`.msg`, `.eml`), ZIP archives, legacy formats (`.doc`, `.xls`, `.ppt`, RTF, ODF), scanned PDFs | companyFILES `read_file` / `save_file_part` / `convert_to_markdown` | Only if available in your tool list; otherwise ask for a PDF or DOCX export |
| Convert between formats | companyFILES `convert_document` (convert skill) | — |
| Company knowledge: manuals, policies, contracts, project files, maintained tables | companyRAG `search_content`; for tables `execute_sql` | Only for collections the user may access. `execute_sql` and the other dataset tools exist only where companyRAG datasets are enabled |
| Audio or video file (MP3, WAV, M4A, MP4, MOV, …) | companyTRANSCRIBE `transcribe_chat_file { "file_id": "…" }`, then `get_transcript_stats` until done, then `get_transcript` | Only if companyTRANSCRIBE is enabled; transcription takes minutes |
| Translate an attached document | companyTRANSLATE `translate_document { "file_id": "…", "target_language": "…" }` (status `running`: `get_translation_status { "job_id": "…" }`) | Only if companyTRANSLATE is enabled; otherwise translate the extracted text yourself and create a new document with companyFILES |
| Translate text | companyTRANSLATE `translate_text { "text": "…", "target_language": "…" }` | Without companyTRANSLATE: translate yourself |
| Outlook mails and attachments, Teams messages, OneDrive/SharePoint files | companyM365 (e.g. `search_emails`, `read_email_attachment`, `search_teams_messages`, `search_files`) | Only if companyM365 is enabled; otherwise ask the user to attach the file |

companyRAG cannot index files attached in the chat. For an ad-hoc question on an attached file, use the companyFILES read tools or code execution. If the data should be searchable permanently or for others, it has to be added to a companyRAG collection or dataset through the companyRAG UI or by an admin.

## Optional: If Code Execution Is Available

Use it for calculations on attached data, charts as images, and bulk edits. Without code execution use the fallback from the table.

- Files attached in the chat are in the sandbox at `/mnt/data/<filename>`. Check with `os.listdir("/mnt/data")` first.
- The sandbox has no network access: no downloads, no API calls, no `pip install`.
- Check a library with `import` before relying on it (usually present: pandas, numpy, openpyxl, python-docx, python-pptx, matplotlib, plotly). If one is missing, use the fallback.
- Save results under a new name in `/mnt/data/`; they come back as chat attachments. Never overwrite the input.
- Work out numbers in code, not in your head, and report the figures from the code output.
- For a formatted XLSX/DOCX/PPTX in the corporate design, prefer companyFILES (or the template route) over files built from scratch in code.

## Rules

1. **Never invent a `file_id`.** Only from the attached-files block or `list_my_files`.
2. **Say what is missing.** If a route depends on an app or on code execution that is not in your tool list, use the fallback or tell the user plainly.
3. **One route per task.** Do not read the same file with several tools "to be safe".
4. **Text extract only?** If a tool answers that LibreChat only holds a text extract of the file, ask the user to attach the original file again.
