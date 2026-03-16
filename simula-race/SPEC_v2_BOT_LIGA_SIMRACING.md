# SPEC TÉCNICA v2.0 — Bot de Gestão de Liga de Sim Racing
## Documento de Arquitetura para Desenvolvimento (Codex)
### Versão revista com UX simplificada — "Zero Knowledge Required"

---

## NOTA PARA O CODEX

Este bot deve ser **extremamente intuitivo**. O utilizador principal (League Owner) não tem conhecimentos técnicos. Toda a interação deve ser feita via **botões, menus dropdown e modals** — nunca obrigar a digitar comandos com parâmetros. O bot guia o utilizador passo a passo.

**Princípios de UX obrigatórios:**
1. **Buttons-first:** Sempre que possível, apresentar opções como botões clicáveis
2. **Wizard-flow:** Operações complexas são guiadas passo a passo (nunca tudo num só comando)
3. **Confirmação visual:** Após cada ação, mostrar resumo claro do que aconteceu
4. **Idioma:** TUDO em Português (PT-PT). Exceções: termos universais de sim racing (DNF, pole, fastest lap, split, stint)
5. **Ajuda contextual:** Cada interação principal tem um botão [❓] que explica o que faz
6. **Drag & drop:** Aceitar ficheiros arrastados para canais específicos (resultados)
7. **Emojis funcionais:** Usar emojis para tornar a informação scannable (🟢 ativo, 🔴 urgente, ⏳ pendente, ✅ feito)
8. **Zero memorização:** O utilizador nunca precisa de lembrar o nome de um comando. O painel central (/painel) dá acesso a TUDO via botões

---

## 1. VISÃO GERAL

### 1.1 Objectivo
Bot Discord em Python que automatiza 80-90% da gestão operacional de uma liga de sim racing multi-sim. O League Owner intervém apenas em: upload de resultados (drag & drop), decisões de stewarding (clique em botões), e comunicação estratégica pontual.

### 1.2 Escala Alvo
- **Season 1:** 20-40 pilotos, 1 divisão, 10 rondas sprint
- **Escalável para:** 80+ pilotos, 3+ divisões, multi-sim, endurance

### 1.3 Stack Tecnológico
```
Runtime:         Python 3.11+
Framework:       discord.py 2.x (slash commands, Views, Buttons, Selects, Modals)
Base de Dados:   SQLite (dev/produção inicial) → PostgreSQL (se escalar)
ORM:             SQLAlchemy 2.x + Alembic (migrações)
Scheduler:       APScheduler (tarefas agendadas)
Imagens:         Pillow (PIL) para gerar standings/resultados em imagem
Parser Results:  JSON (ACC), XML (rF2), API (iRacing)
Hosting:         Oracle Cloud Free Tier (ARM VM) ou Hetzner ~5€/mês
```

### 1.4 API Necessária
**Única API obrigatória:** Discord Bot Token (gratuito, criado no Discord Developer Portal)
- Não há nenhuma outra API necessária para o MVP
- Resultados são ficheiros locais (JSON/XML) gerados pelo servidor de jogo e uploaded via Discord
- APIs opcionais futuras: iRacing Data API, Simracing.GP, SimResults.net

### 1.5 Estrutura de Ficheiros
```
simracing-league-bot/
├── bot.py                      # Entry point, carrega cogs
├── config.py                   # Settings, env vars, constantes
├── database/
│   ├── models.py               # SQLAlchemy models (todas as tabelas)
│   ├── engine.py               # DB connection, session factory
│   └── migrations/             # Alembic migrations
├── cogs/
│   ├── registration.py         # Inscrições, entry lists, elegibilidade
│   ├── stewarding.py           # Protestos, penalty points, licenças
│   ├── results.py              # Parse resultados, standings, pontos
│   ├── communication.py        # Anúncios automáticos, briefings, lembretes
│   ├── admin.py                # Setup wizard, seasons, rounds, config
│   ├── dashboard.py            # Painel central (/painel) — hub de navegação
│   └── stats.py                # Estatísticas, KPIs, dashboards
├── views/
│   ├── setup_wizard.py         # Views do wizard de setup inicial
│   ├── season_wizard.py        # Views do wizard de criação de temporada
│   ├── round_wizard.py         # Views do wizard de criação de rondas
│   ├── registration_views.py   # Views de inscrição (modals, botões)
│   ├── protest_views.py        # Views de protesto (modals, votação stewards)
│   ├── results_views.py        # Views de resultados (confirmação, correção)
│   ├── dashboard_views.py      # Views do painel central
│   ├── rsvp_views.py           # Views de RSVP (presença)
│   └── common.py               # Views partilhadas (confirmação, paginação, ajuda)
├── parsers/
│   ├── acc_parser.py           # Parser de resultados ACC (JSON)
│   ├── iracing_parser.py       # Parser de resultados iRacing (API/JSON)
│   ├── rf2_parser.py           # Parser de resultados rFactor 2 (XML)
│   └── generic_parser.py       # Fallback manual / CSV
├── generators/
│   ├── image_standings.py      # Gera imagens de standings com Pillow
│   ├── image_results.py        # Gera imagens de resultados por ronda
│   ├── image_calendar.py       # Gera imagem do calendário
│   └── templates/              # Fonts, backgrounds, logos
├── utils/
│   ├── permissions.py          # Role checks decorators
│   ├── embeds.py               # Helpers para embeds formatados PT
│   ├── time_utils.py           # Timezone handling (Europe/Lisbon)
│   ├── validators.py           # Validações de input
│   └── strings.py              # TODAS as strings em PT (centralizado)
├── data/
│   ├── tracks.json             # Base de dados de pistas
│   ├── cars.json               # Base de dados de carros por sim
│   ├── points_systems.json     # Sistemas de pontuação pré-definidos
│   └── strings_pt.json         # Strings de UI em Português (fallback)
├── tests/
│   ├── test_registration.py
│   ├── test_stewarding.py
│   ├── test_results.py
│   ├── test_parsers.py
│   └── fixtures/               # Ficheiros de exemplo para testes
│       ├── acc_result_sample.json
│       ├── rf2_result_sample.xml
│       └── csv_result_sample.csv
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 2. STRINGS — IDIOMA PORTUGUÊS

### 2.1 Ficheiro Centralizado (`utils/strings.py`)

**REGRA CRÍTICA:** Nenhuma string de UI deve estar hardcoded nos cogs ou views. Todas as strings visíveis ao utilizador devem vir deste módulo. Isto permite mudar o idioma no futuro com zero refactoring.

```python
"""
Todas as strings de interface em Português (PT-PT).
Importar como: from utils.strings import S
Uso: S.REGISTER_SUCCESS.format(name="João")
"""

class S:
    # ── Geral ──
    BOT_NAME = "🏁 Liga Bot"
    CONFIRM = "Confirmar"
    CANCEL = "Cancelar"
    BACK = "Voltar"
    NEXT = "Seguinte"
    HELP = "Ajuda"
    CLOSE = "Fechar"
    YES = "Sim"
    NO = "Não"
    SAVE = "Guardar"
    EDIT = "Editar"
    DELETE = "Apagar"
    LOADING = "A carregar..."
    SUCCESS = "✅ Sucesso!"
    ERROR = "❌ Erro"
    WARNING = "⚠️ Atenção"
    NO_PERMISSION = "🔒 Não tens permissão para fazer isto."
    
    # ── Setup Wizard ──
    SETUP_WELCOME = "👋 **Bem-vindo ao assistente de configuração!**\nVou ajudar-te a configurar a tua liga passo a passo."
    SETUP_STEP_NAME = "**Passo 1/5** — Como se chama a tua liga?"
    SETUP_STEP_NAME_PLACEHOLDER = "Ex: SimRacing Portugal GT3 Series"
    SETUP_STEP_SIM = "**Passo 2/5** — Qual é o simulador principal?"
    SETUP_STEP_TIMEZONE = "**Passo 3/5** — Qual é o fuso horário?"
    SETUP_STEP_COLORS = "**Passo 4/5** — Escolhe as cores da liga (para imagens e embeds)"
    SETUP_STEP_CHANNELS = "**Passo 5/5** — Vou criar os canais e roles necessários no servidor."
    SETUP_CHANNELS_CONFIRM = "Vou criar os seguintes canais:\n{channels}\n\nE os seguintes roles:\n{roles}\n\nPosso avançar?"
    SETUP_COMPLETE = "🎉 **Liga configurada com sucesso!**\n\n**{league_name}** está pronta.\nUsa `/painel` para ver o painel de controlo."
    
    # ── Painel / Dashboard ──
    DASHBOARD_TITLE = "🏁 PAINEL — {league_name}"
    DASHBOARD_NO_SEASON = "📭 Ainda não tens nenhuma temporada criada.\nClica no botão abaixo para criar a primeira!"
    DASHBOARD_SEASON_ACTIVE = "📅 **{season_name}** — ATIVA"
    DASHBOARD_ROUND_INFO = "Ronda {current}/{total} completada"
    DASHBOARD_NEXT_ROUND = "Próxima: **{track}**, {date} às {time}"
    DASHBOARD_DRIVERS = "👥 Pilotos: {approved} inscritos | {active} ativos"
    DASHBOARD_PROTESTS = "📋 Protestos: {pending} pendentes | {review} em análise"
    DASHBOARD_ALERTS = "⚠️ Alertas: {alerts}"
    DASHBOARD_PP_ALERT = "**{driver}** com {pp}/{max_pp} PP (perto de {consequence})"
    DASHBOARD_BTN_STANDINGS = "📊 Standings"
    DASHBOARD_BTN_RESULTS = "📋 Resultados"
    DASHBOARD_BTN_ENTRYLIST = "👥 Entry List"
    DASHBOARD_BTN_CALENDAR = "📅 Calendário"
    DASHBOARD_BTN_CONFIG = "⚙️ Configurações"
    DASHBOARD_BTN_NEW_SEASON = "➕ Nova Temporada"
    DASHBOARD_BTN_MANAGE_SEASON = "🔧 Gerir Temporada"
    DASHBOARD_BTN_ADD_ROUND = "➕ Adicionar Ronda"
    DASHBOARD_BTN_MANAGE_STAFF = "👤 Gerir Staff"
    DASHBOARD_BTN_PROTESTS = "⚖️ Protestos"
    DASHBOARD_BTN_EXPORT = "📤 Exportar Dados"
    DASHBOARD_BTN_HELP = "❓ Ajuda"
    
    # ── Temporada ──
    SEASON_WIZARD_TITLE = "📅 **Criar Nova Temporada**"
    SEASON_STEP_NAME = "**Passo 1/6** — Nome da temporada?"
    SEASON_STEP_NAME_PLACEHOLDER = "Ex: Season 1 - GT3 Sprint Series"
    SEASON_STEP_SIM = "**Passo 2/6** — Qual o simulador para esta temporada?"
    SEASON_STEP_ROUNDS = "**Passo 3/6** — Quantas rondas vai ter?"
    SEASON_STEP_DROPS = "**Passo 4/6** — Quantos piores resultados são descartados (drops)?"
    SEASON_STEP_DROPS_HELP = "💡 Drops permitem que os pilotos falhem 1-2 corridas sem prejudicar o campeonato. Recomendado: 2 drops para 10 rondas."
    SEASON_STEP_POINTS = "**Passo 5/6** — Qual o sistema de pontuação?"
    SEASON_STEP_CONFIRM = "**Passo 6/6** — Confirma os detalhes:"
    SEASON_CREATED = "✅ **Temporada criada!**\n\n**{name}**\n🎮 {sim} | 🏁 {rounds} rondas | 🗑️ {drops} drops\n📊 Pontuação: {points}\n\nAgora adiciona as rondas ao calendário com o botão abaixo."
    SEASON_STATUS_DRAFT = "📝 Rascunho"
    SEASON_STATUS_REGISTRATION = "📋 Inscrições Abertas"
    SEASON_STATUS_ACTIVE = "🟢 Ativa"
    SEASON_STATUS_FINISHED = "🏁 Terminada"
    SEASON_OPEN_REG = "📋 **Inscrições abertas!**\nOs pilotos já podem inscrever-se com `/inscrever`."
    SEASON_CLOSE_REG = "🔒 **Inscrições fechadas.**"
    
    # ── Rondas ──
    ROUND_WIZARD_TITLE = "🏁 **Adicionar Ronda**"
    ROUND_STEP_NUMBER = "**Passo 1/4** — Número da ronda?"
    ROUND_STEP_TRACK = "**Passo 2/4** — Qual a pista?"
    ROUND_STEP_TRACK_PLACEHOLDER = "Escreve o nome da pista (ex: Spa, Monza, Silverstone...)"
    ROUND_STEP_DATE = "**Passo 3/4** — Data e hora da corrida?"
    ROUND_STEP_DATE_PLACEHOLDER = "Ex: 2026-04-20 21:00"
    ROUND_STEP_DETAILS = "**Passo 4/4** — Detalhes adicionais"
    ROUND_CREATED = "✅ **Ronda {n} adicionada!**\n\n🏟️ {track} {flag}\n📅 {date} às {time}\n🌤️ {weather} | ⏱️ {duration} min | 🚦 {format}\n\n📨 Mensagens automáticas agendadas."
    ROUND_STATUS_SCHEDULED = "⬜ Agendada"
    ROUND_STATUS_NEXT = "🔴 Próxima"
    ROUND_STATUS_FINISHED = "✅ Concluída"
    ROUND_STATUS_RESULTS_PENDING = "⏳ Resultados Pendentes"
    
    # ── Inscrições ──
    REGISTER_TITLE = "📝 **Inscrição na Temporada**"
    REGISTER_BTN = "📝 Inscrever-me"
    REGISTER_MODAL_TITLE = "Inscrição — {season_name}"
    REGISTER_FIELD_NAME = "Nome real (opcional)"
    REGISTER_FIELD_NAME_PLACEHOLDER = "João Silva"
    REGISTER_FIELD_GAMEID = "Steam ID / iRacing ID"
    REGISTER_FIELD_GAMEID_PLACEHOLDER = "O teu ID na plataforma do jogo"
    REGISTER_FIELD_CAR_NUMBER = "Número do carro (1-999)"
    REGISTER_FIELD_CAR_NUMBER_PLACEHOLDER = "Ex: 77"
    REGISTER_FIELD_TEAM = "Nome da equipa (opcional)"
    REGISTER_FIELD_TEAM_PLACEHOLDER = "Ex: GT Racing Portugal"
    REGISTER_FIELD_NATIONALITY = "Nacionalidade"
    REGISTER_FIELD_NATIONALITY_PLACEHOLDER = "Ex: Portugal"
    REGISTER_SUCCESS = "✅ **Inscrição submetida!**\n\nOlá **{name}**, a tua inscrição foi recebida.\nEstado: ⏳ Pendente de aprovação\n\nReceberás uma mensagem quando for aprovada."
    REGISTER_ALREADY = "⚠️ Já estás inscrito nesta temporada."
    REGISTER_CLOSED = "🔒 As inscrições para esta temporada estão fechadas."
    REGISTER_FULL = "🔒 A temporada já atingiu o número máximo de pilotos."
    
    # ── Aprovação de inscrições ──
    APPROVE_NOTIFICATION = "📬 **Nova inscrição!**\n\n👤 {name}\n🎮 ID: {game_id}\n🚗 Carro #{car_number}\n🏳️ {nationality}"
    APPROVE_BTN_APPROVE = "✅ Aprovar"
    APPROVE_BTN_REJECT = "❌ Rejeitar"
    APPROVE_BTN_PROFILE = "👤 Ver Perfil"
    APPROVED_DM = "🎉 **Inscrição aprovada!**\n\nBem-vindo à **{season_name}**!\nDivisão: **{division}**\nNúmero: **#{car_number}**\n\nBoa sorte na pista! 🏁"
    REJECTED_DM = "❌ **Inscrição não aprovada.**\n\nMotivo: {reason}\n\nSe tiveres dúvidas, contacta a organização."
    REJECT_MODAL_TITLE = "Motivo da rejeição"
    REJECT_MODAL_PLACEHOLDER = "Explica brevemente o motivo..."
    
    # ── Entry List ──
    ENTRYLIST_TITLE = "👥 **ENTRY LIST — {season_name}**"
    ENTRYLIST_ROW = "`#{number:>3}` {flag} **{name}** — {team}"
    ENTRYLIST_FOOTER = "{total} pilotos inscritos | {approved} aprovados | {pending} pendentes"
    
    # ── RSVP / Presença ──
    RSVP_TITLE = "📋 **Presença — Ronda {n}: {track}**\n📅 {date} às {time}"
    RSVP_BTN_YES = "✅ Vou estar"
    RSVP_BTN_MAYBE = "🤷 Talvez"
    RSVP_BTN_NO = "❌ Não vou"
    RSVP_CONFIRMED = "✅ Presença confirmada para a Ronda {n}."
    RSVP_COUNT = "✅ {yes} confirmados | 🤷 {maybe} talvez | ❌ {no} ausentes"
    
    # ── Resultados ──
    RESULTS_DETECTED = "📂 **Ficheiro de resultados detetado!**\n\n🏟️ Pista: **{track}**\n👥 Pilotos: **{drivers}**\n🥇 Vencedor: **{winner}**\n⏱️ Melhor volta: **{best_lap}** ({best_lap_driver})\n\nIsto está correto?"
    RESULTS_BTN_PUBLISH = "✅ Publicar Resultados"
    RESULTS_BTN_CANCEL = "❌ Cancelar"
    RESULTS_BTN_CORRECT = "✏️ Corrigir"
    RESULTS_PROVISIONAL = "📊 **RESULTADOS PROVISÓRIOS — Ronda {n}: {track}** {flag}\n\n⏳ Período de cooldown ativo. Protestos abrem às **{protest_open}**."
    RESULTS_FINAL = "📊 **RESULTADOS FINAIS — Ronda {n}: {track}** {flag}"
    RESULTS_ROW = "`P{pos:>2}` {medal} **{name}** — {car} | ⏱️ {best_lap} | 📊 {points} pts"
    RESULTS_DNF = "`DNF` 💀 **{name}** — {car} | Voltas: {laps}"
    RESULTS_MEDAL_1 = "🥇"
    RESULTS_MEDAL_2 = "🥈"
    RESULTS_MEDAL_3 = "🥉"
    RESULTS_MEDAL_OTHER = "  "
    RESULTS_UNKNOWN_DRIVER = "⚠️ {count} piloto(s) no ficheiro não foram encontrados na base de dados:\n{names}\n\nQueres adicionar manualmente ou ignorar?"
    RESULTS_BTN_ADD_MANUAL = "➕ Adicionar"
    RESULTS_BTN_IGNORE = "🔇 Ignorar"
    
    # ── Standings ──
    STANDINGS_TITLE = "📊 **CLASSIFICAÇÃO — {season_name}**"
    STANDINGS_AFTER_ROUND = "Após Ronda {n}/{total} ({drops} drops aplicados)"
    STANDINGS_ROW = "`{pos:>2}.` {medal} **{name}** — **{points}** pts | {wins}V {podiums}P | Melhor: P{best}"
    STANDINGS_FOOTER = "Última atualização: {date}"
    
    # ── Protestos e Stewarding ──
    PROTEST_BTN = "📋 Submeter Protesto"
    PROTEST_COOLDOWN = "⏳ **Período de cooldown ativo.**\nProtestos para a Ronda {n} abrem às **{open_time}**.\nIsto existe para evitar decisões emocionais. Volta mais tarde!"
    PROTEST_EXPIRED = "❌ **Prazo expirado.**\nO prazo para submeter protestos da Ronda {n} encerrou às {close_time}."
    PROTEST_MODAL_TITLE = "Submeter Protesto — Ronda {n}"
    PROTEST_FIELD_ACCUSED = "Contra quem?"
    PROTEST_FIELD_ACCUSED_PLACEHOLDER = "Nome ou número do piloto"
    PROTEST_FIELD_LAP = "Em que volta aconteceu?"
    PROTEST_FIELD_LAP_PLACEHOLDER = "Ex: 5"
    PROTEST_FIELD_ZONE = "Zona da pista"
    PROTEST_FIELD_ZONE_PLACEHOLDER = "Ex: Curva 1, Reta principal"
    PROTEST_FIELD_DESCRIPTION = "Descrição do incidente"
    PROTEST_FIELD_DESCRIPTION_PLACEHOLDER = "Descreve factualmente o que aconteceu (máx. 500 caracteres)"
    PROTEST_FIELD_EVIDENCE = "Link para evidência (replay/clip)"
    PROTEST_FIELD_EVIDENCE_PLACEHOLDER = "https://youtube.com/... ou link do clip"
    PROTEST_SUCCESS = "✅ **Protesto submetido!**\n\n📋 Protesto **#{id}**\nContra: **{accused}**\nRonda {n}, Volta {lap}, {zone}\n\nOs stewards vão analisar o teu protesto. Receberás uma notificação com a decisão."
    PROTEST_NO_EVIDENCE = "❌ **Evidência obrigatória.**\nPrecisas de incluir um link para um clip ou replay do incidente."
    
    # ── Steward Panel ──
    STEWARD_NEW_PROTEST = "⚖️ **NOVO PROTESTO — #{id}**\n\n👤 Autor: **{author}**\n🎯 Acusado: **{accused}**\n🏁 Ronda {n}, Volta {lap}, {zone}\n\n📝 *\"{description}\"*\n🔗 Evidência: {evidence}"
    STEWARD_BTN_CLAIM = "🔍 Reclamar para Análise"
    STEWARD_BTN_GUILTY = "✅ Culpado"
    STEWARD_BTN_NOT_GUILTY = "❌ Não Culpado"
    STEWARD_BTN_RACING_INCIDENT = "🏁 Incidente de Corrida"
    STEWARD_BTN_DISMISS = "🗑️ Rejeitar Protesto"
    STEWARD_CLAIMED = "🔍 **{steward}** reclamou o protesto #{id} para análise."
    
    STEWARD_PENALTY_TITLE = "⚖️ **Seleciona a penalização:**"
    STEWARD_PENALTY_WARNING = "⚠️ Warning (sem tempo)"
    STEWARD_PENALTY_5S = "⏱️ +5 segundos"
    STEWARD_PENALTY_10S = "⏱️ +10 segundos"
    STEWARD_PENALTY_30S = "⏱️ +30 segundos"
    STEWARD_PENALTY_GRID3 = "📉 -3 posições na grelha"
    STEWARD_PENALTY_GRID5 = "📉 -5 posições na grelha"
    STEWARD_PENALTY_DSQ = "🚫 Desqualificação"
    STEWARD_PENALTY_SUSPENSION = "⛔ Suspensão (1 corrida)"
    STEWARD_PENALTY_BAN = "🔴 Ban"
    
    STEWARD_PP_TITLE = "Quantos penalty points?"
    STEWARD_REASONING_TITLE = "Justificação da decisão"
    STEWARD_REASONING_PLACEHOLDER = "Explica brevemente o motivo da decisão..."
    
    STEWARD_DECISION_PUBLISHED = "⚖️ **DECISÃO DOS STEWARDS — Protesto #{id}**\n\n📋 **{author}** vs **{accused}**\n🏁 Ronda {n}, Volta {lap}, {zone}\n\n🔎 **Descrição:** {description}\n\n📜 **Veredicto:** {verdict}\n⚡ **Penalização:** {penalty}\n📊 **Penalty Points:** +{pp} PP (total: {total_pp}/{max_pp})\n\n💬 **Justificação:** {reasoning}\n\n👨‍⚖️ Stewards: {stewards}"
    
    STEWARD_VERDICT_GUILTY = "Culpado"
    STEWARD_VERDICT_NOT_GUILTY = "Não Culpado"
    STEWARD_VERDICT_RACING_INCIDENT = "Incidente de Corrida"
    STEWARD_VERDICT_DISMISSED = "Protesto Rejeitado"
    
    # ── Penalty Points ──
    PP_STATUS = "📊 **Penalty Points — {name}**\n\n🔢 Total: **{total}/{max}** PP\n📈 Estado: {status}\n\n**Histórico:**\n{history}"
    PP_STATUS_CLEAN = "🟢 Limpo"
    PP_STATUS_WARNING = "🟡 Atenção"
    PP_STATUS_DANGER = "🟠 Perigo"
    PP_STATUS_CRITICAL = "🔴 Crítico"
    PP_THRESHOLD_WARNING = "⚠️ **ALERTA:** {name} atingiu **{pp} PP**. Próximo threshold: {next} PP ({consequence})."
    PP_THRESHOLD_SUSPEND = "⛔ **SUSPENSÃO AUTOMÁTICA:** {name} atingiu **{pp} PP** e está automaticamente suspenso da próxima corrida."
    PP_THRESHOLD_BAN = "🔴 **BAN AUTOMÁTICO:** {name} atingiu **{pp} PP** e está banido do campeonato.\n\n@Staff — é necessária confirmação."
    PP_DECAY = "🟢 **Decay:** {name} teve {races} corridas limpas consecutivas. **-{decay} PP** aplicados. (Novo total: {new_total} PP)"
    
    # ── Appeal ──
    APPEAL_BTN = "🔄 Recorrer da Decisão"
    APPEAL_WINDOW = "ℹ️ Tens **24 horas** após a decisão para submeter recurso."
    APPEAL_MODAL_TITLE = "Recurso — Protesto #{id}"
    APPEAL_MODAL_PLACEHOLDER = "Explica porque discordas da decisão..."
    APPEAL_SUCCESS = "🔄 **Recurso submetido!**\n\nO teu recurso ao Protesto #{id} foi registado.\nUm painel diferente de stewards irá re-analisar."
    APPEAL_EXPIRED = "❌ O prazo de 24h para recurso expirou."
    
    # ── Comunicação Automática ──
    COMM_ANNOUNCE_D7 = "📢 **RONDA {n} — {track}** {flag}\n\n📅 **{date}** às **{time}**\n🌤️ Condições: {weather}\n⏱️ Duração: {duration} min\n🚦 Formato: {format}\n\nConfirma a tua presença abaixo! 👇"
    COMM_BRIEFING = "📋 **BRIEFING — Ronda {n}: {track}** {flag}\n\n📅 {date} às {time}\n🌤️ {weather} | ⏱️ {duration} min\n\n🚦 **Procedimento de Arranque:** {start_type}\n🛣️ **Track Limits:** {track_limits}\n📌 **Notas:** {notes}\n\n⚠️ **Lembretes:**\n• Respeita o espaço dos outros pilotos\n• Volta 1: cautela extra\n• Problemas técnicos? Reporta no chat\n\nBoa corrida a todos! 🏁"
    COMM_REMINDER_D1 = "⏰ **LEMBRETE — Amanhã temos corrida!**\n\n🏟️ Ronda {n}: **{track}**\n📅 {date} às {time}\n\n✅ {rsvp_yes} confirmados | 🤷 {rsvp_maybe} talvez\n\nNão te esqueças de verificar o teu setup! 🔧"
    COMM_REMINDER_H2 = "🚨 **A corrida começa em 2 horas!**\n\n🏟️ {track}\n🕐 Servidor abre às {server_open}\n🏁 Corrida às {race_start}\n\n👥 {rsvp_yes} pilotos confirmados\n\nVemo-nos na pista! 🏎️"
    COMM_COOLDOWN_NOTICE = "⏳ **Resultados provisórios publicados.**\n\nPeríodo de cooldown ativo.\n📋 Protestos abrem: **{open_time}**\n📋 Prazo para protestos: **{close_time}**\n\n💡 *O cooldown existe para evitar decisões emocionais.*"
    COMM_PROTESTS_OPEN = "📋 **Protestos abertos para a Ronda {n}!**\n\n⏰ Prazo: até **{close_time}**\nUsa o botão abaixo ou `/protesto` para submeter."
    COMM_PROTESTS_CLOSE = "🔒 **Prazo de protestos encerrado para a Ronda {n}.**\n\nProtestos recebidos: {count}\nOs stewards vão analisar e publicar decisões em breve."
    
    # ── Staff ──
    STAFF_ADD_TITLE = "👤 **Adicionar Staff**"
    STAFF_ROLES = {
        "steward": "⚖️ Steward — Analisa protestos e atribui penalizações",
        "race_director": "🏁 Diretor de Corrida — Gere rondas, briefings e resultados",
        "admin": "⚙️ Admin — Gestão total da liga",
        "broadcaster": "📺 Broadcaster — Acesso a canais de broadcast"
    }
    STAFF_ADDED = "✅ **{name}** adicionado como **{role}**."
    STAFF_REMOVED = "❌ **{name}** removido do cargo de **{role}**."
    
    # ── Config ──
    CONFIG_TITLE = "⚙️ **Configurações — {league_name}**"
    CONFIG_COOLDOWN = "⏳ Cooldown de protestos"
    CONFIG_COOLDOWN_DESC = "Horas de espera obrigatória antes de aceitar protestos após uma corrida"
    CONFIG_PROTEST_DEADLINE = "📋 Prazo de protestos"
    CONFIG_PROTEST_DEADLINE_DESC = "Horas após a corrida para submeter protestos"
    CONFIG_PP_WARN = "🟡 Threshold Warning"
    CONFIG_PP_WARN_DESC = "PP para emitir aviso formal"
    CONFIG_PP_SUSPEND = "🟠 Threshold Suspensão"
    CONFIG_PP_SUSPEND_DESC = "PP para suspensão automática"
    CONFIG_PP_BAN = "🔴 Threshold Ban"
    CONFIG_PP_BAN_DESC = "PP para ban automático"
    CONFIG_PP_DECAY = "🟢 Decay"
    CONFIG_PP_DECAY_DESC = "PP que expiram após corridas limpas"
    CONFIG_PACE_THRESHOLD = "⏱️ Threshold de Pace"
    CONFIG_PACE_THRESHOLD_DESC = "% máxima acima do melhor tempo para pré-qualificação"
    CONFIG_SAVED = "✅ Configuração atualizada: **{setting}** → **{value}**"
    
    # ── Estatísticas ──
    STATS_DRIVER_TITLE = "📊 **Estatísticas — {name}**"
    STATS_POSITION = "🏆 Posição no campeonato: **{pos}º** de {total}"
    STATS_RACES = "🏁 Corridas: {completed}/{total} ({pct}%)"
    STATS_BEST = "⭐ Melhor resultado: **P{best}**"
    STATS_AVG = "📈 Posição média: **{avg}**"
    STATS_WINS = "🥇 Vitórias: **{wins}**"
    STATS_PODIUMS = "🏅 Pódios: **{podiums}**"
    STATS_DNFS = "💀 DNFs: **{dnfs}**"
    STATS_PP = "⚠️ Penalty Points: **{pp}/{max}**"
    STATS_FASTEST = "⚡ Voltas mais rápidas: **{fastest}**"
    
    KPIS_TITLE = "📊 **KPIs — {season_name}**"
    KPIS_RETENTION = "📌 Retenção: **{pct}%** ({count}/{total} pilotos completaram ≥70% das corridas)"
    KPIS_AVG_DRIVERS = "👥 Média de pilotos por corrida: **{avg}**"
    KPIS_INCIDENTS = "⚠️ Protestos por corrida: **{avg}**"
    KPIS_RESOLUTION = "⏱️ Tempo médio resolução: **{hours}h**"
    KPIS_NOSHOWS = "👻 No-shows por corrida: **{avg}**"
    
    # ── Exportação ──
    EXPORT_TITLE = "📤 **Exportar Dados**\n\nEscolhe o que queres exportar:"
    EXPORT_BTN_DRIVERS = "👥 Pilotos"
    EXPORT_BTN_STANDINGS = "📊 Standings"
    EXPORT_BTN_RESULTS = "📋 Resultados"
    EXPORT_BTN_PENALTIES = "⚖️ Penalizações"
    EXPORT_BTN_ALL = "📦 Tudo"
    EXPORT_SUCCESS = "✅ Ficheiro exportado! ({rows} registos)"
    
    # ── Ajuda ──
    HELP_MAIN = """❓ **AJUDA — Liga Bot**
    
🏁 **O que é este bot?**
Este bot gere a tua liga de sim racing automaticamente. Inscrições, resultados, penalizações, comunicação — tudo num sítio.

📌 **Como começar?**
1. Usa `/painel` para ver o painel de controlo
2. Cria uma temporada
3. Adiciona rondas ao calendário
4. Abre inscrições
5. O bot faz o resto!

🔑 **Comandos principais:**
`/painel` — Painel de controlo (acede a tudo)
`/inscrever` — Inscreve-te como piloto
`/protesto` — Submete um protesto
`/standings` — Ver classificação
`/resultados` — Ver resultados
`/pp` — Ver penalty points

👤 **Para Staff:**
`/painel` → Gerir Temporada
`/painel` → Protestos

💡 **Dica:** Não precisas de decorar comandos. O `/painel` dá-te acesso a tudo com botões."""

    HELP_REGISTRATION = """❓ **AJUDA — Inscrições**

📝 **Como me inscrevo?**
Usa `/inscrever` ou clica no botão de inscrição no canal de anúncios.

📋 **O que preciso?**
• Steam ID ou iRacing ID (conforme o sim)
• Número de carro desejado
• Nacionalidade

⏳ **Depois de me inscrever?**
A tua inscrição fica pendente até ser aprovada pela organização. Receberás uma mensagem privada quando for aprovada.

❌ **Posso desistir?**
Sim, usa `/desistir` a qualquer momento."""

    HELP_PROTESTS = """❓ **AJUDA — Protestos**

⚖️ **O que é um protesto?**
Se outro piloto te prejudicou em corrida (contacto, condução perigosa, etc.), podes submeter um protesto para os stewards analisarem.

⏳ **Quando posso protestar?**
Existe um período de cooldown após cada corrida (normalmente 12h). Isto é propositado — evita decisões emocionais. Depois do cooldown, tens normalmente 48h para submeter.

📋 **O que preciso?**
• Volta e zona da pista onde aconteceu
• Descrição factual (sem insultos!)
• Link para um clip/replay do incidente (OBRIGATÓRIO)

🔄 **Posso recorrer?**
Sim, tens 24h após a decisão para submeter recurso. Um painel diferente de stewards irá re-analisar."""

    HELP_PP = """❓ **AJUDA — Penalty Points**

📊 **O que são Penalty Points (PP)?**
São pontos de penalização acumulados durante a temporada. Quanto mais infrações, mais PP acumulas.

⚠️ **O que acontece quando acumulo PP?**
• 0-4 PP → 🟢 Sem consequências
• 5+ PP → 🟡 Warning formal
• 15+ PP → 🟠 Suspensão automática (1 corrida)
• 20+ PP → 🔴 Ban do campeonato

🟢 **Os PP expiram?**
Sim! A cada 4 corridas limpas (sem infrações), perdes 2 PP automaticamente. Condução limpa é recompensada.

💡 **Auto-reporte:** Se reportares o teu próprio erro honestamente, podes receber redução de 1 PP."""
```

---

## 3. BASE DE DADOS — SCHEMA COMPLETO

### 3.1 Diagrama de Relações
```
Guild ──────────┬──── Season ──────┬──── Round
                │                  ├──── Division
                │                  └──── PointsSystem
                │
                ├──── Driver ──────┬──── Registration (per season)
                │                  ├──── RaceResult (per round)
                │                  ├──── Protest (autor ou acusado)
                │                  ├──── PenaltyPoint
                │                  └──── LicenseStatus
                │
                ├──── StaffMember
                │
                └──── ChannelConfig (mapeamento de canais)
```

### 3.2 Tabelas

#### `guilds`
```sql
CREATE TABLE guilds (
    id                  BIGINT PRIMARY KEY,          -- Discord guild ID
    name                TEXT NOT NULL,
    league_name         TEXT NOT NULL,
    timezone            TEXT DEFAULT 'Europe/Lisbon',
    default_sim         TEXT DEFAULT 'ACC',
    cooldown_hours      INTEGER DEFAULT 12,
    protest_deadline_h  INTEGER DEFAULT 48,
    max_penalty_points  INTEGER DEFAULT 20,
    warn_threshold      INTEGER DEFAULT 5,
    suspend_threshold   INTEGER DEFAULT 15,
    decay_rate          INTEGER DEFAULT 2,
    decay_interval      INTEGER DEFAULT 4,
    pace_threshold_pct  REAL DEFAULT 103.0,
    logo_url            TEXT,
    primary_color       TEXT DEFAULT '#FF6600',
    secondary_color     TEXT DEFAULT '#1A1A2E',
    setup_complete      BOOLEAN DEFAULT FALSE,       -- Wizard concluído?
    created_at          TIMESTAMP DEFAULT NOW()
);
```

#### `channel_config` (NOVO — mapeia canais do Discord)
```sql
-- Em vez de hardcodar IDs, o wizard de setup regista os canais criados
CREATE TABLE channel_config (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    purpose             TEXT NOT NULL,               -- Ver lista abaixo
    channel_id          BIGINT NOT NULL,
    
    UNIQUE(guild_id, purpose)
);
-- purposes:
-- 'announcements'        → #anúncios
-- 'registrations'        → #inscrições
-- 'results'              → #resultados
-- 'standings'            → #classificação
-- 'briefing'             → #briefing-pré-corrida
-- 'protests'             → #protestos
-- 'steward_decisions'    → #decisões-stewards (read-only)
-- 'staff_general'        → #staff-geral (privado)
-- 'steward_deliberation' → #steward-deliberação (privado)
-- 'results_upload'       → #upload-resultados (staff, drag&drop)
```

#### `seasons`
```sql
CREATE TABLE seasons (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    name                TEXT NOT NULL,
    sim                 TEXT NOT NULL,
    status              TEXT DEFAULT 'draft',         -- draft, registration, active, finished
    num_rounds          INTEGER NOT NULL,
    drops               INTEGER DEFAULT 2,
    start_date          DATE,
    end_date            DATE,
    points_system_id    INTEGER REFERENCES points_systems(id),
    min_drivers         INTEGER DEFAULT 12,
    max_drivers         INTEGER DEFAULT 40,
    max_divisions       INTEGER DEFAULT 1,
    rulebook_url        TEXT,
    created_at          TIMESTAMP DEFAULT NOW()
);
```

#### `divisions`
```sql
CREATE TABLE divisions (
    id                  SERIAL PRIMARY KEY,
    season_id           INTEGER REFERENCES seasons(id),
    name                TEXT NOT NULL,
    tier                INTEGER DEFAULT 1,
    min_rating          REAL,
    max_rating          REAL,
    max_drivers         INTEGER DEFAULT 30
);
```

#### `rounds`
```sql
CREATE TABLE rounds (
    id                  SERIAL PRIMARY KEY,
    season_id           INTEGER REFERENCES seasons(id),
    round_number        INTEGER NOT NULL,
    track_name          TEXT NOT NULL,
    track_country       TEXT,
    track_flag          TEXT,                         -- Emoji flag
    format              TEXT DEFAULT 'sprint',
    start_type          TEXT DEFAULT 'rolling',       -- rolling, standing
    race_duration_min   INTEGER DEFAULT 40,
    weather             TEXT DEFAULT 'dry',
    date_time           TIMESTAMP NOT NULL,
    status              TEXT DEFAULT 'scheduled',
    server_info         TEXT,
    briefing_text       TEXT,
    track_limits_notes  TEXT,
    results_file_path   TEXT,
    
    -- Timestamps automáticos
    briefing_sent_at    TIMESTAMP,
    reminder_sent_at    TIMESTAMP,
    results_posted_at   TIMESTAMP,
    protests_open_at    TIMESTAMP,
    protests_close_at   TIMESTAMP,
    final_results_at    TIMESTAMP,
    
    UNIQUE(season_id, round_number)
);
```

#### `drivers`
```sql
CREATE TABLE drivers (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    discord_id          BIGINT NOT NULL,
    discord_name        TEXT NOT NULL,
    real_name           TEXT,
    steam_id            TEXT,
    iracing_id          TEXT,
    rf2_id              TEXT,
    nationality         TEXT,
    nationality_flag    TEXT,                         -- Emoji flag
    timezone            TEXT DEFAULT 'Europe/Lisbon',
    car_number          INTEGER,
    team_name           TEXT,
    joined_at           TIMESTAMP DEFAULT NOW(),
    is_active           BOOLEAN DEFAULT TRUE,
    
    UNIQUE(guild_id, discord_id)
);
```

#### `registrations`
```sql
CREATE TABLE registrations (
    id                  SERIAL PRIMARY KEY,
    driver_id           INTEGER REFERENCES drivers(id),
    season_id           INTEGER REFERENCES seasons(id),
    division_id         INTEGER REFERENCES divisions(id),
    status              TEXT DEFAULT 'pending',       -- pending, approved, rejected, withdrawn
    hotlap_time_ms      INTEGER,
    hotlap_track        TEXT,
    registered_at       TIMESTAMP DEFAULT NOW(),
    approved_at         TIMESTAMP,
    approved_by         BIGINT,
    rejection_reason    TEXT,
    
    UNIQUE(driver_id, season_id)
);
```

#### `race_results`
```sql
CREATE TABLE race_results (
    id                  SERIAL PRIMARY KEY,
    round_id            INTEGER REFERENCES rounds(id),
    driver_id           INTEGER REFERENCES drivers(id),
    division_id         INTEGER REFERENCES divisions(id),
    finish_position     INTEGER,
    grid_position       INTEGER,
    best_lap_ms         INTEGER,
    total_time_ms       BIGINT,
    laps_completed      INTEGER,
    status              TEXT DEFAULT 'finished',      -- finished, dnf, dsq, dns
    base_points         INTEGER DEFAULT 0,
    bonus_points        INTEGER DEFAULT 0,
    penalty_time_sec    INTEGER DEFAULT 0,
    final_points        INTEGER DEFAULT 0,
    car_model           TEXT,
    incidents           INTEGER DEFAULT 0,
    
    UNIQUE(round_id, driver_id)
);
```

#### `points_systems`
```sql
CREATE TABLE points_systems (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    name                TEXT NOT NULL,
    points_per_position JSONB NOT NULL,
    pole_bonus          INTEGER DEFAULT 0,
    fastest_lap_bonus   INTEGER DEFAULT 0,
    most_positions_bonus INTEGER DEFAULT 0,
    finish_bonus        INTEGER DEFAULT 0,
    tiebreak_order      JSONB DEFAULT '["wins", "podiums", "best_finish"]'
);
```

#### `protests`
```sql
CREATE TABLE protests (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    round_id            INTEGER REFERENCES rounds(id),
    author_driver_id    INTEGER REFERENCES drivers(id),
    accused_driver_id   INTEGER REFERENCES drivers(id),
    lap_number          INTEGER,
    turn_zone           TEXT,
    description         TEXT NOT NULL,
    evidence_url        TEXT NOT NULL,                -- OBRIGATÓRIO
    status              TEXT DEFAULT 'submitted',
    submitted_at        TIMESTAMP DEFAULT NOW(),
    cooldown_expires_at TIMESTAMP,
    assigned_stewards   JSONB,
    
    -- Votos individuais dos stewards (NOVO)
    votes               JSONB DEFAULT '[]',          -- [{steward_id, verdict, penalty_type, penalty_value, pp, reasoning}]
    
    -- Decisão final (calculada por maioria)
    verdict             TEXT,
    penalty_type        TEXT,
    penalty_value       TEXT,
    penalty_points      INTEGER DEFAULT 0,
    reasoning           TEXT,
    decided_at          TIMESTAMP,
    
    -- Appeal
    appeal_reason       TEXT,
    appeal_deadline     TIMESTAMP,                   -- 24h após decisão
    appeal_verdict      TEXT,
    appeal_decided_at   TIMESTAMP,
    
    -- Mensagens Discord (para editar embeds)
    staff_message_id    BIGINT,                      -- ID da mensagem no canal de stewards
    public_message_id   BIGINT                       -- ID da mensagem no canal de decisões
);
```

#### `penalty_points`
```sql
CREATE TABLE penalty_points (
    id                  SERIAL PRIMARY KEY,
    driver_id           INTEGER REFERENCES drivers(id),
    season_id           INTEGER REFERENCES seasons(id),
    protest_id          INTEGER REFERENCES protests(id),
    round_id            INTEGER REFERENCES rounds(id),
    points              INTEGER NOT NULL,
    reason              TEXT NOT NULL,
    type                TEXT DEFAULT 'penalty',       -- penalty, decay, redemption, manual
    created_at          TIMESTAMP DEFAULT NOW()
);
```

#### `staff_members`
```sql
CREATE TABLE staff_members (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    discord_id          BIGINT NOT NULL,
    role                TEXT NOT NULL,
    is_active           BOOLEAN DEFAULT TRUE,
    appointed_at        TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(guild_id, discord_id, role)
);
```

#### `scheduled_messages`
```sql
CREATE TABLE scheduled_messages (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    round_id            INTEGER REFERENCES rounds(id),
    type                TEXT NOT NULL,
    channel_purpose     TEXT NOT NULL,               -- Referência ao channel_config.purpose
    scheduled_for       TIMESTAMP NOT NULL,
    sent                BOOLEAN DEFAULT FALSE,
    sent_at             TIMESTAMP,
    message_id          BIGINT
);
```

#### `rsvp`
```sql
CREATE TABLE rsvp (
    id                  SERIAL PRIMARY KEY,
    round_id            INTEGER REFERENCES rounds(id),
    driver_id           INTEGER REFERENCES drivers(id),
    status              TEXT DEFAULT 'confirmed',
    responded_at        TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(round_id, driver_id)
);
```

#### `audit_log`
```sql
CREATE TABLE audit_log (
    id                  SERIAL PRIMARY KEY,
    guild_id            BIGINT REFERENCES guilds(id),
    actor_discord_id    BIGINT,
    action              TEXT NOT NULL,
    target_type         TEXT,
    target_id           INTEGER,
    details             JSONB,
    created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## 4. VIEWS — INTERAÇÕES VISUAIS (BUTTONS, SELECTS, MODALS)

### 4.1 Padrão de Views

**REGRA CRÍTICA:** Todas as Views devem ter `timeout=300` (5 minutos) e tratar o timeout gracefully (editar a mensagem para desativar os botões). Usar `discord.ui.View`, `discord.ui.Button`, `discord.ui.Select`, `discord.ui.Modal`.

```python
# Padrão base para todas as Views
class BaseView(discord.ui.View):
    def __init__(self, author_id: int, timeout: float = 300):
        super().__init__(timeout=timeout)
        self.author_id = author_id  # Só o autor pode interagir
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                S.NO_PERMISSION, ephemeral=True
            )
            return False
        return True
    
    async def on_timeout(self):
        # Desativar todos os botões quando expira
        for item in self.children:
            item.disabled = True
        # Tentar editar a mensagem (pode falhar se já foi apagada)
        try:
            await self.message.edit(view=self)
        except Exception:
            pass
```

### 4.2 Setup Wizard (`views/setup_wizard.py`)

**Trigger:** `/setup` (apenas server owner, apenas uma vez)

**Flow visual completo:**

```
PASSO 1 — Nome da Liga
┌─────────────────────────────────────┐
│ 👋 Bem-vindo ao assistente!         │
│                                     │
│ Passo 1/5 — Como se chama a liga?   │
│                                     │
│ [📝 Definir Nome]                   │
└─────────────────────────────────────┘
     │ Clica botão → abre Modal
     ▼
┌─ MODAL ─────────────────────────────┐
│ Nome da Liga                        │
│ ┌─────────────────────────────────┐ │
│ │ SimRacing Portugal GT3 Series   │ │
│ └─────────────────────────────────┘ │
│                    [Cancelar] [OK]  │
└─────────────────────────────────────┘

PASSO 2 — Simulador
┌─────────────────────────────────────┐
│ Passo 2/5 — Simulador principal?    │
│                                     │
│ [ACC] [iRacing] [rF2] [AMS2]       │
│ [RENNSPORT] [Vários]               │
└─────────────────────────────────────┘

PASSO 3 — Fuso Horário
┌─────────────────────────────────────┐
│ Passo 3/5 — Fuso horário?          │
│                                     │
│ ┌─ Dropdown ──────────────────┐     │
│ │ Europe/Lisbon (Portugal)    │     │
│ │ Europe/Madrid (Espanha)     │     │
│ │ Europe/London (Reino Unido) │     │
│ │ America/Sao_Paulo (Brasil)  │     │
│ └─────────────────────────────┘     │
└─────────────────────────────────────┘

PASSO 4 — Cores
┌─────────────────────────────────────┐
│ Passo 4/5 — Estilo visual          │
│                                     │
│ Escolhe um tema de cores:           │
│                                     │
│ [🟠 Laranja Racing]                │
│ [🔵 Azul Velocidade]               │
│ [🔴 Vermelho Paixão]               │
│ [🟢 Verde Endurance]               │
│ [⚪ Personalizar]                   │
└─────────────────────────────────────┘

PASSO 5 — Confirmação e Criação
┌─────────────────────────────────────┐
│ Passo 5/5 — Tudo pronto!           │
│                                     │
│ Liga: SimRacing Portugal GT3 Series │
│ Sim: Vários                         │
│ Timezone: Europe/Lisbon             │
│ Tema: 🟠 Laranja Racing            │
│                                     │
│ Vou criar estes canais:             │
│ #anúncios, #inscrições,            │
│ #resultados, #classificação,        │
│ #briefing-pré-corrida,             │
│ #protestos, #decisões-stewards,     │
│ #upload-resultados,                 │
│ #staff-geral, #steward-deliberação  │
│                                     │
│ E estes roles:                      │
│ @League Owner, @Race Director,      │
│ @Steward, @Piloto, @Inscrito        │
│                                     │
│ [✅ Criar Tudo] [❌ Cancelar]       │
└─────────────────────────────────────┘

RESULTADO
┌─────────────────────────────────────┐
│ 🎉 Liga configurada com sucesso!   │
│                                     │
│ SimRacing Portugal GT3 Series       │
│ está pronta.                        │
│                                     │
│ Próximo passo: cria a tua primeira  │
│ temporada!                          │
│                                     │
│ [📅 Criar Temporada] [📋 Ver Painel]│
└─────────────────────────────────────┘
```

**Implementação:** Cada passo é uma View diferente. Quando o utilizador clica o botão, a View edita a mensagem original com o próximo passo (não cria nova mensagem). Dados acumulados num dict passado entre Views.

```python
class SetupWizardStep1(BaseView):
    def __init__(self, author_id: int):
        super().__init__(author_id=author_id)
        self.data = {}  # Acumula dados ao longo dos passos
    
    @discord.ui.button(label="📝 Definir Nome", style=discord.ButtonStyle.primary)
    async def set_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = SetupNameModal(self)
        await interaction.response.send_modal(modal)

class SetupNameModal(discord.ui.Modal, title="Nome da Liga"):
    name = discord.ui.TextInput(
        label="Nome da Liga",
        placeholder="Ex: SimRacing Portugal GT3 Series",
        max_length=100
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        self.view.data['league_name'] = self.name.value
        # Avança para o passo 2 (editando a mesma mensagem)
        step2 = SetupWizardStep2(self.view.author_id, self.view.data)
        embed = discord.Embed(description=S.SETUP_STEP_SIM, color=0xFF6600)
        await interaction.response.edit_message(embed=embed, view=step2)
```

### 4.3 Painel Central (`views/dashboard_views.py`)

**Trigger:** `/painel`

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ 🏁 PAINEL — SimRacing Portugal GT3 Series       │
│                                                 │
│ 📅 Season 1 — GT3 Sprint (ATIVA)               │
│    Ronda 4/10 completada                        │
│    Próxima: Spa-Francorchamps, 20 Abr 21:00    │
│                                                 │
│ 👥 Pilotos: 28 inscritos | 24 ativos            │
│ 📋 Protestos: 1 pendente                       │
│ ⚠️ João Silva com 13/20 PP (perto de suspensão) │
├─────────────────────────────────────────────────┤
│ Ações Rápidas:                                  │
│                                                 │
│ [📊 Standings] [📋 Resultados] [👥 Entry List]  │
│ [📅 Calendário] [⚖️ Protestos] [⚙️ Config]     │
│                                                 │
│ Gestão (Staff):                                 │
│ [➕ Nova Temporada] [🔧 Gerir Temporada]         │
│ [➕ Adicionar Ronda] [👤 Gerir Staff]            │
│ [📤 Exportar Dados] [❓ Ajuda]                  │
└─────────────────────────────────────────────────┘
```

**Comportamento:** Os botões de "Gestão" só aparecem para utilizadores com roles de staff. Pilotos normais vêm apenas as "Ações Rápidas".

Cada botão do painel abre uma sub-View (editando a mesma mensagem) com um botão [⬅️ Voltar ao Painel] para navegação.

### 4.4 Season Wizard (`views/season_wizard.py`)

**Trigger:** Botão "Nova Temporada" no Painel

```
PASSO 1 — Nome
    Modal: "Nome da temporada"

PASSO 2 — Simulador
    Botões: [ACC] [iRacing] [rF2] [AMS2] [RENNSPORT]

PASSO 3 — Nº de Rondas
    Botões: [6] [8] [10] [12] [Outro]
    Se "Outro" → Modal com campo numérico

PASSO 4 — Drops
    Botões: [0] [1] [2] [3]
    + Texto explicativo: "💡 Drops permitem falhar corridas sem prejudicar o campeonato"

PASSO 5 — Pontuação
    Select Menu:
    - 🏎️ F1 2026 (25-18-15-12-10-8-6-4-2-1 + pole + fastest lap)
    - 📊 Linear (30-27-25-23-21... todos pontuam)
    - 🏁 Endurance (50-40-32... pontos altos + bonus)
    - ⚙️ Personalizar

PASSO 6 — Confirmação
    Resumo + [✅ Criar] [❌ Cancelar]
```

### 4.5 Round Wizard (`views/round_wizard.py`)

**Trigger:** Botão "Adicionar Ronda" no Painel

```
PASSO 1 — Número da Ronda
    Select: [1] [2] [3] ... [N] (filtra números já usados)

PASSO 2 — Pista
    Modal com Autocomplete:
    - O piloto começa a escrever "Spa" → aparece "Circuit de Spa-Francorchamps 🇧🇪"
    - Dados carregados de data/tracks.json

PASSO 3 — Data e Hora
    Modal:
    - Campo "Data" (placeholder: "2026-04-20")
    - Campo "Hora" (placeholder: "21:00")
    - Nota: "Hora de Lisboa (GMT+0/+1)"

PASSO 4 — Detalhes
    Botões para:
    - Formato: [Sprint] [Endurance]
    - Duração: [30 min] [40 min] [60 min] [Outro]
    - Weather: [🌞 Seco] [🌧️ Chuva] [🌤️ Dinâmico] [🎲 Aleatório]
    - Arranque: [🏁 Lançado] [🚦 Parado]

Confirmação + [✅ Criar Ronda]
```

**Após criação:** O bot agenda automaticamente TODAS as mensagens:
- D-7: Anúncio com RSVP
- D-2: Briefing
- D-1: Lembrete
- H-2: Lembrete final
- Post-race + cooldown: Abertura protestos
- Post-race + deadline: Fecho protestos

### 4.6 Protest Wizard (`views/protest_views.py`)

**Trigger:** `/protesto` ou botão "Submeter Protesto" no canal #protestos

**Pre-checks automáticos (antes de mostrar qualquer coisa):**
1. Há temporada ativa? → Se não: "Não há temporada ativa."
2. Há rondas concluídas? → Se não: "Nenhuma corrida realizada ainda."
3. Cooldown ativo? → Se sim: "⏳ Protestos abrem às {hora}."
4. Prazo expirado? → Se sim: "❌ Prazo encerrou."
5. O piloto participou na última ronda? → Se não: "Só pilotos que participaram podem protestar."

**Se tudo OK:**

```
PASSO 1 — Contra quem?
    Select Menu com lista de pilotos que participaram na ronda
    (excluindo o próprio autor)

PASSO 2 — Modal com detalhes
    - Volta (número)
    - Zona da pista (ex: "Curva 1")
    - Descrição (máx 500 chars)
    - Link evidência (OBRIGATÓRIO)

CONFIRMAÇÃO
┌─────────────────────────────────────┐
│ 📋 Protesto #42                     │
│                                     │
│ Contra: João Silva (#77)            │
│ Ronda 4, Volta 5, Curva 1          │
│ "Contacto evitável na entrada..."   │
│ 🔗 Evidência: https://...           │
│                                     │
│ [✅ Confirmar] [❌ Cancelar]         │
└─────────────────────────────────────┘
```

### 4.7 Steward Voting Panel (`views/protest_views.py`)

**Aparece em:** #steward-deliberação (canal privado)

```
PAINEL INICIAL (quando protesto é submetido)
┌─────────────────────────────────────────────────┐
│ ⚖️ NOVO PROTESTO — #42                          │
│                                                 │
│ 👤 Autor: Pedro Santos (#12)                    │
│ 🎯 Acusado: João Silva (#77)                   │
│ 🏁 Ronda 4, Volta 5, Curva 1                   │
│                                                 │
│ 📝 "Contacto evitável na entrada da curva 1.    │
│ O carro #77 travou demasiado tarde e embateu    │
│ no meu carro."                                  │
│                                                 │
│ 🔗 Evidência: https://youtube.com/...           │
│                                                 │
│ [🔍 Reclamar para Análise]                      │
└─────────────────────────────────────────────────┘

APÓS STEWARD RECLAMAR
┌─────────────────────────────────────────────────┐
│ ⚖️ PROTESTO #42 — Em análise                    │
│ 🔍 Steward: @Miguel Costa                      │
│ (... mesmos detalhes ...)                       │
│                                                 │
│ Qual é o teu veredicto?                         │
│                                                 │
│ [✅ Culpado] [❌ Não Culpado]                    │
│ [🏁 Incidente de Corrida] [🗑️ Rejeitar]         │
└─────────────────────────────────────────────────┘

SE CLICA "CULPADO" → Select Menu de penalização
┌─────────────────────────────────────┐
│ Seleciona a penalização:            │
│ ┌─ Dropdown ─────────────────────┐  │
│ │ ⚠️ Warning (sem tempo)         │  │
│ │ ⏱️ +5 segundos                 │  │
│ │ ⏱️ +10 segundos                │  │
│ │ ⏱️ +30 segundos                │  │
│ │ 📉 -3 posições na grelha       │  │
│ │ 📉 -5 posições na grelha       │  │
│ │ 🚫 Desqualificação             │  │
│ │ ⛔ Suspensão (1 corrida)       │  │
│ │ 🔴 Ban                        │  │
│ └────────────────────────────────┘  │
└─────────────────────────────────────┘

→ Select de Penalty Points: [0] [1] [2] [3] [4] [5]

→ Modal para justificação:
┌─ MODAL ─────────────────────────────┐
│ Justificação da decisão             │
│ ┌─────────────────────────────────┐ │
│ │ Contacto evitável. O piloto #77 │ │
│ │ travou demasiado tarde e não    │ │
│ │ tinha overlap suficiente.       │ │
│ └─────────────────────────────────┘ │
│                    [Cancelar] [OK]  │
└─────────────────────────────────────┘

VOTO REGISTADO
┌─────────────────────────────────────────────────┐
│ ⚖️ PROTESTO #42 — Votos: 1/3                    │
│                                                 │
│ ✅ @Miguel Costa: Culpado (+5s, 3PP)            │
│ ⏳ @Ana Ferreira: Pendente                      │
│ ⏳ @Rui Santos: Pendente                        │
│                                                 │
│ Faltam 2 votos para decisão.                    │
└─────────────────────────────────────────────────┘

DECISÃO FINAL (maioria atingida — auto-publicada no #decisões-stewards)
┌─────────────────────────────────────────────────┐
│ ⚖️ DECISÃO DOS STEWARDS — Protesto #42          │
│                                                 │
│ 📋 Pedro Santos vs João Silva                   │
│ 🏁 Ronda 4, Volta 5, Curva 1                   │
│                                                 │
│ 🔎 Contacto na entrada da curva 1               │
│                                                 │
│ 📜 Veredicto: CULPADO                           │
│ ⚡ Penalização: +5 segundos                     │
│ 📊 Penalty Points: +3 PP (total: 6/20)         │
│                                                 │
│ 💬 Justificação: Contacto evitável. O piloto    │
│ #77 travou demasiado tarde e não tinha overlap  │
│ suficiente na entrada da curva.                 │
│                                                 │
│ 👨‍⚖️ Stewards: Miguel Costa, Ana Ferreira,       │
│ Rui Santos                                      │
│ 📅 Decisão: 22/04/2026 às 14:30                │
└─────────────────────────────────────────────────┘
```

### 4.8 Results Upload (`views/results_views.py`)

**Trigger:** Ficheiro arrastado para o canal #upload-resultados (ou `/resultados upload`)

**Deteção automática:** O bot escuta mensagens com attachments no canal #upload-resultados. Quando deteta um ficheiro .json ou .xml:

```python
# Em cogs/results.py
@commands.Cog.listener()
async def on_message(self, message: discord.Message):
    # Verificar se é no canal de upload
    upload_channel = await get_channel(message.guild.id, 'results_upload')
    if message.channel.id != upload_channel:
        return
    
    # Verificar se tem attachment
    if not message.attachments:
        return
    
    for attachment in message.attachments:
        if attachment.filename.endswith(('.json', '.xml', '.csv')):
            await self.process_results_file(message, attachment)
```

**Flow visual:**

```
Utilizador arrasta ficheiro → Bot responde:

┌─────────────────────────────────────────────────┐
│ 📂 Ficheiro de resultados detetado!             │
│                                                 │
│ 🏟️ Pista: Spa-Francorchamps                    │
│ 🎮 Sim: ACC                                    │
│ 👥 Pilotos encontrados: 24                      │
│ 🥇 Vencedor: Pedro Santos (#12)                │
│ ⏱️ Melhor volta: 2:18.456 (João Silva)          │
│                                                 │
│ ⚠️ 2 pilotos não reconhecidos:                  │
│    • SteamID 76561198... → desconhecido         │
│    • SteamID 76561199... → desconhecido         │
│                                                 │
│ Ronda correspondente: Ronda 5 (Spa)             │
│                                                 │
│ [✅ Publicar] [✏️ Corrigir] [❌ Cancelar]        │
└─────────────────────────────────────────────────┘
```

Se "Corrigir" → permite editar posições, adicionar pilotos em falta, corrigir matchings.

### 4.9 RSVP View (`views/rsvp_views.py`)

**Aparece em:** Embed de anúncio de ronda (automático D-7)

```
┌─────────────────────────────────────────────────┐
│ 📢 RONDA 5 — Spa-Francorchamps 🇧🇪              │
│                                                 │
│ 📅 20 de Abril de 2026 às 21:00                 │
│ 🌤️ Seco | ⏱️ 40 min | 🚦 Sprint | 🏁 Lançado   │
│                                                 │
│ ✅ 18 confirmados | 🤷 3 talvez | ❌ 2 ausentes  │
│                                                 │
│ [✅ Vou estar] [🤷 Talvez] [❌ Não vou]          │
└─────────────────────────────────────────────────┘
```

**Comportamento:** O embed atualiza automaticamente a contagem quando alguém clica. Os botões são **persistent** (sobrevivem a reinícios do bot) usando `custom_id` estáticos.

---

## 5. MÓDULOS — ESPECIFICAÇÃO DE COGS

### 5.1 COG: Dashboard (`cogs/dashboard.py`)

**Único comando que o utilizador precisa de saber:** `/painel`

```python
@app_commands.command(name="painel", description="Painel de controlo da liga")
async def dashboard(self, interaction: discord.Interaction):
    """
    Hub central. Verifica o role do utilizador e mostra:
    - Staff: todos os botões (gestão + info)
    - Piloto: apenas botões de info
    - Sem role: mensagem de como se inscrever
    """
```

### 5.2 COG: Admin (`cogs/admin.py`)

**Slash Commands:**

| Comando | Descrição | Trigger alternativo |
|---------|-----------|---------------------|
| `/setup` | Wizard de configuração inicial | Apenas 1ª vez |
| `/painel` | Hub central | — |

Tudo o resto é acessível via botões no painel:
- Nova Temporada → `season_wizard.py`
- Adicionar Ronda → `round_wizard.py`
- Gerir Staff → `StaffManageView`
- Configurações → `ConfigView`
- Exportar → `ExportView`

### 5.3 COG: Registration (`cogs/registration.py`)

**Slash Commands:**

| Comando | Descrição | Acesso |
|---------|-----------|--------|
| `/inscrever` | Abre modal de inscrição | Qualquer |
| `/desistir` | Retira inscrição | Piloto inscrito |
| `/entrylist` | Mostra entry list | Qualquer |
| `/hotlap <tempo>` | Regista tempo de hotlap | Piloto inscrito |

**Listeners:**
- Botão "Inscrever-me" (se postado no canal #inscrições)
- Botões "Aprovar" / "Rejeitar" (no canal #staff-geral quando nova inscrição chega)

### 5.4 COG: Stewarding (`cogs/stewarding.py`)

**Slash Commands:**

| Comando | Descrição | Acesso |
|---------|-----------|--------|
| `/protesto` | Wizard de protesto | Piloto que participou |
| `/pp` | Ver PP próprios | Qualquer |
| `/pp @piloto` | Ver PP de outro piloto | Qualquer |

**Listeners e Views:**
- `ProtestWizardView` — Wizard completo de protesto
- `StewardVotingView` — Painel de votação para stewards (persistent)
- `PenaltySelectView` — Seleção de penalização
- `AppealView` — Botão de recurso (aparece 24h após decisão)

**Automações (APScheduler):**
- `check_cooldown_open` — Quando cooldown expira, publica aviso
- `check_protest_deadline` — Quando prazo expira, fecha protestos
- `check_pp_decay` — Após cada ronda finalizada, verifica decays

**REGRA: steward não pode julgar protesto onde está envolvido:**
```python
async def can_steward_vote(steward_id: int, protest: Protest) -> bool:
    """Verifica se o steward pode votar neste protesto."""
    author = await get_driver_by_discord_id(protest.guild_id, steward_id)
    if author and (author.id == protest.author_driver_id or 
                   author.id == protest.accused_driver_id):
        return False
    return True
```

### 5.5 COG: Results (`cogs/results.py`)

**Slash Commands:**

| Comando | Descrição | Acesso |
|---------|-----------|--------|
| `/resultados` | Mostra resultados da última ronda | Qualquer |
| `/resultados ronda <N>` | Resultados de ronda específica | Qualquer |
| `/standings` | Classificação geral | Qualquer |
| `/finalizar <ronda>` | Finaliza resultados (após protestos) | Staff |

**Listeners:**
- `on_message` no canal #upload-resultados → deteção automática de ficheiros
- Botões "Publicar" / "Corrigir" / "Cancelar" na confirmação

### 5.6 COG: Communication (`cogs/communication.py`)

**Automações agendadas (sem intervenção humana):**

| Evento | Quando | Canal | Conteúdo |
|--------|--------|-------|----------|
| Anúncio + RSVP | D-7 | #anúncios | Embed com detalhes + botões RSVP |
| Briefing | D-2 | #briefing | Embed com track notes, procedimentos |
| Lembrete D-1 | D-1 20:00 | #anúncios | Reminder com contagem RSVP |
| Lembrete H-2 | H-2 | #anúncios | Reminder urgente |
| Cooldown notice | Post-race | #anúncios | Info de quando protestos abrem |
| Protestos abrem | +cooldown | #protestos | Aviso + botão protesto |
| Protestos fecham | +deadline | #protestos | Aviso de fecho |

**Slash Commands opcionais:**

| Comando | Descrição | Acesso |
|---------|-----------|--------|
| `/anuncio <texto>` | Anúncio manual no #anúncios | Staff |
| `/briefing <ronda> [texto]` | Briefing manual ou automático | Race Director |

### 5.7 COG: Stats (`cogs/stats.py`)

| Comando | Descrição | Acesso |
|---------|-----------|--------|
| `/stats` | Stats próprias | Piloto |
| `/stats @piloto` | Stats de outro | Qualquer |
| `/kpis` | Dashboard de KPIs | Staff |
| `/recordes` | Hall of fame | Qualquer |
| `/h2h @p1 @p2` | Head-to-head | Qualquer |

---

## 6. PARSERS DE RESULTADOS

### 6.1 Interface Comum

Todos os parsers retornam a mesma estrutura:

```python
@dataclass
class ParsedResult:
    """Resultado parseado de um piloto, normalizado."""
    player_id: str            # Steam64 ID, iRacing custID, ou nome
    player_name: str          # Nome legível
    finish_position: int
    grid_position: int | None
    best_lap_ms: int | None
    total_time_ms: int | None
    laps_completed: int
    car_model: str | None     # Nome legível do carro
    status: str               # 'finished', 'dnf', 'dsq'
    incidents: int

@dataclass
class ParsedRace:
    """Corrida parseada completa."""
    track_name: str
    sim: str                  # 'ACC', 'iRacing', 'rF2', etc.
    session_type: str         # 'race', 'qualifying'
    results: list[ParsedResult]
    raw_data: dict            # Dados brutos originais
```

### 6.2 ACC Parser (`parsers/acc_parser.py`)

```python
"""
Parser para ficheiros de resultados do Assetto Corsa Competizione.

ACC gera ficheiros JSON no servidor em:
<ACC_folder>/server/results/

Estrutura do JSON:
{
    "sessionType": "R",        // P=Practice, Q=Qualifying, R=Race
    "trackName": "spa",
    "serverName": "...",
    "sessionResult": {
        "bestlap": 137456,     // Melhor volta global em ms
        "bestSplits": [...],
        "isWetSession": 0,
        "type": 1
    },
    "laps": [...],             // Todas as voltas
    "penalties": [...],
    "sessionResult": {
        "leaderBoardLines": [
            {
                "car": {
                    "carId": 1,
                    "raceNumber": 77,
                    "carModel": 30,         // INT → mapear para nome
                    "cupCategory": 0,
                    "carGroup": "GT3"
                },
                "currentDriver": {
                    "firstName": "João",
                    "lastName": "Silva",
                    "playerId": "S76561198..."  // Steam64 com prefixo S
                },
                "timing": {
                    "bestLap": 138234,
                    "bestSplits": [44123, 48234, 45877],
                    "lapCount": 15,
                    "lastLap": 139456,
                    "totalTime": 2234567
                },
                "missingMandatoryPitstop": 0
            },
            ...
        ]
    }
}

NOTAS IMPORTANTES:
- O playerId tem prefixo "S" antes do Steam64 ID → remover o "S"
- carModel é um inteiro → usar ACC_CAR_MODELS dict para converter
- totalTime = 0 ou lapCount muito baixo = DNF provável
- sessionType "R" = Race (o que nos interessa)
- Os resultados já vêm ordenados por posição
- A posição na grelha NÃO está no ficheiro de race → precisa do ficheiro de qualifying
"""

ACC_CAR_MODELS = {
    0: "Porsche 991 GT3 R", 1: "Mercedes-AMG GT3", 2: "Ferrari 488 GT3",
    3: "Audi R8 LMS", 4: "Lamborghini Huracán GT3", 5: "McLaren 650S GT3",
    6: "Nissan GT-R Nismo GT3 2018", 7: "BMW M6 GT3", 8: "Bentley Continental GT3 2018",
    9: "Porsche 991 II GT3 Cup", 10: "Nissan GT-R Nismo GT3 2017",
    11: "Bentley Continental GT3 2016", 12: "Aston Martin Vantage V12 GT3",
    13: "Lamborghini Gallardo R-EX", 14: "Emil Frey Jaguar G3",
    15: "Lexus RC F GT3", 16: "Lamborghini Huracán GT3 Evo",
    17: "Honda NSX GT3", 18: "Lamborghini Huracán SuperTrofeo",
    19: "Audi R8 LMS Evo", 20: "AMR V8 Vantage", 21: "Honda NSX GT3 Evo",
    22: "McLaren 720S GT3", 23: "Porsche 991 II GT3 R", 24: "Ferrari 488 GT3 Evo",
    25: "Mercedes-AMG GT3 2020", 26: "Ferrari 488 Challenge Evo",
    27: "BMW M2 CS Racing", 28: "Porsche 992 GT3 Cup",
    29: "Lamborghini Huracán SuperTrofeo EVO2", 30: "BMW M4 GT3",
    31: "Audi R8 LMS Evo II",
    50: "Alpine A110 GT4", 51: "Aston Martin Vantage GT4",
    52: "Audi R8 LMS GT4", 53: "BMW M4 GT4", 55: "Chevrolet Camaro GT4.R",
    56: "Ginetta G55 GT4", 57: "KTM X-Bow GT4", 58: "Maserati MC GT4",
    59: "McLaren 570S GT4", 60: "Mercedes AMG GT4", 61: "Porsche 718 Cayman GT4"
}

ACC_TRACK_NAMES = {
    "barcelona": "Circuit de Barcelona-Catalunya",
    "brands_hatch": "Brands Hatch",
    "cota": "Circuit of the Americas",
    "donington": "Donington Park",
    "hungaroring": "Hungaroring",
    "imola": "Autodromo Enzo e Dino Ferrari",
    "kyalami": "Kyalami Grand Prix Circuit",
    "laguna_seca": "WeatherTech Raceway Laguna Seca",
    "misano": "Misano World Circuit",
    "monza": "Autodromo Nazionale Monza",
    "mount_panorama": "Mount Panorama Circuit",
    "nurburgring": "Nürburgring",
    "paul_ricard": "Circuit Paul Ricard",
    "silverstone": "Silverstone Circuit",
    "snetterton": "Snetterton Circuit",
    "spa": "Circuit de Spa-Francorchamps",
    "suzuka": "Suzuka International Racing Course",
    "valencia": "Circuit Ricardo Tormo",
    "watkins_glen": "Watkins Glen International",
    "zandvoort": "Circuit Zandvoort",
    "zolder": "Circuit Zolder",
    "oulton_park": "Oulton Park",
    "indianapolis": "Indianapolis Motor Speedway",
    "red_bull_ring": "Red Bull Ring"
}
```

### 6.3 rFactor 2 Parser (`parsers/rf2_parser.py`)

```python
"""
Parser para ficheiros de resultados do rFactor 2.

rF2 gera XML em: <rF2>/UserData/Log/Results/

Estrutura XML:
<rFactorXML>
  <RaceResults>
    <Race>
      <Track>Spa-Francorchamps</Track>
      <Laps>15</Laps>
      <Driver>
        <Name>João Silva</Name>
        <VehFile>...</VehFile>
        <GridPos>5</GridPos>
        <Position>1</Position>
        <ClassGridPos>5</ClassGridPos>
        <ClassPosition>1</ClassPosition>
        <Laps>15</Laps>
        <BestLapTime>138.234</BestLapTime>  (segundos com decimais)
        <FinishTime>2234.567</FinishTime>
        <FinishStatus>Finished</FinishStatus>  ou "DNF"
        <Pitstops>1</Pitstops>
      </Driver>
      ...
    </Race>
  </RaceResults>
</rFactorXML>

NOTAS:
- Tempos em SEGUNDOS (float) → converter para ms (* 1000)
- FinishStatus: "Finished", "DNF", "DQ"
- Match de pilotos é por Name (pode haver discrepâncias → usar fuzzy match)
"""
```

### 6.4 Generic / CSV Parser (`parsers/generic_parser.py`)

```python
"""
Parser genérico para CSV manual ou sims sem parser dedicado.

Formato CSV esperado:
position,driver_name,best_lap,total_time,laps,status,car
1,João Silva,2:18.456,35:42.123,15,finished,BMW M4 GT3
2,Pedro Santos,2:18.789,35:43.456,15,finished,Ferrari 296 GT3
...

NOTAS:
- Tempos no formato m:ss.sss → converter para ms
- Status: "finished", "dnf", "dsq", "dns"
- Este parser é o fallback para: AMS2, RENNSPORT, ou qualquer sim
"""
```

---

## 7. GERAÇÃO DE IMAGENS

### 7.1 Especificação Geral
```
- Font: Liberation Sans (incluída em Linux, sem dependências)
- Font Bold: Liberation Sans Bold
- Cores: usar guild.primary_color e guild.secondary_color
- Anti-aliasing: sempre ativado
- Formato de output: PNG
- Tamanho base: 1200px largura, altura dinâmica conforme conteúdo
```

### 7.2 Standings Image (`generators/image_standings.py`)
```
Dimensão: 1200 x (100 + N_pilotos * 40) px
Background: guild.secondary_color
Header (100px): 
    - Logo da liga (se existe) à esquerda
    - Título: "CLASSIFICAÇÃO — {season_name}" em branco, bold, 28px
    - Subtítulo: "Após Ronda X/Y | Z drops" em cinza, 16px
Tabela:
    - Header row: Pos | Piloto | Equipa | Pts | V | P | Melhor
    - Linhas alternadas: background ligeiramente mais claro/escuro
    - Top 3 com barra lateral na primary_color
    - Fonte: 18px regular, nome em bold
Footer (40px):
    - "Atualizado: DD/MM/AAAA HH:MM" em cinza, 14px
```

### 7.3 Results Image (`generators/image_results.py`)
```
Dimensão: 1200 x (120 + N_pilotos * 40) px
Background: guild.secondary_color
Header (120px):
    - "RESULTADOS — Ronda X" em bold, 28px
    - Track name + flag, 22px
    - Data + condições, 16px
Tabela:
    - Header: Pos | # | Piloto | Carro | Melhor Volta | Gap | Pts
    - Medalhas para top 3 (emoji estilo 🥇🥈🥉 ou cores)
    - DNFs no fundo com cor diferente (vermelho escuro)
    - Pole e fastest lap destacados com ícones
Footer: data, condições
```

### 7.4 Calendar Image (`generators/image_calendar.py`)
```
Dimensão: 1200 x 600px (ou dinâmico)
Layout: grid 2 colunas se >6 rondas
Cada ronda: card de 250x80px
    - Status: ✅ feita | 🔴 próxima | ⬜ futura
    - "R{N} — {Track} {Flag}"
    - "{Data} às {Hora}"
Background: guild.secondary_color
```

---

## 8. PERMISSÕES E ROLES

### 8.1 Hierarquia
```
League Owner (guild owner)
├── Admin (gestão total, config, seasons)
├── Race Director (rounds, briefings, results, registrations)
├── Steward (protests, verdicts, PP)
├── Broadcaster (read-only em staff channels)
└── Piloto (register, protest, rsvp, view)
    └── Inscrito (pré-aprovação, acesso limitado)
```

### 8.2 Decorator de Permissões
```python
# utils/permissions.py
from functools import wraps

def staff_only(roles: list[str] = None):
    """
    Decorator que verifica se o utilizador é staff.
    Se roles especificados, verifica role específico.
    
    Uso:
    @staff_only()                    # Qualquer staff
    @staff_only(['admin', 'owner'])  # Apenas admin ou owner
    @staff_only(['steward'])         # Apenas steward
    """
    ...

# Uso nos cogs:
@app_commands.command(name="finalizar")
@staff_only(['admin', 'race_director'])
async def finalize(self, interaction: discord.Interaction):
    ...
```

### 8.3 Matriz de Acesso (via botões no painel)

| Funcionalidade | Owner | Admin | Race Dir | Steward | Piloto |
|---|---|---|---|---|---|
| Ver painel completo | ✅ | ✅ | ✅ | ✅ | Parcial |
| Setup wizard | ✅ | | | | |
| Criar/editar temporada | ✅ | ✅ | | | |
| Adicionar rondas | ✅ | ✅ | ✅ | | |
| Abrir/fechar inscrições | ✅ | ✅ | ✅ | | |
| Aprovar/rejeitar inscrições | ✅ | ✅ | ✅ | | |
| Upload resultados | ✅ | ✅ | ✅ | | |
| Finalizar resultados | ✅ | ✅ | ✅ | | |
| Votar em protestos | ✅ | ✅ | | ✅ | |
| PP manual | ✅ | ✅ | ✅ | | |
| Configurações | ✅ | ✅ | | | |
| Gerir staff | ✅ | ✅ | | | |
| Exportar dados | ✅ | ✅ | | | |
| Ver KPIs | ✅ | ✅ | ✅ | ✅ | |
| Inscrever-se | | | | | ✅ |
| Submeter protesto | | | | | ✅ |
| RSVP | | | | | ✅ |
| Ver standings/results | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver PP | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 9. WORKFLOWS AUTOMÁTICOS

### 9.1 Workflow Semanal

```
    AUTOMÁTICO                              MANUAL
    ──────────                              ──────
D-7 │ Bot publica anúncio + RSVP           │
D-2 │ Bot publica briefing                 │
D-1 │ Bot envia lembrete                   │
H-2 │ Bot envia lembrete final             │
    │                                      │
D+0 │ ─── CORRIDA ACONTECE ───             │
    │                                      │
D+0 │                                      │ Staff arrasta ficheiro
    │ Bot deteta → mostra preview          │   para #upload-resultados
    │                                      │ Staff clica [✅ Publicar]
    │ Bot publica resultados provisórios   │
    │ Bot publica cooldown notice          │
    │                                      │
D+0 │ Bot abre protestos (após cooldown)   │
+12h│                                      │
    │                                      │ Stewards clicam botões
D+2 │ Bot fecha protestos                  │   para votar (SE houver
    │ Bot aplica decisões automáticas      │   protestos)
    │                                      │
D+3 │                                      │ Staff clica [✅ Finalizar]
    │ Bot publica resultados finais        │   no painel
    │ Bot publica standings atualizados    │
    │ Bot verifica PP thresholds           │
    │ Bot aplica decay de PP               │
    │                                      │

RESULTADO: 1-2 cliques de staff por semana
           (upload + finalizar)
           + votação de stewards se houver protestos
```

### 9.2 Workflow de Protesto

```
Piloto usa /protesto ou clica botão
    │
    ├─ Pre-checks (automáticos):
    │   ├─ Temporada ativa?
    │   ├─ Ronda concluída?
    │   ├─ Cooldown passado?
    │   ├─ Dentro do prazo?
    │   └─ Piloto participou?
    │
    ├─ Se falha → mensagem de erro clara em PT
    │
    └─ Se OK → Wizard visual:
        │
        ├─ Select: contra quem? (lista de pilotos)
        ├─ Modal: volta, zona, descrição, evidência
        ├─ Confirmação com preview
        │
        └─ Protesto criado:
            │
            ├─ Embed no #steward-deliberação
            │   └─ Botão [🔍 Reclamar]
            │       │
            │       └─ Steward reclama → botões de voto aparecem
            │           │
            │           ├─ [✅ Culpado] → dropdown penalização → PP → justificação
            │           ├─ [❌ Não Culpado] → justificação
            │           ├─ [🏁 Incidente de Corrida] → justificação
            │           └─ [🗑️ Rejeitar] → motivo
            │
            ├─ Quando maioria vota:
            │   │
            │   ├─ Decisão publicada no #decisões-stewards
            │   ├─ DM ao protestante + acusado
            │   ├─ Se culpado:
            │   │   ├─ PP aplicados
            │   │   ├─ Threshold checks automáticos
            │   │   └─ Time penalty aplicado aos resultados
            │   │
            │   └─ Botão [🔄 Recorrer] disponível 24h
            │       │
            │       └─ Appeal → novo painel → nova decisão
            │
            ├─ DM confirmação ao protestante
            └─ DM notificação ao acusado
```

---

## 10. PERSISTENT VIEWS

**CRÍTICO:** As Views de RSVP e de Steward Voting devem sobreviver a reinícios do bot. Usar `discord.ui.DynamicItem` ou registar Views com `custom_id` fixos no startup.

```python
# Em bot.py, no on_ready:
class PersistentRSVPView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Sem timeout = persistente
    
    @discord.ui.button(label="✅ Vou estar", style=discord.ButtonStyle.success, 
                       custom_id="rsvp_yes")
    async def rsvp_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
    
    @discord.ui.button(label="🤷 Talvez", style=discord.ButtonStyle.secondary,
                       custom_id="rsvp_maybe")
    async def rsvp_maybe(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
    
    @discord.ui.button(label="❌ Não vou", style=discord.ButtonStyle.danger,
                       custom_id="rsvp_no")
    async def rsvp_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...

# Registar no startup
bot.add_view(PersistentRSVPView())
bot.add_view(PersistentStewardVoteView())
```

---

## 11. CONFIGURAÇÃO E DEPLOYMENT

### 11.1 `.env`
```env
# Discord (OBRIGATÓRIO)
DISCORD_TOKEN=your_bot_token_here

# Database
DATABASE_URL=sqlite:///data/league.db

# Logging
LOG_LEVEL=INFO

# Paths
FONT_PATH=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf
FONT_BOLD_PATH=/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf
```

### 11.2 `requirements.txt`
```
discord.py>=2.3.0
SQLAlchemy>=2.0
alembic>=1.12
APScheduler>=3.10
Pillow>=10.0
aiohttp>=3.9
python-dotenv>=1.0
pytz>=2023.3
aiosqlite>=0.19     # Para SQLite async
```

### 11.3 Dockerfile
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y fonts-liberation && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

### 11.4 `docker-compose.yml`
```yaml
version: '3.8'
services:
  bot:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./data:/app/data    # Persistência da BD e logs
```

---

## 12. PRIORIDADE DE DESENVOLVIMENTO

### Fase 1 — Fundação (Semana 1)
```
1. Estrutura de projeto + config + env
2. database/models.py + engine.py (todas as tabelas)
3. utils/strings.py (todas as strings PT)
4. utils/permissions.py (decorators)
5. utils/embeds.py (helpers)
6. views/common.py (BaseView, ConfirmView, PaginationView)
7. bot.py (entry point, cog loading, persistent views)
```

### Fase 2 — Setup e Gestão (Semana 1-2)
```
8. views/setup_wizard.py (wizard completo 5 passos)
9. cogs/admin.py (/setup, criação de canais e roles)
10. views/season_wizard.py (wizard 6 passos)
11. views/round_wizard.py (wizard 4 passos)
12. cogs/dashboard.py (/painel — hub central)
13. views/dashboard_views.py (todos os botões e sub-views)
```

### Fase 3 — Inscrições e Resultados (Semana 2-3)
```
14. cogs/registration.py (/inscrever, /desistir, /entrylist)
15. views/registration_views.py (modals, aprovação)
16. parsers/acc_parser.py
17. parsers/generic_parser.py (CSV fallback)
18. cogs/results.py (upload auto, /standings, /finalizar)
19. views/results_views.py (confirmação, correção)
20. generators/image_standings.py
21. generators/image_results.py
```

### Fase 4 — Stewarding (Semana 3-4)
```
22. cogs/stewarding.py (/protesto, /pp, automações)
23. views/protest_views.py (wizard, steward voting, appeal)
24. Penalty points automáticos (thresholds, decay)
25. Publicação automática de decisões
```

### Fase 5 — Comunicação e Polish (Semana 4)
```
26. cogs/communication.py (scheduler todas as mensagens)
27. views/rsvp_views.py (persistent)
28. generators/image_calendar.py
29. cogs/stats.py (/stats, /kpis, /recordes)
30. Export CSV
31. Testes
```

### Fase 6 — Expansão (Futuro)
```
32. parsers/iracing_parser.py
33. parsers/rf2_parser.py
34. Dashboard web (opcional)
35. Integração SGP API (opcional)
```

---

## 13. ANTI-PADRÕES A EVITAR

1. **NÃO usar prefixed commands** (`!comando`). Apenas slash commands + botões/menus.
2. **NÃO guardar estado em memória.** Tudo na BD. O bot pode reiniciar.
3. **NÃO hardcodar IDs de canais.** Usar `channel_config` na BD.
4. **NÃO enviar mensagens longas de texto.** Usar embeds + imagens.
5. **NÃO bloquear o event loop.** Usar `asyncio.to_thread()` para I/O pesado (imagens, ficheiros).
6. **NÃO pedir ao utilizador para digitar parâmetros complexos.** Usar Modals, Selects, Buttons.
7. **NÃO mostrar erros técnicos.** Apanhar exceções e mostrar mensagens amigáveis em PT.
8. **NÃO permitir stewards em protestos onde estão envolvidos.**
9. **NÃO aceitar protestos sem evidência.**
10. **NÃO publicar resultados sem cooldown.**
11. **NÃO deixar strings em inglês na UI.** Tudo em `utils/strings.py`.
12. **NÃO esquecer timeouts nas Views.** Todas com 5 min + graceful disable.
13. **NÃO criar mensagens novas quando pode editar a existente.** Wizard = edita mesma mensagem.

---

## 14. DADOS DE REFERÊNCIA

### 14.1 Points Systems Pré-definidos (`data/points_systems.json`)
```json
{
  "f1_2026": {
    "name": "🏎️ F1 2026 (25-18-15...)",
    "description": "Sistema clássico F1 com bonus de pole e fastest lap",
    "points_per_position": [25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
    "pole_bonus": 1,
    "fastest_lap_bonus": 1,
    "finish_bonus": 0
  },
  "flat_30": {
    "name": "📊 Linear (30-27-25...)",
    "description": "Todos os pilotos pontuam, diferenças mais pequenas",
    "points_per_position": [30, 27, 25, 23, 21, 19, 17, 15, 13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    "pole_bonus": 0,
    "fastest_lap_bonus": 0,
    "finish_bonus": 1
  },
  "endurance": {
    "name": "🏁 Endurance (50-40-32...)",
    "description": "Pontos altos com bónus generosos",
    "points_per_position": [50, 40, 32, 26, 22, 19, 16, 14, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    "pole_bonus": 2,
    "fastest_lap_bonus": 2,
    "finish_bonus": 2
  }
}
```

### 14.2 Tracks (`data/tracks.json`) — Amostra ACC
```json
[
  {"id": "barcelona", "name": "Circuit de Barcelona-Catalunya", "country": "Spain", "flag": "🇪🇸"},
  {"id": "brands_hatch", "name": "Brands Hatch", "country": "UK", "flag": "🇬🇧"},
  {"id": "cota", "name": "Circuit of the Americas", "country": "USA", "flag": "🇺🇸"},
  {"id": "donington", "name": "Donington Park", "country": "UK", "flag": "🇬🇧"},
  {"id": "hungaroring", "name": "Hungaroring", "country": "Hungary", "flag": "🇭🇺"},
  {"id": "imola", "name": "Imola", "country": "Italy", "flag": "🇮🇹"},
  {"id": "kyalami", "name": "Kyalami", "country": "South Africa", "flag": "🇿🇦"},
  {"id": "laguna_seca", "name": "Laguna Seca", "country": "USA", "flag": "🇺🇸"},
  {"id": "misano", "name": "Misano", "country": "Italy", "flag": "🇮🇹"},
  {"id": "monza", "name": "Monza", "country": "Italy", "flag": "🇮🇹"},
  {"id": "mount_panorama", "name": "Mount Panorama", "country": "Australia", "flag": "🇦🇺"},
  {"id": "nurburgring", "name": "Nürburgring", "country": "Germany", "flag": "🇩🇪"},
  {"id": "paul_ricard", "name": "Paul Ricard", "country": "France", "flag": "🇫🇷"},
  {"id": "silverstone", "name": "Silverstone", "country": "UK", "flag": "🇬🇧"},
  {"id": "spa", "name": "Spa-Francorchamps", "country": "Belgium", "flag": "🇧🇪"},
  {"id": "suzuka", "name": "Suzuka", "country": "Japan", "flag": "🇯🇵"},
  {"id": "valencia", "name": "Ricardo Tormo", "country": "Spain", "flag": "🇪🇸"},
  {"id": "watkins_glen", "name": "Watkins Glen", "country": "USA", "flag": "🇺🇸"},
  {"id": "zandvoort", "name": "Zandvoort", "country": "Netherlands", "flag": "🇳🇱"},
  {"id": "zolder", "name": "Zolder", "country": "Belgium", "flag": "🇧🇪"},
  {"id": "oulton_park", "name": "Oulton Park", "country": "UK", "flag": "🇬🇧"},
  {"id": "red_bull_ring", "name": "Red Bull Ring", "country": "Austria", "flag": "🇦🇹"}
]
```

### 14.3 Color Themes Pré-definidos
```json
{
  "laranja_racing": {
    "name": "🟠 Laranja Racing",
    "primary": "#FF6600",
    "secondary": "#1A1A2E",
    "accent": "#FF8833",
    "text": "#FFFFFF"
  },
  "azul_velocidade": {
    "name": "🔵 Azul Velocidade",
    "primary": "#0066FF",
    "secondary": "#0D1B2A",
    "accent": "#3388FF",
    "text": "#FFFFFF"
  },
  "vermelho_paixao": {
    "name": "🔴 Vermelho Paixão",
    "primary": "#CC0000",
    "secondary": "#1A0A0A",
    "accent": "#FF3333",
    "text": "#FFFFFF"
  },
  "verde_endurance": {
    "name": "🟢 Verde Endurance",
    "primary": "#00AA44",
    "secondary": "#0A1A0F",
    "accent": "#33CC66",
    "text": "#FFFFFF"
  }
}
```

---

*Spec v2.0 compilada em março de 2026. Inclui todas as melhorias de UX (wizard flows, buttons-first, PT nativo, zero memorização). Baseada nos relatórios [R1, R2, R3] e documento de estratégia consolidado.*

*Para o Codex: seguir a prioridade de desenvolvimento (secção 12). Começar pela Fase 1 (fundação) e avançar sequencialmente. Cada fase deve ser funcional e testável antes de avançar para a seguinte.*
