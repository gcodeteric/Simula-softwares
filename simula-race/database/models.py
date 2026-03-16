from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import JSON, BigInteger, Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def enum_column(enum_cls: type[StrEnum], default: StrEnum) -> Any:
    return mapped_column(
        Enum(enum_cls, native_enum=False, create_constraint=True, validate_strings=True),
        default=default,
        nullable=False,
    )


class SeasonStatus(StrEnum):
    DRAFT = "draft"
    REGISTRATION = "registration"
    ACTIVE = "active"
    FINISHED = "finished"


class RoundStatus(StrEnum):
    SCHEDULED = "scheduled"
    NEXT = "next"
    FINISHED = "finished"
    RESULTS_PENDING = "results_pending"


class RegistrationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ResultStatus(StrEnum):
    FINISHED = "finished"
    DNF = "dnf"
    DSQ = "dsq"
    DNS = "dns"


class ProtestStatus(StrEnum):
    SUBMITTED = "submitted"
    CLAIMED = "claimed"
    DECIDED = "decided"
    APPEALED = "appealed"
    CLOSED = "closed"


class PenaltyPointType(StrEnum):
    PENALTY = "penalty"
    DECAY = "decay"
    REDEMPTION = "redemption"
    MANUAL = "manual"


class StaffRole(StrEnum):
    ADMIN = "admin"
    RACE_DIRECTOR = "race_director"
    STEWARD = "steward"
    BROADCASTER = "broadcaster"


class ScheduledMessageType(StrEnum):
    ANNOUNCEMENT = "announcement"
    BRIEFING = "briefing"
    REMINDER_DAY = "reminder_day"
    REMINDER_FINAL = "reminder_final"
    COOLDOWN_NOTICE = "cooldown_notice"
    PROTESTS_OPEN = "protests_open"
    PROTESTS_CLOSE = "protests_close"


class ChannelPurpose(StrEnum):
    ANNOUNCEMENTS = "announcements"
    REGISTRATIONS = "registrations"
    RESULTS = "results"
    STANDINGS = "standings"
    BRIEFING = "briefing"
    PROTESTS = "protests"
    STEWARD_DECISIONS = "steward_decisions"
    STAFF_GENERAL = "staff_general"
    STEWARD_DELIBERATION = "steward_deliberation"
    RESULTS_UPLOAD = "results_upload"


class RSVPStatus(StrEnum):
    CONFIRMED = "confirmed"
    MAYBE = "maybe"
    ABSENT = "absent"


class Guild(Base):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    league_name: Mapped[str] = mapped_column(Text, nullable=False)
    timezone: Mapped[str] = mapped_column(String(100), default="Europe/Lisbon", nullable=False)
    default_sim: Mapped[str] = mapped_column(String(50), default="ACC", nullable=False)
    cooldown_hours: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    protest_deadline_h: Mapped[int] = mapped_column(Integer, default=48, nullable=False)
    max_penalty_points: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    warn_threshold: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    suspend_threshold: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    decay_rate: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    decay_interval: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    pace_threshold_pct: Mapped[float] = mapped_column(Float, default=103.0, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(Text)
    primary_color: Mapped[str] = mapped_column(String(7), default="#FF6600", nullable=False)
    secondary_color: Mapped[str] = mapped_column(String(7), default="#1A1A2E", nullable=False)
    setup_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    channel_configs: Mapped[list["ChannelConfig"]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    seasons: Mapped[list["Season"]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    drivers: Mapped[list["Driver"]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    points_systems: Mapped[list["PointsSystem"]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    staff_members: Mapped[list["StaffMember"]] = relationship(back_populates="guild", cascade="all, delete-orphan")
    scheduled_messages: Mapped[list["ScheduledMessage"]] = relationship(back_populates="guild", cascade="all, delete-orphan")


class ChannelConfig(Base):
    __tablename__ = "channel_config"
    __table_args__ = (UniqueConstraint("guild_id", "purpose", name="uq_channel_config_guild_purpose"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    purpose: Mapped[ChannelPurpose] = enum_column(ChannelPurpose, ChannelPurpose.ANNOUNCEMENTS)
    channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="channel_configs")


class PointsSystem(Base):
    __tablename__ = "points_systems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int | None] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    points_per_position: Mapped[list[int]] = mapped_column(JSON, nullable=False)
    pole_bonus: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fastest_lap_bonus: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    most_positions_bonus: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    finish_bonus: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tiebreak_order: Mapped[list[str]] = mapped_column(JSON, default=lambda: ["wins", "podiums", "best_finish"], nullable=False)

    guild: Mapped[Guild | None] = relationship(back_populates="points_systems")
    seasons: Mapped[list["Season"]] = relationship(back_populates="points_system")


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    sim: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[SeasonStatus] = enum_column(SeasonStatus, SeasonStatus.DRAFT)
    num_rounds: Mapped[int] = mapped_column(Integer, nullable=False)
    drops: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    points_system_id: Mapped[int | None] = mapped_column(ForeignKey("points_systems.id", ondelete="SET NULL"))
    min_drivers: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    max_drivers: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    max_divisions: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    rulebook_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="seasons")
    points_system: Mapped[PointsSystem | None] = relationship(back_populates="seasons")
    divisions: Mapped[list["Division"]] = relationship(back_populates="season", cascade="all, delete-orphan")
    rounds: Mapped[list["Round"]] = relationship(back_populates="season", cascade="all, delete-orphan")
    registrations: Mapped[list["Registration"]] = relationship(back_populates="season", cascade="all, delete-orphan")
    penalty_points: Mapped[list["PenaltyPoint"]] = relationship(back_populates="season")


class Division(Base):
    __tablename__ = "divisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    tier: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    min_rating: Mapped[float | None] = mapped_column(Float)
    max_rating: Mapped[float | None] = mapped_column(Float)
    max_drivers: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    season: Mapped[Season] = relationship(back_populates="divisions")
    registrations: Mapped[list["Registration"]] = relationship(back_populates="division")
    race_results: Mapped[list["RaceResult"]] = relationship(back_populates="division")


class Round(Base):
    __tablename__ = "rounds"
    __table_args__ = (UniqueConstraint("season_id", "round_number", name="uq_rounds_season_round_number"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    round_number: Mapped[int] = mapped_column(Integer, nullable=False)
    track_name: Mapped[str] = mapped_column(Text, nullable=False)
    track_country: Mapped[str | None] = mapped_column(Text)
    track_flag: Mapped[str | None] = mapped_column(String(16))
    format: Mapped[str] = mapped_column(String(50), default="sprint", nullable=False)
    start_type: Mapped[str] = mapped_column(String(50), default="rolling", nullable=False)
    race_duration_min: Mapped[int] = mapped_column(Integer, default=40, nullable=False)
    weather: Mapped[str] = mapped_column(String(50), default="dry", nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[RoundStatus] = enum_column(RoundStatus, RoundStatus.SCHEDULED)
    server_info: Mapped[str | None] = mapped_column(Text)
    briefing_text: Mapped[str | None] = mapped_column(Text)
    track_limits_notes: Mapped[str | None] = mapped_column(Text)
    results_file_path: Mapped[str | None] = mapped_column(Text)
    briefing_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reminder_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    results_posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    protests_open_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    protests_close_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    final_results_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    season: Mapped[Season] = relationship(back_populates="rounds")
    results: Mapped[list["RaceResult"]] = relationship(back_populates="round", cascade="all, delete-orphan")
    protests: Mapped[list["Protest"]] = relationship(back_populates="round", cascade="all, delete-orphan")
    scheduled_messages: Mapped[list["ScheduledMessage"]] = relationship(back_populates="round")
    rsvps: Mapped[list["RSVP"]] = relationship(back_populates="round")


class Driver(Base):
    __tablename__ = "drivers"
    __table_args__ = (UniqueConstraint("guild_id", "discord_id", name="uq_drivers_guild_discord"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    discord_name: Mapped[str] = mapped_column(Text, nullable=False)
    real_name: Mapped[str | None] = mapped_column(Text)
    steam_id: Mapped[str | None] = mapped_column(Text)
    iracing_id: Mapped[str | None] = mapped_column(Text)
    rf2_id: Mapped[str | None] = mapped_column(Text)
    nationality: Mapped[str | None] = mapped_column(Text)
    nationality_flag: Mapped[str | None] = mapped_column(String(16))
    timezone: Mapped[str] = mapped_column(String(100), default="Europe/Lisbon", nullable=False)
    car_number: Mapped[int | None] = mapped_column(Integer)
    team_name: Mapped[str | None] = mapped_column(Text)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="drivers")
    registrations: Mapped[list["Registration"]] = relationship(back_populates="driver", cascade="all, delete-orphan")
    results: Mapped[list["RaceResult"]] = relationship(back_populates="driver")
    authored_protests: Mapped[list["Protest"]] = relationship(
        back_populates="author_driver",
        foreign_keys="Protest.author_driver_id",
    )
    accused_protests: Mapped[list["Protest"]] = relationship(
        back_populates="accused_driver",
        foreign_keys="Protest.accused_driver_id",
    )
    penalty_points: Mapped[list["PenaltyPoint"]] = relationship(back_populates="driver")
    rsvps: Mapped[list["RSVP"]] = relationship(back_populates="driver")


class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = (UniqueConstraint("driver_id", "season_id", name="uq_registrations_driver_season"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    division_id: Mapped[int | None] = mapped_column(ForeignKey("divisions.id", ondelete="SET NULL"))
    status: Mapped[RegistrationStatus] = enum_column(RegistrationStatus, RegistrationStatus.PENDING)
    hotlap_time_ms: Mapped[int | None] = mapped_column(Integer)
    hotlap_track: Mapped[str | None] = mapped_column(Text)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[int | None] = mapped_column(BigInteger)
    rejection_reason: Mapped[str | None] = mapped_column(Text)

    driver: Mapped[Driver] = relationship(back_populates="registrations")
    season: Mapped[Season] = relationship(back_populates="registrations")
    division: Mapped[Division | None] = relationship(back_populates="registrations")


class RaceResult(Base):
    __tablename__ = "race_results"
    __table_args__ = (UniqueConstraint("round_id", "driver_id", name="uq_race_results_round_driver"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    division_id: Mapped[int | None] = mapped_column(ForeignKey("divisions.id", ondelete="SET NULL"))
    finish_position: Mapped[int | None] = mapped_column(Integer)
    grid_position: Mapped[int | None] = mapped_column(Integer)
    best_lap_ms: Mapped[int | None] = mapped_column(Integer)
    total_time_ms: Mapped[int | None] = mapped_column(BigInteger)
    laps_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[ResultStatus] = enum_column(ResultStatus, ResultStatus.FINISHED)
    base_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bonus_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    penalty_time_sec: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    final_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    car_model: Mapped[str | None] = mapped_column(Text)
    incidents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    round: Mapped[Round] = relationship(back_populates="results")
    driver: Mapped[Driver] = relationship(back_populates="results")
    division: Mapped[Division | None] = relationship(back_populates="race_results")


class Protest(Base):
    __tablename__ = "protests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False)
    author_driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    accused_driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    lap_number: Mapped[int | None] = mapped_column(Integer)
    turn_zone: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_url: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ProtestStatus] = enum_column(ProtestStatus, ProtestStatus.SUBMITTED)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    cooldown_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    assigned_stewards: Mapped[list[int]] = mapped_column(JSON, default=list, nullable=False)
    votes: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    verdict: Mapped[str | None] = mapped_column(Text)
    penalty_type: Mapped[str | None] = mapped_column(Text)
    penalty_value: Mapped[str | None] = mapped_column(Text)
    penalty_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reasoning: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    appeal_reason: Mapped[str | None] = mapped_column(Text)
    appeal_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    appeal_verdict: Mapped[str | None] = mapped_column(Text)
    appeal_decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    staff_message_id: Mapped[int | None] = mapped_column(BigInteger)
    public_message_id: Mapped[int | None] = mapped_column(BigInteger)

    round: Mapped[Round] = relationship(back_populates="protests")
    author_driver: Mapped[Driver] = relationship(back_populates="authored_protests", foreign_keys=[author_driver_id])
    accused_driver: Mapped[Driver] = relationship(back_populates="accused_protests", foreign_keys=[accused_driver_id])
    penalty_point_entries: Mapped[list["PenaltyPoint"]] = relationship(back_populates="protest")


class PenaltyPoint(Base):
    __tablename__ = "penalty_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    protest_id: Mapped[int | None] = mapped_column(ForeignKey("protests.id", ondelete="SET NULL"))
    round_id: Mapped[int | None] = mapped_column(ForeignKey("rounds.id", ondelete="SET NULL"))
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[PenaltyPointType] = enum_column(PenaltyPointType, PenaltyPointType.PENALTY)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    driver: Mapped[Driver] = relationship(back_populates="penalty_points")
    season: Mapped[Season] = relationship(back_populates="penalty_points")
    protest: Mapped[Protest | None] = relationship(back_populates="penalty_point_entries")


class StaffMember(Base):
    __tablename__ = "staff_members"
    __table_args__ = (UniqueConstraint("guild_id", "discord_id", "role", name="uq_staff_members_role"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role: Mapped[StaffRole] = enum_column(StaffRole, StaffRole.ADMIN)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    appointed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    guild: Mapped[Guild] = relationship(back_populates="staff_members")


class ScheduledMessage(Base):
    __tablename__ = "scheduled_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    round_id: Mapped[int | None] = mapped_column(ForeignKey("rounds.id", ondelete="CASCADE"))
    type: Mapped[ScheduledMessageType] = enum_column(ScheduledMessageType, ScheduledMessageType.ANNOUNCEMENT)
    channel_purpose: Mapped[ChannelPurpose] = enum_column(ChannelPurpose, ChannelPurpose.ANNOUNCEMENTS)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    message_id: Mapped[int | None] = mapped_column(BigInteger)

    guild: Mapped[Guild] = relationship(back_populates="scheduled_messages")
    round: Mapped[Round | None] = relationship(back_populates="scheduled_messages")


class RSVP(Base):
    __tablename__ = "rsvp"
    __table_args__ = (UniqueConstraint("round_id", "driver_id", name="uq_rsvp_round_driver"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    round_id: Mapped[int] = mapped_column(ForeignKey("rounds.id", ondelete="CASCADE"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[RSVPStatus] = enum_column(RSVPStatus, RSVPStatus.CONFIRMED)
    responded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    round: Mapped[Round] = relationship(back_populates="rsvps")
    driver: Mapped[Driver] = relationship(back_populates="rsvps")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.id", ondelete="CASCADE"), nullable=False)
    actor_discord_id: Mapped[int | None] = mapped_column(BigInteger)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[str | None] = mapped_column(Text)
    target_id: Mapped[int | None] = mapped_column(Integer)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
