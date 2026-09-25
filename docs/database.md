# 🗄 Database Schema & ORM Models

## 📌 Overview

MindVault uses **PostgreSQL** configured via SQLAlchemy 2.0 ORM.

Configuration file: [`backend/app/database.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/database.py)
Declarative Base: `DeclarativeBase` / `Base.metadata.create_all(bind=engine)`

---

## 📊 Entity Relationship Diagram (ERD)

```
       +-----------------------+
       |         users         |
       +-----------------------+
       | id (PK, Integer)      |
       | email (String, Unique)|
       | password_hash (String)|
       | created_at (DateTime) |
       +-----------------------+
           |               |
 1 to Many |               | 1 to Many
           v               v
+---------------------+  +--------------------------+
|      captures       |  |          files           |
+---------------------+  +--------------------------+
| id (PK, Integer)    |  | id (PK, Integer)         |
| user_id (FK -> users)| | user_id (FK -> users)   |
| title (String 255)  |  | filename (String 255)   |
| url (String 2048)   |  | storage_key (Unique)     |
| content (Text)      |  | content_type (String 100)|
| status (String 50)  |  | size (Integer)           |
+---------------------+  | created_at (DateTime)    |
                         +--------------------------+
```

---

## 🗂 Table Specifications

### 1. `users` Table
Stores user account records and credentials.
Source file: [`backend/app/models/user.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/user.py)

| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `Integer` | No | Primary Key, Indexed | Auto-incrementing user ID |
| `email` | `String` | No | Unique, Indexed | User email address |
| `password_hash` | `String` | No | None | Securely hashed password string |
| `created_at` | `DateTime` | No | Default `datetime.utcnow` | Account creation timestamp |

---

### 2. `captures` Table
Stores web page clippings, notes, and bookmark content.
Source file: [`backend/app/models/capture.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/capture.py)

| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `Integer` | No | Primary Key, Indexed | Auto-incrementing capture ID |
| `user_id` | `Integer` | No | Foreign Key (`users.id`) | Owner user reference |
| `title` | `String(255)` | No | None | Title of web capture |
| `url` | `String(2048)` | Yes | None | Source URL |
| `content` | `Text` | No | None | Full text or markdown body |
| `status` | `String(50)` | No | Default `"active"` | Status tag (`active`, `saved`, `archived`) |

---

### 3. `files` Table
Tracks uploaded documents and binary media metadata.
Source file: [`backend/app/models/file.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/file.py)

| Column Name | Data Type | Nullable | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `Integer` | No | Primary Key, Indexed | Auto-incrementing file record ID |
| `user_id` | `Integer` | No | Foreign Key (`users.id`) | Uploader user reference |
| `filename` | `String(255)` | No | None | Original uploaded file name |
| `storage_key` | `String(500)` | No | Unique | Path or S3 key on storage engine |
| `content_type` | `String(100)` | No | None | MIME type (e.g. `application/pdf`) |
| `size` | `Integer` | No | None | File size in bytes |
| `created_at` | `DateTime` | No | Default `datetime.utcnow` | Upload timestamp |

---

## 🛠 DB Connection & Migration

- **Connection URL**: Configured via `DATABASE_URL` env variable (e.g. `postgresql+psycopg2://postgres:password@localhost:5432/mindvault`).
- **Table Creation**: `Base.metadata.create_all(bind=engine)` is called automatically on FastAPI startup in `backend/app/main.py`.
- **Future Migrations**: Alembic support planned for seamless schema migrations in production.
