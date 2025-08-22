Pytest test suite for the backend API.

How to run:
- Ensure the backend dependencies are installed (pip install -r requirements.txt).
- Run tests in non-interactive CI style:
  pytest -q

Notes:
- Tests use a temporary SQLite database file at ./test_app.db.
- Since the MVP AuthService returns a placeholder token, tests generate a valid JWT using the security.create_access_token and seed a user in the DB to satisfy get_current_user.
- Endpoints under /trading, /strategies, and /auth/me therefore include a proper Authorization header with the generated token.
