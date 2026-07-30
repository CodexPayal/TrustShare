# TrustShare

Secure File Sharing System built with FastAPI.

## Authentication Module

This module provides secure authentication, authorization, and user management for the TrustShare platform.

## Features Implemented

### Authentication APIs
- User Registration
- User Login
- User Logout
- Forgot Password
- Reset Password
- Refresh Token
- User Profile Access

### Security Features
- JWT Authentication
- OAuth2 Password Flow
- Password Hashing with bcrypt
- Role-Based Access Control (RBAC)

### Database
- PostgreSQL Integration
- Users Table

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Security
- JWT
- OAuth2
- bcrypt

## Project Structure

```text
backend/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── security/
│   └── main.py
│
├── requirements.txt
└── .gitignore
```

## Setup

### Clone Repository

```bash
git clone <repository-url>
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn app.main:app --reload
```

## Contributors

- Priyanka Swain
- Reshma Challa

## Internship

Developed as part of the Infosys Springboard Virtual Internship 7.0.
