# Abdullah Kaisar Fardin

**Email:** [YOUR_EMAIL@example.com]
**Phone:** [YOUR_PHONE_NUMBER]
**LinkedIn:** [YOUR_LINKEDIN_URL]
**GitHub:** https://github.com/kaisarfardin6620
**Location:** Dhaka, Bangladesh

---
## SUMMARY

AI Engineer with approximately 1 year of hands-on experience designing and deploying
intelligent backend systems, LLM integrations, and machine learning pipelines.
Proven ability to build production-grade AI microservices (FastAPI, Django),
implement Retrieval-Augmented Generation (RAG) architectures, and apply deep learning
across computer vision and NLP tasks. Currently pursuing an M.Sc. degree while
contributing to research-oriented AI projects. Passionate about explainable, scalable,
and trustworthy AI systems.

---

## SKILLS

**Programming Languages:** Python, SQL

**AI / Machine Learning:** Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Knowledge Graphs, Natural Language Processing (NLP), Computer Vision, CNN, Transfer Learning, Autoencoders, Anomaly Detection, Sentiment Analysis, Text Classification, LSTM, Siamese Networks

**Frameworks & Libraries:** FastAPI, Django, Django REST Framework (DRF), TensorFlow, Keras, scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, NLTK, sentence-transformers (SBERT), XGBoost, Celery

**AI / LLM APIs:** OpenAI API (GPT-4o, DALL-E 3), ElevenLabs Text-to-Speech, Firebase Cloud Messaging

**Databases:** PostgreSQL, MongoDB, Redis, Neo4j (Graph Database), Pinecone (Vector Database), SQLite

**DevOps & Infrastructure:** Docker, Docker Compose, Nginx, Git, GitHub, WebSockets, Uvicorn, Gunicorn, Daphne

**Other Tools:** Swagger / OpenAPI, Jupyter Notebook, Google Colab, Postman

---
## PROJECTS

### Explainable Hybrid KG-RAG Chatbot
**Tech Stack:** Python, FastAPI, OpenAI GPT-4o, Pinecone, Neo4j, NLI
**GitHub:** https://github.com/kaisarfardin6620/explainable-rag-chatbot

- Built a hybrid RAG system combining vector search (Pinecone) and knowledge graph reasoning (Neo4j) to reduce LLM hallucinations.
- Implemented automatic KG construction from PDFs using LLM-based entity and relationship extraction.
- Designed a post-hoc NLI claim-verification layer with a confidence-based refusal mechanism.
- Applied Freeman's Degree Centrality to weight evidence from authoritative graph nodes.
- Built ablation-ready modes (rag_only, kg_only, hybrid); associated with research paper 'Hybrid KG-Guided Explainable RAG for Trustworthy QA'.

### MagicTale AI Backend
**Tech Stack:** Python, Django 5, DRF, Celery, Redis, WebSockets, PostgreSQL, OpenAI GPT-4o, DALL-E 3, ElevenLabs, Firebase, Docker
**GitHub:** https://github.com/kaisarfardin6620/magictale

- Engineered a production-grade async AI storytelling platform integrating GPT-4o (text), DALL-E 3 (images), and ElevenLabs (audio) in a 3-stage pipeline.
- Delivered real-time story generation progress via Django Channels WebSockets.
- Integrated Google OAuth2, Apple Sign-In, and JWT with Pwned Passwords API validation.
- Automated FCM push notifications on story completion; managed subscriptions via RevenueCat webhooks.
- Deployed with Docker Compose, Nginx, Celery workers, and Daphne ASGI server.

### Reho AI Finance Microservice
**Tech Stack:** Python, FastAPI, OpenAI GPT-4o, MongoDB, Redis, WebSockets, Docker
**GitHub:** https://github.com/kaisarfardin6620/Reho-AI-Service

- Developed an AI intelligence layer for a finance management system with real-time WebSocket chat powered by GPT-4o.
- Built dynamic context injection fetching live user financial data (income, expenses, debts) before each LLM response.
- Designed admin dashboard with AI user summaries, spending heatmaps, debt-to-income risk assessment, and anonymized peer comparisons.
- Implemented nightly pre-computation of heavy analytics via scheduled background jobs to minimize dashboard load times.

### Wingman AI Backend
**Tech Stack:** Python, Django 5, DRF, Celery, Redis, PostgreSQL, OpenAI, WebSockets, Docker, Nginx
**GitHub:** https://github.com/kaisarfardin6620/wingman

- Built a scalable Django backend with AI-powered real-time chat, JWT authentication, and subscription management.
- Integrated Celery + Redis for async task processing and Django Channels for WebSocket communication.
- Deployed via Docker Compose with Nginx for production-ready static file handling and CORS management.

### HR AI Assistant Suite
**Tech Stack:** Python, OpenAI GPT API
**GitHub:** https://github.com/kaisarfardin6620/Hr-Ai-Assistant

- Built 8 modular domain-specific AI assistants (Compensation, Compliance, Talent Acquisition, Organizational Development, etc.) using OpenAI GPT.
- Implemented per-user conversation history, input sanitization, caching, and structured logging for production use.
- Designed for seamless integration with Flask or FastAPI REST APIs.

### Customer Churn Prediction
**Tech Stack:** Python, scikit-learn, XGBoost, TensorFlow/Keras, Pandas, Seaborn, SMOTE
**GitHub:** https://github.com/kaisarfardin6620/Customer-Churn-Prediction

- Trained and compared 12+ ML models (Logistic Regression, Random Forest, XGBoost, SVM, Gradient Boosting, Voting/Stacking Classifiers, ANN) for bank churn prediction.
- Applied SMOTE for class imbalance; performed hyperparameter tuning with GridSearchCV and StratifiedKFold cross-validation.
- Evaluated with ROC-AUC, Precision, Recall, F1-Score, and Confusion Matrices; visualized with Plotly and Seaborn.

### Lung Cancer Chest X-Ray Classification
**Tech Stack:** Python, TensorFlow/Keras, CNN, VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0
**GitHub:** https://github.com/kaisarfardin6620/LungCancer-ImageNet

- Built a multi-class chest X-ray classifier distinguishing adenocarcinoma, large cell carcinoma, squamous cell carcinoma, and normal cases.
- Applied two-stage transfer learning fine-tuning across 5 architectures with automatic class weight balancing and data augmentation.

### Additional Machine Learning and Deep Learning Projects
**GitHub:** https://github.com/kaisarfardin6620

- Bangladeshi Medicinal Leaf Classification — CNN transfer learning (VGG16, ResNet50, etc.) for medicinal plant identification.
- NLP Twitter Sentiment Analysis — SVM, Random Forest, ANN with TF-IDF and SMOTE.
- Quora Question Pair Classification — SBERT embeddings with ANN, LSTM, and Siamese Networks.
- Autoencoder Anomaly Detection / AppleNet-AE — VAE, denoising autoencoder, t-SNE, One-Class SVM.
- Real vs. Fake News Classifier — NLP misinformation detection pipeline.
- LSTM for IMDb Sentiment Analysis — Sequence classification with LSTM.
- Sales Forecasting Regression — End-to-end regression pipeline for business forecasting.
- AI Image Creator (Glimmcatcher) — DALL-E powered image generation CLI tool.
- Bondly AI Financial Assistant, Bible AI Assistant — Domain-specific GPT-powered conversational assistants.
- Other classifiers: Marine Life, Butterfly, Shoe, FlowerNet, Fashion-MNIST (supervised/semi-supervised), Breast Cancer Survival, Wine Quality, Weather Forecasting, Cat vs. Dog.

---
## EDUCATION

**Master of Science (M.Sc.) — [Your Field of Study]** *(In Progress)*
[University Name], Dhaka, Bangladesh
Expected Graduation: [Year]

**Bachelor of Science (B.Sc.) — [Your Field of Study]** *(Completed)*
[University Name], Dhaka, Bangladesh
Graduated: [Year]

---
## EXPERIENCE

**[FILL: Job Title / Internship Title]**
[FILL: Company Name], [FILL: City, Country / Remote]
[FILL: Month Year, e.g., Jan 2024] – [FILL: Month Year or Present]

- [FILL: Describe your primary responsibility and impact here.]
- [FILL: Mention tools, technologies, or frameworks used.]
- [FILL: Quantify impact where possible, e.g., 'Improved accuracy by X%'.]

> Note: Replace the placeholders above with your actual experience, or remove this section if you have no formal employment yet.

---
*Last updated: April 2026 | GitHub: kaisarfardin6620*
