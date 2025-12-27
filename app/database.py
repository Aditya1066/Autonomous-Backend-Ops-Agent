from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

db_url = "sqlite:///test.db"


class Base(DeclarativeBase):
    pass

engine = create_engine(db_url, echo=True)

Base.metadata.create_all(engine)

def create_session():
    with Session(engine) as session:
        yield session