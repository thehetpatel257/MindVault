# ☁️ Cloud & File Storage Specification

## 📌 Overview

MindVault supports uploading and tracking binary assets (PDFs, images, documents) alongside web page captures.

The file management data model is implemented in [`backend/app/models/file.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/file.py).

---

## 🗄 Storage Architecture

```
+-------------------------------------------------------------------+
|                        File Upload Request                        |
|                  POST /files/upload (Multipart)                   |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                           FastAPI API                             |
|       1. Validate File Size & Content-Type                        |
|       2. Generate Unique storage_key (UUID / path)                |
+-------------------------------------------------------------------+
             |                                              |
             v Local Storage Adapter                        v S3 / Cloud Adapter
+--------------------------+                      +--------------------------+
| Save to backend/uploads/ |                      | Upload object via boto3  |
+--------------------------+                      +--------------------------+
             \                                              /
              v                                            v
+-------------------------------------------------------------------+
|                   Save File Record to PostgreSQL                  |
| (user_id, filename, storage_key, content_type, size, created_at)  |
+-------------------------------------------------------------------+
```

---

## 📂 Storage Key Indexing & Structure

- **Local Storage Directory**: `backend/uploads/`
- **Storage Key Naming Pattern**: `<user_id>/<uuid4>_<filename>` (e.g., `1/a4f89b-paper.pdf`)

---

## 🚀 Planned Storage Endpoints

- `POST /files/upload`: Upload file via `UploadFile` multipart form payload.
- `GET /files`: List user uploaded files metadata.
- `GET /files/{file_id}`: Get metadata for a specific file.
- `GET /files/{file_id}/download`: Download file payload or return signed S3 presigned URL.
- `DELETE /files/{file_id}`: Remove file binary from disk/S3 and delete PostgreSQL record.
