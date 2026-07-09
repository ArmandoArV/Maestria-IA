---
name: pdf-reader
description: >
  Read and extract text content from PDF files using Python's pymupdf (fitz). Use this skill whenever
  the user references a .pdf file, asks to read, open, parse, extract, or analyze a PDF, or needs the
  text content of a PDF document (slides, papers, exams, reports). Also trigger on requests like
  "what does this PDF say", "extract the text from", or "read the presentation".
---
# PDF Reader Skill

## Description

Read and extract text content from PDF files using Python's `pymupdf` (fitz) library. Use this skill whenever the user references a `.pdf` file, asks to read/analyze a PDF, or needs content extracted from a PDF document.

---

## How to Read a PDF

Run the following Python snippet, replacing the path as needed:

```python
import fitz, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

doc = fitz.open(r'<PATH_TO_PDF>')
print(f'Pages: {len(doc)}')
for page in doc:
    print(page.get_text())
```

### For large PDFs (avoid output truncation)

Read in page ranges:

```python
import fitz, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

doc = fitz.open(r'<PATH_TO_PDF>')
for i, page in enumerate(doc):
    if START <= i < END:  # e.g., 0 <= i < 20
        print(f'--- page {i+1} ---')
        print(page.get_text())
```

### For extracting images from a PDF

```python
import fitz

doc = fitz.open(r'<PATH_TO_PDF>')
for i, page in enumerate(doc):
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        ext = base_image["ext"]
        with open(f"page{i+1}_img{img_index}.{ext}", "wb") as f:
            f.write(image_bytes)
```

---

## Prerequisites

The `pymupdf` package must be installed:

```
pip install pymupdf
```

---

## Behavior Instructions

1. **Always use `sys.stdout` with UTF-8 encoding** on Windows to avoid codec errors with special characters (math symbols, accented characters, etc.).
2. **For large PDFs (>20 pages)**, read in batches of 15–20 pages to avoid output truncation. Use `Select-Object -First N` in PowerShell to limit output lines.
3. **Pipe output** through `Select-Object -First N` when only a preview is needed.
4. **When the user asks to "read a PDF"**, extract the full text and summarize the content unless they ask for verbatim output.
5. **For structured PDFs** (homework assignments, papers), identify sections, questions, or headings and present them clearly.

