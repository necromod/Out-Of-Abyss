# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```powershell
# Setup (from System/ directory)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run (auto-opens http://127.0.0.1:5000)
python System/main.py
# or use the convenience script:
.\System\run_system.ps1

# Stop
.\System\stop_system.ps1

# Tests (server must be running first)
python -m pytest System/tests/test_sistema_completo.py -v

# Run a specific test class
python -m pytest System/tests/test_sistema_completo.py::TestAPIRest -v

# Run tests matching a keyword
python -m pytest System/tests/test_sistema_completo.py -v -k "personagem"
```

4 tests are intentionally skipped due to known bugs.

## Architecture

Flask app (localhost-only) for managing D&D 5e "Out of the Abyss" campaign sessions. Portuguese-language UI. All data is stored in `System/data/campaign.db` (SQLite, WAL mode).

```
System/
├── main.py                     # Entry point
├── app/
│   ├── __init__.py             # create_app() factory
│   ├── config.py               # Paths, SECRET_KEY, REGRAS_ATIVAS toggles
│   ├── modulos/                # Business logic
│   │   ├── database.py         # SQLite interface, BaseRepository, migrations
│   │   ├── repositories.py     # CRUD repositories for all entities
│   │   ├── combate.py          # Combat engine (initiative, rounds, turns)
│   │   ├── acoes.py            # Attack/damage resolution
│   │   ├── condicoes.py        # 15 PHB conditions with turn counters
│   │   ├── dados.py            # Dice expression parser ("2d6+3")
│   │   ├── regras_dnd_data.py  # Static D&D 5e data (races, classes, spells) — 67KB
│   │   └── regras/             # Modular rule books (phb, xanathar, tasha, etc.)
│   ├── routes/                 # Flask Blueprints
│   │   ├── api.py              # REST API (/api/*)
│   │   ├── fichas.py           # Character/monster/NPC CRUD (/fichas/*)
│   │   ├── sessao.py           # Session management (/sessao/*)
│   │   └── combate.py          # Combat actions (/combate/*)
│   └── static/
│       ├── js/
│       │   ├── sessao.js       # Core combat/session logic — 193KB, do not refactor lightly
│       │   ├── fichas.js       # Character sheet auto-save and form handling
│       │   └── widgets.js      # Draggable/resizable floating window system
│       └── css/
├── templates/                  # Jinja2 templates (base.html, fichas/, sessao/, widgets/)
├── data/
│   ├── campaign.db             # SQLite database (gitignored)
│   └── sessoes/                # Session state as JSON files
└── tests/
    └── test_sistema_completo.py  # 87 tests across 11 classes
```

**Rule system:** `config.py` has a `REGRAS_ATIVAS` dict that toggles which sourcebooks are active (`livro_jogador` is always required; others like `xanathar`, `tasha`, `fora_abismo` are optional). Rule modules in `app/modulos/regras/` implement a common base interface.

**Widget system:** The frontend `Widget` JS class provides draggable/resizable floating windows; `WidgetManager` persists their position and minimized state across page loads.

**All database access goes through repositories** — no raw SQL in route handlers. `BaseRepository` in `database.py` provides the common CRUD interface.
