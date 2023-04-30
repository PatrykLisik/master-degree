from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    fullname: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
