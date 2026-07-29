# TrustShare

Secure File Sharing System built with FastAPI.

## Authentication Module

The authentication module provides secure user authentication and role-based access management for the TrustShare platform.

## Implemented Features

* User Registration
* User Login
* Logout
* JWT Authentication
* Role-Based Access Control (RBAC)
* Password Hashing using bcrypt

## Database

* PostgreSQL Integration
* Users Table

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### Security

* JWT Authentication
* OAuth2
* bcrypt Password Hashing

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

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn app.main:app --reload
```

## Contributors

* Priyanka Swain
* Reshma Challa

Developed as part of Infosys Springboard Virtual Internship.
