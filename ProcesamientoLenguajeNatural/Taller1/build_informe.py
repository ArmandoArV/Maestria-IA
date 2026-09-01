# -*- coding: utf-8 -*-
"""Genera el informe de 2 paginas (+ caratula) copiando preguntas y respuestas
tal cual estan en el notebook del Taller 1."""
import json, re

NB = '/Users/armandoav/Downloads/Copia_de_Taller_1_Word_Embedding_con_w2v.ipynb'
nb = json.load(open(NB, encoding='utf-8'))
def src(i): return ''.join(nb['cells'][i]['source'])

SPECIAL = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
           '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
           '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}

def esc(t):
    return ''.join(SPECIAL.get(c, c) for c in t)

def md2tex(t):
    """Convierte un fragmento markdown del notebook a LaTeX, sin alterar el texto."""
    out, i = [], 0
    for m in re.finditer(r'`([^`]*)`', t):          # spans de codigo primero
        out.append(('txt', t[i:m.start()]))
        out.append(('code', m.group(1)))
        i = m.end()
    out.append(('txt', t[i:]))
    res = []
    for kind, chunk in out:
        if kind == 'code':
            res.append(r'\code{' + esc(chunk) + '}')
            continue
        c = esc(chunk)
        c = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', c)
        c = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'\\textit{\1}', c)
        c = re.sub(r'"([^"]*)"', r"``\1''", c)
        res.append(c)
    return ''.join(res).strip()

# ── Preguntas (verbatim desde las celdas de enunciado) ──
def preguntas(cell):
    txt = src(cell)
    out = {}
    for m in re.finditer(r'^(\d\.\d)\.\s*(.*?)(?=^\d\.\d\.|\Z)', txt, re.M | re.S):
        out[m.group(1)] = ' '.join(m.group(2).split())
    return out

P = {}
P.update(preguntas(6)); P.update(preguntas(10)); P.update(preguntas(18))
m = re.search(r'\*\*Pregunta 3\.1\*\*\s*(\(1 punto\))\s*(.*)', src(14), re.S)
P['3.1'] = ' '.join(m.group(2).split())

# ── Respuestas (verbatim desde las celdas de respuesta) ──
def respuestas(cell):
    txt = src(cell)
    out = {}
    for m in re.finditer(r'^\*\*Respuesta (\d\.\d)\.\*\*\s*(.*?)(?=^\*\*Respuesta|\Z)',
                         txt, re.M | re.S):
        out[m.group(1)] = ' '.join(m.group(2).split())
    return out

R = {}
for c in (9, 13, 17, 20):
    R.update(respuestas(c))

assert set(P) == set(R) == {'1.1','1.2','2.1','2.2','2.3','3.1','4.1','4.2'}, (sorted(P), sorted(R))

EJERCICIOS = [
    ('Ejercicio 1: entrenamiento comparativo (CBOW frente a Skip-gram)', ['1.1', '1.2']),
    ('Ejercicio 2: álgebra vectorial y analogías semánticas',            ['2.1', '2.2', '2.3']),
    ('Ejercicio 3: reducción de dimensionalidad y visualización',        ['3.1']),
    ('Ejercicio 4: modelado de tópicos con document embeddings',         ['4.1', '4.2']),
]

cuerpo = []
for titulo, ids in EJERCICIOS:
    cuerpo.append('\\section{%s}\n' % titulo)
    for pid in ids:
        cuerpo.append('\\pregunta{%s}{%s}' % (pid, md2tex(P[pid])))
        cuerpo.append('\\textbf{Respuesta %s.} %s\n' % (pid, md2tex(R[pid])))

open('cuerpo_generado.tex', 'w', encoding='utf-8').write('\n'.join(cuerpo))
n = sum(len(P[k]) + len(R[k]) for k in P)
print('ejercicios 1-4:', n, 'caracteres')

# ── Discusión y reflexión final (sin nota): celda 21 preguntas, celda 22 respuestas ──
PD = {m.group(1): ' '.join(m.group(2).split())
      for m in re.finditer(r'^(\d)\.\s+(.*?)(?=^\d\.\s|\Z)', src(21), re.M | re.S)}
RD = {m.group(1): ' '.join(m.group(0).split())
      for m in re.finditer(r'^\*\*(\d)\..*?(?=^\*\*\d\.|\Z)', src(22), re.M | re.S)}
assert sorted(PD) == sorted(RD) == ['1', '2', '3'], (sorted(PD), sorted(RD))

refl = ['\\section{Discusión y reflexión final (sin nota)}\n']
for k in ('1', '2', '3'):
    refl.append('\\pregunta{%s}{%s}' % (k, md2tex(PD[k])))
    refl.append(md2tex(RD[k]) + '\n')
open('cuerpo_reflexion.tex', 'w', encoding='utf-8').write('\n'.join(refl))
nd = sum(len(PD[k]) + len(RD[k]) for k in PD)
print('discusión final:', nd, 'caracteres')
print('cuerpo_generado.tex y cuerpo_reflexion.tex escritos')
