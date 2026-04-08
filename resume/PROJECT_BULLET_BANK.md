# Project Bullet Bank
<!-- ================================================================
  HOW TO USE THIS FILE
  --------------------
  Each project block has multiple bullet options.
  - Pick 2–3 bullets per project for your resume.
  - Prefer bullets that quantify impact or highlight AI engineering.
  - To add a NEW project, copy the template at the bottom of this
    file and fill in the details. Then re-run generate_resume.py.
================================================================ -->

---

## 1. Explainable Hybrid KG-RAG Chatbot
**Repo:** https://github.com/kaisarfardin6620/explainable-rag-chatbot  
**Stack:** Python, FastAPI, OpenAI GPT-4o, Pinecone (Vector DB), Neo4j (Knowledge Graph), SQLite, NLI

**Bullets (pick 2–3):**
- Designed and implemented a research-grade Hybrid RAG system combining Pinecone vector search with Neo4j knowledge-graph traversal to reduce LLM hallucinations and provide claim-level explainability.
- Built a post-hoc Natural Language Inference (NLI) verification layer that abstains from answering when confidence scores fall below 0.4, improving answer trustworthiness.
- Automated knowledge-graph construction from raw PDFs using LLM-based entity and relationship extraction, enabling zero-manual-annotation ingestion.
- Applied Freeman's Degree Centrality to weight evidence from authoritative graph entities, boosting retrieval precision in multi-hop reasoning tasks.
- Architected three ablation modes (`hybrid`, `rag_only`, `kg_only`) and a benchmark automation script that generates comparative F1, semantic similarity, and latency reports — supporting the paper *"Hybrid Knowledge Graph–Guided Explainable RAG for Trustworthy QA"*.
- Delivered a FastAPI REST API with Swagger docs, session-based chat history, and structured reasoning-chain citations in every response.

---

## 2. MagicTale — AI Storytelling Platform Backend
**Repo:** https://github.com/kaisarfardin6620/magictale  
**Stack:** Python, Django 5, DRF, Celery, Redis, PostgreSQL, OpenAI GPT-4o, DALL-E 3, ElevenLabs, Firebase FCM, Docker, WebSockets

**Bullets (pick 2–3):**
- Engineered an asynchronous AI content pipeline (Celery + Redis) that generates personalized children's stories (GPT-4o), cover illustrations (DALL-E 3), and voice narration (ElevenLabs TTS) without blocking the HTTP layer.
- Implemented real-time story-generation progress updates over Django Channels WebSockets, streaming status events (`progress`, `message`) to connected clients.
- Integrated Google OAuth2 and Apple Sign-In alongside email/password JWT auth, and registered FCM device tokens for push notifications on story completion.
- Wired RevenueCat webhook listener for in-app subscription lifecycle management, syncing entitlement states to a PostgreSQL database.
- Containerized the full stack (Django/Daphne + Celery worker + Redis + PostgreSQL + Nginx) with Docker Compose; exposed auto-generated OpenAPI 3.0 docs via drf-spectacular.

---

## 3. Reho AI Finance Microservice
**Repo:** https://github.com/kaisarfardin6620/Reho-AI-Service  
**Stack:** Python, FastAPI, OpenAI GPT-4o, MongoDB (Motor async), Redis, Docker, Nginx

**Bullets (pick 2–3):**
- Built an AI microservice that injects live user financial data (incomes, expenses, debts) into the GPT-4o system prompt at runtime, enabling context-aware conversational financial advice via real-time WebSockets.
- Developed admin intelligence endpoints that auto-generate user 360 summaries, spending heatmaps, debt-to-income risk scores (Low/Medium/High), and anonymized peer-comparison insights using GPT-4o.
- Implemented a 50/30/20 budget analyzer, Avalanche vs. Snowball debt-strategy comparator, and subscription-audit detector to surface actionable optimization tips.
- Architected a scheduled background job system that pre-computes heavy analytics reports nightly (FastAPI background tasks + Redis caching), reducing dashboard load times.
- Deployed behind Nginx using Docker Compose; exposed full Swagger UI and ReDoc documentation.

---

## 4. Wingman — AI Assistant Backend
**Repo:** https://github.com/kaisarfardin6620/wingman  
**Stack:** Python, Django 5, DRF, Celery, Redis, OpenAI, Channels (WebSockets), PostgreSQL, Docker

**Bullets (pick 2–3):**
- Developed a full-featured Django REST API backend powering an AI chat assistant, with JWT-secured endpoints, real-time WebSocket chat (Django Channels), and subscription tier management.
- Integrated OpenAI and Google GenAI (Gemini) APIs to serve multi-modal AI responses; implemented token-counting with tiktoken for accurate usage billing.
- Built an async task pipeline with Celery + Redis for background AI processing; containerized services (Django/Daphne + Celery + Nginx + Redis) with Docker Compose.

---

## 5. Benjaminkley — 3D Head Scanner & Biometric Analysis
**Repo:** https://github.com/kaisarfardin6620/benjaminkley  
**Stack:** Python, Django 5, DRF, Celery, Redis, PostgreSQL, trimesh, numpy, KeenTools API, AWS S3, Firebase FCM, Docker

**Bullets (pick 2–3):**
- Designed an end-to-end 3D scanning pipeline: uploads multi-image datasets to KeenTools API for 3D reconstruction, downloads the resulting `.obj` mesh, and automatically calculates biometric measurements (head width, circumference, ear-to-ear, eye-to-eye) using trimesh and numpy.
- Implemented asynchronous scan processing with Celery and Redis so heavy 3D computation does not block the API; triggered PDF report generation and FCM push notifications on completion.
- Built a role-based access control system (Admin, Doctor, Provider, Client) with email OTP verification, approval workflow, and JWT authentication.
- Served generated `.obj`/`.glb` 3D models and auto-generated biometric PDF reports via secured API endpoints; stored media files on AWS S3.

---

## 6. Rai Backend — AI Community Platform
**Repo:** https://github.com/kaisarfardin6620/Rai_Backend  
**Stack:** Python, Django 5, DRF, Celery, Channels (WebSockets), Redis, OpenAI, Google GenAI, PostgreSQL, Docker

**Bullets (pick 2–3):**
- Built a scalable Django REST API backend integrating OpenAI and Google GenAI for an AI-powered community platform, with JWT authentication, subscription management, and real-time chat via Django Channels.
- Implemented asynchronous task handling (Celery + Redis) for background AI inference and notification delivery; used Django Anymail for transactional email and Daphne as the ASGI server.

---

## 7. DELUX_AI — FastAPI AI Service
**Repo:** https://github.com/kaisarfardin6620/DELUX_AI  
**Stack:** Python, FastAPI, PostgreSQL (asyncpg), OpenAI, Redis, JWT, Docker

**Bullets (pick 2–3):**
- Engineered a high-performance async FastAPI service with PostgreSQL (asyncpg), per-user rate limiting (Redis), structured JSON logging, and JWT-based authentication.
- Integrated OpenAI API for AI inference endpoints; containerized the service with Docker and Docker Compose.

---

## 8. Maiz FastAPI — AI Service
**Repo:** https://github.com/kaisarfardin6620/maiz-fastapi  
**Stack:** Python, FastAPI, MongoDB (Motor async), OpenAI, JWT, Docker

**Bullets (pick 2–3):**
- Developed an async FastAPI microservice backed by MongoDB (Motor) and OpenAI for AI-driven features, secured with JWT authentication and Pydantic data validation.

---

<!-- ================================================================
  TEMPLATE FOR A NEW PROJECT
  ---------------------------
  Copy this block and fill in your details, then re-run
  generate_resume.py to rebuild the resume with the new project.

## N. Project Name
**Repo:** https://github.com/kaisarfardin6620/<repo-name>
**Stack:** Language, Framework, AI library, Database, …

**Bullets (pick 2–3):**
- [Action verb] [what you built] using [key tech], achieving [impact/metric].
- [Action verb] [key technical challenge solved] with [approach], resulting in [outcome].
- [Action verb] [deployment/infra/testing detail] to [goal].

================================================================ -->
