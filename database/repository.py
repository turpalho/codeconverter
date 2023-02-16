import logging
from typing import List

from sqlalchemy import exc, select, update, func, desc, text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine


from database.db import (
    User, Config
)

logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    # config
    async def get_config_parameters(self):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(Config).where(Config.id == 1)
            result = await session.execute(stmt)
            result = result.first()
            await session.commit()
        return result


    async def create_config(self, admins_ids: list) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            new_str = str(admins_ids)[1:-1]
            session.add(Config(id=1, admins_ids=new_str))
            await session.commit()
        return


    async def update_admin_ids(self, admins_ids: list) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            new_str = str(admins_ids)[1:-1]
            stmt = update(Config).where(Config.id == 1).values(admins_ids=new_str)
            await session.execute(stmt)
            await session.commit()
        return
    

    async def update_admin_deleted(self, new_status: bool) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = update(Config).where(Config.id == 1).values(admin_deleted=new_status)
            await session.execute(stmt)
            await session.commit()
        return