from enum import Enum

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.model.database import Base


class UserType(Enum):
    App = 1
    Backoffice = 2


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email_address: Mapped[str] = mapped_column(String(60), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    user_type: Mapped[UserType] = mapped_column(String(60))
    # created_at = mapped_column(DateTime, default=datetime.now)
    # updated_at = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
