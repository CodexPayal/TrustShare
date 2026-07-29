from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, ForgotPassword, ResetPassword
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token, create_refresh_token
from app.security.oauth2 import get_current_user
from app.security.roles import require_role


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/test")
def auth_test():
    return {
        "message": "Auth route working"
    }


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
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

    password_match = verify_password(
        form_data.password,
        db_user.hashed_password
    )

    if not password_match:
        return {
            "message": "Invalid password"
        }

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    refresh_token = create_refresh_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/profile")
def profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "Profile access granted",
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }


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


@router.post("/logout")
def logout():
    return {
        "message": "Logout successful"
    }

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
            "message": "User not found"
        }

    return {
        "message": "Password reset link sent to email"
    }

@router.post("/reset-password")
def reset_password(
    user: ResetPassword,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    db_user.hashed_password = hash_password(
        user.new_password
    )

    db.commit()

    return {
        "message": "Password reset successful"
    }