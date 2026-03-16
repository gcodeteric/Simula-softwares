from __future__ import annotations

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import cogs.registration as registration_module
import cogs.results as results_module
import cogs.stewarding as stewarding_module
import database.engine as engine_module
from database.models import Base


@pytest_asyncio.fixture()
async def session_factory(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    monkeypatch.setattr(engine_module, "SessionFactory", factory, raising=False)
    monkeypatch.setattr(registration_module, "SessionFactory", factory, raising=False)
    monkeypatch.setattr(results_module, "SessionFactory", factory, raising=False)
    monkeypatch.setattr(stewarding_module, "SessionFactory", factory, raising=False)
    try:
        yield factory
    finally:
        await engine.dispose()
