# Repository Analysis Report

**Repository:** `kaisarfardin6620/wingman`  
**Branch:** `main`  
**Analysis status: ✅ SUCCESS — Code, structure, and project details were fully read and extracted.**

---

## What Was Analyzed

The following files were read directly from this repository:

| File / Path | What was extracted |
|---|---|
| `requirements.txt` | Full list of Python dependencies and frameworks |
| `Dockerfile` | Runtime environment, Python version, deployment setup |
| `docker-compose.yml` | Service architecture (app, database, Redis, Celery, Nginx) |
| `wingman/settings.py` | Django configuration, installed apps, infrastructure details |
| `wingman/celery.py` | Async task queue setup |
| `authentication/models.py` | Custom user model with JWT, OTP, premium subscription fields |
| `authentication/views.py` | Auth endpoints (register, login, OTP, password reset, Google login) |
| `authentication/tasks.py` | Email task queue (OTP emails, admin password reset emails) |
| `chat/models.py` | Chat session, Message, MessageImage, DetectedEvent models |
| `chat/services.py` | AI service, context window management, file upload handling |
| `chat/tasks.py` | Celery tasks: AI response generation, screenshot OCR, audio transcription |
| `chat/consumers.py` | Django Channels WebSocket consumer for real-time messaging |
| `core/models.py` | Tone, Persona, UserSettings, TargetProfile, FCMDevice, Notification models |
| `dashboard/views.py` | Admin dashboard: analytics, user management, config management |
| `dashboard/services.py` | Dashboard analytics: user stats, conversion rate, monthly growth charts |
| `subscription/` | Subscription app structure |
| `nginx.conf` | Reverse proxy config (HTTP/WebSocket routing) |
| `entrypoint.sh` | Container startup script (migrations, static files, server launch) |

---

## Project Description

**Wingman AI** is a production-grade, AI-powered dating coach backend built with Django and Django REST Framework. It provides personalized AI coaching for conversations and dating strategy, accessible via REST API and real-time WebSocket connections.

The backend supports multimodal AI interactions (text, images via OCR, voice notes via Whisper transcription), a freemium subscription model, multilingual responses, and a full admin management system.

---

## Tech Stack (Detected from Code)

**Backend Framework:**
- Python 3.11, Django 5.x, Django REST Framework (DRF)
- Django Channels (WebSockets / ASGI)
- Daphne / Uvicorn ASGI server
- Gunicorn (production WSGI/ASGI process manager)

**AI & Machine Learning:**
- OpenAI API — GPT-4o (text + vision), Whisper (audio transcription)
- Tiktoken — token counting / context window management
- LangChain-style RAG patterns (context window + prompt engineering)
- Pillow — image processing before OCR

**Async / Task Queue:**
- Celery with Redis broker
- Django Celery Results + Beat (scheduled tasks)
- Gevent (async I/O)

**Databases & Storage:**
- PostgreSQL (primary relational DB, via `psycopg2-binary`)
- Redis (cache, Celery broker, channel layers)
- AWS S3 via `boto3` / `django-storages` (media file storage)
- Firebase Admin SDK (FCM push notifications)

**Authentication & Security:**
- JWT via `djangorestframework-simplejwt`
- Google OAuth (`google-auth`)
- OTP email verification
- HMAC-peppered passcode hashing
- `cryptography`, `PyJWT`

**DevOps & Infrastructure:**
- Docker + Docker Compose (multi-container: app, PostgreSQL, Redis, Celery worker, Celery Beat, Nginx)
- Nginx (reverse proxy, WebSocket upgrade, static file serving)
- Sentry SDK (error monitoring)
- Prometheus + `django-prometheus` (metrics)
- `structlog` (structured logging)

**Other:**
- `drf-spectacular` (OpenAPI / Swagger docs)
- `django-allauth` (social authentication)
- `django-cors-headers` (CORS)
- `django-filter` (querystring filtering)
- `whitenoise` (static file serving)
- `firebase-admin` (push notifications)
- `python-dateutil`, `requests`

---

## Key Features (Extracted from Code)

1. **AI Chat Coaching** — Users send messages to receive AI-generated dating advice and reply suggestions, powered by GPT-4o with configurable personas and tones.

2. **Multimodal Input** — Screenshots (OCR via GPT-4o Vision) and voice notes (transcription via Whisper) are processed asynchronously via Celery tasks and returned to the user via WebSocket.

3. **Real-Time WebSocket Messaging** — Django Channels powers a live chat interface where AI responses are pushed in real time as Celery tasks complete.

4. **Persona & Tone System** — Users can select AI personas (e.g., wingman character) and communication tones (e.g., bold, playful, romantic) to personalize AI responses.

5. **Target Profile Management** — Users can create detailed profiles of the person they are pursuing (interests, notes, conversation context), which the AI uses to tailor its advice.

6. **Freemium Subscription Model** — Free users have daily message and upload limits (configurable via admin dashboard); premium users get unlimited, uncensored responses.

7. **JWT + OTP Authentication** — Email/password and Google OAuth login with JWT tokens and OTP-based email verification and account activation.

8. **Admin Dashboard** — Admins can view real-time analytics (total users, premium/free split, conversion rate, monthly growth graph), manage users, tones, personas, global config, and push bulk notifications.

9. **Push Notifications** — Firebase Cloud Messaging (FCM) integration for real-time alerts to mobile devices.

10. **Multilingual Support** — The AI is explicitly instructed to detect and respond in the user's input language or script (English, Arabic, Banglish, Hinglish, French, Spanish, etc.).

11. **Structured Logging & Monitoring** — `structlog` for structured application logs, Sentry for error tracking, Prometheus for metrics scraping.

---

## Architecture Summary

```
Client (Mobile/Web)
    │
    ├── REST API (HTTP) ──► Django + DRF ──► PostgreSQL
    │                              │
    │                              ├── Redis Cache
    │                              └── Celery Tasks ──► OpenAI API
    │                                      │               (GPT-4o, Whisper)
    └── WebSocket ──────► Django Channels ──► Redis Channel Layer
                                  │
                          Celery pushes AI results
                          back via WebSocket
```

---

## Resume Bullet Points for This Project

Use these directly in your resume's **Projects** section:

- **Wingman AI Backend** — Engineered a production-grade AI dating coach API using **Django, DRF, and Celery**, handling concurrent AI inference requests via async task queues backed by **Redis**.
- Integrated **OpenAI GPT-4o Vision** for screenshot OCR and **Whisper** for audio transcription, delivering multimodal AI coaching via real-time **WebSocket** connections (Django Channels / Daphne).
- Built a **freemium subscription system** with JWT + OTP authentication, configurable user limits, and admin analytics dashboard tracking user growth, conversion rates, and monthly active users.
- Containerized the full stack with **Docker Compose** (Django, PostgreSQL, Redis, Celery worker/beat, Nginx), deployed with Gunicorn/Uvicorn ASGI workers, AWS S3 media storage, and Firebase FCM push notifications.
- Implemented **structured logging** (`structlog`), **error monitoring** (Sentry), and **metrics** (Prometheus) for production observability.

---

## Why No README Was Found

This repository does **not** currently contain a `README.md` file. All project information above was extracted directly from:
- Source code (models, views, services, tasks, consumers)
- `requirements.txt` (dependency list)
- `Dockerfile` and `docker-compose.yml` (infrastructure)
- `demo.env` (environment variable keys)
- `nginx.conf` and `entrypoint.sh` (deployment configuration)

**The absence of a README was not a blocker.** The code itself was fully readable and contained sufficient detail to extract all project information needed for resume generation.

---

*This report was auto-generated by analyzing the repository code and configuration files on 2026-04-08.*
