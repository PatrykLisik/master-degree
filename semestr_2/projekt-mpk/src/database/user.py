from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Integer, String, Enum as SQL_Enum
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


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
