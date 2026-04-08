# Abdullah Kaisar Fardin

**AI Systems Engineer | Backend Architect | MSc Data Science Candidate**

📧 kaisarfardin128@gmail.com
🌐 [Portfolio](https://kaisarfardin6620.github.io) | [GitHub](https://github.com/kaisarfardin6620) | [LinkedIn](https://www.linkedin.com/in/abdullah-kaisar-fardin)

---

## Professional Summary

Results-driven AI Systems Engineer specialising in production-grade AI backends, scalable microservices, and applied machine learning. Proven track record of architecting asynchronous RAG pipelines, real-time WebSocket systems, and multi-modal GenAI applications using FastAPI, Django, Celery, and Redis. Currently pursuing an MSc in Data Science, bridging advanced ML research with deployment-ready engineering. Passionate about making AI reliable, explainable, and production-ready.

---

## Technical Skills

### Languages
- Python, SQL

### AI / Machine Learning
- OpenAI API (GPT-4o, GPT-4, DALL-E 3), Retrieval-Augmented Generation (RAG), Hybrid KG-RAG, Prompt Engineering
- PyTorch, TensorFlow/Keras, Hugging Face Transformers, scikit-learn
- Natural Language Inference (NLI), Hallucination Mitigation, Explainable AI (XAI)
- Convolutional Neural Networks (CNN), ResNet, VGG, EfficientNet, LSTM, Autoencoders
- Sentiment Analysis, Text Classification, Semi-supervised Learning, Anomaly Detection

### Backend Frameworks
- Django, Django REST Framework (DRF), FastAPI (async), Django Channels (WebSockets)
- Celery (Chains/Groups), APScheduler, Celery Beat, Daphne, Uvicorn, Gunicorn

### Databases & Storage
- PostgreSQL, MongoDB (Motor async driver), Redis, SQLite, Neo4j (Knowledge Graph)
- Pinecone (Vector DB), AWS S3 (boto3), Firebase Admin SDK

### DevOps / Deployment
- Docker, Docker Compose, Nginx (reverse proxy), Linux

### Libraries & Tools
- Pydantic, PyJWT, djangorestframework-simplejwt, python-dotenv, tiktoken
- Pillow (image processing), OpenCV, MediaPipe
- Sentry SDK, structlog, loguru, django-prometheus
- drf-spectacular (OpenAPI/Swagger), django-allauth, django-filter

---

## Projects

### 1. Wingman — AI-Powered Interview Preparation Platform
**Tech:** Django, DRF, Django Channels, Celery, Redis, PostgreSQL, OpenAI, Docker, Nginx, JWT
- Engineered a full-stack AI interview-coaching platform with real-time chat via Django Channels (WebSockets).
- Designed asynchronous AI task orchestration using Celery chains and Redis as a message broker, enabling non-blocking response generation under high concurrency.
- Implemented a subscription management module with tiered access control and JWT-based authentication using djangorestframework-simplejwt.
- Containerised the full stack (Django + Celery + Redis + PostgreSQL) using Docker Compose behind an Nginx reverse proxy for production deployment.
- Integrated OpenAI GPT for dynamic question generation, answer evaluation, and personalised coaching feedback.

---

### 2. Explainable Hybrid KG-RAG Chatbot *(Research Project)*
**Tech:** FastAPI, Python 3.10+, Pinecone, Neo4j, OpenAI GPT-4o, SQLite, Uvicorn
- Architected a research-grade Hybrid RAG system merging vector retrieval (Pinecone) with Knowledge Graph reasoning (Neo4j) to support multi-hop logical inference and reduce hallucinations.
- Implemented a post-hoc NLI verification layer that checks every generated claim against retrieved evidence, with a configurable confidence threshold (0.4) for refusal.
- Applied Freeman's Degree Centrality to weight evidence from authoritative knowledge graph nodes, improving answer reliability.
- Built three interchangeable retrieval modes (`rag_only`, `kg_only`, `hybrid`) and automated benchmark scripts for ablation studies reporting F1 score, semantic similarity, and latency.
- Source code supports the paper: *"Hybrid Knowledge Graph–Guided Explainable RAG for Trustworthy QA"* (In Preparation).

---

### 3. Reho AI Finance Microservice
**Tech:** FastAPI, OpenAI GPT-4o, MongoDB (Motor), Redis, WebSockets, Docker, Nginx, APScheduler
- Built a standalone AI microservice that shares a MongoDB Atlas database with a Node.js main backend, enabling context-aware financial advice without duplicating user data.
- Implemented real-time financial chat over WebSockets with dynamic context injection (balances, debts, income) into the LLM system prompt per request.
- Developed an admin intelligence module generating risk assessments (Low/Medium/High based on debt-to-income ratios), spending heatmaps, and anonymised peer comparisons using GPT-4o.
- Created a 50/30/20 budget analysis feature comparing Avalanche vs. Snowball debt strategies specific to each user's loan portfolio.
- Scheduled nightly background analysis jobs (APScheduler) to pre-compute heavy reports, reducing dashboard load time.

---

### 4. Bondly AI — Emotionally Intelligent Financial Coach
**Tech:** Python, OpenAI GPT-4o
- Designed a GPT-4o-powered financial coaching assistant that adapts its tone and advice based on detected user mood and relationship status.
- Implemented micro-consent mechanisms for sensitive financial topics (investments, debt) and milestone celebration prompts to improve user engagement.
- Built dynamic context tracking across conversation turns, enabling natural follow-up question handling without user repetition.

---

### 5. Magictale — AI Storytelling Platform
**Tech:** Django, DRF, Django Channels, Celery, OpenAI, PostgreSQL, Redis, Firebase, Docker, Nginx
- Developed an AI-powered story generation platform with subscription tiers, push notification support (Firebase Admin SDK), and real-time story streaming.
- Designed a fully documented REST API (drf-spectacular / OpenAPI schema) covering authentication, subscription management, AI story endpoints, and support ticketing.
- Architected the AI module for multi-turn narrative generation using GPT-4o with contextual memory across story chapters.

---

### 6. DELUX AI — Multi-Modal GenAI API
**Tech:** FastAPI, OpenAI (GPT-4o, DALL-E 3), PostgreSQL, Redis, Docker, Nginx
- Built a production-grade multi-modal API that orchestrates Text-to-Image-to-Audio workflows using GPT-4o, DALL-E 3, and ElevenLabs.
- Implemented rate-limiting middleware (Redis-backed), structured JSON logging, and fault-tolerant retry mechanisms for third-party API calls.
- Deployed with Docker Compose behind Nginx with JWT-secured endpoints.

---

### 7. maiz-fastapi — AI Image & Content API
**Tech:** FastAPI, MongoDB (Motor), OpenAI, JWT, Pillow, Python
- Developed an asynchronous FastAPI service for AI-driven content generation with MongoDB Atlas as the primary datastore.
- Integrated Pillow for server-side image preprocessing and transformation before passing to OpenAI vision models.
- Implemented secure JWT authentication using python-jose.

---

### 8. HR AI Assistant Suite
**Tech:** Python, OpenAI GPT-4, News API, REST
- Built a suite of six specialised HR AI assistants: Talent Acquisition, Compliance, Compensation, HR Strategy, Learning & Development, and Organisational Development.
- Each assistant uses purpose-engineered system prompts with domain-specific guardrails, enabling accurate role-play scenarios for HR professionals.
- Integrated a live Google News feed module to provide HR assistants with real-time compliance updates and industry news.

---

### 9. Bangladeshi Medicinal Leaf Classification *(Computer Vision)*
**Tech:** Python, TensorFlow/Keras, CNN, Jupyter Notebook
- Built and trained a CNN-based multi-class image classifier to identify Bangladeshi medicinal plant species from leaf images.
- Applied data augmentation (rotation, flipping, brightness adjustment) to address class imbalance and improve generalisation on limited domain data.

---

### 10. NLP & ML Research Projects
**Projects:** Customer Churn Prediction, Sales Forecasting Regression, Spam Classification (Word Embeddings), Real vs. Fake News Classifier, Fashion-MNIST Semi-supervised Learning, Lung Cancer Prediction, Weather Rainfall Prediction, LSTM IMDb Sentiment Analysis, Autoencoder Anomaly Detection
- Developed end-to-end ML pipelines covering EDA, feature engineering, model training, and evaluation across classification, regression, and NLP tasks.
- Applied advanced architectures including LSTMs for sequential sentiment modelling, Autoencoders for unsupervised anomaly detection, and semi-supervised learning on Fashion-MNIST with limited labelled data.
- Demonstrated proficiency with scikit-learn, TensorFlow/Keras, and PyTorch across structured and unstructured data domains.

---

## Education

**MSc Data Science** *(Ongoing)*
_University — To be added_

**BSc Computer Science / Related Degree**
_University — To be added_

---

## Contact & Links

| | |
|---|---|
| **Email** | kaisarfardin128@gmail.com |
| **GitHub** | https://github.com/kaisarfardin6620 |
| **LinkedIn** | https://www.linkedin.com/in/abdullah-kaisar-fardin |
| **Portfolio** | https://kaisarfardin6620.github.io |

---

> *This resume draft was generated from a full scan of all GitHub repositories. Please fill in your university name(s), graduation year(s), and any work experience or internship details before submitting applications.*
