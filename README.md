# TrustShare — Authentication Module

**TrustShare** is a secure file-sharing system focused on protecting user authentication, authorization, and session access.

This repository contains the **Authentication Module**, built with **FastAPI**, implementing secure user authentication, token management, OAuth, RBAC, MFA, and session management.

## ✨ Key Features

* **User Authentication** — Registration, Login & Logout
* **Password Management** — Forgot Password & Reset Password
* **JWT Authentication** — Access & Refresh Token management
* **Google OAuth 2.0** — Secure Google Sign-In
* **Role-Based Access Control** — Role-based authorization
* **Multi-Factor Authentication** — Authenticator-based MFA
* **Session Management** — PostgreSQL + Redis sessions
* **Password Security** — bcrypt hashing
* **OAuth2** — Bearer-token based protected APIs

## 🛠️ Tech Stack

| Category           | Technologies                  |
| ------------------ | ----------------------------- |
| Backend            | Python, FastAPI               |
| Database           | PostgreSQL                    |
| ORM                | SQLAlchemy                    |
| Authentication     | JWT, OAuth2, Google OAuth 2.0 |
| Security           | bcrypt, MFA                   |
| Session Management | Redis                         |
| Server             | Uvicorn                       |

## 📁 Project Structure

```text
backend/
└── app/
    ├── database/
    │   └── database.py
    ├── models/
    │   ├── user.py
    │   └── session.py
    ├── routes/
    │   └── auth.py
    ├── schemas/
    │   └── user.py
    ├── security/
    │   ├── jwt.py
    │   ├── oauth2.py
    │   ├── password.py
    │   ├── reset_token.py
    │   └── roles.py
    └── services/
        ├── mfa.py
        ├── redis_client.py
        └── session.py
```

## 🔐 Authentication APIs

| Method | Endpoint                | Description                     |
| ------ | ----------------------- | ------------------------------- |
| `POST` | `/auth/register`        | Register a new user             |
| `POST` | `/auth/login`           | Authenticate user               |
| `POST` | `/auth/logout`          | End active session              |
| `POST` | `/auth/refresh`         | Generate a new access token     |
| `POST` | `/auth/forgot-password` | Initiate password recovery      |
| `POST` | `/auth/reset-password`  | Reset user password             |
| `GET`  | `/auth/profile`         | Access authenticated profile    |
| `GET`  | `/auth/admin`           | Access admin-protected resource |
| `GET`  | `/auth/google/login`    | Authenticate with Google        |
| `POST` | `/auth/mfa/setup`       | Configure MFA                   |
| `POST` | `/auth/mfa/verify`      | Verify MFA code                 |
| `POST` | `/auth/mfa/disable`     | Disable MFA                     |

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd TrustShare/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_url
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIS_URL=your_redis_url
```

> Keep `.env` and all credentials private. Never commit secrets to the repository.

### 5. Run the Backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## 📚 API Documentation

Interactive API documentation is available through FastAPI Swagger UI:

`http://127.0.0.1:8000/docs`

## 🔒 Security Highlights

* bcrypt-based password hashing
* JWT access and refresh tokens
* OAuth2 bearer authentication
* Google OAuth 2.0 integration
* Role-based authorization
* Time-based MFA
* Redis-backed session validation
* PostgreSQL-based user and session persistence

---

### Authors

**Priyanka Swain** 

**Reshma Challa**

**TrustShare — Secure File Sharing System**
