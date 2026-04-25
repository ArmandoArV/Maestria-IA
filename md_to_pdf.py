"""
Markdown to PDF converter.

Usage:
    python md_to_pdf.py <input.md> [output.pdf]

If output is not specified, it uses the same name as input with .pdf extension.
Supports tables, code blocks, and standard markdown formatting.
"""

import sys
import os
import markdown
from xhtml2pdf import pisa

CSS = """
@page {
    size: A4;
    margin: 2cm;
}
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #1a1a1a;
}
h1 { font-size: 18pt; color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 6px; }
h2 { font-size: 14pt; color: #34495e; margin-top: 20px; }
h3 { font-size: 12pt; color: #2c3e50; }
blockquote {
    border-left: 3px solid #3498db;
    padding: 8px 14px;
    margin: 14px 0;
    background-color: #eaf2f8;
    font-style: italic;
}
table { width: 100%; margin: 10px 0; font-size: 9pt; }
th { background-color: #2c3e50; color: white; padding: 6px 8px; text-align: left; }
td { padding: 5px 8px; border-bottom: 1px solid #ddd; }
code {
    background-color: #f4f4f4;
    padding: 1px 4px;
    font-family: Courier;
    font-size: 9pt;
}
pre {
    background-color: #2d2d2d;
    color: #f8f8f2;
    padding: 12px;
    font-size: 8pt;
    line-height: 1.3;
}
pre code { background-color: transparent; color: inherit; padding: 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 16px 0; }
"""


def md_to_pdf(input_path, output_path=None):
    if not os.path.isfile(input_path):
        print(f"Error: '{input_path}' not found.")
        sys.exit(1)

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite", "toc"],
    )

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_body}</body></html>"""

    with open(output_path, "w+b") as pdf_file:
        status = pisa.CreatePDF(full_html, dest=pdf_file)

    if status.err:
        print(f"Error generating PDF (code {status.err})")
        sys.exit(1)
    else:
        print(f"PDF created: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    md_to_pdf(in_file, out_file)
