# AGENTS.md — Bot Liga Sim Racing

## Repo Layout
- `bot.py` — entry point, carrega cogs
- `config.py` — variáveis de ambiente e constantes
- `database/` — SQLAlchemy models + Alembic migrations
- `cogs/` — lógica principal (admin, dashboard, registration, stewarding, results, communication, stats)
- `views/` — discord.py Views, Buttons, Selects, Modals
- `parsers/` — parsers de resultados (ACC JSON, rF2 XML, iRacing, CSV)
- `generators/` — geração de imagens com Pillow
- `utils/` — permissions, embeds, time_utils, validators, strings
- `data/` — tracks.json, cars.json, points_systems.json
- `tests/` — pytest + fixtures

## Stack
- Python 3.11+
- discord.py 2.x (slash commands, Views, Buttons, Selects, Modals)
- SQLite + SQLAlchemy 2.x + Alembic
- APScheduler
- Pillow

## Como correr
```bash
cp .env.example .env
# editar .env com DISCORD_BOT_TOKEN
pip install -r requirements.txt
alembic upgrade head
python bot.py
```

## Build & Test
```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Convenções obrigatórias
- Todas as strings de UI devem estar em `utils/strings.py` — NUNCA hardcoded nos cogs/views
- Idioma: Português PT-PT em toda a UI
- UX: buttons-first, wizard-flow, zero memorização
- Type hints em todo o código
- Sem broad try/catch — propagar erros explicitamente
- DRY: pesquisar helpers existentes antes de criar novos

## Definition of Done
- `pytest tests/ -v` passa sem erros
- Bot conecta ao Discord com `python bot.py` sem erros
- `/setup` dispara wizard com botões e modals
- `/painel` mostra hub central com botões funcionais
- Alembic migrations aplicam sem erros
