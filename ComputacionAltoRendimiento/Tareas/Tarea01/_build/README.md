# Cómo se construyó la entrega

Pipeline reproducible (requiere el `.venv` de la carpeta superior):

```bash
source ../.venv/bin/activate
python build_nb.py          # genera Tarea01.ipynb (código + estructura, sin ejecutar)
jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=2400 ../Tarea01.ipynb
python add_informe.py       # genera la sección 6 (Informe) desde resultados.json
```

`add_informe.py` es **idempotente** y toma **todas** las cifras del informe desde
`resultados.json`, de modo que el texto nunca queda desincronizado de las mediciones.

Entorno: `uv venv --python 3.12` + numpy, scipy, joblib, matplotlib, scikit-learn,
psutil, threadpoolctl, jupyter.
