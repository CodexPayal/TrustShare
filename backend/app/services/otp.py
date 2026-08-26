import random

from app.services.redis_client import redis_client


OTP_EXPIRY_SECONDS = 300  # 5 minutes


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def store_otp(email: str, otp: str):
    key = f"email_otp:{email}"
    redis_client.setex(
        key,
        OTP_EXPIRY_SECONDS,
        otp
    )


def verify_otp(email: str, otp: str) -> bool:
    key = f"email_otp:{email}"

    stored_otp = redis_client.get(key)

    if stored_otp is None:
        return False

    if stored_otp != otp:
        return False

    redis_client.delete(key)

    return True