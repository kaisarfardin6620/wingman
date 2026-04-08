# Technical Skills

> **Evidence-based extraction** — all skills below are sourced directly from
> `requirements.txt`, `Dockerfile`, `docker-compose.yml`, source-code imports,
> and `README.md` files across the following repositories:
> `wingman` · `Rai_Backend` · `Reho-AI-Service` · `explainable-rag-chatbot` ·
> `magictale` · `benjaminkley` · `maiz-fastapi` · `DELUX_AI` · `AppleNet-AE` ·
> `Fashion-Mnist-Sup-Semisup` · `LungCancer-ImageNet` · `Ai-Image-Creator-Glimmcatcher` ·
> `Hr-Ai-Assistant` · `Bondly-Ai_Financial-Assistant` · `Bible-Ai-Assistant` ·
> `Customer-Churn-Prediction` · `LeafDiseaseClassifier` · `Weather_Forecasting_Models` ·
> `Butterfly-Classifier` · `Cnn_Preprocessings` · `Cnn_Visuals` · `Marine_Life_Classifier` ·
> `Shoe_Classifier` · `FlowerNet-Comparison` · `Wine-Quality-Testing-` ·
> `Lung-Cancer-Prediction-using-Machine-Learning.` ·
> `Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning` ·
> `Breast-Cancer-Survival-Prediction-using-Machine-Learning.` ·
> `Bangladeshi-Medicinal-Leaf-Classification` · `Text-Pair-Classification` ·
> `NLP-based-Twitter-Sentiment-Analysis` · `Real-vs.-Fake-News-Classifier` ·
> `NLP-Based-Spam-Classification-with-Word-Embeddings` · `LSTM-for-IMDb-Sentiment-Analysis` ·
> `Sales-Forecasting-Regression` · `Weather-rainfall-prediction` ·
> `Cat-Vs-Dog-Classification` · `Autoencoder-Anomaly-Detection`

---

## Programming Languages
- **Python** (primary language across all repositories — backend services, ML/DL models, data science notebooks)
- **SQL** (via PostgreSQL, SQLAlchemy ORM, raw queries in Django/FastAPI backends)

---

## Web & API Frameworks
- **Django** (≥5.0) — REST APIs, async/ASGI applications, ORM, admin, middleware
- **Django REST Framework (DRF)** — serializers, viewsets, routers, JWT auth, filtering, OpenAPI spec (drf-spectacular)
- **FastAPI** — async REST APIs, dependency injection, Pydantic validation, OAuth2/JWT
- **Daphne / ASGI** — async server gateway interface for WebSocket and HTTP/2 support
- **Gunicorn + Uvicorn** — production WSGI/ASGI multi-worker deployment
- **Django Channels** — WebSocket & real-time messaging (channels-redis backend)
- **Starlette** — underlying ASGI toolkit used with FastAPI

---

## AI / Machine Learning
- **OpenAI API** (GPT-4, DALL·E, Whisper) — chat completions, image generation, speech-to-text, streaming responses
- **LangChain / RAG pipelines** — retrieval-augmented generation with vector stores and LLM chains (explainable-rag-chatbot)
- **Pinecone** — managed vector database for semantic search / RAG
- **Sentence Transformers (SBERT)** — semantic sentence embeddings for question-pair classification and similarity tasks
- **tiktoken** — token counting for OpenAI prompt management
- **ElevenLabs** — text-to-speech synthesis (magictale)
- **Google Generative AI (google-genai)** — Gemini model integration (Rai_Backend)

---

## Deep Learning
- **TensorFlow 2.x / Keras** — CNN, RNN/LSTM, Autoencoder, VAE, transfer learning; `tf.data`, `ImageDataGenerator`, TensorBoard callbacks
- **Transfer Learning Models** — VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0/V2 (fine-tuning & feature extraction)
- **Custom CNN architectures** — classification, image reconstruction, anomaly detection, inpainting
- **LSTM / GRU** — sequence modeling for sentiment analysis (IMDb) and NLP tasks
- **Siamese Networks** — text-pair similarity (Quora question-pair classification)
- **Variational Autoencoders (VAE)** — latent-space learning and image generation (AppleNet-AE)
- **t-SNE** — latent-space and high-dimensional feature visualization

---

## Classical Machine Learning & Data Science
- **Scikit-learn** — Logistic Regression, Random Forest, SVM, KNN, Decision Tree, SVR, K-Means, One-Class SVM, cross-validation, `GridSearchCV`, pipelines, `StandardScaler`, `LabelEncoder`
- **XGBoost** — gradient-boosted trees for classification tasks
- **PyCaret** — automated ML workflows for regression and classification
- **Pandas / NumPy** — data wrangling, feature engineering, time-series processing
- **Matplotlib / Seaborn** — EDA, confusion matrices, ROC curves, training history plots
- **SMOTE (imbalanced-learn)** — synthetic minority over-sampling for imbalanced datasets
- **SciPy** — statistical computations and signal processing

---

## Natural Language Processing (NLP)
- **NLTK** — tokenization, stop-word removal, lemmatization, stemming
- **TF-IDF (Scikit-learn)** — text vectorization for classification tasks
- **Gensim** — Word2Vec, FastText, GloVe pretrained word embeddings for spam/text classification
- **Wordcloud** — text frequency visualization
- **Sentence Transformers / SBERT** — semantic search and duplicate detection

---

## Databases
- **PostgreSQL** — primary relational database (production, wingman / Rai_Backend / DELUX_AI)
- **PgBouncer** — connection pooling for PostgreSQL at scale
- **MongoDB** — NoSQL document store (Reho-AI-Service, maiz-fastapi via `motor` async driver, `pymongo`)
- **Redis** — caching, session storage, Celery broker, pub/sub (redis-py, django-redis, channels-redis)
- **SQLite** — lightweight local DB for RAG pipeline (explainable-rag-chatbot)
- **Neo4j** — graph database for knowledge-graph-based RAG (explainable-rag-chatbot)
- **SQLAlchemy** (async) — ORM for FastAPI async PostgreSQL backend (DELUX_AI)

---

## Infrastructure & DevOps
- **Docker** — containerisation of all services with multi-stage Python images
- **Docker Compose** — multi-container orchestration (web, Celery workers, Redis, Nginx, PgBouncer)
- **Nginx** — reverse proxy and static file serving
- **Celery** — distributed task queue; `worker`, `beat`, `threads` and `prefork` pool configurations
- **Celery Beat + django-celery-beat** — periodic / scheduled task execution
- **Gevent** — cooperative green-thread concurrency for Celery workers
- **WhiteNoise** — efficient static file serving without a separate file server
- **Structlog** — structured, context-aware application logging
- **Sentry SDK** — error monitoring and performance tracing
- **django-prometheus** — Prometheus metrics exposure for Django applications
- **TensorBoard** — training visualisation and model debugging

---

## Cloud & Storage
- **AWS S3** — object / media file storage (boto3, django-storages)
- **Google Cloud Storage** — GCS blob storage backend (magictale)
- **Google Cloud Firestore** — NoSQL document database (magictale)
- **Firebase Admin SDK** — Firebase Authentication and FCM push notifications
- **FCM (Firebase Cloud Messaging)** — mobile push notification delivery

---

## Authentication & Security
- **JWT** — stateless authentication (djangorestframework-simplejwt, PyJWT, python-jose)
- **django-allauth / dj-rest-auth** — social and standard auth flows
- **Google OAuth 2.0** — sign-in with Google integration
- **Stripe** — payment processing and subscription billing (magictale)
- **cryptography** — low-level cryptographic primitives (Fernet, RSA, etc.)
- **HTTPS / TLS** — served behind Nginx with secure headers

---

## Computer Vision
- **OpenCV** (`opencv-python-headless`) — image processing and computer vision pipelines
- **MediaPipe** — real-time pose, hand, and face landmark detection (benjaminkley)
- **Pillow / PIL** — image I/O, resizing, format conversion
- **Open3D** — 3D point-cloud and mesh processing (benjaminkley)
- **Trimesh** — 3D mesh loading and manipulation (benjaminkley)
- **pdfplumber** — PDF text and table extraction (explainable-rag-chatbot)

---

## Developer Tools & Environments
- **Jupyter Notebook / JupyterLab** — interactive ML experimentation and EDA
- **Google Colab** — cloud-based GPU training for deep learning models
- **python-dotenv / pydantic-settings** — environment variable management
- **httpx / requests** — async and sync HTTP clients
- **APScheduler** — in-process job scheduling (Reho-AI-Service)
- **Loguru** — developer-friendly logging (Reho-AI-Service)
- **ReportLab / WeasyPrint** — programmatic PDF generation (benjaminkley, magictale)
- **Git / GitHub** — version control and collaborative development
