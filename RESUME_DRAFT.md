# Kaisar Fardin
**Backend & AI Engineer** | Python · Django · FastAPI · LLM Integration

GitHub: [kaisarfardin6620](https://github.com/kaisarfardin6620) · Email: [your.email@example.com] · LinkedIn: [linkedin.com/in/yourprofile]

---

## Summary

Results-driven Backend & AI Engineer with hands-on experience designing and shipping production-grade Python microservices and AI-integrated platforms. Proven ability to architect asynchronous pipelines, integrate large language models (OpenAI GPT-4o, DALL-E 3), build RAG/Knowledge-Graph systems, and containerise services for cloud deployment. Comfortable owning full backend lifecycles from API design to Docker/Nginx production deployment.

---

## Technical Skills

| Category | Technologies |
|---|---|
| **Languages** | Python |
| **Frameworks** | Django 5, FastAPI, Django REST Framework (DRF) |
| **AI / LLM** | OpenAI API (GPT-4o, DALL-E 3), ElevenLabs TTS, RAG, Vector Search (Pinecone), Knowledge Graphs (Neo4j) |
| **Databases** | PostgreSQL, MongoDB (Motor async), Redis, SQLite, Neo4j |
| **Async / Real-time** | Celery, Redis, WebSockets, Django Channels, Daphne, APScheduler |
| **Auth & Security** | JWT (SimpleJWT), Google OAuth2, Apple Sign-In, OTP/email verification, RBAC |
| **DevOps** | Docker, Docker Compose, Nginx, Gunicorn, Uvicorn, AWS S3 |
| **Computer Vision / 3D** | trimesh, NumPy, OpenCV, MediaPipe, open3d |
| **Monitoring** | Sentry, Prometheus, django-prometheus, Loguru, structlog |
| **Integrations** | Firebase FCM, RevenueCat, Stripe, KeenTools API |

---

## Projects

### [Explainable Hybrid KG-RAG Chatbot](https://github.com/kaisarfardin6620/explainable-rag-chatbot)
*FastAPI · Pinecone · Neo4j · OpenAI GPT-4o · NLI · Python*

- Designed a research-grade hybrid RAG system combining vector search (Pinecone) and Knowledge Graph traversal (Neo4j) to reduce hallucination by (X%) vs. pure-vector baseline.
- Implemented a claim-level NLI verification layer that abstains from answering when confidence drops below a configurable threshold, improving answer trustworthiness by (X%).
- Applied Freeman's Degree Centrality to weight evidence from authoritative graph nodes; supported ablation study modes (`rag_only`, `kg_only`, `hybrid`) for scientific reproducibility.
- Built automated benchmarking pipeline generating F1, Semantic Similarity, and Latency comparison reports across (N) test cases.

### [MagicTale AI Backend](https://github.com/kaisarfardin6620/magictale)
*Django 5 · Celery · Redis · OpenAI GPT-4o · DALL-E 3 · ElevenLabs · WebSockets · PostgreSQL*

- Architected an asynchronous multi-stage AI pipeline (text → image → audio) for a children's storytelling app serving (N) users; reduced perceived wait time via real-time WebSocket progress events.
- Integrated DALL-E 3 for cover illustration and ElevenLabs TTS for per-page narration, stitching audio segments into a single file using pydub.
- Implemented Google OAuth2 and Apple Sign-In alongside JWT authentication, ensuring zero-friction onboarding across iOS, Android, and Web.
- Connected RevenueCat webhook for subscription lifecycle management and Firebase FCM for push notifications on story completion.

### [3D Head Scanner & Biometric Analysis Backend](https://github.com/kaisarfardin6620/benjaminkley)
*Django 5 · Celery · trimesh · NumPy · open3d · AWS S3 · PostgreSQL · ReportLab*

- Built an asynchronous 3D scanning pipeline: ingested 5+ user photos, delegated reconstruction to the KeenTools API via Celery workers, and computed biometric measurements (head width, circumference, ear-to-eye distance) using trimesh geometry algorithms.
- Auto-generated medical-grade PDF reports (ReportLab) containing user details, front image, and full measurement table, reducing manual reporting time by (X hours/week).
- Implemented RBAC with roles (Admin, Doctor, Provider, Client) and an approval workflow; push notifications via Firebase FCM kept users informed of scan status.
- Stored 3D model assets (.obj / .glb) on AWS S3, serving files through signed URLs for secure frontend visualisation.

### [Reho AI Finance Microservice](https://github.com/kaisarfardin6620/Reho-AI-Service)
*FastAPI · OpenAI GPT-4o · MongoDB (Motor async) · Redis · WebSockets · Docker · Nginx*

- Built a context-aware financial AI assistant that injects real-time user balance, expense, and debt data into GPT-4o system prompts before answering queries, delivering personalised advice to (N) users.
- Designed admin intelligence features: spending heatmaps, 360° user summaries, debt-to-income risk scoring, and anonymised peer comparisons.
- Implemented APScheduler background jobs to pre-compute nightly analysis reports, cutting dashboard load time by (X%).
- Cached user financial summaries in Redis, reducing MongoDB round-trips and lowering average API latency by (X ms).

### [Wingman AI Platform Backend](https://github.com/kaisarfardin6620/wingman)
*Django 5 · DRF · Celery · Redis · WebSockets · PostgreSQL · Docker · Nginx*

- Developed a full-featured multi-tenant backend with authentication, real-time chat, subscription management, dashboard analytics, and i18n locale support.
- Containerised with Docker + Nginx; entrypoint script automates migrations, static file collection, and service orchestration.

### [Rai Backend](https://github.com/kaisarfardin6620/Rai_Backend)
*Django 5 · DRF · OpenAI · Google Gemini · Celery · Redis · PostgreSQL · Firebase · Sentry*

- Engineered a production-ready backend platform with JWT/OAuth authentication, community features, subscription billing, and AI-powered chat; monitored with Sentry and django-prometheus.
- Integrated OpenAI and google-genai for intelligent feature enhancements across authentication and dashboard modules.

### [DELUX AI Service](https://github.com/kaisarfardin6620/DELUX_AI)
*FastAPI · SQLAlchemy (asyncpg) · PostgreSQL · Redis · OpenAI · Docker · Nginx*

- Delivered a standalone FastAPI microservice with async PostgreSQL via SQLAlchemy/asyncpg, Redis-backed rate limiting, structured JSON logging, and JWT authentication.
- Containerised with Docker Compose behind Nginx for one-command deployment.

### [Maiz FastAPI Service](https://github.com/kaisarfardin6620/maiz-fastapi)
*FastAPI · MongoDB (Motor) · OpenAI · JWT · Pillow*

- Developed a lightweight async REST service backed by MongoDB, featuring JWT auth, image processing with Pillow, and OpenAI integration for AI-driven functionality.

---

## Education

**[Degree, e.g., B.Sc. in Computer Science]** — [University Name], [Year]

---

*Generated: 2026-04-08 | [Resume generator](resume/generate_resume.py)*
