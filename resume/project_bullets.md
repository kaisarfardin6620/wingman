# Project Bullet Bank
# Each project block is delimited by `## PROJECT: <id>`.
# The generate_resume.py script reads this file and injects matching bullets
# into the template wherever it finds `<!-- PROJECT:<id> -->` markers.
#
# Metric placeholders — replace these with real numbers before submitting:
#   (X%)        → percentage improvement, e.g. "by 30%"
#   (N)         → count of users / requests / test cases, e.g. "500+ users"
#   (X ms)      → latency improvement, e.g. "by ~200 ms"
#   (X hrs/wk)  → time saved per week, e.g. "~5 hours/week"

---

## PROJECT: explainable-rag-chatbot

**Name:** Explainable Hybrid KG-RAG Chatbot
**URL:** https://github.com/kaisarfardin6620/explainable-rag-chatbot
**Stack:** FastAPI · Pinecone · Neo4j · OpenAI GPT-4o · NLI · Python

- Designed a research-grade hybrid RAG system combining vector search (Pinecone) and Knowledge Graph traversal (Neo4j) to reduce hallucination by (X%) vs. a pure-vector baseline.
- Implemented claim-level NLI verification that abstains from answering when confidence drops below a configurable threshold, improving answer trustworthiness for (N) evaluated queries.
- Applied Freeman's Degree Centrality to weight evidence from authoritative graph nodes; supported ablation study modes (`rag_only`, `kg_only`, `hybrid`) for scientific reproducibility.
- Built automated benchmarking pipeline generating F1 Score, Semantic Similarity, and Latency reports across (N) test cases.

---

## PROJECT: magictale

**Name:** MagicTale AI Backend
**URL:** https://github.com/kaisarfardin6620/magictale
**Stack:** Django 5 · Celery · Redis · OpenAI GPT-4o · DALL-E 3 · ElevenLabs · WebSockets · PostgreSQL

- Architected an asynchronous multi-stage AI pipeline (text → image → audio) for a children's storytelling app; reduced perceived latency via real-time WebSocket progress events to (N) concurrent users.
- Integrated DALL-E 3 for cover illustration and ElevenLabs TTS for per-page narration, stitching audio segments with pydub into a single playback-ready file.
- Implemented Google OAuth2 and Apple Sign-In alongside JWT auth (SimpleJWT) for zero-friction multi-platform onboarding (iOS, Android, Web).
- Managed subscription lifecycles via RevenueCat webhooks and delivered story-completion push notifications through Firebase FCM.

---

## PROJECT: benjaminkley

**Name:** 3D Head Scanner & Biometric Analysis Backend
**URL:** https://github.com/kaisarfardin6620/benjaminkley
**Stack:** Django 5 · Celery · trimesh · NumPy · open3d · AWS S3 · PostgreSQL · ReportLab

- Built an async 3D scanning pipeline: ingested 5+ photos, delegated reconstruction to the KeenTools API via Celery workers, and computed biometric measurements (head width, circumference, ear-to-eye) using trimesh geometry algorithms.
- Auto-generated medical-grade PDF reports (ReportLab) containing user details, front image, and full measurement table, saving an estimated (X) hours/week of manual reporting.
- Implemented RBAC with roles (Admin, Doctor, Provider, Client) and an approval workflow; stored 3D assets (.obj / .glb) on AWS S3 with signed URL access.
- Delivered admin dashboard with analytics for user growth and scan volume; push notifications via Firebase FCM kept users informed of scan status changes.

---

## PROJECT: Reho-AI-Service

**Name:** Reho AI Finance Microservice
**URL:** https://github.com/kaisarfardin6620/Reho-AI-Service
**Stack:** FastAPI · OpenAI GPT-4o · MongoDB (Motor async) · Redis · WebSockets · Docker · Nginx

- Engineered a context-aware financial AI assistant that dynamically injects real-time user balance, expense, and debt data into GPT-4o prompts, personalising advice for (N) active users.
- Designed admin intelligence features: spending heatmaps, 360° user health summaries, debt-to-income risk scoring (Low/Medium/High), and anonymised peer spending comparisons.
- Scheduled APScheduler background jobs for nightly pre-computation of heavy analysis reports, cutting average dashboard load time by (X%).
- Cached financial summaries in Redis, reducing MongoDB round-trips and lowering average API response latency by (X ms).

---

## PROJECT: wingman

**Name:** Wingman AI Platform Backend
**URL:** https://github.com/kaisarfardin6620/wingman
**Stack:** Django 5 · DRF · Celery · Redis · WebSockets · PostgreSQL · Docker · Nginx

- Developed a multi-tenant backend with JWT authentication, real-time chat (Django Channels / WebSockets), subscription billing, dashboard analytics, and i18n locale support.
- Containerised with Docker + Nginx; entrypoint script automates migrations, static file collection, and service orchestration for zero-downtime deployments.

---

## PROJECT: Rai_Backend

**Name:** Rai Backend
**URL:** https://github.com/kaisarfardin6620/Rai_Backend
**Stack:** Django 5 · DRF · OpenAI · Google Gemini · Celery · Redis · PostgreSQL · Firebase · Sentry

- Engineered a production-ready AI backend platform featuring JWT/OAuth authentication, community features, subscription billing, and OpenAI-powered chat.
- Integrated Sentry for error tracking and django-prometheus for metrics collection, improving observability across (N) production endpoints.

---

## PROJECT: DELUX_AI

**Name:** DELUX AI Service
**URL:** https://github.com/kaisarfardin6620/DELUX_AI
**Stack:** FastAPI · SQLAlchemy (asyncpg) · PostgreSQL · Redis · OpenAI · Docker · Nginx

- Delivered a standalone async FastAPI microservice with Redis-backed rate limiting, structured JSON logging (python-json-logger), and JWT authentication.
- Integrated OpenAI for AI-driven endpoints; containerised with Docker Compose behind Nginx for one-command production deployment.

---

## PROJECT: maiz-fastapi

**Name:** Maiz FastAPI Service
**URL:** https://github.com/kaisarfardin6620/maiz-fastapi
**Stack:** FastAPI · MongoDB (Motor) · OpenAI · JWT · Pillow

- Developed a lightweight async REST API backed by MongoDB (Motor), featuring JWT auth, image processing (Pillow), and OpenAI integration for AI-driven features.
- Designed Pydantic schemas for strict request/response validation and pydantic-settings for environment-based configuration management.
