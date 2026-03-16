# Bot Liga Sim Racing

Bot Discord em Python para gerir ligas de sim racing com foco em UX guiada por botões, Wizards e modals.

## Funcionalidades

- Setup inicial do servidor com wizard de 5 passos
- Gestão de temporadas, rondas, inscrições e staff
- Upload e publicação de resultados com parsers multi-sim
- Protestos com votação de stewards, penalty points e appeals
- Comunicação automática com APScheduler
- Geração de imagens para standings, resultados e calendário

## Requisitos

- Python 3.11+
- Discord Bot Token

## Instalação

```bash
cp .env.example .env
pip install -r requirements.txt
alembic upgrade head
python bot.py
```

## Variáveis de ambiente

- `DISCORD_BOT_TOKEN` ou `DISCORD_TOKEN`
- `DATABASE_URL`
- `GUILD_ID`
- `LOG_LEVEL`
- `TIMEZONE`
- `FONT_PATH`
- `FONT_BOLD_PATH`

## Estrutura

- `bot.py`: entrypoint assíncrono e carregamento de cogs
- `config.py`: leitura de ambiente e normalização de URLs
- `database/`: modelos, engine async e migrações Alembic
- `cogs/`: comandos slash, listeners e fluxos de negócio
- `views/`: componentes discord.py para Wizards e painéis
- `parsers/`: normalização de resultados ACC, rF2, iRacing e CSV
- `generators/`: renderização PNG com Pillow
- `utils/`: strings PT-PT, embeds, permissões, datas, validação
- `tests/`: cobertura de parsers e regras de domínio

## Testes

```bash
pytest tests/ -v
```

## Notas

- O runtime usa SQLAlchemy async.
- As migrações Alembic usam a URL síncrona derivada de `DATABASE_URL`.
- Sem token real, o projeto valida arranque estrutural, mas não autenticação live no Discord.
