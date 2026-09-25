# 🛡 Security Model & Guidelines

## 📌 Security Principles

MindVault prioritizes user privacy, data isolation, and defensible security standards.

---

## 🔒 Implemented Security Controls

### 1. Cryptographic Password Hashing
- **Library**: `pwdlib` (`PasswordHash.recommended()`)
- Plaintext passwords are **never** logged, cached, or stored.
- Password hashes are generated during `/users/register` and validated during `/users/login`.

### 2. User Data Isolation (Multi-Tenancy Scoping)
- Every capture or file query strictly verifies that `user_id == current_user.id`.
- Users cannot read, modify, or delete captures belonging to other user accounts.

### 3. JWT Signature & Expiration Enforcement
- HMAC-SHA256 signatures guarantee JWT integrity.
- Short token lifespan (30 minutes) limits damage from compromised client tokens.

### 4. SQL Injection Protection
- All database interactions use SQLAlchemy ORM parameter binding, preventing SQL injection vulnerabilities.

### 5. Input Validation
- All API request bodies are parsed and validated by **Pydantic v2** models (e.g. `EmailStr`, `HttpUrl`). Invalid inputs are rejected immediately with `422 Unprocessable Entity`.

---

## ⚠️ Security Best Practices & Hardening Checklist

When deploying MindVault to production:

- [ ] **HTTPS Enforcement**: Always place FastAPI behind a TLS/SSL reverse proxy (e.g., Nginx, Caddy, or Cloudflare).
- [ ] **Environment Secret Rotation**: Generate a strong random `JWT_SECRET_KEY` (e.g. `openssl rand -hex 32`) and keep it secret.
- [ ] **CORS Middleware**: Explicitly configure `CORSMiddleware` in `main.py` with allowed origins rather than wildcard `*`.
- [ ] **Rate Limiting**: Add rate-limiting middleware (e.g., `slowapi`) to public endpoints (`/users/login`, `/users/register`) to prevent brute-force attacks.
- [ ] **Database Connection Security**: Enable SSL mode in `DATABASE_URL` (`sslmode=require`).
