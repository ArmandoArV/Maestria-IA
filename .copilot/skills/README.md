# Maestría IA — Copilot Skills

Expert skills for the Magíster en IA (PUC Chile). Each folder is a self-contained skill
(`SKILL.md` + optional `references/`).

- `maestria-ia` — umbrella index/router across all courses (+ Bases de Datos, Data Science, Ética)
- `aprendizaje-supervisado` — EPG4001
- `aprendizaje-no-supervisado` — EPG4002
- `fundamentos-matematicos-ia` — IMT3850
- `recuperacion-informacion` — INF3841
- `pdf-reader` — utility for extracting PDF text

## Install on another computer

Copy these folders into your global Copilot skills directory:

```powershell
# Windows
Copy-Item -Recurse -Force .\.copilot\skills\* "$HOME\.copilot\skills\"
```

```bash
# macOS / Linux
cp -r ./.copilot/skills/* ~/.copilot/skills/
```

They also load automatically when working inside this repository.
