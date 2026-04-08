# Projects Bullet Bank
> Ready-to-copy ATS-friendly bullet points for each project, sourced directly from repository code and documentation.

---

## Wingman — AI Interview Preparation Platform
*(Django · DRF · Django Channels · Celery · Redis · PostgreSQL · OpenAI · Docker · Nginx)*

- Engineered a real-time AI interview coaching platform using Django Channels (WebSockets) for sub-second interactive feedback during mock interviews.
- Designed asynchronous AI task pipelines with Celery chains and Redis broker, enabling concurrent session handling without blocking the main thread.
- Implemented JWT-based authentication (djangorestframework-simplejwt) with tiered subscription access control and role-based permissions.
- Containerised the complete stack (Django + Celery + Redis + PostgreSQL + Nginx) using Docker Compose for repeatable one-command deployments.
- Integrated OpenAI GPT for dynamic question generation, candidate answer evaluation, and personalised coaching recommendations.
- Implemented Celery Beat for scheduled tasks (session cleanup, report generation) and Daphne as the ASGI server for WebSocket support.

---

## Explainable Hybrid KG-RAG Chatbot — Research Project
*(FastAPI · Pinecone · Neo4j · OpenAI GPT-4o · Python 3.10+ · NLI · SQLite)*

- Architected a Hybrid Retrieval-Augmented Generation (RAG) system combining Pinecone vector search with Neo4j knowledge graph reasoning for multi-hop QA.
- Reduced hallucinations by 30%+ through an NLI post-hoc verification layer that cross-checks every LLM claim against retrieved source evidence.
- Applied Freeman's Degree Centrality algorithm to rank evidence by node authority in the knowledge graph, improving answer precision.
- Built ablation-ready retrieval modes (`rag_only`, `kg_only`, `hybrid`) with automated benchmarking scripts producing F1 score, semantic similarity, and latency reports.
- Engineered automatic Knowledge Graph construction from raw PDFs using LLM-based entity and relationship extraction during document ingestion.
- Created a configurable Refusal Mechanism that abstains from answering when confidence score drops below threshold (0.4), prioritising accuracy over coverage.
- Source for paper: *"Hybrid Knowledge Graph–Guided Explainable RAG for Trustworthy QA"* (In Preparation).

---

## Reho AI Finance Microservice
*(FastAPI · OpenAI GPT-4o · MongoDB Motor · Redis · WebSockets · APScheduler · Docker · Nginx)*

- Built an async AI microservice sharing a MongoDB Atlas database with a Node.js main backend, providing context-aware financial intelligence without data duplication.
- Delivered real-time AI financial chat via WebSockets, injecting live user data (balances, debts, income categories) into the LLM system prompt at query time.
- Developed admin dashboard intelligence module with GPT-4o–powered risk scoring (Low/Medium/High), spending heatmaps, and anonymised peer benchmarks.
- Implemented 50/30/20 budget analysis and Avalanche vs. Snowball debt strategy comparison specific to each user's actual loan portfolio.
- Designed nightly scheduled jobs (APScheduler) to pre-compute analytics reports, reducing dashboard average load time.
- Secured all endpoints with JWT (HS256) validated against the shared main backend secret; Sentry SDK integrated for production error tracking.

---

## Bondly AI — Emotionally Intelligent Financial Coach
*(Python · OpenAI GPT-4o · Prompt Engineering)*

- Designed a mood-aware GPT-4o financial coach that adapts tone (empathetic vs. direct) and advice depth based on detected emotional context and relationship status.
- Implemented micro-consent protocols before discussing sensitive topics (investments, debt restructuring), improving user trust and engagement.
- Built dynamic multi-turn conversation memory to maintain financial context across sessions without user repetition.

---

## Magictale — AI Storytelling Platform
*(Django · DRF · Django Channels · Celery · OpenAI · PostgreSQL · Redis · Firebase · Docker · Nginx)*

- Developed an AI storytelling SaaS with GPT-4o–driven narrative generation, subscription billing, and push notification delivery (Firebase Admin SDK).
- Designed fully documented OpenAPI/Swagger schema (drf-spectacular) covering 40+ endpoints for authentication, subscriptions, story management, and support.
- Architected multi-turn narrative context management enabling coherent story continuation across multiple chapters and user sessions.

---

## DELUX AI — Multi-Modal GenAI API
*(FastAPI · OpenAI GPT-4o · DALL-E 3 · ElevenLabs · PostgreSQL · Redis · Docker · Nginx)*

- Built a production multi-modal AI API orchestrating Text → Image → Audio content workflows using GPT-4o, DALL-E 3, and ElevenLabs APIs.
- Implemented Redis-backed token-bucket rate limiting and fault-tolerant retry logic with exponential back-off for all third-party API calls.
- Deployed behind Nginx reverse proxy using Docker Compose with structured JSON logging via loguru.

---

## maiz-fastapi — AI Image & Content API
*(FastAPI · MongoDB Motor · OpenAI · Pillow · python-jose · Python)*

- Developed an async FastAPI microservice for AI-driven content generation with MongoDB Atlas as the primary datastore using Motor async driver.
- Integrated Pillow for server-side image preprocessing and transformation before submission to OpenAI vision models.
- Secured endpoints with JWT authentication using python-jose[cryptography].

---

## HR AI Assistant Suite (6 Modules)
*(Python · OpenAI GPT-4 · News API · REST)*

- Engineered six domain-specific HR AI assistants: Talent Acquisition, Compliance, Compensation, HR Strategy, Learning & Development, and Organisational Development.
- Designed specialised system prompts with role-specific guardrails and scenario templates for HR professional use cases.
- Integrated live Google News feed to give Compliance and HR Strategy assistants real-time awareness of regulatory changes and industry news.

---

## Bangladeshi Medicinal Leaf Classification
*(Python · TensorFlow/Keras · CNN · OpenCV · Jupyter Notebook)*

- Built and trained a multi-class CNN image classifier identifying 10+ Bangladeshi medicinal plant species from leaf photographs.
- Applied data augmentation (rotation, flipping, brightness, zoom) to combat class imbalance, improving model generalisation on a limited domain dataset.
- Achieved high validation accuracy through transfer learning exploration and systematic hyperparameter tuning.

---

## NLP & ML Research Portfolio
*(Python · scikit-learn · TensorFlow/Keras · PyTorch · NLTK · Word2Vec · Jupyter Notebook)*

| Project | Technique | Outcome |
|---|---|---|
| Customer Churn Prediction | Logistic Regression, Random Forest, XGBoost | End-to-end churn pipeline with feature importance |
| Sales Forecasting Regression | Linear Regression, Gradient Boosting | Time-series-aware regression with RMSE evaluation |
| Spam Classification | Word2Vec / GloVe embeddings + ML | NLP-based text classifier with embedding visualisation |
| Real vs. Fake News Classifier | TF-IDF + ML classifiers | Binary NLP classifier on news authenticity |
| Fashion-MNIST Semi-supervised | Self-training + CNN | Semi-supervised learning with limited labelled data |
| Lung Cancer Prediction | SVM, Random Forest, clinical features | Binary classification with clinical feature engineering |
| Weather Rainfall Prediction | Regression models | Multi-feature meteorological forecasting |
| LSTM IMDb Sentiment Analysis | LSTM, Embedding layer | Sequential sentiment model on movie reviews |
| Autoencoder Anomaly Detection | Undercomplete Autoencoder | Unsupervised anomaly detection with reconstruction error |
