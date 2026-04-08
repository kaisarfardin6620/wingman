# Abdullah Kaisar Fardin

**AI Developer | Dhaka, Bangladesh**

📧 kaisarfardin128@gmail.com &nbsp;|&nbsp; 📞 +880 1708050645 &nbsp;|&nbsp; 🔗 [linkedin.com/in/abdullah-kaisar-fardin](https://www.linkedin.com/in/abdullah-kaisar-fardin) &nbsp;|&nbsp; 🐙 [github.com/kaisarfardin6620](https://github.com/kaisarfardin6620)

---

## PROFESSIONAL SUMMARY

Results-driven AI Developer with hands-on experience in designing and deploying scalable, production-grade AI systems. Skilled in bridging the gap between cutting-edge research models and real-world applications, with expertise in building asynchronous backends using FastAPI and Django. Proficient in integrating multimodal AI solutions, including vision and audio models, into high-performance workflows. Strong foundation in data engineering, cloud deployment, and microservices architecture, complemented by ongoing postgraduate studies in Data Science. Passionate about delivering efficient, intelligent systems that solve complex business problems at scale.

---

## TECHNICAL SKILLS

| Category | Technologies |
|---|---|
| **Languages** | Python (Advanced), SQL |
| **Core Frameworks** | Django, Django Channels (WebSockets), FastAPI, Celery |
| **AI & ML** | TensorFlow, MediaPipe (CV), OpenAI (Vision/Audio), LangChain, RAG |
| **Data Engineering** | Neo4j (Graph DB), Pinecone (Vector DB), Redis, PostgreSQL, MongoDB |
| **Infrastructure** | Docker, Nginx, AWS S3, Firebase (FCM), CI/CD Pipelines |

---

## WORK EXPERIENCE

### Jr AI Developer
**SparkTech Agency** &nbsp;|&nbsp; Dhaka &nbsp;|&nbsp; Aug 2025 – Present

- Architecting asynchronous backend systems using Django & FastAPI, handling concurrent AI inference requests via Celery task queues.
- Integrated Multimodal AI models (GPT-4o Vision, Whisper Audio) into production workflows, handling file uploads, OCR, and transcription at scale.

### Trainee AI Developer
**SparkTech Agency** &nbsp;|&nbsp; Dhaka &nbsp;|&nbsp; May 2025 – Aug 2025

- Developed modular backend services for data preprocessing and LLM context window management.
- Assisted in the containerization (Docker) and deployment of ML services to cloud environments.

---

## PROJECTS

### Production AI Backend Systems

**MagicTale AI Storytelling Platform** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/magictale)
*Django 5, Celery, Django Channels, WebSockets, OpenAI GPT-4o, DALL-E 3, ElevenLabs TTS, PostgreSQL, Redis, Firebase FCM, Docker*

- Built an async three-stage AI pipeline (GPT-4o story generation → DALL-E 3 cover illustration → ElevenLabs voice narration) offloaded to Celery workers with real-time WebSocket progress streaming.
- Integrated Google OAuth2, Apple Sign-In (JWT via .p8 key), RevenueCat subscription webhooks, and Firebase Cloud Messaging (FCM) push notifications in a single production-grade Django backend.
- Enforced end-to-end security: Pwned Passwords API validation, WebSocket JWT ownership checks, and RevenueCat webhook auth-header verification.

**Explainable Hybrid KG-RAG Chatbot** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/explainable-rag-chatbot)
*FastAPI, Neo4j, Pinecone, OpenAI, SQLite, Python 3.10+*

- Designed a research-grade Hybrid RAG architecture combining Pinecone semantic vector search with Neo4j knowledge graph multi-hop traversal to reduce hallucinations and enable granular explainability.
- Implemented post-generation NLI claim-level verification and a refusal mechanism that abstains from answering when confidence score falls below a configurable threshold (default 0.4).
- Automated Knowledge Graph construction from raw PDFs via LLM-based entity/relation extraction during ingestion; applied Freeman's Degree Centrality to weight evidence from authoritative graph nodes.
- Exposed ablation study modes (`rag_only`, `kg_only`, `hybrid`) for scientific benchmarking with automated F1, semantic similarity, and latency metrics.

**3D Head Scanner & Biometric Analysis API** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/benjaminkley)
*Django 5, DRF, Celery, Redis, PostgreSQL, AWS S3, trimesh, numpy, Firebase FCM, Docker*

- Built an async scanning pipeline integrating the KeenTools external AI API to reconstruct 3D head models from 2D photos; used Celery to handle background processing and poll for completion without blocking the API.
- Extracted biometric measurements (head width, ear-to-ear, eye-to-eye, circumference) from downloaded `.obj` mesh files using trimesh principal-axis alignment and Euclidean/surface distance calculations.
- Designed Role-Based Access Control (Admin, Doctor, Provider, Client) with OTP email verification, an admin approval workflow, and automated PDF report generation via ReportLab.

**DELUX AI – E-Commerce Shopping Chatbot** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/DELUX_AI)
*FastAPI, OpenAI GPT-4o-mini, WebSocket, PostgreSQL (SQLAlchemy Async), Redis, Docker, Nginx*

- Built a production WebSocket chatbot using OpenAI function-calling (tool-use) to execute dynamic product database searches with filters (keyword, price range, condition, free shipping).
- Implemented per-user Redis connection pooling and sliding-window message rate limiting; personalized responses by injecting fetched user profile context into LLM system prompts.
- Added conversation history trimming, global exception handling, APITimeoutError/RateLimitError recovery, and structured JSON logging for production observability.

**Reho Finance AI Microservice** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Reho-AI-Service)
*FastAPI, OpenAI GPT-4o, MongoDB (Motor async), Redis, Docker, Nginx, Uvicorn*

- Developed a context-aware financial AI microservice sharing MongoDB with a Node.js main backend; dynamically injected live user income/expense/debt snapshots into LLM prompts before each AI response.
- Built a nightly scheduled job runner (`daily_job_runner.py`) pre-computing admin analytics (50/30/20 budget analysis, Avalanche vs. Snowball debt strategies, anonymized peer spending comparisons) for instant dashboard loads.
- Implemented risk assessment endpoints auto-calculating user financial risk level (Low/Medium/High) from debt-to-income ratios with AI-generated 360-degree user summaries for admin dashboards.

**Wingman AI Chat Platform** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/wingman)
*Django 5, Django Channels, Celery, Redis, OpenAI, PostgreSQL, Docker*

- Developed a real-time AI conversational backend using Django Channels WebSocket consumers with Celery-powered async task dispatch for AI inference and multi-turn conversation management.
- Architected modular Django apps for JWT authentication, live chat (WebSocket consumers), subscription billing, and admin dashboard within a Dockerized deployment.

---

### NLP & Language Models

**Quora Question Pair Classification (SBERT + Deep Learning)** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning)
*Python, Sentence-BERT (SBERT), TensorFlow/Keras, SMOTE, scikit-learn*

- Leveraged Sentence-BERT to generate high-quality sentence embeddings for Quora question pairs and trained a Siamese Network alongside ANN and LSTM classifiers for semantic duplicate detection.
- Applied SMOTE for class-imbalance correction; evaluated all models with F1-score, ROC-AUC, and confusion matrix heatmaps.

**LSTM Sentiment Analysis – IMDb** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis)
*Python, TensorFlow/Keras, LSTM, NLTK*

- Built a binary LSTM sentiment classifier on 50,000 IMDb reviews achieving ~85% test accuracy with an embedding layer, LSTM, dropout, and batch normalization trained via Adam + binary cross-entropy.
- Applied full NLP preprocessing (HTML stripping, stopword removal, lemmatization, Keras Tokenizer, sequence padding) with EarlyStopping regularization.

**Spam Classification with Pretrained Word Embeddings** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings)
*Python, Gensim (Word2Vec, GloVe, FastText), scikit-learn, XGBoost*

- Detected spam emails using sentence vectorization via averaged pretrained Word2Vec, GloVe, and FastText embeddings; benchmarked Logistic Regression, SVM, and XGBoost classifiers across all three embedding types.

**Twitter Sentiment Analysis** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis)
*Python, NLTK, TF-IDF, scikit-learn, TensorFlow/Keras, SMOTE*

- Classified multi-class tweet sentiment using TF-IDF vectorization with SMOTE oversampling; evaluated Random Forest, KNN, SVM, and ANN classifiers on accuracy, F1-score, and confusion matrices.

**Real vs. Fake News Classifier** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier)
*Python, NLTK, TF-IDF, scikit-learn, TensorFlow/Keras*

- Developed a fake news detection pipeline using NLP feature engineering (n-grams, TF-IDF) and compared Logistic Regression, Decision Tree, Random Forest, KNN, SVM, and ANN classifiers.

---

### Computer Vision & Machine Learning

**Lung Cancer Chest X-Ray Classification** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/LungCancer-ImageNet)
*Python, TensorFlow/Keras, Transfer Learning (VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0)*

- Built a 4-class chest X-ray classifier (adenocarcinoma, large cell carcinoma, squamous cell carcinoma, normal) benchmarking 5 pretrained CNN architectures via two-stage fine-tuning (freeze base → unfreeze last 20 layers).
- Applied automatic class weight computation to handle dataset imbalance with EarlyStopping and ReduceLROnPlateau callbacks.

**FlowerNet – 9-Architecture CNN Benchmark** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/FlowerNet-Comparison)
*Python, TensorFlow/Keras, MobileNetV2, InceptionV3, VGG16/19, ResNet50/101, DenseNet121, Xception, InceptionResNetV2*

- Benchmarked 9 state-of-the-art CNN architectures for flower classification with an automated training pipeline, cross-model performance comparison plots, and statistical logging.
- Designed a custom InceptionV3 classification head (1024→512→256→128 dense layers, LeakyReLU, BatchNorm, progressive dropout 0.5→0.2) as the highest-performing single-model solution.

**AppleNet – Autoencoder & Anomaly Detection** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/AppleNet-AE)
*Python, TensorFlow/Keras, VAE, KMeans, t-SNE, One-Class SVM, scikit-learn*

- Implemented an end-to-end unsupervised pipeline: convolutional autoencoder for reconstruction, Variational Autoencoder for latent space modeling, masked image inpainting, and KMeans + t-SNE clustering.
- Deployed One-Class SVM on encoder latent features for anomaly scoring; visualized top anomalous test images ranked by reconstruction error.

**Fashion-MNIST Supervised & Semi-Supervised Learning** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup)
*Python, TensorFlow/Keras, MobileNetV2, EfficientNetV2B0, TensorBoard*

- Implemented a semi-supervised pseudo-labeling pipeline: trained on a small labeled set, assigned high-confidence pseudo-labels to unlabeled samples, then fine-tuned on the combined dataset.
- Used `tf.data` pipelines with random flip/rotation/zoom augmentation, EarlyStopping, ReduceLROnPlateau, and TensorBoard experiment tracking.

**Customer Churn Prediction** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Customer-Churn-Prediction)
*Python, scikit-learn, XGBoost, TensorFlow/Keras, SMOTE, GridSearchCV*

- Compared 12 classifiers (Logistic Regression, Random Forest, XGBoost, SVC, ANN, Voting/Stacking ensembles) for bank customer churn prediction.
- Applied SMOTE within ColumnTransformer preprocessing pipelines; performed GridSearchCV with StratifiedKFold and manual ANN architecture search for hyperparameter optimization.

**Bangladeshi Medicinal Leaf Classification** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification)
*Python, TensorFlow/Keras, Transfer Learning (VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0)*

- Built a CNN-based medicinal plant leaf identifier for Bangladeshi species using transfer learning with five pretrained architectures and custom classification heads (Dense, BatchNorm, Dropout, GlobalAveragePooling2D).

**Butterfly Species Classifier** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Butterfly-Classifier)
*Python, TensorFlow/Keras, MobileNetV2, KerasTuner (Hyperband), Stratified K-Fold*

- Classified 40 butterfly species using a progressive four-script pipeline: basic training → two-stage transfer learning → dataset balancing via augmentation → KerasTuner Hyperband hyperparameter optimization with stratified K-fold cross-validation.

**Marine Life Classifier** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Marine_Life_Classifier)
*Python, TensorFlow/Keras, ResNet101, MobileNetV2, OpenCV (Bilateral Filter), CosineDecay LR*

- Developed three marine life classification approaches: baseline ResNet101, ResNet101 with bilateral-filter image denoising preprocessing, and a two-stage MobileNetV2 pipeline (feature extraction → fine-tuning with CosineDecay LR scheduling).

**Leaf Disease Classifier** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/LeafDiseaseClassifier)
*Python, TensorFlow/Keras, MobileNetV2, KerasTuner (Hyperband), K-Fold Cross-Validation*

- Built a robust plant disease classifier using MobileNetV2 with KerasTuner Hyperband learning-rate search and 5-fold stratified cross-validation for reliable performance estimation.
- Generated ensemble predictions by combining K-Fold model outputs; produced detailed classification reports, ROC curves, and Precision-Recall curves on the test set.

---

### Regression & Predictive Modeling

**Sales Profit Forecasting** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Sales-Forecasting-Regression)
*Python, scikit-learn, PyCaret, GridSearchCV*

- Predicted sales profit using Linear Regression, Decision Tree, Random Forest, SVR, and KNN regressors in scikit-learn pipelines; applied temporal feature engineering (Month, Quarter, cyclical encoding) from date columns.
- Leveraged PyCaret AutoML for automated model comparison and best-model selection; visualized residuals and actual-vs-predicted plots for each tuned model.

**Weather Rainfall Prediction** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Weather-rainfall-prediction)
*Python, scikit-learn, PyCaret, GridSearchCV, Polynomial Features*

- Predicted rainfall using polynomial feature engineering, IQR outlier removal, and multiple regression models; used GridSearchCV for Decision Tree, Random Forest, and KNN hyperparameter tuning.
- Applied PyCaret AutoML to compare and evaluate a broad set of regression algorithms automatically.

**Breast Cancer Survival Prediction** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.)
*Python, scikit-learn (Logistic Regression, Decision Tree, Random Forest, SVM, KNN)*

- Predicted breast cancer patient survival using five ML algorithms with EDA, feature correlation analysis, and survival rate visualizations.

**Lung Cancer Risk Prediction** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.)
*Python, scikit-learn (Logistic Regression, SVM, Decision Tree, Random Forest, KNN)*

- Predicted lung cancer likelihood from patient feature data using five ML classifiers with EDA, GridSearch/RandomSearch hyperparameter tuning, and evaluation via accuracy, precision, recall, and F1-score.

---

### Domain-Specific AI Assistants

**HR AI Assistant Suite** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Hr-Ai-Assistant)
*Python, OpenAI GPT API, Flask/FastAPI-ready, JSON prompt management*

- Built a production-ready multi-domain HR AI assistant covering Compensation, Compliance, Talent Acquisition, L&D, Organizational Development, HR Strategy, and Total Rewards using OpenAI GPT with modular backend files per domain.
- Implemented per-user conversation history, input sanitization, caching, structured logging, and a GNews RSS feed summarizer (`Gnews_backend.py`) for HR news intelligence.

**Bondly – Financial Coaching AI** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant)
*Python, OpenAI API*

- Developed an emotionally intelligent AI financial coach providing personalized advice based on user goals, relationship status, and mood; incorporated micro-consent handling for sensitive topics (investments, debt) and dynamic tone adaptation.

**Bible AI Assistant (Preachly)** &nbsp;|&nbsp; [GitHub](https://github.com/kaisarfardin6620/Bible-Ai-Assistant)
*Python, OpenAI API, Scripture API, Flask*

- Built a scripture-grounded AI assistant that fetches Bible verses via the Scripture API across multiple versions (NIV, RSVCE, CSB) and provides compassionate, context-aware biblical guidance via a Flask REST endpoint.

---

## EDUCATION

**MSc in Data Science & Analytics**
East West University &nbsp;|&nbsp; Jan 2026 – Present

**BSc in Computer Science & Engineering**
Bangladesh University of Business & Technology &nbsp;|&nbsp; 2019 – 2024

---

*Resume generated from public GitHub repositories: all project descriptions extracted from repository code and README documentation.*
