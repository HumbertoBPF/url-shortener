from typing import List

import bcrypt
import jwt
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.config import db
from settings import SECRET_JWT


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    urls: Mapped[List["Url"]] = relationship()

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password.encode('utf-8'))

    def issue_token(self):
        return jwt.encode({"id": self.id}, SECRET_JWT, algorithm="HS256")


class Url(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    short_url: Mapped[str] = mapped_column(String(256), unique=True)
    long_url: Mapped[str] = mapped_column(String(1024))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
