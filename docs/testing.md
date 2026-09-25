# 🧪 Testing & Verification Guide

## 📌 Overview

MindVault maintains API reliability through automated testing with `pytest` and HTTP integration verification using `curl` or FastAPI's interactive Swagger UI.

---

## 🛠 Running Tests

### Automated Testing Setup

Install testing dependencies:

```bash
pip install pytest httpx pytest-asyncio
```

Run test suite from the `backend` directory:

```bash
cd backend
pytest -v
```

---

## 🧪 Endpoint Verification via `curl`

### 1. Health Check
```bash
curl -X GET http://127.0.0.1:8000/health
```

### 2. User Registration
```bash
curl -X POST http://127.0.0.1:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@mindvault.local", "password": "password123"}'
```

### 3. User Login
```bash
curl -X POST http://127.0.0.1:8000/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@mindvault.local&password=password123"
```

### 4. Create Capture
```bash
curl -X POST http://127.0.0.1:8000/captures \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MindVault Architecture",
    "url": "https://mindvault.local/docs/architecture",
    "content": "System architecture overview document.",
    "status": "saved"
  }'
```

### 5. Get User Captures
```bash
curl -X GET http://127.0.0.1:8000/captures \
  -H "Authorization: Bearer <token>"
```

---

## 🖥 Interactive Verification

FastAPI provides built-in Swagger UI documentation:
1. Start application server: `uvicorn app.main:app --reload`
2. Open browser at `http://127.0.0.1:8000/docs`
3. Click **Authorize** and enter your Bearer token to test protected routes interactively.
