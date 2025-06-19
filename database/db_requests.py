from sqlalchemy import select
from database.db_tabels import async_session, User, Collection, Painting


# Для преобразования пользовательского ввода в нормализованную строку для поиска картины по названию
def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace('ё', 'е')

    result = []
    for char in text:
        if 'а' <= char <= 'я':
            result.append(char)
    return ''.join(result)


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


# Выбор коллекции
async def get_collections():
    async with async_session() as session:
        return await session.scalars(select(Collection))


# Для отправления списка картин коллекции
async def get_collection_painting(collection_id):
    async with async_session() as session:
        return await session.scalars(select(Painting).where(Painting.collection_id == collection_id))


# Для поиска через каталог
async def get_painting_by_id(painting_id):
    async with async_session() as session:
        return await session.scalar(select(Painting).where(Painting.id == painting_id))


# Для поиска по названию
async def get_painting_ids_by_name(painting_name: str):
    normalized = normalize(painting_name)
    async with async_session() as session:
        result = await session.execute(
            select(Painting.id).where(Painting.normalized_name.like(f"%{normalized}%"))
        )
        ids = result.scalars().all()
        return ids


# Для поиска по фото
async def get_painting_id_by_prediction(painting_prediction: str) -> int | None:
    async with async_session() as session:
        result = await session.scalar(
            select(Painting.id).where(Painting.prediction_name == painting_prediction)
        )
        return result if result else None
