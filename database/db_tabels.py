from pathlib import Path

from sqlalchemy import BigInteger, String, ForeignKey, text
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"

engine = create_async_engine(url=f"sqlite+aiosqlite:///{DB_PATH}")
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Collection(Base):
    __tablename__ = 'collections'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class Painting(Base):
    __tablename__ = 'paintings'

    id: Mapped[int] = mapped_column(primary_key=True)
    collection_id: Mapped[int] = mapped_column(ForeignKey('collections.id'))
    name: Mapped[str] = mapped_column(String(50))
    normalized_name: Mapped[str] = mapped_column(String(50))
    prediction_name: Mapped[str] = mapped_column(String(50))
    author: Mapped[str] = mapped_column(String(50))
    year: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(1000))
    material: Mapped[str] = mapped_column(String(200))
    size: Mapped[str] = mapped_column(String(200))
    image: Mapped[str] = mapped_column(String(255))
    image_page_link: Mapped[str] = mapped_column(String(255))
    audio: Mapped[str] = mapped_column(String(255))
    audio_page_link: Mapped[str] = mapped_column(String(255))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def alter_table():
    async with engine.begin() as conn:
        await conn.execute(
            text("ALTER TABLE paintings ADD COLUMN prediction VARCHAR(100)")
        )
