---
name: dsdoc-convert
description: dsdoc skill that converts PDF or image documents (e.g. a lean canvas) into Markdown, verbatim, for dsdoc-business-context to read. Use it when the user asks dsdoc to convert, import, or read a PDF or a lean canvas.
context: fork
agent: dsdoc-convert-writer
---

# dsdoc: convert PDFs to Markdown

Convert every file in `context.pdf_inputs` (in `dsdoc.yaml`) into
`<output_dir>/sources/<file name without extension>.md`. Overwrite a file
if it exists. If the user gives a path directly, convert that file
instead. If neither is set, stop and ask for one.

This is a copy, not a summary. Mapping the content to business sections is
the job of `dsdoc-business-context`.

## dsdoc ground rules

- **Source only.** Read only the file being converted.
- **Verbatim.** Copy the text word for word. Fix only line breaks that the
  PDF broke in the middle of a sentence. Keep typos, acronyms, and £ figures
  exactly as written.
- **Keep the structure.** Each heading, box or titled area of the
  document becomes a Markdown heading with its original text. Keep the
  reading order: title first, then top to bottom, left to right. Tables
  stay tables.
- **Never invent.** Don't add headings the document doesn't have, and
  don't move text between them.
- **Drop template hints.** Guidance text of a template (grey hints such as
  "Provide a high-level overview...") is not content.

## Steps

1. **Read the whole file.** For a PDF, read every page.
2. **Mark pending text.** Text in red, highlighted, in square brackets as
   a placeholder (e.g. `[Mike Robinson]`), or worded as still to do keeps
   its place and gets the prefix `[PENDING]`. Only this step sees colours
   and highlights, so don't skip it.
   Every value in square brackets is marked, even if it looks like a real
   value (e.g. `[UKI7]`): the template uses brackets for placeholders, and
   only the owner can say it is final.
3. **Mark what cannot be read.** Unreadable text (a scan, an image, a
   cropped box) becomes `[UNREADABLE: <where>]`. Never guess it.
4. **Write the file** with the header below, then the content.

## Template

```markdown
# <document title, as written>

| Field | Value |
|---|---|
| Source | `<input file path>` |
| Converted | <YYYY-MM-DD HH:MM, from `date`> |
| Pages | <n> |

## <first heading, as written>
<verbatim>
```

## At the end

Report, per file: the output path, the number of pages, and the number of
`[PENDING]` and `[UNREADABLE]` marks.
