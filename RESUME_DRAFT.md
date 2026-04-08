# Abdullah Kaisar Fardin

**Email:** kaisarfardin128@gmail.com | **Phone:** 01708050645  
**LinkedIn:** [linkedin.com/in/abdullah-kaisar-fardin](https://www.linkedin.com/in/abdullah-kaisar-fardin)  
**GitHub:** [github.com/kaisarfardin6620](https://github.com/kaisarfardin6620)

---

## PROFESSIONAL SUMMARY

Results-driven AI Developer with hands-on experience in designing and deploying scalable, production-grade AI systems. Skilled in bridging the gap between cutting-edge research models and real-world applications, with expertise in building asynchronous backends using FastAPI and Django. Proficient in integrating multimodal AI solutions, including vision and audio models, into high-performance workflows. Strong foundation in data engineering, cloud deployment, and microservices architecture, complemented by ongoing postgraduate studies in Data Science. Passionate about delivering efficient, intelligent systems that solve complex business problems at scale.

---

## TECHNICAL SKILLS

| Category | Skills |
|---|---|
| **Languages** | Python (Advanced), SQL |
| **Core Frameworks** | Django 5, Django REST Framework, FastAPI, Celery, Django Channels (WebSockets), Daphne |
| **AI & ML** | TensorFlow 2.x, Keras, OpenAI API (GPT-4o, DALL-E 3, Whisper), LangChain, RAG, SBERT, LSTM, CNNs, Transfer Learning, Autoencoders, MediaPipe |
| **NLP** | NLTK, TF-IDF, Word Embeddings, Sentence-BERT (SBERT), SMOTE |
| **Data Engineering** | Neo4j (Graph DB), Pinecone (Vector DB), Redis, PostgreSQL, MongoDB (Motor async), SQLite |
| **Infrastructure** | Docker, Docker Compose, Nginx, AWS S3, Firebase (FCM), CI/CD Pipelines, Uvicorn, Gunicorn |
| **ML Libraries** | scikit-learn, XGBoost, PyCaret, pandas, NumPy, matplotlib, seaborn, trimesh, KerasTuner |

---

## WORK EXPERIENCE

### Jr AI Developer
**SparkTech Agency** · Dhaka, Bangladesh | *Aug 2025 – Present*

- Architecting asynchronous backend systems using Django & FastAPI, handling concurrent AI inference requests via Celery task queues.
- Integrated Multimodal AI models (GPT-4o Vision, Whisper Audio) into production workflows, handling file uploads, OCR, and transcription at scale.

### Trainee AI Developer
**SparkTech Agency** · Dhaka, Bangladesh | *May 2025 – Aug 2025*

- Developed modular backend services for data preprocessing and LLM context window management.
- Assisted in the containerization (Docker) and deployment of ML services to cloud environments.

---

## PROJECTS

> *All project details below are extracted directly from repository READMEs, code, and documentation.*

---

### 🔬 PRODUCTION AI BACKENDS

---

#### Explainable Hybrid KG-RAG Chatbot
**GitHub:** [github.com/kaisarfardin6620/explainable-rag-chatbot](https://github.com/kaisarfardin6620/explainable-rag-chatbot)  
**Tech Stack:** Python, FastAPI, Neo4j, Pinecone, OpenAI GPT-4o, SQLite, Uvicorn

- Built a research-grade Hybrid Retrieval-Augmented Generation (RAG) system integrating Vector Search (Pinecone) with Knowledge Graph Reasoning (Neo4j) to mitigate hallucinations.
- Implemented a claim-level NLI (Natural Language Inference) post-hoc verification layer that abstains from answering when confidence scores fall below 0.4, reducing hallucination rates.
- Developed Freeman's Degree Centrality-based Graph Centrality Scoring to weight evidence from authoritative entities in multi-hop reasoning chains.
- Supports ablation-ready benchmarking modes (`rag_only`, `kg_only`, `hybrid`) with automated F1/Semantic Similarity/Latency benchmarking pipeline.
- Source code for the paper: *"Hybrid Knowledge Graph–Guided Explainable RAG for Trustworthy QA (In Preparation)"*.

---

#### MagicTale — AI-Powered Children's Storytelling Platform
**GitHub:** [github.com/kaisarfardin6620/magictale](https://github.com/kaisarfardin6620/magictale)  
**Tech Stack:** Django 5, Celery, Redis, PostgreSQL, Django Channels, WebSockets, OpenAI GPT-4o, DALL-E 3, ElevenLabs TTS, Firebase FCM, RevenueCat, Docker, Nginx

- Designed a 3-stage asynchronous story generation pipeline: GPT-4o for text → DALL-E 3 for cover illustration → ElevenLabs for voice narration, all orchestrated via Celery workers.
- Implemented real-time WebSocket progress events to push live status updates (e.g., "Writing text…", "Drawing cover image…", "Recording audio…") to clients during AI generation.
- Integrated multi-provider OAuth authentication (Google OAuth2 + Apple Sign-In) alongside email/password JWT authentication via SimpleJWT.
- Implemented Firebase Cloud Messaging (FCM) push notifications triggered on story completion and profile events.
- Secured RevenueCat webhook-based subscription management for in-app purchase handling.

---

#### Benjaminkley — 3D Head Scanner & Biometric Analysis Backend
**GitHub:** [github.com/kaisarfardin6620/benjaminkley](https://github.com/kaisarfardin6620/benjaminkley)  
**Tech Stack:** Django 5, DRF, Celery, Redis, PostgreSQL, trimesh, numpy, open3d, KeenTools API, AWS S3, Firebase FCM, Docker, Nginx

- Built an asynchronous 3D head scanning pipeline integrating with the external KeenTools API to reconstruct 3D head models from 2D photos via Celery background workers.
- Implemented biometric measurement calculations (Head Width, Ear-to-Ear, Eye-to-Eye, Circumference) from `.obj` files using trimesh and numpy mesh alignment algorithms.
- Developed auto-generated PDF reports containing user details and biometric measurements, served securely via AWS S3.
- Implemented Role-Based Access Control (RBAC) with JWT authentication, email OTP verification, and admin approval workflow.

---

#### Wingman — AI Interview Preparation Platform
**GitHub:** [github.com/kaisarfardin6620/wingman](https://github.com/kaisarfardin6620/wingman)  
**Tech Stack:** Django 5, Django Channels, WebSockets, Celery, Redis, PostgreSQL, OpenAI, Google GenAI, Daphne, Docker, Nginx, AWS S3

- Built a production-grade async AI backend platform with real-time WebSocket chat and asynchronous task processing via Celery.
- Integrated OpenAI and Google GenAI APIs for intelligent, context-aware AI responses in an interview preparation context.
- Implemented comprehensive subscription management, JWT authentication, and multi-module architecture (auth, chat, dashboard, subscription).
- Containerized the full stack (Django + Celery Worker + Redis + PostgreSQL + Nginx) via Docker Compose with environment-separated configuration.

---

#### Rai Backend — Community AI Platform
**GitHub:** [github.com/kaisarfardin6620/Rai_Backend](https://github.com/kaisarfardin6620/Rai_Backend)  
**Tech Stack:** Django 5, Django Channels, WebSockets, Celery, Redis, PostgreSQL, OpenAI, Google GenAI, Daphne, Docker, Nginx, AWS S3

- Developed a modular Django backend for a community AI platform with multi-domain modules including AI services, authentication, community management, dashboard analytics, and subscription management.
- Integrated both OpenAI (GPT-4o) and Google GenAI APIs for multi-model AI routing within the platform.
- Deployed with a full production stack: Django + Celery Workers + Redis + Daphne (ASGI/WebSockets) + Nginx reverse proxy, containerized via Docker Compose.

---

#### Reho AI Finance Microservice
**GitHub:** [github.com/kaisarfardin6620/Reho-AI-Service](https://github.com/kaisarfardin6620/Reho-AI-Service)  
**Tech Stack:** Python, FastAPI (Async), OpenAI GPT-4o, MongoDB (Motor async), Redis, Docker, Nginx, Uvicorn

- Designed a standalone AI microservice serving as the intelligence layer for a Finance Management System, sharing a MongoDB database with the main Node.js backend for real-time data awareness.
- Implemented context-aware WebSocket chat ("Reho" assistant) that dynamically injects the user's actual financial data (incomes, expenses, debts) into the LLM system prompt before responding.
- Built scheduled background jobs for nightly pre-computation of heavy analysis reports, enabling instant dashboard load times during the day.
- Developed admin-facing financial intelligence features including 360 user views, spending heatmaps, debt-to-income risk assessment, and peer comparison analytics.
- Implemented 50/30/20 budget rule analysis, Avalanche vs. Snowball debt strategy comparison, and expense audit features for user financial optimization.

---

#### DELUX AI (Dealnux Chatbot)
**GitHub:** [github.com/kaisarfardin6620/DELUX_AI](https://github.com/kaisarfardin6620/DELUX_AI)  
**Tech Stack:** Python, FastAPI, OpenAI GPT-4o-mini (Function Calling), SQLAlchemy (async), PostgreSQL, Redis, JWT, Docker, Nginx

- Built a production-ready AI shopping assistant for an e-commerce platform using FastAPI WebSockets and OpenAI function calling (tool use) to query a live product database.
- Implemented OpenAI tool calling to intelligently extract product search parameters (keyword, price range, condition, shipping) from natural language and execute structured database queries.
- Engineered per-user connection limiting, message rate limiting, conversation history trimming, and comprehensive error handling for production-grade resilience.
- Delivered personalized chat experiences by fetching user profile data and addressing users by name within LLM system prompts.

---

#### Maiz FastAPI Service
**GitHub:** [github.com/kaisarfardin6620/maiz-fastapi](https://github.com/kaisarfardin6620/maiz-fastapi)  
**Tech Stack:** Python, FastAPI, Motor (MongoDB async), pymongo, OpenAI, Pydantic, JWT

- Built a FastAPI microservice with async MongoDB integration (Motor driver) for AI-driven data processing workflows.
- Integrated OpenAI API for intelligent content generation with JWT-secured endpoints.

---

#### HR AI Assistant Suite
**GitHub:** [github.com/kaisarfardin6620/Hr-Ai-Assistant](https://github.com/kaisarfardin6620/Hr-Ai-Assistant)  
**Tech Stack:** Python, OpenAI GPT, Flask/FastAPI-compatible modules, JSON prompt engineering

- Developed a modular suite of 8 production-ready Python backend modules covering HR domains: Compensation, Compliance, Talent Acquisition, HR Strategy, Learning & Development, Organizational Development, Total Rewards, and HR Business Partner.
- Each module implements consistent patterns: structured logging, input sanitization, per-user conversation history for context continuity, and error handling.
- Integrated a GNews-based HR news aggregator (`Gnews_backend.py`) for surfacing relevant HR industry updates to professionals.

---

#### Glimmcatcher — AI Image Creator
**GitHub:** [github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher](https://github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher)  
**Tech Stack:** Python, OpenAI (DALL-E), FastAPI

- Built an AI-powered image generation assistant using OpenAI's image generation API, enabling users to brainstorm, create, and refine visual concepts via natural language prompts.
- Implemented a modular frontend/backend separation (`Glimmcatcher.py` / `Glimmcatcher_backend.py`) with a REST API layer for easy integration.

---

### 🧠 COMPUTER VISION & DEEP LEARNING

---

#### Marine Life Classifier
**GitHub:** [github.com/kaisarfardin6620/Marine_Life_Classifier](https://github.com/kaisarfardin6620/Marine_Life_Classifier)  
**Tech Stack:** Python, TensorFlow/Keras, ResNet101, MobileNetV2, OpenCV, scikit-image

- Implemented three distinct deep learning approaches: (1) ResNet101 with denoising preprocessing (Bilateral Filter), (2) baseline ResNet101, and (3) MobileNetV2 with two-stage training (feature extraction + fine-tuning).
- Applied CosineDecay learning rate scheduling and per-class accuracy metrics for rigorous evaluation.

---

#### LungCancer-ImageNet — Chest X-ray Multi-Class Classification
**GitHub:** [github.com/kaisarfardin6620/LungCancer-ImageNet](https://github.com/kaisarfardin6620/LungCancer-ImageNet)  
**Tech Stack:** Python, TensorFlow/Keras, VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0

- Built a multi-class chest X-ray classification pipeline to distinguish four lung cancer subtypes: adenocarcinoma, large cell carcinoma, squamous cell carcinoma, and normal.
- Applied automatic class weight computation to handle class imbalance, two-stage fine-tuning on 5 pre-trained ImageNet architectures, and EarlyStopping callbacks.

---

#### FlowerNet — 9-Model CNN Architecture Comparison
**GitHub:** [github.com/kaisarfardin6620/FlowerNet-Comparison](https://github.com/kaisarfardin6620/FlowerNet-Comparison)  
**Tech Stack:** Python, TensorFlow/Keras, MobileNetV2, InceptionV3, VGG16/19, ResNet50/101, DenseNet121, Xception, InceptionResNetV2

- Systematically benchmarked 9 state-of-the-art CNN architectures on a flower classification dataset with unified training pipelines, logging, and comparative visualization tools.
- Implemented adaptive learning rate scheduling, early stopping with best weights restoration, and per-model checkpoint saving.

---

#### LeafDiseaseClassifier
**GitHub:** [github.com/kaisarfardin6620/LeafDiseaseClassifier](https://github.com/kaisarfardin6620/LeafDiseaseClassifier)  
**Tech Stack:** Python, TensorFlow/Keras, MobileNetV2, KerasTuner (Hyperband), scikit-learn

- Built a leaf disease classification pipeline using MobileNetV2 with extensive data augmentation (rotation, shifts, shear, zoom, flip, brightness).
- Implemented automated hyperparameter tuning via KerasTuner Hyperband and 5-fold stratified cross-validation with ensemble prediction across folds for robust performance estimation.

---

#### Fashion-MNIST Supervised & Semi-Supervised Learning Lab
**GitHub:** [github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup](https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup)  
**Tech Stack:** Python, TensorFlow/Keras, MobileNetV2, EfficientNetV2B0, TensorBoard

- Implemented supervised learning with ImageNet transfer learning (MobileNetV2/EfficientNetV2B0) and semi-supervised learning via pseudo-labeling on high-confidence unlabeled samples.
- Tracked experiments with TensorBoard and evaluated models using accuracy/loss curves, confusion matrices, ROC-AUC per class, and misclassified image visualization.

---

#### AppleNet-AE — Unsupervised Apple Image Analysis
**GitHub:** [github.com/kaisarfardin6620/AppleNet-AE](https://github.com/kaisarfardin6620/AppleNet-AE)  
**Tech Stack:** Python, TensorFlow/Keras, VAE, KMeans, t-SNE, One-Class SVM, scikit-learn

- Built a modular unsupervised deep learning pipeline featuring a standard Autoencoder, Variational Autoencoder (VAE), masked image inpainting, KMeans latent space clustering with t-SNE visualization, and One-Class SVM anomaly detection.

---

#### Autoencoder Anomaly Detection
**GitHub:** [github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection](https://github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection)  
**Tech Stack:** Python, TensorFlow/Keras, scikit-learn, t-SNE

- Designed an image anomaly detection system using a convolutional autoencoder and denoising autoencoder, flagging images with high reconstruction error and visualizing latent features with t-SNE.

---

#### Bangladeshi Medicinal Leaf Classification
**GitHub:** [github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification](https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification)  
**Tech Stack:** Python, TensorFlow/Keras, VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0

- Developed a multi-architecture transfer learning pipeline for classifying Bangladeshi medicinal plant leaves from images, incorporating ImageDataGenerator augmentation and EarlyStopping.

---

#### Additional Computer Vision Projects

| Project | Description | Tech |
|---|---|---|
| [Butterfly-Classifier](https://github.com/kaisarfardin6620/Butterfly-Classifier) | Multi-class butterfly species classification | TensorFlow/Keras, Transfer Learning |
| [Shoe_Classifier](https://github.com/kaisarfardin6620/Shoe_Classifier) | Shoe type image classification | TensorFlow/Keras, CNN |
| [Cat-Vs-Dog-Classification](https://github.com/kaisarfardin6620/Cat-Vs-Dog-Classification) | Binary image classification | TensorFlow/Keras, CNN |
| [Cnn_Preprocessings](https://github.com/kaisarfardin6620/Cnn_Preprocessings) | CNN image preprocessing techniques | TensorFlow/Keras |
| [Cnn_Visuals](https://github.com/kaisarfardin6620/Cnn_Visuals) | CNN feature map & activation visualization | TensorFlow/Keras |

---

### 📊 NLP & MACHINE LEARNING

---

#### Quora Question Pair Classification — SBERT + Deep Learning
**GitHub:** [github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning](https://github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning)  
**Tech Stack:** Python, Sentence-BERT (SBERT), TensorFlow/Keras, ANN, LSTM, Siamese Network, SMOTE, scikit-learn

- Classified Quora question pairs as duplicate or non-duplicate using pretrained SBERT embeddings as input features to ANN, LSTM, and Siamese Network architectures.
- Applied SMOTE for class balancing and evaluated models using Classification Reports, ROC-AUC curves, and Confusion Matrices.

---

#### LSTM for IMDb Sentiment Analysis
**GitHub:** [github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis](https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis)  
**Tech Stack:** Python, TensorFlow/Keras, LSTM, NLTK, scikit-learn

- Built a binary sentiment classifier on 50,000 IMDb movie reviews achieving approximately **85% test accuracy** using LSTM with embedding layer, dropout, and batch normalization.
- Applied comprehensive text preprocessing: HTML tag removal, lemmatization, stop word removal, Keras tokenization, and sequence padding.

---

#### NLP-Based Twitter Sentiment Analysis
**GitHub:** [github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis](https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis)  
**Tech Stack:** Python, NLTK, TF-IDF, scikit-learn (RF, KNN, SVM), TensorFlow/Keras (ANN), SMOTE, WordCloud

- Performed multi-class sentiment classification on Twitter data with full NLP preprocessing (lowercase, URL removal, lemmatization, stop word removal) and TF-IDF vectorization.
- Handled class imbalance with SMOTE and compared 4 classification models (Random Forest, KNN, SVM, ANN) using accuracy, precision, recall, F1-score, and confusion matrices.

---

#### Real vs. Fake News Classifier
**GitHub:** [github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier](https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier)  
**Tech Stack:** Python, NLTK, TF-IDF, scikit-learn, TensorFlow/Keras, WordCloud

- Developed a fake news detection system using TF-IDF feature engineering and compared Logistic Regression, Decision Tree, Random Forest, KNN, SVM, and ANN classifiers.

---

#### Customer Churn Prediction
**GitHub:** [github.com/kaisarfardin6620/Customer-Churn-Prediction](https://github.com/kaisarfardin6620/Customer-Churn-Prediction)  
**Tech Stack:** Python, scikit-learn, XGBoost, TensorFlow/Keras (ANN), SMOTE, GridSearchCV, Plotly, pandas

- Trained and compared 12 ML models (including Logistic Regression, Random Forest, XGBoost, SVC, Gradient Boosting, Voting/Stacking Ensembles, and a tuned ANN) for bank customer churn prediction.
- Applied SMOTE for class imbalance, IQR-based outlier capping, and GridSearchCV with StratifiedKFold for systematic hyperparameter optimization.
- Visualized ROC curves and confusion matrices using Plotly for interactive model comparison.

---

#### Sales Profit Forecasting — Regression Models
**GitHub:** [github.com/kaisarfardin6620/Sales-Forecasting-Regression](https://github.com/kaisarfardin6620/Sales-Forecasting-Regression)  
**Tech Stack:** Python, scikit-learn, PyCaret (AutoML), pandas, matplotlib, seaborn

- Built a regression pipeline comparing Linear Regression, Decision Tree, Random Forest, SVR, and KNN for sales profit prediction with GridSearchCV hyperparameter tuning.
- Leveraged PyCaret AutoML for automated model comparison and selection, including time-series feature engineering (cyclical month/day encoding, week/weekend indicators).

---

#### Weather Forecasting with ML Classification Models
**GitHub:** [github.com/kaisarfardin6620/Weather_Forecasting_Models](https://github.com/kaisarfardin6620/Weather_Forecasting_Models)  
**Tech Stack:** Python, scikit-learn, pandas, NumPy, seaborn, scipy

- Developed a weather summary classification pipeline with advanced EDA, feature engineering (cyclical Hour_sin/Hour_cos, Month encoding, interaction features), and comparison of 6 ML models (Logistic Regression, Decision Tree, KNN, Random Forest, SVC, Naive Bayes).

---

#### Additional ML Projects

| Project | Description | Tech |
|---|---|---|
| [Lung-Cancer-Prediction-using-ML](https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.) | Lung cancer prediction from survey data | scikit-learn, pandas |
| [Breast-Cancer-Survival-Prediction](https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.) | Breast cancer survival prediction | scikit-learn, TensorFlow/Keras |
| [Weather-Rainfall-Prediction](https://github.com/kaisarfardin6620/Weather-rainfall-prediction) | Rainfall prediction with regression/classification | scikit-learn, pandas |
| [Wine-Quality-Testing](https://github.com/kaisarfardin6620/Wine-Quality-Testing-) | Wine quality prediction | scikit-learn, pandas |
| [NLP-Spam-Classification](https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings) | Spam detection using word embeddings | TensorFlow/Keras, NLTK |
| [Text-Pair-Classification](https://github.com/kaisarfardin6620/Text-Pair-Classification) | NLP-based text pair relationship classification | TensorFlow/Keras, NLTK |

---

## EDUCATION

### MSc in Data Science & Analytics
**East West University** | *Jan 2026 – Present*

### BSc in Computer Science & Engineering
**Bangladesh University of Business & Technology (BUBT)** | *2019 – 2024*

---

*This resume was generated by analyzing all GitHub repositories listed above. All project descriptions, tech stacks, and impact bullets are sourced exclusively from README files, code, and repository structure — not from user-provided descriptions.*
