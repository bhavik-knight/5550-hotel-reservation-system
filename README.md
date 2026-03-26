Hotel Reservation System API
============================

Setup
-----

Install uv

Windows (PowerShell):

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies

```bash
uv sync
```

Run with live reload

```bash
uv run uvicorn reservation_system.asgi:application --reload
```

Docker and Docker Compose

Build and run the API and database with Docker Compose:

```bash
docker compose up --build
```

Architecture and Models
-----------------------

Architecture

- Django + Django REST Framework API
- MySQL database (via Docker Compose)
- OpenAPI/Swagger UI at `/api/docs/`

Models and Relationships

Hotel
- `id`, `name`, `description`, `phone`, `email`, `base_rate`

Guest
- `id`, `name`, `gender`, `phone_number`, `email`

Reservation
- `id`, `hotel_name`, `hotel` (optional FK), `checkin`, `checkout`, `price`, `confirmation_number`, `guests`

Relationships
- A Reservation can reference a Hotel (optional FK).
- A Reservation has many Guests, and a Guest can appear on many Reservations (many-to-many).

Project Structure
-----------------

```
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── reservation_system
    ├── manage.py
    ├── apps
    │   ├── hotels
    │   └── reservations
    └── reservation_system
        ├── settings.py
        └── urls.py
```

API Endpoints
-------------

Base URL: `http://localhost:8000/api/`

Swagger UI: `/api/docs/`

Hotels

- **GET** `/api/getListOfHotels/` - list hotels, optional `checkin` and `checkout` query params for availability
- **GET** `/api/hotels/` - list hotels
- **POST** `/api/hotels/` - create a hotel
- **GET** `/api/hotels/<id>/` - get a hotel by id
- **PUT** `/api/hotels/<id>/` - update a hotel
- **PATCH** `/api/hotels/<id>/` - partial update a hotel
- **DELETE** `/api/hotels/<id>/` - delete a hotel

Reservations

- **POST** `/api/reservationConfirmation/` - create a reservation and return confirmation number
- **GET** `/api/reservations/` - list reservations
- **GET** `/api/reservations/<confirmation_number>/` - get a reservation by confirmation number

Guests

- **GET** `/api/guests/` - list guests
- **POST** `/api/guests/` - create a guest
- **GET** `/api/guests/<id>/` - get a guest by id
- **PUT** `/api/guests/<id>/` - update a guest
- **PATCH** `/api/guests/<id>/` - partial update a guest
- **DELETE** `/api/guests/<id>/` - delete a guest

Docker Details
--------------

Dockerfile

- Uses `python:3.14-slim` base image.
- Installs system dependencies for MySQL client builds.
- Installs uv and syncs dependencies.
- Copies the project into `/app`.
- Exposes port 8000 and defines a default `uvicorn` command.

Docker Compose

- Two containers:
  - `api` for the Django backend.
  - `db` for MySQL 8.0.
- The `api` service runs migrations, seeds data, collects static files, and starts Uvicorn.
- The `db` service persists data in a named volume.

Validation Rules
----------------

Reservation

- `hotel_name` is required and cannot be blank.
- `guests_list` is required.
- `price` is required and cannot be negative.
- `checkin` cannot be in the past.
- `checkin` cannot be more than 1 year in the future.
- `checkout` must be after `checkin`.
- `guest_name` cannot be empty.
- `gender` must be Male, Female, Other, or Prefer not to say.

Guest

- `name` must be at least 2 characters.
- `phone_number` must have at least 7 digits.
