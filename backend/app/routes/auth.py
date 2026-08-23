import base64
import os

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth

from app.database.database import get_db
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    ForgotPassword,
    ResetPassword,
    MFAVerify,
    MFAChallenge
)

from app.security.password import hash_password, verify_password

from app.security.jwt import (
    create_access_token,
    create_refresh_token,
    create_mfa_challenge_token,
    verify_token
)

from app.security.reset_token import (
    create_reset_token,
    verify_reset_token
)

from app.security.oauth2 import get_current_user
from app.security.roles import require_role

from app.services.redis_client import redis_client
from app.services.session import create_session, delete_session

from app.services.mfa import (
    generate_mfa_secret,
    get_mfa_uri,
    generate_qr_code,
    verify_mfa_code
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# GOOGLE OAUTH CONFIGURATION
# =========================================================

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=(
        "https://accounts.google.com/"
        ".well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile"
    }
)


# =========================================================
# TEST
# =========================================================

@router.get("/test")
def auth_test():
    return {
        "message": "Auth route working"
    }


# =========================================================
# REGISTER
# =========================================================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "username": new_user.username,
        "email": new_user.email
    }


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    if not db_user.hashed_password:
        return {
            "message": "This account uses Google login"
        }

    password_match = verify_password(
        form_data.password,
        db_user.hashed_password
    )

    if not password_match:
        return {
            "message": "Invalid password"
        }

    # MFA-enabled users need OTP verification.
    if db_user.mfa_enabled:
        mfa_token = create_mfa_challenge_token(
            db_user.email
        )

        return {
            "message": "MFA verification required",
            "mfa_required": True,
            "mfa_token": mfa_token
        }

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    refresh_token = create_refresh_token(
        data={"sub": db_user.email}
    )

    create_session(
        db=db,
        redis_client=redis_client,
        user_id=db_user.id,
        refresh_token=refresh_token
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# =========================================================
# MFA LOGIN
# =========================================================

@router.post("/login/mfa")
def login_with_mfa(
    data: MFAChallenge,
    db: Session = Depends(get_db)
):
    payload = verify_token(data.mfa_token)

    if payload is None:
        return {
            "message": "Invalid or expired MFA challenge"
        }

    if payload.get("type") != "mfa_challenge":
        return {
            "message": "Invalid MFA challenge"
        }

    email = payload.get("sub")

    if not email:
        return {
            "message": "Invalid MFA challenge"
        }

    db_user = db.query(User).filter(
        User.email == email
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    if not db_user.mfa_enabled:
        return {
            "message": "MFA is not enabled"
        }

    if not db_user.mfa_secret:
        return {
            "message": "MFA setup required"
        }

    valid = verify_mfa_code(
        db_user.mfa_secret,
        data.code
    )

    if not valid:
        return {
            "message": "Invalid MFA code"
        }

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    refresh_token = create_refresh_token(
        data={"sub": db_user.email}
    )

    create_session(
        db=db,
        redis_client=redis_client,
        user_id=db_user.id,
        refresh_token=refresh_token
    )

    return {
        "message": "MFA login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# =========================================================
# GOOGLE LOGIN
# =========================================================

@router.get("/google/login")
async def google_login(
    request: Request
):
    redirect_uri = request.url_for(
        "google_callback"
    )

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )


# =========================================================
# GOOGLE CALLBACK
# =========================================================

@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        token = await oauth.google.authorize_access_token(
            request
        )
    except Exception:
        return {
            "message": "Google authentication failed"
        }

    user_info = token.get("userinfo")

    if not user_info:
        return {
            "message": "Unable to get Google user information"
        }

    google_id = user_info.get("sub")
    email = user_info.get("email")
    name = user_info.get("name")

    if not google_id or not email:
        return {
            "message": "Google account information incomplete"
        }

    if not name:
        name = email.split("@")[0]

    # First try Google ID.
    db_user = db.query(User).filter(
        User.google_id == google_id
    ).first()

    # If Google ID is not found, try email.
    if not db_user:
        db_user = db.query(User).filter(
            User.email == email
        ).first()

    # Existing user.
    if db_user:

        if not db_user.google_id:
            db_user.google_id = google_id

        db.commit()
        db.refresh(db_user)

    # New Google user.
    else:

        db_user = User(
            username=name,
            email=email,
            google_id=google_id,
            hashed_password=None
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # Create our normal TrustShare JWT tokens.
    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    refresh_token = create_refresh_token(
        data={"sub": db_user.email}
    )

    # Create Redis + DB session.
    create_session(
        db=db,
        redis_client=redis_client,
        user_id=db_user.id,
        refresh_token=refresh_token
    )

    return {
        "message": "Google login successful",
        "username": db_user.username,
        "email": db_user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# =========================================================
# REFRESH TOKEN
# =========================================================

@router.post("/refresh")
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    payload = verify_token(refresh_token)

    if payload is None:
        return {
            "message": "Invalid or expired refresh token"
        }

    email = payload.get("sub")

    if not email:
        return {
            "message": "Invalid refresh token"
        }

    from app.models.session import Session as UserSession

    session = db.query(UserSession).filter(
        UserSession.refresh_token == refresh_token
    ).first()

    if session is None:
        return {
            "message": "Session not found"
        }

    redis_session = redis_client.get(
        f"session:{refresh_token}"
    )

    if redis_session is None:
        return {
            "message": "Session expired"
        }

    new_access_token = create_access_token(
        data={"sub": email}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# =========================================================
# PROFILE
# =========================================================

@router.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Profile access granted",
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "mfa_enabled": current_user.mfa_enabled
    }


# =========================================================
# ADMIN
# =========================================================

@router.get("/admin")
def admin_panel(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return {
        "message": "Welcome Admin",
        "username": current_user.username,
        "role": current_user.role
    }


# =========================================================
# LOGOUT
# =========================================================

@router.post("/logout")
def logout(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    delete_session(
        db=db,
        redis_client=redis_client,
        refresh_token=refresh_token
    )

    return {
        "message": "Logout successful"
    }


# =========================================================
# FORGOT PASSWORD
# =========================================================

@router.post("/forgot-password")
def forgot_password(
    user: ForgotPassword,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": (
                "If the email exists, "
                "a reset link has been generated"
            )
        }

    reset_token = create_reset_token(
        db_user.email
    )

    return {
        "message": "Password reset token generated",
        "reset_token": reset_token
    }


# =========================================================
# RESET PASSWORD
# =========================================================

@router.post("/reset-password")
def reset_password(
    user: ResetPassword,
    db: Session = Depends(get_db)
):
    email = verify_reset_token(user.token)

    if not email:
        return {
            "message": "Invalid or expired reset token"
        }

    db_user = db.query(User).filter(
        User.email == email
    ).first()

    if not db_user:
        return {
            "message": "Invalid or expired reset token"
        }

    db_user.hashed_password = hash_password(
        user.new_password
    )

    db.commit()

    return {
        "message": "Password reset successful"
    }


# =========================================================
# MFA SETUP
# =========================================================

@router.post("/mfa/setup")
def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.mfa_enabled:
        return {
            "message": "MFA is already enabled"
        }

    secret = generate_mfa_secret()

    current_user.mfa_secret = secret

    db.commit()

    uri = get_mfa_uri(
        current_user.email,
        secret
    )

    qr_code = generate_qr_code(
        current_user.email,
        secret
    )

    qr_base64 = base64.b64encode(
        qr_code
    ).decode("utf-8")

    return {
        "message": "MFA setup initiated",
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_base64}",
        "otpauth_uri": uri
    }


# =========================================================
# MFA VERIFY / ENABLE
# =========================================================

@router.post("/mfa/verify")
def verify_mfa(
    data: MFAVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.mfa_secret:
        return {
            "message": "MFA setup required first"
        }

    valid = verify_mfa_code(
        current_user.mfa_secret,
        data.code
    )

    if not valid:
        return {
            "message": "Invalid MFA code"
        }

    current_user.mfa_enabled = True

    db.commit()

    return {
        "message": "MFA enabled successfully"
    }


# =========================================================
# MFA DISABLE
# =========================================================

@router.post("/mfa/disable")
def disable_mfa(
    data: MFAVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.mfa_enabled:
        return {
            "message": "MFA is not enabled"
        }

    if not current_user.mfa_secret:
        return {
            "message": "MFA setup required"
        }

    valid = verify_mfa_code(
        current_user.mfa_secret,
        data.code
    )

    if not valid:
        return {
            "message": "Invalid MFA code"
        }

    current_user.mfa_enabled = False
    current_user.mfa_secret = None

    db.commit()

    return {
        "message": "MFA disabled successfully"
    }