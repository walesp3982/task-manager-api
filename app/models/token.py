from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities import CreateToken, Token
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import UserModel


class TokenModel(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    token: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(back_populates="tokens")

    def __init__(self, token: CreateToken):
        self.expires_at = token.expires_at
        self.token = token.token
        self.user_id = token.user_id

    def get_entity(self):
        return Token(
            id=self.id,
            user_id=self.user_id,
            expires_at=self.expires_at,
            token=self.token,
        )
