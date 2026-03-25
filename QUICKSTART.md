# Quick Start Guide - Hotel Reservation System API

**Get up and running in 5 minutes!**

---

## 🚀 Development (Local)

### 1. Clone & Setup

```bash
git clone https://github.com/bhavik-knight/5550-hotel-reservation-system.git
cd hotel_reservation_system
uv sync
```

### 2. Run Server

```bash
cd reservation_system
python manage.py migrate
python manage.py runserver
```

**API available at:** `http://localhost:8000/api/`

---

## 🐳 Docker (Recommended)

### 1. Build

```bash
docker build -t hotel-api:1.0.0 .
```

### 2. Run

```bash
docker run -d -p 8000:8000 --name hotel-api hotel-api:1.0.0
```

**API available at:** `http://localhost:8000/api/`

---

## 📡 Test the API

### Create a Reservation

```bash
curl -X POST http://localhost:8000/api/reservationConfirmation/ \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_name": "Grand Hotel",
    "checkin": "2026-04-15",
    "checkout": "2026-04-18",
    "guests_list": [
      {
        "name": "John Doe",
        "phone_number": "555-1234",
        "email": "john@example.com"
      }
    ]
  }'
```

**Response:**
```json
{
  "confirmation_number": "CONF-A7B9C2D1",
  "hotel_name": "Grand Hotel",
  "checkin": "2026-04-15",
  "checkout": "2026-04-18",
  "guests_list": [...]
}
```

### Retrieve Reservation

```bash
curl http://localhost:8000/api/reservation/CONF-A7B9C2D1/
```

### Get All Guests

```bash
curl http://localhost:8000/api/people/
```

---

## 📁 Project Structure

```
hotel_reservation_system/
├── README.md              # Full documentation
├── DEPLOYMENT.md          # Deployment guide
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
├── pyproject.toml         # Dependencies
├── uv.lock                # Dependency lock file
└── reservation_system/    # Django project
    ├── manage.py
    ├── apps/
    │   ├── addresses/    # Address models
    │   ├── hotels/       # Hotel models
    │   └── reservations/ # Reservations & People
    └── reservation_system/
        ├── settings.py
        ├── urls.py
        └── asgi.py
```

---

## 🔗 Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/reservationConfirmation/` | Create reservation |
| GET | `/api/reservation/{confirmation}` | Get reservation details |
| GET | `/api/people/` | List all guests |
| POST | `/api/people/` | Create guest |
| GET | `/api/people/{id}/` | Get guest details |

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation including:
- Architecture overview
- Database design
- API specifications
- Production deployment
- Security configuration

---

## 🆘 Common Issues

**Port 8000 in use?**
```bash
docker run -p 8001:8000 ...  # Use different port
```

**Database not initialized?**
```bash
docker exec hotel-api python manage.py migrate
```

**Want to access container shell?**
```bash
docker exec -it hotel-api bash
```

---

## 🎯 Next Steps

1. Read [README.md](README.md) for architecture details
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
3. Check API endpoints in README
4. Customize for your needs

---

**Version:** 1.0.0 | **Updated:** March 25, 2026

