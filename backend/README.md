# AI Shield Backend

This is the backend for the AI Shield project, built with FastAPI.

## Structure

- `main.py` — FastAPI app setup, CORS, health check, and router inclusion
- `model.py` — SQLAlchemy database models and database setup
- `routes.py` — API endpoints (signup, login, etc.)

## Getting Started

1. **Activate your Python environment** (conda or venv).
2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose pydantic jwt
   ```
3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
4. **Database:**
   - The backend uses SQLite by default (`users.db` will be created automatically in the backend directory).

## API Endpoints

### Health Check
- `GET /health` — Returns `{ "status": "ok" }` if the server is running.

### Signup
- `POST /signup`
  - Body (JSON): `{ "username": "your_username", "password": "your_password" }`
  - Returns: `{ "access_token": "...", "token_type": "bearer" }`

### Login
- `POST /login`
  - Form data: `username`, `password`
  - Returns: `{ "access_token": "...", "token_type": "bearer" }`

---

- Add new database models in `model.py`.
- Add new API endpoints in `routes.py` and include them in `main.py` as needed. 