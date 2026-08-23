import pyotp
import qrcode
from io import BytesIO


def generate_mfa_secret():
    return pyotp.random_base32()


def get_mfa_uri(email: str, secret: str):
    totp = pyotp.TOTP(secret)

    return totp.provisioning_uri(
        name=email,
        issuer_name="TrustShare"
    )


def generate_qr_code(email: str, secret: str):
    uri = get_mfa_uri(email, secret)

    qr = qrcode.make(uri)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return buffer.getvalue()


def verify_mfa_code(secret: str, code: str):
    totp = pyotp.TOTP(secret)

    return totp.verify(
        code,
        valid_window=1
    )