from datetime import datetime, timedelta, timezone

from jose import jwt

from app.security.jwt import SECRET_KEY, ALGORITHM


RESET_TOKEN_EXPIRE_MINUTES = 15


def create_reset_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=RESET_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": email,
        "type": "password_reset",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "password_reset":
            return None

        return payload.get("sub")

    except Exception:
        return None