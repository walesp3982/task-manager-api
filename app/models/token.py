from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    expires_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship("User", back_populates="tokens")
