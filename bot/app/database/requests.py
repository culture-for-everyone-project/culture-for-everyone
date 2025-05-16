from app.database.models import async_session
from app.database.models import User, Collection, Painting
from sqlalchemy import select


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_collections():
    async with async_session() as session:
        return await session.scalars(select(Collection))


async def get_collection_painting(collection_id):
    async with async_session() as session:
        return await session.scalars(select(Painting).where(Painting.collection_id == collection_id))


async def get_painting(painting_id):
    async with async_session() as session:
        return await session.scalar(select(Painting).where(Painting.id == painting_id))


async def get_painting_by_name(painting_name: str):
    async with async_session() as session:
        painting = await session.scalar(select(Painting).where(Painting.name == painting_name))
        return painting
