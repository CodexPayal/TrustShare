from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    google_id = Column(
        String,
        unique=True,
        nullable=True
    )

    hashed_password = Column(
        String,
        nullable=True
    )

    role = Column(
        String,
        default="user"
    )

    is_active = Column(
        Boolean,
        default=True
    )

    # MFA
    mfa_enabled = Column(
        Boolean,
        default=False
    )

    mfa_secret = Column(
        String,
        nullable=True
    )