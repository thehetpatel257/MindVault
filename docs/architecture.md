# 🏗 Architecture Overview

## 📌 Introduction

**MindVault** is designed as a modular web application backend for capturing, organizing, and querying web content, notes, and documents. The core philosophy emphasizes performance, privacy, data ownership, and simple extensibility.

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance Python async web framework with automatic OpenAPI spec generation. |
| **Database ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Declarative Python SQL toolkit and Object Relational Mapper. |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Relational database engine for structured data persistence. |
| **Authentication** | [PyJWT](https://pyjwt.readthedocs.io/) | JSON Web Token encoding/decoding using HMAC-SHA256 (HS256). |
| **Password Security**| [pwdlib](https://github.com/hynek/pwdlib) | Modern password hashing helper library utilizing recommended secure hashing. |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Strict data typing, schema validation, and Serialization. |

---

## 📐 System Diagram

```
+-------------------------------------------------------+
|                 Client Application                   |
|  (Web App / Mobile App / Browser Extension Interface)  |
+-------------------------------------------------------+
                           |
                           | HTTP / REST (Bearer Token)
                           v
+-------------------------------------------------------+
|                    FastAPI Server                     |
|                                                       |
|  +--------------------+      +---------------------+  |
|  | /users Router      |      | /captures Router    |  |
|  +--------------------+      +---------------------+  |
|            |                            |             |
|            +------------+---------------+             |
|                         |                             |
|                         v                             |
|             +-----------------------+                 |
|             | Auth & Security Layer |                 |
|             | (get_current_user)    |                 |
|             +-----------------------+                 |
|                         |                             |
|                         v                             |
|             +-----------------------+                 |
|             | SQLAlchemy ORM Models |                 |
|             +-----------------------+                 |
+-------------------------|-----------------------------+
                          |
                          v (psycopg2)
+-------------------------------------------------------+
|                 PostgreSQL Database                   |
|    [ users ]  <--->  [ captures ]  <--->  [ files ]   |
+-------------------------------------------------------+
```

---

## 📂 Core Module Organization

The backend repository is organized cleanly by responsibility:

- [`backend/app/main.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/main.py): Application entrypoint. Instantiates FastAPI app, binds database metadata, registers middleware & routes.
- [`backend/app/database.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/database.py): Initializes database engine, creates session factory (`SessionLocal`), and provides DB session dependency (`get_db`).
- [`backend/app/core/auth.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/core/auth.py): Contains the FastAPI dependency `get_current_user` to validate bearer tokens and retrieve active database user.
- [`backend/app/services/security.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/services/security.py): Password hashing/verification functions and JWT token creation logic.
- [`backend/app/models/`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models): SQLAlchemy declarative models mapping database tables.
- [`backend/app/schemas/`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/schemas): Pydantic schemas validating input payloads and controlling JSON response shapes.
- [`backend/app/api/`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/api): API route handlers broken down into resource namespaces (`/users`, `/captures`).

---

## 🔮 Future Architecture Components

1. **Browser Extension (`/extension`)**: A Manifest V3 Chrome extension to capture selected text, page URLs, and screenshots directly into MindVault.
2. **File & Cloud Storage Service**: Upload pipeline saving binary assets (images, PDFs) locally or into S3-compatible object storage.
3. **Full-Text & Vector Search**: Search engine integration to query captures by content similarity and keyword matching.
