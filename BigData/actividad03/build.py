#!/usr/bin/env python3
"""Renderiza los diagramas Mermaid a SVG y arma el PDF de la Actividad 03."""
import pathlib, re, subprocess, tempfile, sys

AQUI = pathlib.Path(__file__).parent.resolve()
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FUENTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
           'family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">')

PAGINA = """<!doctype html><meta charset="utf-8">{fuentes}
<style>body{{margin:0;background:#fff;font-family:"IBM Plex Sans",Helvetica,Arial,sans-serif}}
#d{{width:1600px}}</style>
<pre class="mermaid" id="d">{src}</pre>
<script src="vendor/mermaid.min.js"></script>
<script>
  mermaid.initialize({{startOnLoad:false, securityLevel:"strict",
    htmlLabels:false, flowchart:{{htmlLabels:false}}}});
  Promise.all([
    document.fonts.load('400 15px "IBM Plex Sans"'),
    document.fonts.load('600 15px "IBM Plex Sans"'),
    document.fonts.load('400 15px "IBM Plex Mono"')
  ]).then(() => document.fonts.ready)
    .then(() => mermaid.run({{querySelector:"#d"}}))
    .then(() => document.body.setAttribute("data-listo","1"));
</script>"""


def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                           "--virtual-time-budget=25000",
                           "--run-all-compositor-stages-before-draw", *args],
                          capture_output=True, text=True)


def render(nombre: str) -> str:
    """Un diagrama por página: así ninguno se renderiza encima de otro."""
    src = (AQUI / "diagramas" / f"{nombre}.mmd").read_text()
    tmp = AQUI / f".render_{nombre}.html"
    tmp.write_text(PAGINA.format(fuentes=FUENTES, src=src))
    try:
        dom = chrome("--dump-dom", f"file://{tmp}").stdout
    finally:
        tmp.unlink()
    if 'data-listo="1"' not in dom:
        sys.exit(f"{nombre}: Mermaid no terminó de renderizar")
    svg = re.search(r"<svg\b.*?</svg>", dom, re.S)
    if not svg:
        sys.exit(f"{nombre}: no se encontró el SVG")
    svg = re.sub(r'\s(?:width|height|style)="[^"]*"', "", svg.group(0), count=3)
    (AQUI / "diagramas" / f"{nombre}.svg").write_text(svg)
    return svg


def main():
    html = (AQUI / "deck.template.html").read_text()
    for nombre in ("hdfs", "mapreduce"):
        html = html.replace("{{DIAGRAMA:%s}}" % nombre, render(nombre))
        print(f"  · {nombre}.svg")
    salida = AQUI / "actividad03.html"
    salida.write_text(html)
    pdf = AQUI / "Actividad03_BigData_ArredondoValle.pdf"
    chrome("--no-pdf-header-footer", f"--print-to-pdf={pdf}", f"file://{salida}")
    print(f"  · {pdf.name}")


if __name__ == "__main__":
    main()
