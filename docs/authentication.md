# 🔐 Authentication Architecture

## 🔑 Overview

MindVault implements OAuth2 with JWT (JSON Web Tokens) Bearer token authentication.

Authentication spans three core application modules:
1. [`backend/app/services/security.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/services/security.py): Hashing passwords and generating JWTs.
2. [`backend/app/core/auth.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/core/auth.py): Middleware dependency validating incoming tokens.
3. [`backend/app/api/users.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/api/users.py): User registration, login endpoint, and profile lookup.

---

## 🔄 Authentication Workflow

```
Client                               FastAPI App                            PostgreSQL DB
  |                                       |                                      |
  |-- 1. POST /users/register ----------->|                                      |
  |     (email, password)                 |-- Check existing email ------------->|
  |                                       |<-- Existing user status -------------|
  |                                       |-- Hash password with pwdlib          |
  |                                       |-- Save user record ----------------->|
  |<-- 200 OK (User Object) --------------|                                      |
  |                                       |                                      |
  |-- 2. POST /users/login -------------->|                                      |
  |     (username=email, password)        |-- Fetch user record ---------------->|
  |                                       |<-- User hash record -----------------|
  |                                       |-- Verify password hash               |
  |                                       |-- Generate JWT token (HS256)         |
  |<-- 200 OK (access_token) -------------|                                      |
  |                                       |                                      |
  |-- 3. GET /captures (Header: Bearer) ->|                                      |
  |                                       |-- Decode token & verify exp/sub      |
  |                                       |-- Fetch User by user_id ------------>|
  |                                       |<-- Active User entity ---------------|
  |                                       |-- Query user's captures ------------>|
  |<-- 200 OK (Captures array) -----------|                                      |
```

---

## 🔒 Security Configuration & Parameters

- **Algorithm**: `HS256` (HMAC using SHA-256)
- **Token Expiration**: `30 minutes`
- **Secret Key**: Loaded dynamically from `JWT_SECRET_KEY` in `backend/.env`.
- **Password Hasher**: Powered by `pwdlib` (`PasswordHash.recommended()`), generating secure hash representations stored in `users.password_hash`.

---

## 📜 Token Structure

Decoded JWT Payload:

```json
{
  "sub": "1",
  "exp": 1758482400
}
```

- `sub`: User ID stored as a string.
- `exp`: Expiration timestamp in UTC seconds (`datetime.now(timezone.utc) + timedelta(minutes=30)`).

---

## 🛡 Auth Dependency Usage

In protected API routers (e.g. `captures.py`), the `get_current_user` dependency automatically extracts the user from the Request header:

```python
from fastapi import Depends
from app.core.auth import get_current_user
from app.models.user import User

@router.get("/my-endpoint")
def my_protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}"}
```

If the token is missing, expired, or invalid, FastAPI automatically halts execution and responds with `401 Unauthorized`.
