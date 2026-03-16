from __future__ import annotations


class S:
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
    NO_ACTIVE_SEASON = "📭 Não há nenhuma temporada ativa neste momento."
    NO_COMPLETED_ROUND = "📭 Ainda não há rondas concluídas."
    NOT_REGISTERED = "🔒 Não tens uma inscrição aprovada nesta temporada."
    GENERIC_HELP = "Usa o painel para navegar sem memorizar comandos."
    BACK_TO_DASHBOARD = "⬅️ Voltar ao Painel"
    DASHBOARD_SECTION_INFO = "Ações Rápidas"
    DASHBOARD_SECTION_MANAGEMENT = "Gestão"
    SETTINGS_UPDATED = "✅ Definições atualizadas."
    VIEW_EXPIRED = "⏳ Esta interação expirou. Abre novamente o fluxo no painel."
    ONLY_OWNER_SETUP = "🔒 Apenas o owner do servidor pode correr o setup inicial."
    SETUP_ALREADY_DONE = "⚠️ O setup já foi concluído neste servidor."
    SETUP_CREATE_ALL = "✅ Criar Tudo"
    SETUP_DEFINE_NAME = "📝 Definir Nome"
    SETUP_CUSTOM_THEME = "⚪ Personalizar"
    SETUP_CREATE_SEASON = "📅 Criar Temporada"
    SETUP_VIEW_DASHBOARD = "📋 Ver Painel"

    SETUP_WELCOME = (
        "👋 **Bem-vindo ao assistente de configuração!**\n"
        "Vou ajudar-te a configurar a tua liga passo a passo."
    )
    SETUP_STEP_NAME = "**Passo 1/5** — Como se chama a tua liga?"
    SETUP_STEP_NAME_PLACEHOLDER = "Ex: SimRacing Portugal GT3 Series"
    SETUP_STEP_SIM = "**Passo 2/5** — Qual é o simulador principal?"
    SETUP_STEP_TIMEZONE = "**Passo 3/5** — Qual é o fuso horário?"
    SETUP_STEP_COLORS = "**Passo 4/5** — Escolhe as cores da liga (para imagens e embeds)"
    SETUP_STEP_CHANNELS = "**Passo 5/5** — Vou criar os canais e roles necessários no servidor."
    SETUP_CHANNELS_CONFIRM = (
        "Vou criar os seguintes canais:\n{channels}\n\n"
        "E os seguintes roles:\n{roles}\n\nPosso avançar?"
    )
    SETUP_COMPLETE = (
        "🎉 **Liga configurada com sucesso!**\n\n"
        "**{league_name}** está pronta.\n"
        "Usa `/painel` para ver o painel de controlo."
    )

    DASHBOARD_TITLE = "🏁 PAINEL — {league_name}"
    DASHBOARD_NO_SEASON = (
        "📭 Ainda não tens nenhuma temporada criada.\n"
        "Clica no botão abaixo para criar a primeira!"
    )
    DASHBOARD_SEASON_ACTIVE = "📅 **{season_name}** — ATIVA"
    DASHBOARD_ROUND_INFO = "Ronda {current}/{total} completada"
    DASHBOARD_NEXT_ROUND = "Próxima: **{track}**, {date} às {time}"
    DASHBOARD_DRIVERS = "👥 Pilotos: {approved} inscritos | {active} ativos"
    DASHBOARD_PROTESTS = "📋 Protestos: {pending} pendentes | {review} em análise"
    DASHBOARD_ALERTS = "⚠️ Alertas: {alerts}"
    DASHBOARD_PP_ALERT = "**{driver}** com {pp}/{max_pp} PP (perto de {consequence})"
    DASHBOARD_FIELD_STATUS = "Estado"
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

    SEASON_WIZARD_TITLE = "📅 **Criar Nova Temporada**"
    SEASON_STEP_NAME = "**Passo 1/6** — Nome da temporada?"
    SEASON_STEP_NAME_PLACEHOLDER = "Ex: Season 1 - GT3 Sprint Series"
    SEASON_STEP_SIM = "**Passo 2/6** — Qual o simulador para esta temporada?"
    SEASON_STEP_ROUNDS = "**Passo 3/6** — Quantas rondas vai ter?"
    SEASON_STEP_DROPS = "**Passo 4/6** — Quantos piores resultados são descartados (drops)?"
    SEASON_STEP_DROPS_HELP = (
        "💡 Drops permitem que os pilotos falhem 1-2 corridas sem prejudicar o campeonato. "
        "Recomendado: 2 drops para 10 rondas."
    )
    SEASON_STEP_POINTS = "**Passo 5/6** — Qual o sistema de pontuação?"
    SEASON_STEP_CONFIRM = "**Passo 6/6** — Confirma os detalhes:"
    SEASON_CREATED = (
        "✅ **Temporada criada!**\n\n"
        "**{name}**\n🎮 {sim} | 🏁 {rounds} rondas | 🗑️ {drops} drops\n"
        "📊 Pontuação: {points}\n\nAgora adiciona as rondas ao calendário com o botão abaixo."
    )
    SEASON_STATUS_DRAFT = "📝 Rascunho"
    SEASON_STATUS_REGISTRATION = "📋 Inscrições Abertas"
    SEASON_STATUS_ACTIVE = "🟢 Ativa"
    SEASON_STATUS_FINISHED = "🏁 Terminada"
    SEASON_OPEN_REG = "📋 **Inscrições abertas!**\nOs pilotos já podem inscrever-se com `/inscrever`."
    SEASON_CLOSE_REG = "🔒 **Inscrições fechadas.**"
    SEASON_CREATE = "✅ Criar"
    SEASON_CUSTOM_ROUNDS = "Outro"
    SEASON_POINTS_CUSTOM = "⚙️ Personalizar"

    ROUND_WIZARD_TITLE = "🏁 **Adicionar Ronda**"
    ROUND_STEP_NUMBER = "**Passo 1/4** — Número da ronda?"
    ROUND_STEP_TRACK = "**Passo 2/4** — Qual a pista?"
    ROUND_STEP_TRACK_PLACEHOLDER = "Escreve o nome da pista (ex: Spa, Monza, Silverstone...)"
    ROUND_STEP_DATE = "**Passo 3/4** — Data e hora da corrida?"
    ROUND_STEP_DATE_PLACEHOLDER = "Ex: 2026-04-20 21:00"
    ROUND_FIELD_DATE = "Data"
    ROUND_FIELD_TIME = "Hora"
    ROUND_STEP_DETAILS = "**Passo 4/4** — Detalhes adicionais"
    ROUND_CREATED = (
        "✅ **Ronda {n} adicionada!**\n\n🏟️ {track} {flag}\n📅 {date} às {time}\n"
        "🌤️ {weather} | ⏱️ {duration} min | 🚦 {format}\n\n📨 Mensagens automáticas agendadas."
    )
    ROUND_STATUS_SCHEDULED = "⬜ Agendada"
    ROUND_STATUS_NEXT = "🔴 Próxima"
    ROUND_STATUS_FINISHED = "✅ Concluída"
    ROUND_STATUS_RESULTS_PENDING = "⏳ Resultados Pendentes"
    ROUND_FORMAT_SPRINT = "Sprint"
    ROUND_FORMAT_ENDURANCE = "Endurance"
    ROUND_WEATHER_DRY = "🌞 Seco"
    ROUND_WEATHER_RAIN = "🌧️ Chuva"
    ROUND_WEATHER_DYNAMIC = "🌤️ Dinâmico"
    ROUND_WEATHER_RANDOM = "🎲 Aleatório"
    ROUND_START_ROLLING = "🏁 Lançado"
    ROUND_START_STANDING = "🚦 Parado"
    ROUND_DURATION_PLACEHOLDER = "40 min"
    ROUND_DURATION_30 = "30 min"
    ROUND_DURATION_40 = "40 min"
    ROUND_DURATION_60 = "60 min"
    ROUND_DURATION_90 = "90 min"
    ROUND_CREATE = "✅ Criar Ronda"
    ROUND_SET_TRACK = "🛣️ Definir pista"
    ROUND_SET_DATETIME = "📅 Definir data/hora"

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
    REGISTER_SUCCESS = (
        "✅ **Inscrição submetida!**\n\nOlá **{name}**, a tua inscrição foi recebida.\n"
        "Estado: ⏳ Pendente de aprovação\n\nReceberás uma mensagem quando for aprovada."
    )
    REGISTER_ALREADY = "⚠️ Já estás inscrito nesta temporada."
    REGISTER_CLOSED = "🔒 As inscrições para esta temporada estão fechadas."
    REGISTER_FULL = "🔒 A temporada já atingiu o número máximo de pilotos."
    REGISTER_WITHDRAWN = "✅ A tua inscrição foi retirada."
    HOTLAP_RECORDED = "⏱️ Hotlap registado com sucesso."

    APPROVE_NOTIFICATION = (
        "📬 **Nova inscrição!**\n\n👤 {name}\n🎮 ID: {game_id}\n🚗 Carro #{car_number}\n🏳️ {nationality}"
    )
    APPROVE_BTN_APPROVE = "✅ Aprovar"
    APPROVE_BTN_REJECT = "❌ Rejeitar"
    APPROVE_BTN_PROFILE = "👤 Ver Perfil"
    APPROVED_DM = (
        "🎉 **Inscrição aprovada!**\n\nBem-vindo à **{season_name}**!\n"
        "Divisão: **{division}**\nNúmero: **#{car_number}**\n\nBoa sorte na pista! 🏁"
    )
    REJECTED_DM = (
        "❌ **Inscrição não aprovada.**\n\nMotivo: {reason}\n\n"
        "Se tiveres dúvidas, contacta a organização."
    )
    REJECT_MODAL_TITLE = "Motivo da rejeição"
    REJECT_MODAL_PLACEHOLDER = "Explica brevemente o motivo..."
    DEFAULT_DIVISION_NAME = "Divisão 1"
    PROFILE_SUMMARY = (
        "Discord: {discord_name}\n"
        "Steam/iRacing: {game_id}\n"
        "Carro: #{car_number}\n"
        "Equipa: {team_name}"
    )

    ENTRYLIST_TITLE = "👥 **ENTRY LIST — {season_name}**"
    ENTRYLIST_ROW = "`#{number:>3}` {flag} **{name}** — {team}"
    ENTRYLIST_FOOTER = "{total} pilotos inscritos | {approved} aprovados | {pending} pendentes"

    RSVP_TITLE = "📋 **Presença — Ronda {n}: {track}**\n📅 {date} às {time}"
    RSVP_BTN_YES = "✅ Vou estar"
    RSVP_BTN_MAYBE = "🤷 Talvez"
    RSVP_BTN_NO = "❌ Não vou"
    RSVP_CONFIRMED = "✅ Presença confirmada para a Ronda {n}."
    RSVP_COUNT = "✅ {yes} confirmados | 🤷 {maybe} talvez | ❌ {no} ausentes"

    RESULTS_DETECTED = (
        "📂 **Ficheiro de resultados detetado!**\n\n🏟️ Pista: **{track}**\n👥 Pilotos: **{drivers}**\n"
        "🥇 Vencedor: **{winner}**\n⏱️ Melhor volta: **{best_lap}** ({best_lap_driver})\n\nIsto está correto?"
    )
    RESULTS_BTN_PUBLISH = "✅ Publicar Resultados"
    RESULTS_BTN_CANCEL = "❌ Cancelar"
    RESULTS_BTN_CORRECT = "✏️ Corrigir"
    RESULTS_PROVISIONAL = (
        "📊 **RESULTADOS PROVISÓRIOS — Ronda {n}: {track}** {flag}\n\n"
        "⏳ Período de cooldown ativo. Protestos abrem às **{protest_open}**."
    )
    RESULTS_FINAL = "📊 **RESULTADOS FINAIS — Ronda {n}: {track}** {flag}"
    RESULTS_ROW = "`P{pos:>2}` {medal} **{name}** — {car} | ⏱️ {best_lap} | 📊 {points} pts"
    RESULTS_DNF = "`DNF` 💀 **{name}** — {car} | Voltas: {laps}"
    RESULTS_MEDAL_1 = "🥇"
    RESULTS_MEDAL_2 = "🥈"
    RESULTS_MEDAL_3 = "🥉"
    RESULTS_MEDAL_OTHER = "  "
    RESULTS_UNKNOWN_DRIVER = (
        "⚠️ {count} piloto(s) no ficheiro não foram encontrados na base de dados:\n{names}\n\n"
        "Queres adicionar manualmente ou ignorar?"
    )
    RESULTS_BTN_ADD_MANUAL = "➕ Adicionar"
    RESULTS_BTN_IGNORE = "🔇 Ignorar"
    RESULTS_CORRECTION_MODAL = "Correção manual"
    RESULTS_CORRECTION_LABEL = "Notas de correção"
    RESULTS_CORRECTION_PLACEHOLDER = "Explica o que deve ser corrigido..."

    STANDINGS_TITLE = "📊 **CLASSIFICAÇÃO — {season_name}**"
    STANDINGS_AFTER_ROUND = "Após Ronda {n}/{total} ({drops} drops aplicados)"
    STANDINGS_ROW = "`{pos:>2}.` {medal} **{name}** — **{points}** pts | {wins}V {podiums}P | Melhor: P{best}"
    STANDINGS_FOOTER = "Última atualização: {date}"

    PROTEST_BTN = "📋 Submeter Protesto"
    PROTEST_COOLDOWN = (
        "⏳ **Período de cooldown ativo.**\nProtestos para a Ronda {n} abrem às **{open_time}**.\n"
        "Isto existe para evitar decisões emocionais. Volta mais tarde!"
    )
    PROTEST_EXPIRED = (
        "❌ **Prazo expirado.**\nO prazo para submeter protestos da Ronda {n} encerrou às {close_time}."
    )
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
    PROTEST_SUCCESS = (
        "✅ **Protesto submetido!**\n\n📋 Protesto **#{id}**\nContra: **{accused}**\n"
        "Ronda {n}, Volta {lap}, {zone}\n\nOs stewards vão analisar o teu protesto. "
        "Receberás uma notificação com a decisão."
    )
    PROTEST_NO_EVIDENCE = (
        "❌ **Evidência obrigatória.**\nPrecisas de incluir um link para um clip ou replay do incidente."
    )
    PROTEST_NOT_PARTICIPANT = "🔒 Só pilotos que participaram na última ronda podem protestar."

    STEWARD_NEW_PROTEST = (
        "⚖️ **NOVO PROTESTO — #{id}**\n\n👤 Autor: **{author}**\n🎯 Acusado: **{accused}**\n"
        "🏁 Ronda {n}, Volta {lap}, {zone}\n\n📝 *\"{description}\"*\n🔗 Evidência: {evidence}"
    )
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
    STEWARD_DECISION_PUBLISHED = (
        "⚖️ **DECISÃO DOS STEWARDS — Protesto #{id}**\n\n📋 **{author}** vs **{accused}**\n"
        "🏁 Ronda {n}, Volta {lap}, {zone}\n\n🔎 **Descrição:** {description}\n\n"
        "📜 **Veredicto:** {verdict}\n⚡ **Penalização:** {penalty}\n"
        "📊 **Penalty Points:** +{pp} PP (total: {total_pp}/{max_pp})\n\n"
        "💬 **Justificação:** {reasoning}\n\n👨‍⚖️ Stewards: {stewards}"
    )
    STEWARD_VERDICT_GUILTY = "Culpado"
    STEWARD_VERDICT_NOT_GUILTY = "Não Culpado"
    STEWARD_VERDICT_RACING_INCIDENT = "Incidente de Corrida"
    STEWARD_VERDICT_DISMISSED = "Protesto Rejeitado"
    STEWARD_WAITING_VOTES = "⏳ Faltam votos para atingir maioria."
    STEWARD_CONFLICT = "🔒 Não podes votar neste protesto porque estás envolvido."

    PP_STATUS = "📊 **Penalty Points — {name}**\n\n🔢 Total: **{total}/{max}** PP\n📈 Estado: {status}\n\n**Histórico:**\n{history}"
    PP_STATUS_CLEAN = "🟢 Limpo"
    PP_STATUS_WARNING = "🟡 Atenção"
    PP_STATUS_DANGER = "🟠 Perigo"
    PP_STATUS_CRITICAL = "🔴 Crítico"
    PP_THRESHOLD_WARNING = "⚠️ **ALERTA:** {name} atingiu **{pp} PP**. Próximo threshold: {next} PP ({consequence})."
    PP_THRESHOLD_SUSPEND = "⛔ **SUSPENSÃO AUTOMÁTICA:** {name} atingiu **{pp} PP** e está automaticamente suspenso da próxima corrida."
    PP_THRESHOLD_BAN = "🔴 **BAN AUTOMÁTICO:** {name} atingiu **{pp} PP** e está banido do campeonato.\n\n@Staff — é necessária confirmação."
    PP_DECAY = "🟢 **Decay:** {name} teve {races} corridas limpas consecutivas. **-{decay} PP** aplicados. (Novo total: {new_total} PP)"

    APPEAL_BTN = "🔄 Recorrer da Decisão"
    APPEAL_WINDOW = "ℹ️ Tens **24 horas** após a decisão para submeter recurso."
    APPEAL_MODAL_TITLE = "Recurso — Protesto #{id}"
    APPEAL_MODAL_PLACEHOLDER = "Explica porque discordas da decisão..."
    APPEAL_SUCCESS = (
        "🔄 **Recurso submetido!**\n\nO teu recurso ao Protesto #{id} foi registado.\n"
        "Um painel diferente de stewards irá re-analisar."
    )
    APPEAL_EXPIRED = "❌ O prazo de 24h para recurso expirou."

    COMM_ANNOUNCE_D7 = (
        "📢 **RONDA {n} — {track}** {flag}\n\n📅 **{date}** às **{time}**\n🌤️ Condições: {weather}\n"
        "⏱️ Duração: {duration} min\n🚦 Formato: {format}\n\nConfirma a tua presença abaixo! 👇"
    )
    COMM_BRIEFING = (
        "📋 **BRIEFING — Ronda {n}: {track}** {flag}\n\n📅 {date} às {time}\n🌤️ {weather} | ⏱️ {duration} min\n\n"
        "🚦 **Procedimento de Arranque:** {start_type}\n🛣️ **Track Limits:** {track_limits}\n"
        "📌 **Notas:** {notes}\n\n⚠️ **Lembretes:**\n• Respeita o espaço dos outros pilotos\n"
        "• Volta 1: cautela extra\n• Problemas técnicos? Reporta no chat\n\nBoa corrida a todos! 🏁"
    )
    COMM_REMINDER_D1 = (
        "⏰ **LEMBRETE — Amanhã temos corrida!**\n\n🏟️ Ronda {n}: **{track}**\n📅 {date} às {time}\n\n"
        "✅ {rsvp_yes} confirmados | 🤷 {rsvp_maybe} talvez\n\nNão te esqueças de verificar o teu setup! 🔧"
    )
    COMM_REMINDER_H2 = (
        "🚨 **A corrida começa em 2 horas!**\n\n🏟️ {track}\n🕐 Servidor abre às {server_open}\n🏁 Corrida às {race_start}\n\n"
        "👥 {rsvp_yes} pilotos confirmados\n\nVemo-nos na pista! 🏎️"
    )
    COMM_COOLDOWN_NOTICE = (
        "⏳ **Resultados provisórios publicados.**\n\nPeríodo de cooldown ativo.\n📋 Protestos abrem: **{open_time}**\n"
        "📋 Prazo para protestos: **{close_time}**\n\n💡 *O cooldown existe para evitar decisões emocionais.*"
    )
    COMM_PROTESTS_OPEN = (
        "📋 **Protestos abertos para a Ronda {n}!**\n\n⏰ Prazo: até **{close_time}**\n"
        "Usa o botão abaixo ou `/protesto` para submeter."
    )
    COMM_PROTESTS_CLOSE = (
        "🔒 **Prazo de protestos encerrado para a Ronda {n}.**\n\nProtestos recebidos: {count}\n"
        "Os stewards vão analisar e publicar decisões em breve."
    )

    STAFF_ADD_TITLE = "👤 **Adicionar Staff**"
    STAFF_ADDED = "✅ **{name}** adicionado como **{role}**."
    STAFF_REMOVED = "❌ **{name}** removido do cargo de **{role}**."

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
    RECORDS_TITLE = "🏆 Recordes"
    H2H_TITLE = "H2H"
    KPIS_TITLE = "📊 **KPIs — {season_name}**"
    KPIS_RETENTION = "📌 Retenção: **{pct}%** ({count}/{total} pilotos completaram ≥70% das corridas)"
    KPIS_AVG_DRIVERS = "👥 Média de pilotos por corrida: **{avg}**"
    KPIS_INCIDENTS = "⚠️ Protestos por corrida: **{avg}**"
    KPIS_RESOLUTION = "⏱️ Tempo médio resolução: **{hours}h**"
    KPIS_NOSHOWS = "👻 No-shows por corrida: **{avg}**"

    EXPORT_TITLE = "📤 **Exportar Dados**\n\nEscolhe o que queres exportar:"
    EXPORT_BTN_DRIVERS = "👥 Pilotos"
    EXPORT_BTN_STANDINGS = "📊 Standings"
    EXPORT_BTN_RESULTS = "📋 Resultados"
    EXPORT_BTN_PENALTIES = "⚖️ Penalizações"
    EXPORT_BTN_ALL = "📦 Tudo"
    EXPORT_SUCCESS = "✅ Ficheiro exportado! ({rows} registos)"

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

    CMD_DASHBOARD = "Painel de controlo da liga"
    CMD_SETUP = "Assistente inicial de configuração da liga"
    CMD_REGISTER = "Abre o assistente de inscrição"
    CMD_WITHDRAW = "Retira a tua inscrição atual"
    CMD_ENTRYLIST = "Mostra a entry list atual"
    CMD_HOTLAP = "Regista um hotlap de pré-qualificação"
    CMD_PROTEST = "Abre o assistente de protesto"
    CMD_PP = "Mostra penalty points"
    CMD_RESULTS = "Mostra os resultados da última ronda"
    CMD_STANDINGS = "Mostra a classificação atual"
    CMD_FINALIZE = "Finaliza os resultados após protestos"
    CMD_STATS = "Mostra estatísticas do piloto"
    CMD_KPIS = "Mostra KPIs da temporada"
    CMD_RECORDS = "Mostra recordes da liga"
    CMD_H2H = "Compara dois pilotos"
    CMD_ANNOUNCE = "Publica um anúncio manual"
    CMD_BRIEFING = "Publica um briefing manual"

    ROLE_LEAGUE_OWNER = "League Owner"
    ROLE_ADMIN = "Admin"
    ROLE_RACE_DIRECTOR = "Race Director"
    ROLE_STEWARD = "Steward"
    ROLE_BROADCASTER = "Broadcaster"
    ROLE_DRIVER = "Piloto"
    ROLE_REGISTERED = "Inscrito"

    CHANNEL_ANNOUNCEMENTS = "anúncios"
    CHANNEL_REGISTRATIONS = "inscrições"
    CHANNEL_RESULTS = "resultados"
    CHANNEL_STANDINGS = "classificação"
    CHANNEL_BRIEFING = "briefing-pré-corrida"
    CHANNEL_PROTESTS = "protestos"
    CHANNEL_STEWARD_DECISIONS = "decisões-stewards"
    CHANNEL_STAFF_GENERAL = "staff-geral"
    CHANNEL_STEWARD_DELIBERATION = "steward-deliberação"
    CHANNEL_RESULTS_UPLOAD = "upload-resultados"

    STAFF_ROLES = {
        "steward": "⚖️ Steward — Analisa protestos e atribui penalizações",
        "race_director": "🏁 Diretor de Corrida — Gere rondas, briefings e resultados",
        "admin": "⚙️ Admin — Gestão total da liga",
        "broadcaster": "📺 Broadcaster — Acesso a canais de broadcast",
    }

    CHANNEL_PURPOSES = {
        "announcements": CHANNEL_ANNOUNCEMENTS,
        "registrations": CHANNEL_REGISTRATIONS,
        "results": CHANNEL_RESULTS,
        "standings": CHANNEL_STANDINGS,
        "briefing": CHANNEL_BRIEFING,
        "protests": CHANNEL_PROTESTS,
        "steward_decisions": CHANNEL_STEWARD_DECISIONS,
        "staff_general": CHANNEL_STAFF_GENERAL,
        "steward_deliberation": CHANNEL_STEWARD_DELIBERATION,
        "results_upload": CHANNEL_RESULTS_UPLOAD,
    }

    ROLE_NAME_MAP = {
        "owner": ROLE_LEAGUE_OWNER,
        "admin": ROLE_ADMIN,
        "race_director": ROLE_RACE_DIRECTOR,
        "steward": ROLE_STEWARD,
        "broadcaster": ROLE_BROADCASTER,
        "driver": ROLE_DRIVER,
        "registered": ROLE_REGISTERED,
    }

    SIM_OPTIONS = ("ACC", "iRacing", "rF2", "AMS2", "RENNSPORT", "Vários")
    TIMEZONE_OPTIONS = (
        "Europe/Lisbon",
        "Europe/Madrid",
        "Europe/London",
        "America/Sao_Paulo",
    )
    COLOR_THEMES = {
        "laranja_racing": {"name": "🟠 Laranja Racing", "primary": "#FF6600", "secondary": "#1A1A2E"},
        "azul_velocidade": {"name": "🔵 Azul Velocidade", "primary": "#0066FF", "secondary": "#0D1B2A"},
        "vermelho_paixao": {"name": "🔴 Vermelho Paixão", "primary": "#CC0000", "secondary": "#1A0A0A"},
        "verde_endurance": {"name": "🟢 Verde Endurance", "primary": "#00AA44", "secondary": "#0A1A0F"},
    }
    SETUP_THEME_PRIMARY_LABEL = "Cor Primária"
    SETUP_THEME_SECONDARY_LABEL = "Cor Secundária"
    STANDINGS_IMAGE_TITLE = "CLASSIFICAÇÃO — {season_name}"
    STANDINGS_IMAGE_ROW = "{position:>2}  {name}  {points} pts  {wins}V {podiums}P"
    RESULTS_IMAGE_TITLE = "RESULTADOS — {round_name}"
    RESULTS_IMAGE_ROW = "P{position:>2}  #{number:>3}  {name}  {car}  {best_lap}  {points} pts"
