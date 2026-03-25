# Hotel Reservation System - Deployment Guide

**Last Updated:** March 25, 2026

---

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Docker Compose Deployment](#docker-compose-deployment)
4. [Production Deployment](#production-deployment)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites
- Python 3.14+
- `uv` package manager
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/bhavik-knight/5550-hotel-reservation-system.git
cd hotel_reservation_system
```

### Step 2: Sync Dependencies

```bash
uv sync
```

This automatically:
- Creates a virtual environment
- Installs all dependencies from `pyproject.toml`
- Uses reproducible builds from `uv.lock`

### Step 3: Run Migrations

```bash
cd reservation_system
python manage.py migrate
```

### Step 4: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 5: Start Development Server

```bash
python manage.py runserver
```

**Access Points:**
- API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

---

## Docker Deployment

### Build the Image

```bash
docker build -t hotel-reservation-system:1.0.0 .
```

**Build Arguments (Optional):**
```bash
docker build \
  --build-arg PYTHON_VERSION=3.14 \
  -t hotel-reservation-system:1.0.0 .
```

### Run the Container

#### Basic Run

```bash
docker run -d \
  --name hotel-api \
  -p 8000:8000 \
  hotel-reservation-system:1.0.0
```

#### Run with Environment Variables

```bash
docker run -d \
  --name hotel-api \
  -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY="your-secret-key-here" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  hotel-reservation-system:1.0.0
```

#### Run with Volume Mounting (Development)

```bash
docker run -d \
  --name hotel-api \
  -p 8000:8000 \
  -v $(pwd)/reservation_system:/app/reservation_system \
  -e DEBUG=True \
  hotel-reservation-system:1.0.0
```

### Verify Container

```bash
# Check if container is running
docker ps | grep hotel-api

# View logs
docker logs hotel-api

# Follow logs in real-time
docker logs -f hotel-api

# Test the API
curl http://localhost:8000/api/

# Access shell
docker exec -it hotel-api bash
```

### Stop Container

```bash
docker stop hotel-api
docker rm hotel-api  # Remove container
```

### Push to Docker Registry

#### DockerHub

```bash
# Login
docker login

# Tag image
docker tag hotel-reservation-system:1.0.0 \
  bhavik-knight/hotel-reservation-system:1.0.0

# Push
docker push bhavik-knight/hotel-reservation-system:1.0.0
```

#### GitHub Container Registry

```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag image
docker tag hotel-reservation-system:1.0.0 \
  ghcr.io/bhavik-knight/hotel-reservation-system:1.0.0

# Push
docker push ghcr.io/bhavik-knight/hotel-reservation-system:1.0.0
```

---

## Docker Compose Deployment

### Single Container (Development)

```bash
docker-compose up -d
```

Access API at: http://localhost:8000/api/

### With PostgreSQL (Production)

1. Uncomment the `db` and `cache` services in `docker-compose.yml`
2. Update `settings.py` to use PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hotel_db',
        'USER': 'hotel_user',
        'PASSWORD': 'hotel_password',
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

3. Start services:

```bash
docker-compose up -d
```

### Useful Commands

```bash
# View running services
docker-compose ps

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api

# Execute command in container
docker-compose exec api python manage.py shell

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Scale service (if applicable)
docker-compose up -d --scale api=3
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Generate secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure static files storage (S3, CloudFront, etc.)
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

### Secure Settings Template

Create `.env.production`:

```bash
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db-host:5432/hotel_db
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CORS_ALLOWED_ORIGINS=https://yourdomain.com
SENTRY_DSN=your-sentry-dsn
```

### Update settings.py for Production

```python
import os
from pathlib import Path

# ... existing settings ...

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600
        )
    }

# HTTPS
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Deploy with Docker

```bash
# Build production image
docker build -t hotel-reservation-system:production .

# Run with production settings
docker run -d \
  --name hotel-api-prod \
  -p 80:8000 \
  --env-file .env.production \
  --restart always \
  hotel-reservation-system:production
```

### Deploy with Kubernetes (Advanced)

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hotel-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hotel-api
  template:
    metadata:
      labels:
        app: hotel-api
    spec:
      containers:
      - name: api
        image: hotel-reservation-system:production
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "False"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: django-secret
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
```

---

## Environment Variables

### Development

```bash
DEBUG=True
SECRET_KEY=django-insecure-dev-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Production

```bash
DEBUG=False
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@db:5432/hotel_db
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SENTRY_DSN=<sentry-dsn>
```

### Generate Secure SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs hotel-api

# Check container status
docker inspect hotel-api

# Rebuild with verbose output
docker build -t hotel-reservation-system:1.0.0 . --progress=plain
```

### Database migration errors

```bash
# Run migrations manually
docker exec hotel-api python manage.py migrate

# Check migration status
docker exec hotel-api python manage.py showmigrations
```

### Permission denied errors

```bash
# Fix ownership in running container
docker exec -u root hotel-api chown -R appuser:appuser /app
```

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
docker run -p 8001:8000 ...
```

### Out of memory

```bash
# Check resource usage
docker stats

# Increase memory limit
docker run -m 2g ...
```

### API returns 500 errors

```bash
# Check Django logs
docker logs hotel-api | grep ERROR

# Test in Django shell
docker exec -it hotel-api python manage.py shell
>>> from reservations.models import Person
>>> Person.objects.all()
```

---

## Monitoring & Logging

### View Logs

```bash
# Last 50 lines
docker logs --tail 50 hotel-api

# Real-time logs
docker logs -f hotel-api

# Since specific time
docker logs --since 2026-03-25T10:00:00 hotel-api
```

### Health Check

```bash
# Check health endpoint
curl http://localhost:8000/api/

# Check specific endpoint
curl http://localhost:8000/api/people/
```

### Performance Monitoring

```bash
# Resource usage
docker stats hotel-api

# Inspect container
docker inspect hotel-api

# Network connections
docker exec hotel-api netstat -tulpn
```

---

## Rollback Strategy

### Tag and Version

```bash
# Tag releases
docker tag hotel-reservation-system:latest \
  hotel-reservation-system:1.0.0
docker tag hotel-reservation-system:latest \
  hotel-reservation-system:stable

# View tags
docker image ls | grep hotel-reservation
```

### Rollback to Previous Version

```bash
# Stop current
docker stop hotel-api
docker rm hotel-api

# Run previous version
docker run -d --name hotel-api -p 8000:8000 \
  hotel-reservation-system:1.0.0
```

---

## Performance Optimization

### Enable Gzip Compression

Add to `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... other middleware ...
]
```

### Configure Caching

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://cache:6379/1',
    }
}
```

### Database Connection Pooling

Install `django-db-conn-pool`:

```bash
uv pip install django-db-conn-pool
```

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_db_conn_pool.mysql',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'MAX_CONNS': 20,
        }
    }
}
```

### Static Files Serving

```bash
# Collect static files
docker exec hotel-api python manage.py collectstatic --noinput

# Serve via CDN (S3, CloudFront, etc.)
# Configure in settings.py
```

---

## Backup & Recovery

### Database Backup

```bash
# PostgreSQL backup
docker exec hotel-reservation-db pg_dump \
  -U hotel_user hotel_db > backup.sql

# Restore
docker exec -i hotel-reservation-db psql \
  -U hotel_user hotel_db < backup.sql
```

### Volume Backup

```bash
# Backup volume
docker run --rm \
  -v hotel-reservation_db_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/db_backup.tar.gz -C /data .

# Restore
docker run --rm \
  -v hotel-reservation_db_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/db_backup.tar.gz -C /data
```

---

## Next Steps

1. ✅ Set up monitoring (DataDog, New Relic, etc.)
2. ✅ Configure automated backups
3. ✅ Set up CI/CD pipeline (GitHub Actions, GitLab CI)
4. ✅ Enable logging aggregation (ELK Stack, Splunk)
5. ✅ Configure alerts for errors
6. ✅ Set up load balancing (nginx, HAProxy)
7. ✅ Plan disaster recovery procedures

---

## Support

For issues or questions:
- Create an issue on GitHub
- Check Django/DRF documentation
- Review Docker logs for errors

---

**Version:** 1.0.0  
**Last Updated:** March 25, 2026

