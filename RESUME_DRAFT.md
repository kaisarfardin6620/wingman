# Abdullah Kaisar Fardin

📧 kaisarfardin128@gmail.com | 📞 01708050645
🔗 linkedin.com/in/abdullah-kaisar-fardin | 🐙 github.com/kaisarfardin6620

---

## PROFESSIONAL SUMMARY

Results-driven AI Developer with hands-on experience in designing and deploying scalable, production-grade AI systems. Skilled in bridging the gap between cutting-edge research models and real-world applications, with expertise in building asynchronous backends using FastAPI and Django. Proficient in integrating multimodal AI solutions, including vision and audio models, into high-performance workflows. Strong foundation in data engineering, cloud deployment, and microservices architecture, complemented by ongoing postgraduate studies in Data Science. Passionate about delivering efficient, intelligent systems that solve complex business problems at scale.

---

## WORK EXPERIENCE

### Jr. AI Developer
**SparkTech Agency** | Dhaka, Bangladesh | Aug 2025 – Present

- Architecting asynchronous backend systems using Django & FastAPI, handling concurrent AI inference requests via Celery task queues.
- Integrated Multimodal AI models (GPT-4o Vision, Whisper Audio) into production workflows, handling file uploads, OCR, and transcription at scale.

### Trainee AI Developer
**SparkTech Agency** | Dhaka, Bangladesh | May 2025 – Aug 2025

- Developed modular backend services for data preprocessing and LLM context window management.
- Assisted in the containerization (Docker) and deployment of ML services to cloud environments.

---

## TECHNICAL SKILLS

<!-- Skills marked [U] are from user-supplied message. Skills marked [R] were detected by scanning repo files. -->

**Languages:** Python (Advanced) [U], SQL [U]

**Frameworks:** Django [U], Django Channels / WebSockets [U], FastAPI [U], Celery [U], Flask [R]

**AI & ML:** TensorFlow [U], Keras [R], Scikit-learn [R], MediaPipe (CV) [U], OpenAI (Vision/Audio) [U], LangChain [U], RAG [U], Sentence-Transformers / SBERT [R], XGBoost [R], Imbalanced-learn / SMOTE [R]

**NLP:** NLTK [R], TF-IDF [R], Word Embeddings [R], LSTM [R]

**Data Engineering:** Neo4j (Graph DB) [U], Pinecone (Vector DB) [U], Redis [U], PostgreSQL [U], MongoDB [U], Pandas [R], NumPy [R]

**Infrastructure:** Docker [U], Nginx [U], AWS S3 [U], Firebase (FCM) [U], CI/CD Pipelines [U]

**Visualization:** Matplotlib [R], Seaborn [R], Plotly [R]

> **Legend:** `[U]` = from your supplied skills message · `[R]` = detected from repo files (README / requirements.txt / code imports). See `RESUME_DATA_SOURCES.md` for full detail.

---

## PROJECTS

> All project descriptions and tech stacks are sourced exclusively from GitHub repository analysis (README.md, requirements.txt, and code imports). No manually provided project descriptions are used. See `RESUME_DATA_SOURCES.md` for per-project extraction detail.

### HR AI Assistant Suite
🔗 github.com/kaisarfardin6620/Hr-Ai-Assistant

*Source signals: README.md (features + structure), requirements.txt*

- Built a production-ready multi-domain HR AI assistant suite covering Compensation, Compliance, Talent Acquisition, Organizational Development, and more, powered by OpenAI GPT models.
- Implemented per-user conversation history, input sanitization, request caching, and robust error handling for reliable production use.
- Designed modular backend architecture ready for seamless integration with Flask, FastAPI, or Express.js web APIs.
- **Tech stack (from requirements.txt):** Python, openai ≥1.0.0, tenacity, sounddevice, scipy, requests, python-dotenv

---

### AppleNet-AE — Unsupervised Deep Learning Pipeline
🔗 github.com/kaisarfardin6620/AppleNet-AE

*Source signals: README.md (features list + pipeline steps)*

- Developed a modular unsupervised deep learning pipeline for apple image analysis using Convolutional Autoencoder and Variational Autoencoder (VAE) with Keras/TensorFlow.
- Implemented masked image inpainting, latent space clustering (KMeans + t-SNE), and outlier scoring via One-Class SVM for anomaly detection.
- **Tech stack (from README pip install):** TensorFlow, scikit-learn, matplotlib, Pillow

---

### LungCancer-ImageNet — Chest X-Ray Multi-Class Classifier
🔗 github.com/kaisarfardin6620/LungCancer-ImageNet

*Source signals: README.md (features + requirements)*

- Built a multi-class chest X-ray classification pipeline for adenocarcinoma, large cell carcinoma, squamous cell carcinoma, and normal using custom CNN and five transfer learning architectures (VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0).
- Implemented two-stage fine-tuning, automatic class weight calculation, data augmentation, early stopping, and per-model accuracy reporting.
- **Tech stack (from README):** TensorFlow, Keras, scikit-learn, matplotlib, seaborn

---

### Bondly — AI Financial Coach
🔗 github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant

*Source signals: README.md (features + description)*

- Engineered an emotionally intelligent AI financial coaching chatbot with dynamic tone adaptation based on user mood, micro-consent for sensitive financial topics, and milestone celebration features.
- Supports personalized advice based on user profile, relationship status, and goals; tracks full conversation history.
- **Tech stack (from requirements.txt):** Python, openai

---

### Customer Churn Prediction
🔗 github.com/kaisarfardin6620/Customer-Churn-Prediction

*Source signals: README.md (project overview + models list + installation section)*

- Benchmarked 12+ ML classification algorithms (Logistic Regression, Decision Tree, Random Forest, XGBoost, KNN, SVC, Gradient Boosting, AdaBoost, Bagging, Voting, Stacking, ANN) for bank customer churn prediction.
- Applied SMOTE for class imbalance, IQR-based outlier handling, feature engineering, hyperparameter tuning (GridSearchCV with StratifiedKFold), and ROC/AUC comparison.
- **Tech stack (from README pip install):** pandas, numpy, scikit-learn, imbalanced-learn, xgboost, tensorflow, scikeras, plotly, matplotlib, seaborn

---

### Quora Question Pair Classification (SBERT + Deep Learning)
🔗 github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning

*Source signals: README.md (overview + steps), notebook pip install lines and import statements*

- Classified duplicate/non-duplicate Quora question pairs using SBERT sentence embeddings as input features to ANN, LSTM, and Siamese Network architectures.
- Applied SMOTE, EDA, ROC-AUC curve comparison, confusion matrix analysis, and generated final submission file.
- **Tech stack (from notebook imports/pip install):** sentence-transformers, TensorFlow/Keras, scikit-learn, NLTK, imbalanced-learn, pandas, seaborn, matplotlib

---

### NLP-based Twitter Sentiment Analysis
🔗 github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis

*Source signals: README.md (methodology + technologies section)*

- Built a sentiment classification pipeline for Twitter data with full NLP preprocessing (lowercasing, URL removal, stop-word removal, lemmatization), TF-IDF vectorization, and class imbalance handling via SMOTE.
- Trained and evaluated Random Forest, KNN, SVM, and ANN models; visualized results with word clouds, ROC curves, and bar charts.
- **Tech stack (from README technologies section):** Python, pandas, NumPy, scikit-learn, TensorFlow/Keras, NLTK, wordcloud, imbalanced-learn, matplotlib, seaborn

---

### Glimmcatcher — AI Image Creator
🔗 github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher

*Source signals: README.md (features + description), requirements.txt*

- Built an AI-powered image generation and creative ideation assistant allowing users to generate, analyze, enhance, and save images via an interactive CLI.
- **Tech stack (from requirements.txt):** Python, openai, Pillow, python-dotenv, tenacity, scipy, sounddevice

---

### Preachly — Bible AI Assistant
🔗 github.com/kaisarfardin6620/Bible-Ai-Assistant

*Source signals: README.md (features + setup section)*

- Developed an AI-powered Bible assistant that fetches and contextualizes Bible verses via the Scripture API, supporting multiple Bible versions (NIV, RSVCE, CSB), voice and text input, and a Flask REST API endpoint.
- Implemented robust error handling, environment-based configuration, and user-friendly book name aliases.
- **Tech stack (from README setup pip install):** Python, openai, requests, python-dotenv, flask

---

## EDUCATION

### MSc in Data Science & Analytics
**East West University** | Jan 2026 – Present

### BSc in Computer Science & Engineering
**Bangladesh University of Business & Technology (BUBT)** | 2019 – 2024

---

*For a full list of 30+ projects, see github.com/kaisarfardin6620*
*For the complete data-sourcing breakdown of this resume, see `RESUME_DATA_SOURCES.md`*
