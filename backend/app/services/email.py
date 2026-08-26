import os

from dotenv import load_dotenv
from aiosmtplib import send

from email.message import EmailMessage


load_dotenv()


async def send_otp_email(
    recipient_email: str,
    otp: str
):
    message = EmailMessage()

    message["From"] = os.getenv("SMTP_FROM")
    message["To"] = recipient_email
    message["Subject"] = "TrustShare Email Verification OTP"

    message.set_content(
        f"""
Hello,

Your TrustShare email verification OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not create a TrustShare account, please ignore this email.

Regards,
TrustShare Team
"""
    )

    await send(
        message,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT", 587)),
        username=os.getenv("SMTP_USERNAME"),
        password=os.getenv("SMTP_PASSWORD"),
        start_tls=True
    )