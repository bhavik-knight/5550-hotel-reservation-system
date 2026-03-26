Hotel Reservation System API
============================

Project Title & Student Info
----------------------------

**Hotel Reservation System API**  
**Student:** Bhavik  
**Date:** March 25, 2026

Installation & Setup
--------------------

**uv Installation**

Linux / macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Environment Setup
-----------------

1) Sync dependencies:

```bash
uv sync
```

2) Create a local environment file by copying [ .env.example](.env.example):

```bash
cp .env.example .env
```

Then fill in the values in [ .env](.env) (do not commit it).

Local Execution
---------------

Run the app with live reload using Uvicorn:

```bash
uv run uvicorn reservation_system.asgi:application --reload
```

Containerization (Docker Compose)
---------------------------------

Build and run the stack (Django API + MySQL 8.0) using [docker-compose.yml](docker-compose.yml):

```bash
docker compose up --build
```

This launches both the MySQL 8.0 database and the Django API simultaneously.

Project Structure
-----------------

Project tree (depth 3):

```
.
├── DEPLOYMENT.md
├── Dockerfile
├── QUICKSTART.md
├── README.md
├── docker-compose.yml
├── pyproject.toml
└── reservation_system
    ├── manage.py
    ├── apps
    │   ├── addresses
    │   │   ├── migrations
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   └── views.py
    │   ├── hotels
    │   │   ├── migrations
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   └── views.py
    │   └── reservations
    │       ├── migrations
    │       ├── models.py
    │       ├── serializers.py
    │       └── views.py
    └── reservation_system
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

Core Components & Data Model
----------------------------

**ERD Relationships**

- **Hotel** has a one-to-one relationship with **Address** (each hotel has exactly one address).
- **Reservation** references a **Hotel** and has a many-to-many relationship with **Person** (a reservation can include multiple guests, and a person can be in multiple reservations).
- **Person** can optionally reference **Address** for contact information.

**Why Address and Person are decoupled**

- Normalization prevents duplication of contact data across reservations and hotels.
- **Address** is reusable by both **Hotel** and **Person** without duplicating fields.
- **Person** is reusable across multiple reservations, so contact updates are made in one place.

API Documentation
-----------------

Swagger UI is available at: `/api/docs/`.

Endpoints:

- **GET** `/api/getListOfHotels/` — returns the list of hotels.
- **POST** `/api/reservationConfirmation/` — creates a reservation and returns a confirmation number.

Beyond Requirements (Complexity)
--------------------------------

- **Python 3.14** latest stable runtime.
- **uv** for high-speed dependency management and reproducible installs.
- **MySQL 8.0** integration instead of SQLite for production-grade relational behavior.
- **Environment Variable security** using [ .env.example](.env.example) and a local [ .env](.env).
- **OpenAPI 3.0 / Swagger** auto-generated API documentation at `/api/docs/`.
### Python 3.14 with `uv` - Lightning-Fast Dependency Management

The project uses **`uv`**, a Rust-based replacement for `pip` that's 10-100x faster.

**Why `uv`?**
- ⚡ **10-100x faster** than pip for dependency resolution
- 🔒 **Deterministic** - `uv.lock` ensures reproducible builds
- 📦 **Simplified workflow** - Single tool for pip, virtualenv, and pip-tools
- 🔄 **Python version management** - Built-in Python version selection
- 🪶 **Lightweight** - Single binary, no external dependencies

**Example Performance:**
```
pip install:    45 seconds
uv install:     4 seconds  ✨
```

### Uvicorn - Asynchronous ASGI Server

The API runs on **Uvicorn**, a lightning-fast ASGI server implementation.

**Benefits:**
- 🚀 **Async-first** - Handles thousands of concurrent connections
- 📊 **High-performance** - Built on uvloop for maximum speed
- 🔧 **Production-ready** - Used by industry leaders (FastAPI, etc.)
- 🌐 **HTTP/2 support** - Modern protocol for faster responses

**Performance Comparison:**
```
Django dev server (WSGI):    ~500 req/sec
Uvicorn (ASGI):            ~10,000+ req/sec ✨
```

### Dockerfile - Containerized Deployment

The project includes Docker support for:
- 📦 **Reproducibility** - Same environment across dev, test, prod
- 🔒 **Isolation** - No conflicts with system dependencies
- 🌍 **Portability** - Run anywhere Docker is installed
- 📈 **Scalability** - Easy to deploy multiple instances

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
Currently, all endpoints are open (no authentication required). In production, add token-based auth.

---

### 🏨 GET `/api/getListOfHotels/`

**Description:** Retrieve a list of all available hotels with their addresses.

**Method:** `GET`

**URL:** `/api/getListOfHotels/`

**Query Parameters:** None

**Response:** `200 OK`

```json
{
  "count": 2,
  "hotels": [
    {
      "id": 1,
      "name": "Grand Hotel Downtown",
      "description": "Luxury 5-star hotel in the heart of the city",
      "phone": "555-0001",
      "email": "info@grand-hotel.com",
      "base_rate": "299.99",
      "address": {
        "id": 1,
        "street_address": "123 Main Street",
        "city": "Boston",
        "province": "MA",
        "postal_code": "02101",
        "country": "USA"
      }
    },
    {
      "id": 2,
      "name": "Waterfront Inn",
      "description": "Oceanfront property with premium views",
      "phone": "555-0002",
      "email": "reservations@waterfront.com",
      "base_rate": "199.99",
      "address": {
        "id": 2,
        "street_address": "456 Ocean Boulevard",
        "city": "Miami",
        "province": "FL",
        "postal_code": "33101",
        "country": "USA"
      }
    }
  ]
}
```

**Example Usage:**
```bash
curl -X GET http://localhost:8000/api/getListOfHotels/
```

---

### 📋 POST `/api/reservationConfirmation/`

**Description:** Create a new reservation with one or more guests and receive a confirmation number.

**Method:** `POST`

**URL:** `/api/reservationConfirmation/`

**Content-Type:** `application/json`

#### Request Payload

```json
{
  "hotel_name": "Grand Hotel Downtown",
  "checkin": "2026-04-15",
  "checkout": "2026-04-18",
  "guests_list": [
    {
      "name": "John Doe",
      "phone_number": "555-1234",
      "email": "john.doe@example.com",
      "address": {
        "street_address": "789 Oak Lane",
        "city": "Chicago",
        "province": "IL",
        "postal_code": "60601",
        "country": "USA"
      }
    },
    {
      "name": "Jane Smith",
      "phone_number": "555-5678",
      "email": "jane.smith@example.com",
      "address": {
        "street_address": "789 Oak Lane",
        "city": "Chicago",
        "province": "IL",
        "postal_code": "60601",
        "country": "USA"
      }
    }
  ]
}
```

#### Response: `201 Created`

```json
{
  "id": 1,
  "hotel_name": "Grand Hotel Downtown",
  "checkin": "2026-04-15",
  "checkout": "2026-04-18",
  "confirmation_number": "CONF-A7B9C2D1",
  "guests_list": [
    {
      "id": 1,
      "name": "John Doe",
      "phone_number": "555-1234",
      "email": "john.doe@example.com",
      "address": {
        "id": 3,
        "street_address": "789 Oak Lane",
        "city": "Chicago",
        "province": "IL",
        "postal_code": "60601",
        "country": "USA"
      }
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "phone_number": "555-5678",
      "email": "jane.smith@example.com",
      "address": {
        "id": 3,
        "street_address": "789 Oak Lane",
        "city": "Chicago",
        "province": "IL",
        "postal_code": "60601",
        "country": "USA"
      }
    }
  ]
}
```

#### Confirmation Number Format

Confirmation numbers are generated using the format: `CONF-{8-CHARACTER-HEX}`

**Example:** `CONF-A7B9C2D1`

**Properties:**
- ✅ Unique across all reservations
- ✅ Hard to guess (UUID-based)
- ✅ Human-readable
- ✅ Used for reservation lookups

#### Error Responses

**400 Bad Request** - Missing required fields:
```json
{
  "hotel_name": ["This field may not be blank."],
  "checkin": ["This field may not be blank."],
  "guests_list": ["This list may not be empty."]
}
```

**400 Bad Request** - Invalid email format:
```json
{
  "guests_list": [
    {
      "email": ["Enter a valid email address."]
    }
  ]
}
```

#### Example Usage

**cURL:**
```bash
curl -X POST http://localhost:8000/api/reservationConfirmation/ \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_name": "Grand Hotel Downtown",
    "checkin": "2026-04-15",
    "checkout": "2026-04-18",
    "guests_list": [
      {
        "name": "John Doe",
        "phone_number": "555-1234",
        "email": "john@example.com",
        "address": {
          "street_address": "789 Oak Lane",
          "city": "Chicago",
          "province": "IL",
          "postal_code": "60601",
          "country": "USA"
        }
      }
    ]
  }'
```

**Python (requests):**
```python
import requests

payload = {
    "hotel_name": "Grand Hotel Downtown",
    "checkin": "2026-04-15",
    "checkout": "2026-04-18",
    "guests_list": [
        {
            "name": "John Doe",
            "phone_number": "555-1234",
            "email": "john@example.com",
            "address": {
                "street_address": "789 Oak Lane",
                "city": "Chicago",
                "province": "IL",
                "postal_code": "60601",
                "country": "USA"
            }
        }
    ]
}

response = requests.post(
    "http://localhost:8000/api/reservationConfirmation/",
    json=payload
)
print(response.json())
```

---

### 📜 GET `/api/reservation/{confirmation_number}/`

**Description:** Retrieve reservation details using the confirmation number.

**Method:** `GET`

**URL:** `/api/reservation/CONF-A7B9C2D1/`

**Response:** `200 OK`

```json
{
  "id": 1,
  "hotel_name": "Grand Hotel Downtown",
  "checkin": "2026-04-15",
  "checkout": "2026-04-18",
  "confirmation_number": "CONF-A7B9C2D1",
  "guests_list": [
    {
      "id": 1,
      "name": "John Doe",
      "phone_number": "555-1234",
      "email": "john.doe@example.com",
      "address": {
        "id": 3,
        "street_address": "789 Oak Lane",
        "city": "Chicago",
        "province": "IL",
        "postal_code": "60601",
        "country": "USA"
      }
    }
  ]
}
```

---

### 👥 Additional Endpoints

#### GET `/api/people/` - List All Guests

```bash
curl -X GET http://localhost:8000/api/people/
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone_number": "555-1234",
    "email": "john@example.com",
    "address": { ... }
  }
]
```

#### POST `/api/people/` - Create a Guest

```bash
curl -X POST http://localhost:8000/api/people/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone_number": "555-1234",
    "email": "john@example.com"
  }'
```

#### GET `/api/people/{id}/` - Get Guest Details

```bash
curl -X GET http://localhost:8000/api/people/1/
```

#### PUT/DELETE `/api/people/{id}/` - Update/Delete Guest

```bash
curl -X PUT http://localhost:8000/api/people/1/ \
  -H "Content-Type: application/json" \
  -d '{ "name": "Jane Doe" }'

curl -X DELETE http://localhost:8000/api/people/1/
```

---

## 💻 Development Setup

### Prerequisites
- Python 3.14+ (specified in `.python-version`)
- `uv` package manager installed ([Installation Guide](https://docs.astral.sh/uv/))
- Git

### Installation & Running

#### 1. Clone the Repository
```bash
git clone https://github.com/bhavik-knight/5550-hotel-reservation-system.git
cd hotel_reservation_system
```

#### 2. Sync Dependencies with `uv`
```bash
uv sync
```

This command:
- ✅ Creates a virtual environment automatically
- ✅ Reads from `pyproject.toml` and `uv.lock`
- ✅ Installs all dependencies in seconds
- ✅ Sets up the project for development

**What's installed:**
```
✓ Django 6.0.3+
✓ Django REST Framework 3.17.1+
✓ Uvicorn 0.42.0+
✓ Gunicorn 25.2.0+
✓ Ruff (code formatter)
```

#### 3. Run Migrations
```bash
cd reservation_system
python manage.py migrate
```

This creates the SQLite3 database with all tables:
- `addresses_address`
- `hotels_hotel`
- `reservations_person`
- `reservations_reservation`
- `reservations_reservation_guests`

#### 4. Create a Superuser (Optional - for Admin Panel)
```bash
python manage.py createsuperuser
```

#### 5. Start the Development Server
```bash
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
```

Access the API at: `http://localhost:8000/api/`  
Access Django Admin at: `http://localhost:8000/admin/`

---

## 🐳 Docker Deployment

### Dockerfile

A production-ready Dockerfile is included in the project root.

### Build the Docker Image

```bash
docker build -t hotel-reservation-system:1.0.0 .
```

**What this does:**
1. Uses Python 3.14 base image
2. Installs system dependencies
3. Copies project files
4. Installs Python dependencies via uv
5. Runs migrations
6. Sets up Uvicorn as the entrypoint

### Run the Container Locally

```bash
docker run -d \
  --name hotel-api \
  -p 8000:8000 \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  hotel-reservation-system:1.0.0
```

**Parameters:**
- `-d` - Run in detached mode
- `--name hotel-api` - Container name
- `-p 8000:8000` - Map port 8000 to host
- `-e DEBUG=False` - Production mode
- `-e ALLOWED_HOSTS=...` - Allowed hostnames

### Verify the Container

```bash
# Check logs
docker logs hotel-api

# Test the API
curl http://localhost:8000/api/

# Stop the container
docker stop hotel-api
```

### Docker Compose (Optional)

For production with PostgreSQL and Redis:

```bash
docker-compose up -d
```

---

## 🧪 Testing

### Run Django Tests

```bash
cd reservation_system
python manage.py test
```

### Test API Endpoints

Using `curl`:
```bash
# Create a reservation
curl -X POST http://localhost:8000/api/reservationConfirmation/ \
  -H "Content-Type: application/json" \
  -d '...'

# Get confirmation number from response
# Then retrieve the reservation
curl -X GET http://localhost:8000/api/reservation/{confirmation_number}/
```

Using Postman:
1. Import the collection (if provided)
2. Set variables for `base_url` and `confirmation_number`
3. Run requests in sequence

---

## 📁 Project Structure

```
hotel_reservation_system/
├── .github/                    # GitHub workflows (CI/CD)
├── .idea/                      # PyCharm IDE config
├── reservation_system/         # Django project root
│   ├── manage.py              # Django CLI
│   ├── db.sqlite3             # Development database
│   ├── reservation_system/    # Project settings
│   │   ├── settings.py        # Django configuration
│   │   ├── urls.py            # URL routing
│   │   ├── wsgi.py            # WSGI entrypoint
│   │   └── asgi.py            # ASGI entrypoint (for Uvicorn)
│   └── apps/                  # Modular apps
│       ├── addresses/         # Address domain
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── migrations/
│       ├── hotels/            # Hotel domain
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── migrations/
│       └── reservations/      # Reservation domain
│           ├── models.py      # Person & Reservation models
│           ├── serializers.py # Serializers with nested relationships
│           ├── views.py       # API views
│           ├── urls.py        # URL patterns
│           └── migrations/
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # (Optional) Multi-container setup
├── pyproject.toml            # uv configuration & dependencies
├── uv.lock                   # Lock file for reproducible builds
├── .python-version           # Python 3.14 specification
├── README.md                 # This file
└── LICENSE                   # Project license
```

---

## 🔒 Security Considerations

### Development vs. Production

**Development (current `settings.py`):**
- ✅ `DEBUG = True` - Shows detailed error pages
- ✅ `SECRET_KEY` - Hardcoded (OK for dev)
- ✅ `ALLOWED_HOSTS = []` - All hosts allowed

**Production (before deploying):**
- ❌ Set `DEBUG = False`
- ❌ Use environment variables for `SECRET_KEY`
- ❌ Configure `ALLOWED_HOSTS` with your domain
- ❌ Enable HTTPS/SSL
- ❌ Add CORS configuration
- ❌ Implement authentication (JWT tokens)
- ❌ Use PostgreSQL instead of SQLite3
- ❌ Configure database backups

### Example Production Settings

```python
# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👤 Author

**Bhavik** - Master's Student, MCDA 5550  
GitHub: [@bhavik-knight](https://github.com/bhavik-knight)  
Course Project: Hotel Reservation System API

---

## 🤝 Contributing

This is a course project. For contributions or questions:
1. Open an issue on GitHub
2. Submit a pull request with detailed description
3. Follow the existing code style and architecture

---

**Last Updated:** March 25, 2026  
**Version:** 1.0.0
