from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from redis import Redis

from app.models.session import Session as UserSession


REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_session(
    db: Session,
    redis_client: Redis,
    user_id: int,
    refresh_token: str
):
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    new_session = UserSession(
        user_id=user_id,
        refresh_token=refresh_token,
        expires_at=expires_at
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    redis_client.setex(
        f"session:{refresh_token}",
        int(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS).total_seconds()),
        str(user_id)
    )

    return new_session


def delete_session(
    db: Session,
    redis_client: Redis,
    refresh_token: str
):
    db.query(UserSession).filter(
        UserSession.refresh_token == refresh_token
    ).delete()

    db.commit()

    redis_client.delete(
        f"session:{refresh_token}"
    )