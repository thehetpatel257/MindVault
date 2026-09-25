# 🧠 MindVault

**MindVault** is a privacy-first web clipping and knowledge capturing backend service built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It allows users to register accounts, authenticate securely, and store captured web content, notes, and file metadata.

---

## 🌟 Features

- **User Authentication**: Secure user registration, password hashing (`pwdlib`), and JWT token-based authentication (`PyJWT`).
- **Web Captures Management**: CRUD operations for captured web snippets, URLs, and notes, strictly isolated per user.
- **File Metadata Tracking**: Database model support for user file storage key management.
- **RESTful Architecture**: Clean modular FastAPI routers, Pydantic schemas, and OpenAPI standard documentation.
- **Database ORM**: SQLAlchemy 2.0 declarative models with PostgreSQL connection pooling.

---

## 🏗 Project Structure

```
MindVault/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # API Route Handlers (users, captures)
│   │   ├── core/             # Core Config & Authentication Dependencies
│   │   ├── models/           # SQLAlchemy Data Models (User, Capture, File)
│   │   ├── schemas/          # Pydantic Request & Response Schemas
│   │   ├── services/         # Business Logic & Security Services
│   │   ├── database.py       # Database Connection & Session Setup
│   │   └── main.py           # FastAPI Application Entrypoint
│   ├── uploads/              # Local file uploads directory
│   ├── .env                  # Environment Variables (Database & Secret Keys)
│   └── requirements.txt      # Python Dependencies
├── docs/                     # System Documentation
│   ├── README.md             # Documentation Index
│   ├── architecture.md       # Architecture & Tech Stack Overview
│   ├── api.md                # REST API Endpoint Documentation
│   ├── authentication.md     # JWT Auth & Security Details
│   ├── database.md           # Database Schemas & Relations
│   ├── security.md           # Security Model & Best Practices
│   ├── cloud-storage.md      # File Upload & Cloud Storage Design
│   ├── testing.md            # Testing Guidelines & Commands
│   └── development-log.md    # Development Progress & Roadmap
└── extension/                # Browser Extension (Upcoming)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL database instance running locally or hosted

### 1. Environment Setup

Configure environment variables in [`backend/.env`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/.env):

```env
DATABASE_URL=postgresql+psycopg2://<user>:<password>@localhost:5432/mindvault
JWT_SECRET_KEY=your-super-secret-jwt-key
```

### 2. Install Dependencies & Run Server

```bash
cd backend
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install fastapi uvicorn sqlalchemy psycopg2-binary pyjwt pwdlib python-dotenv pydantic

uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

Interactive API Documentation (Swagger UI) is available at:
👉 **`http://127.0.0.1:8000/docs`**

---

## 📚 Documentation

Detailed documentation is available in the [`docs/`](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs) directory:

- 📐 [Architecture Overview](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/architecture.md)
- 🔌 [API Reference](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/api.md)
- 🔐 [Authentication Guide](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/authentication.md)
- 🗄 [Database Schema](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/database.md)
- 🛡 [Security Policies](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/security.md)
- ☁️ [Storage Design](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/cloud-storage.md)
- 🧪 [Testing & Verification](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/testing.md)
- 📝 [Development Log & Roadmap](file:///c:/Users/Het%20Patel/Desktop/MindVault/docs/development-log.md)
