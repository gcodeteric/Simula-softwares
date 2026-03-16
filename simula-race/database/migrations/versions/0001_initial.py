"""initial schema"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


season_status = sa.Enum("draft", "registration", "active", "finished", name="seasonstatus", native_enum=False, create_constraint=True)
round_status = sa.Enum("scheduled", "next", "finished", "results_pending", name="roundstatus", native_enum=False, create_constraint=True)
registration_status = sa.Enum("pending", "approved", "rejected", "withdrawn", name="registrationstatus", native_enum=False, create_constraint=True)
result_status = sa.Enum("finished", "dnf", "dsq", "dns", name="resultstatus", native_enum=False, create_constraint=True)
protest_status = sa.Enum("submitted", "claimed", "decided", "appealed", "closed", name="proteststatus", native_enum=False, create_constraint=True)
penalty_type = sa.Enum("penalty", "decay", "redemption", "manual", name="penaltypointtype", native_enum=False, create_constraint=True)
staff_role = sa.Enum("admin", "race_director", "steward", "broadcaster", name="staffrole", native_enum=False, create_constraint=True)
scheduled_message_type = sa.Enum(
    "announcement",
    "briefing",
    "reminder_day",
    "reminder_final",
    "cooldown_notice",
    "protests_open",
    "protests_close",
    name="scheduledmessagetype",
    native_enum=False,
    create_constraint=True,
)
channel_purpose = sa.Enum(
    "announcements",
    "registrations",
    "results",
    "standings",
    "briefing",
    "protests",
    "steward_decisions",
    "staff_general",
    "steward_deliberation",
    "results_upload",
    name="channelpurpose",
    native_enum=False,
    create_constraint=True,
)
rsvp_status = sa.Enum("confirmed", "maybe", "absent", name="rsvpstatus", native_enum=False, create_constraint=True)


def upgrade() -> None:
    op.create_table(
        "guilds",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("league_name", sa.Text(), nullable=False),
        sa.Column("timezone", sa.String(length=100), nullable=False, server_default="Europe/Lisbon"),
        sa.Column("default_sim", sa.String(length=50), nullable=False, server_default="ACC"),
        sa.Column("cooldown_hours", sa.Integer(), nullable=False, server_default="12"),
        sa.Column("protest_deadline_h", sa.Integer(), nullable=False, server_default="48"),
        sa.Column("max_penalty_points", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("warn_threshold", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("suspend_threshold", sa.Integer(), nullable=False, server_default="15"),
        sa.Column("decay_rate", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("decay_interval", sa.Integer(), nullable=False, server_default="4"),
        sa.Column("pace_threshold_pct", sa.Float(), nullable=False, server_default="103.0"),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("primary_color", sa.String(length=7), nullable=False, server_default="#FF6600"),
        sa.Column("secondary_color", sa.String(length=7), nullable=False, server_default="#1A1A2E"),
        sa.Column("setup_complete", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "channel_config",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("purpose", channel_purpose, nullable=False),
        sa.Column("channel_id", sa.BigInteger(), nullable=False),
        sa.UniqueConstraint("guild_id", "purpose", name="uq_channel_config_guild_purpose"),
    )
    op.create_table(
        "points_systems",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("points_per_position", sa.JSON(), nullable=False),
        sa.Column("pole_bonus", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("fastest_lap_bonus", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("most_positions_bonus", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("finish_bonus", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tiebreak_order", sa.JSON(), nullable=False, server_default='["wins", "podiums", "best_finish"]'),
    )
    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("sim", sa.String(length=50), nullable=False),
        sa.Column("status", season_status, nullable=False),
        sa.Column("num_rounds", sa.Integer(), nullable=False),
        sa.Column("drops", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("points_system_id", sa.Integer(), sa.ForeignKey("points_systems.id", ondelete="SET NULL"), nullable=True),
        sa.Column("min_drivers", sa.Integer(), nullable=False, server_default="12"),
        sa.Column("max_drivers", sa.Integer(), nullable=False, server_default="40"),
        sa.Column("max_divisions", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("rulebook_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "divisions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("season_id", sa.Integer(), sa.ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("tier", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("min_rating", sa.Float(), nullable=True),
        sa.Column("max_rating", sa.Float(), nullable=True),
        sa.Column("max_drivers", sa.Integer(), nullable=False, server_default="30"),
    )
    op.create_table(
        "rounds",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("season_id", sa.Integer(), sa.ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("track_name", sa.Text(), nullable=False),
        sa.Column("track_country", sa.Text(), nullable=True),
        sa.Column("track_flag", sa.String(length=16), nullable=True),
        sa.Column("format", sa.String(length=50), nullable=False, server_default="sprint"),
        sa.Column("start_type", sa.String(length=50), nullable=False, server_default="rolling"),
        sa.Column("race_duration_min", sa.Integer(), nullable=False, server_default="40"),
        sa.Column("weather", sa.String(length=50), nullable=False, server_default="dry"),
        sa.Column("date_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", round_status, nullable=False),
        sa.Column("server_info", sa.Text(), nullable=True),
        sa.Column("briefing_text", sa.Text(), nullable=True),
        sa.Column("track_limits_notes", sa.Text(), nullable=True),
        sa.Column("results_file_path", sa.Text(), nullable=True),
        sa.Column("briefing_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reminder_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("results_posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("protests_open_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("protests_close_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("final_results_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("season_id", "round_number", name="uq_rounds_season_round_number"),
    )
    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("discord_id", sa.BigInteger(), nullable=False),
        sa.Column("discord_name", sa.Text(), nullable=False),
        sa.Column("real_name", sa.Text(), nullable=True),
        sa.Column("steam_id", sa.Text(), nullable=True),
        sa.Column("iracing_id", sa.Text(), nullable=True),
        sa.Column("rf2_id", sa.Text(), nullable=True),
        sa.Column("nationality", sa.Text(), nullable=True),
        sa.Column("nationality_flag", sa.String(length=16), nullable=True),
        sa.Column("timezone", sa.String(length=100), nullable=False, server_default="Europe/Lisbon"),
        sa.Column("car_number", sa.Integer(), nullable=True),
        sa.Column("team_name", sa.Text(), nullable=True),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("guild_id", "discord_id", name="uq_drivers_guild_discord"),
    )
    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("season_id", sa.Integer(), sa.ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("division_id", sa.Integer(), sa.ForeignKey("divisions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", registration_status, nullable=False),
        sa.Column("hotlap_time_ms", sa.Integer(), nullable=True),
        sa.Column("hotlap_track", sa.Text(), nullable=True),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by", sa.BigInteger(), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.UniqueConstraint("driver_id", "season_id", name="uq_registrations_driver_season"),
    )
    op.create_table(
        "race_results",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("round_id", sa.Integer(), sa.ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("division_id", sa.Integer(), sa.ForeignKey("divisions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("finish_position", sa.Integer(), nullable=True),
        sa.Column("grid_position", sa.Integer(), nullable=True),
        sa.Column("best_lap_ms", sa.Integer(), nullable=True),
        sa.Column("total_time_ms", sa.BigInteger(), nullable=True),
        sa.Column("laps_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", result_status, nullable=False),
        sa.Column("base_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("bonus_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("penalty_time_sec", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("final_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("car_model", sa.Text(), nullable=True),
        sa.Column("incidents", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("round_id", "driver_id", name="uq_race_results_round_driver"),
    )
    op.create_table(
        "protests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("round_id", sa.Integer(), sa.ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_driver_id", sa.Integer(), sa.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("accused_driver_id", sa.Integer(), sa.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("lap_number", sa.Integer(), nullable=True),
        sa.Column("turn_zone", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_url", sa.Text(), nullable=False),
        sa.Column("status", protest_status, nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("cooldown_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("assigned_stewards", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("votes", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("verdict", sa.Text(), nullable=True),
        sa.Column("penalty_type", sa.Text(), nullable=True),
        sa.Column("penalty_value", sa.Text(), nullable=True),
        sa.Column("penalty_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reasoning", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("appeal_reason", sa.Text(), nullable=True),
        sa.Column("appeal_deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("appeal_verdict", sa.Text(), nullable=True),
        sa.Column("appeal_decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("staff_message_id", sa.BigInteger(), nullable=True),
        sa.Column("public_message_id", sa.BigInteger(), nullable=True),
    )
    op.create_table(
        "penalty_points",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("season_id", sa.Integer(), sa.ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("protest_id", sa.Integer(), sa.ForeignKey("protests.id", ondelete="SET NULL"), nullable=True),
        sa.Column("round_id", sa.Integer(), sa.ForeignKey("rounds.id", ondelete="SET NULL"), nullable=True),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("type", penalty_type, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "staff_members",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("discord_id", sa.BigInteger(), nullable=False),
        sa.Column("role", staff_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("appointed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("guild_id", "discord_id", "role", name="uq_staff_members_role"),
    )
    op.create_table(
        "scheduled_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("round_id", sa.Integer(), sa.ForeignKey("rounds.id", ondelete="CASCADE"), nullable=True),
        sa.Column("type", scheduled_message_type, nullable=False),
        sa.Column("channel_purpose", channel_purpose, nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sent", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("message_id", sa.BigInteger(), nullable=True),
    )
    op.create_table(
        "rsvp",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("round_id", sa.Integer(), sa.ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", rsvp_status, nullable=False),
        sa.Column("responded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("round_id", "driver_id", name="uq_rsvp_round_driver"),
    )
    op.create_table(
        "audit_log",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("guild_id", sa.BigInteger(), sa.ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False),
        sa.Column("actor_discord_id", sa.BigInteger(), nullable=True),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("target_type", sa.Text(), nullable=True),
        sa.Column("target_id", sa.Integer(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("rsvp")
    op.drop_table("scheduled_messages")
    op.drop_table("staff_members")
    op.drop_table("penalty_points")
    op.drop_table("protests")
    op.drop_table("race_results")
    op.drop_table("registrations")
    op.drop_table("drivers")
    op.drop_table("rounds")
    op.drop_table("divisions")
    op.drop_table("seasons")
    op.drop_table("points_systems")
    op.drop_table("channel_config")
    op.drop_table("guilds")
