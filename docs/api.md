# 🔌 REST API Reference

Base URL: `http://localhost:8000`

All endpoints return JSON responses. Protected endpoints require an HTTP `Authorization` header containing a valid Bearer JWT:

```http
Authorization: Bearer <your_jwt_access_token>
```

---

## 🏥 Health Endpoint

### `GET /health`
Checks API operational status.

- **Authentication**: None required
- **Response**: `200 OK`
```json
{
  "status": "ok",
  "service": "MindVault API"
}
```

---

## 👥 Users Endpoint (`/users`)

### `POST /users/register`
Registers a new user account.

- **Authentication**: None required
- **Request Body**: `application/json`
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Response**: `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com"
}
```
- **Error Responses**:
  - `409 Conflict`: `"Email already registered"`
  - `422 Unprocessable Entity`: Validation failure (e.g. invalid email format)

---

### `POST /users/login`
Authenticates user credentials and returns a Bearer access token.

- **Authentication**: None required
- **Request Content-Type**: `application/x-www-form-urlencoded` (OAuth2 Password Request Form)
- **Form Parameters**:
  - `username`: `user@example.com`
  - `password`: `securepassword123`
- **Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
- **Error Responses**:
  - `401 Unauthorized`: `"Invalid email or password"`

---

### `GET /users/me`
Retrieves details of the currently authenticated user.

- **Authentication**: Required (`Bearer <token>`)
- **Response**: `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com"
}
```
- **Error Responses**:
  - `401 Unauthorized`: `"Invalid token"`, `"Invalid or expired token"`, or `"User not found"`

---

## 📌 Captures Endpoint (`/captures`)

### `POST /captures`
Creates a new web capture snippet for the authenticated user.

- **Authentication**: Required (`Bearer <token>`)
- **Request Body**: `application/json`
```json
{
  "title": "Interesting Article on FastAPIs",
  "url": "https://fastapi.tiangolo.com/",
  "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
  "status": "saved"
}
```
- **Response**: `200 OK`
```json
{
  "id": 10,
  "user_id": 1,
  "title": "Interesting Article on FastAPIs",
  "url": "https://fastapi.tiangolo.com/",
  "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
  "status": "saved"
}
```

---

### `GET /captures`
Retrieves all captures owned by the authenticated user.

- **Authentication**: Required (`Bearer <token>`)
- **Response**: `200 OK`
```json
[
  {
    "id": 10,
    "user_id": 1,
    "title": "Interesting Article on FastAPIs",
    "url": "https://fastapi.tiangolo.com/",
    "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
    "status": "saved"
  }
]
```

---

### `GET /captures/{capture_id}`
Retrieves a specific capture by ID owned by the authenticated user.

- **Authentication**: Required (`Bearer <token>`)
- **Path Parameters**:
  - `capture_id` (integer, required)
- **Response**: `200 OK`
```json
{
  "id": 10,
  "user_id": 1,
  "title": "Interesting Article on FastAPIs",
  "url": "https://fastapi.tiangolo.com/",
  "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
  "status": "saved"
}
```
- **Error Responses**:
  - `404 Not Found`: `"Capture not found"`

---

### `PUT /captures/{capture_id}`
Updates one or more fields of an existing capture owned by the authenticated user.

- **Authentication**: Required (`Bearer <token>`)
- **Path Parameters**:
  - `capture_id` (integer, required)
- **Request Body**: `application/json` (all fields optional)
```json
{
  "title": "Updated Title",
  "url": "https://example.com",
  "content": "Updated content text.",
  "status": "archived"
}
```
- **Response**: `200 OK`
```json
{
  "id": 10,
  "user_id": 1,
  "title": "Updated Title",
  "url": "https://example.com",
  "content": "Updated content text.",
  "status": "archived"
}
```
- **Error Responses**:
  - `404 Not Found`: `"Capture not found"`

---

### `DELETE /captures/{capture_id}`
Deletes a capture owned by the authenticated user.

- **Authentication**: Required (`Bearer <token>`)
- **Path Parameters**:
  - `capture_id` (integer, required)
- **Response**: `200 OK`
```json
{
  "message": "Capture deleted successfully"
}
```
- **Error Responses**:
  - `404 Not Found`: `"Capture not found"`
