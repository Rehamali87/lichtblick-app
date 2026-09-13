import os
from collections.abc import Generator
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from sqlalchemy import Integer, String, Text, create_engine
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


DATABASE_URL = f"sqlite:///lichtblick.db"

class Base(DeclarativeBase):
	pass


class Memory(Base):
	__tablename__ = "memories"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	user_key: Mapped[str] = mapped_column(
		String(36), default=lambda: str(uuid4()), nullable=False, index=True
	)
	title: Mapped[str] = mapped_column(String, nullable=False)
	details: Mapped[str] = mapped_column(Text, nullable=False)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
	Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()


def add_memory(user_key: str, title: str, details: str) -> Memory:
	with SessionLocal() as session:
		memory = Memory(user_key=user_key, title=title, details=details)
		session.add(memory)
		session.commit()
		session.refresh(memory)
		return memory


def get_memories(user_key: str) -> list[Memory]:
	with SessionLocal() as session:
		return list(
			session.scalars(
				select(Memory)
				.where(Memory.user_key == user_key)
				.order_by(Memory.id.desc())
			).all()
		)


init_db()
