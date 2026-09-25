# 📝 Development Log & Roadmap

## 📌 Project Milestones

### Phase 1: Core Backend & Data Models (Completed ✅)
- [x] Initialized FastAPI application structure ([`backend/app/main.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/main.py)).
- [x] Configured SQLAlchemy 2.0 database engine & session pool ([`backend/app/database.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/database.py)).
- [x] Implemented ORM Models:
  - `User` ([`models/user.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/user.py))
  - `Capture` ([`models/capture.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/capture.py))
  - `File` ([`models/file.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/models/file.py))
- [x] Implemented Security & JWT Authentication Service:
  - Password hashing with `pwdlib` ([`services/security.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/services/security.py))
  - Bearer token authentication dependency ([`core/auth.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/core/auth.py))
- [x] Implemented API Routers & Schemas:
  - `/users/register`, `/users/login`, `/users/me` ([`api/users.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/api/users.py))
  - Full CRUD on `/captures` ([`api/captures.py`](file:///c:/Users/Het%20Patel/Desktop/MindVault/backend/app/api/captures.py))
- [x] Created comprehensive project documentation suite in `docs/`.

---

### Phase 2: Browser Extension Development (In Progress ⏳)
- [ ] Initialize Manifest V3 Chrome / Firefox Extension in [`extension/`](file:///c:/Users/Het%20Patel/Desktop/MindVault/extension).
- [ ] Implement Popup UI for quick web content clipping.
- [ ] Implement context menu item ("Save selection to MindVault").
- [ ] Store user JWT token securely in browser storage (`chrome.storage.local`).

---

### Phase 3: Advanced Features & Cloud Storage (Upcoming 🚀)
- [ ] File upload API (`POST /files/upload`) supporting local storage & S3 / Object storage bucket.
- [ ] Tagging system for captures (`tags` table & M2M relationships).
- [ ] Full-text search and filtering options for captures.
- [ ] Export captures (Markdown, JSON, PDF).
