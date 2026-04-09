# Hotel Reservation System API

A comprehensive REST API for a hotel reservation system, built with Django REST Framework and Docker.

---

## 1. Prerequisites (Install uv)

The project uses **uv** for extremely fast dependency management.

**macOS / Linux / Windows (WSL):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 2. Setup & Run (Automated)

We provide a script that handles dependency installation, database migrations, and data seeding in one go.

```bash
chmod +x setup_local.sh
./setup_local.sh
```

---

## 3. Manual Setup (Step-by-Step)

If you prefer to run the commands individually:

### Install Dependencies
```bash
uv sync
```

### Apply Migrations & Seed Data
```bash
uv run python reservation_system/manage.py migrate
uv run python reservation_system/manage.py seed_data --hotels 20 --reservations 250
```

### Start the Server
```bash
uv run uvicorn --app-dir reservation_system reservation_system.asgi:application --reload
```

---

## 4. Docker Deployment

To run the entire stack (API + MySQL Database) using Docker Compose:

```bash
docker compose up --build
```
*Note: Docker environment automatically performs migrations and seeding on startup.*

---

## API Documentation
Once the server is running, access the interactive Swagger documentation at:
👉 **[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)**

### Validation Rules
- **Reservation**: `hotel_name`, `guests_list`, and `price` (non-negative) are required.
- **Dates**: `checkin` must be in the future (max 1 year) and `checkout` must be after `checkin`.
- **Guest**: `name` (min 2 chars) and `phone_number` (min 7 digits) are required.

---

## License
MIT
