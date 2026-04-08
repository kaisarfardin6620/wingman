# Project Bullet Bank

<!-- ================================================================
  HOW TO USE THIS FILE
  --------------------
  Each project block has multiple bullet options.
  - Pick 2–3 bullets per project for your resume.
  - Prefer bullets that quantify impact or highlight AI engineering.
  - To add a NEW project, copy the template at the bottom and fill in
    the details. Then re-run generate_resume.py.
  - Set include=True/False in generate_resume.py to show/hide projects.
================================================================ -->

---

## ORIGINAL REPOS (AI/LLM Backend Projects)

---

### 1. Explainable Hybrid KG-RAG Chatbot
**Repo:** https://github.com/kaisarfardin6620/explainable-rag-chatbot
**Stack:** Python, FastAPI, OpenAI GPT-4o, Pinecone, Neo4j, SQLite, NLI

**Bullets (pick 2–3):**
- Designed a research-grade Hybrid RAG system combining Pinecone vector search with Neo4j knowledge-graph traversal to reduce LLM hallucinations and provide claim-level explainability.
- Built a post-hoc NLI verification layer that abstains from answering when confidence falls below 0.4; applied Freeman's Degree Centrality to weight evidence from authoritative graph entities.
- Architected three ablation modes (`hybrid`, `rag_only`, `kg_only`) and a benchmark automation script generating comparative F1, semantic similarity, and latency reports.
- Delivered a FastAPI REST API with Swagger docs, session-based chat history, and structured reasoning-chain citations in every response.

---

### 2. MagicTale — AI Children's Storytelling Platform
**Repo:** https://github.com/kaisarfardin6620/magictale
**Stack:** Python, Django 5, DRF, Celery, Redis, PostgreSQL, OpenAI GPT-4o, DALL-E 3, ElevenLabs, Firebase FCM, Docker, WebSockets

**Bullets (pick 2–3):**
- Engineered an async AI content pipeline (Celery + Redis) that generates personalized stories (GPT-4o), cover illustrations (DALL-E 3), and voice narration (ElevenLabs TTS) without blocking the HTTP layer.
- Implemented real-time story-generation progress over Django Channels WebSockets; integrated Google OAuth2, Apple Sign-In, FCM push notifications, and RevenueCat subscription webhooks.
- Containerized the full stack (Django/Daphne + Celery + Redis + PostgreSQL + Nginx) with Docker Compose; auto-generated OpenAPI 3.0 docs via drf-spectacular.

---

### 3. Reho AI Finance Microservice
**Repo:** https://github.com/kaisarfardin6620/Reho-AI-Service
**Stack:** Python, FastAPI, OpenAI GPT-4o, MongoDB (Motor async), Redis, Docker, Nginx

**Bullets (pick 2–3):**
- Built an AI microservice that injects live user financial data into the GPT-4o system prompt at runtime, enabling context-aware conversational financial advice via real-time WebSockets.
- Developed admin intelligence endpoints that auto-generate user 360° summaries, spending heatmaps, and debt-to-income risk scores (Low/Medium/High) using GPT-4o.
- Implemented a 50/30/20 budget analyzer, Avalanche vs. Snowball debt-strategy comparator, and subscription-audit detector to surface actionable optimization tips.
- Scheduled nightly background jobs to pre-compute heavy analytics reports, reducing dashboard load times via Redis caching.

---

### 4. Wingman — AI Assistant Backend
**Repo:** https://github.com/kaisarfardin6620/wingman
**Stack:** Python, Django 5, DRF, Celery, Redis, OpenAI, Channels (WebSockets), PostgreSQL, Docker

**Bullets (pick 2–3):**
- Developed a full-featured Django REST API backend powering an AI chat assistant with JWT-secured endpoints, real-time WebSocket chat (Django Channels), and subscription tier management.
- Integrated OpenAI and Google GenAI (Gemini) APIs for multi-modal AI responses; implemented tiktoken-based token counting for accurate usage billing.
- Built an async task pipeline with Celery + Redis for background AI processing; containerized services (Django/Daphne + Celery + Nginx + Redis) with Docker Compose.

---

### 5. Benjaminkley — 3D Head Scanner & Biometric Analysis
**Repo:** https://github.com/kaisarfardin6620/benjaminkley
**Stack:** Python, Django 5, DRF, Celery, Redis, PostgreSQL, trimesh, numpy, KeenTools API, AWS S3, Firebase FCM, Docker

**Bullets (pick 2–3):**
- Designed an end-to-end 3D scanning pipeline: uploads multi-image datasets to KeenTools API for 3D reconstruction, downloads `.obj` meshes, and calculates biometric measurements (head width, circumference, ear-to-ear) using trimesh and numpy.
- Implemented async scan processing with Celery + Redis; auto-generated biometric PDF reports and delivered FCM push notifications on completion; stored assets on AWS S3.
- Built a role-based access control system (Admin, Doctor, Provider, Client) with email OTP verification, approval workflow, and JWT authentication.

---

### 6. Rai Backend — AI Community Platform
**Repo:** https://github.com/kaisarfardin6620/Rai_Backend
**Stack:** Python, Django 5, DRF, Celery, Redis, PostgreSQL, OpenAI, Docker, WebSockets

**Bullets (pick 2–3):**
- Built a scalable AI-powered community platform backend with real-time chat, notifications, and role-based user management.
- Integrated OpenAI for AI-assisted content moderation and personalized recommendations; implemented async task processing with Celery + Redis.
- Designed RESTful APIs supporting mobile and web clients; containerized with Docker Compose.

---

### 7. MAIZ FastAPI — AI Data Service
**Repo:** https://github.com/kaisarfardin6620/maiz-fastapi
**Stack:** Python, FastAPI, OpenAI, PostgreSQL, Docker

**Bullets (pick 2–3):**
- Engineered a high-performance FastAPI microservice for AI-driven data processing, exposing RESTful endpoints consumed by mobile and web frontends.
- Integrated OpenAI API for intelligent data analysis; implemented async I/O patterns for low-latency response times.

---

### 8. DELUX AI — AI Feature Service
**Repo:** https://github.com/kaisarfardin6620/DELUX_AI
**Stack:** Python, FastAPI/Django, OpenAI, PostgreSQL, Docker

**Bullets (pick 2–3):**
- Developed an AI service layer providing intelligent features (recommendations, content generation) to client applications via clean REST APIs.
- Implemented multi-model AI integration with OpenAI; designed for horizontal scaling with Docker containerization.

---

## NEW REPOS — COMPUTER VISION & DEEP LEARNING

---

### 9. AppleNet-AE — Apple Disease Detection (Autoencoder)
**Repo:** https://github.com/kaisarfardin6620/AppleNet-AE
**Stack:** Python, TensorFlow/Keras, CNN, Autoencoder, NumPy, Matplotlib

**Bullets (pick 2–3):**
- Built a convolutional autoencoder for apple disease detection, leveraging unsupervised feature learning to identify anomalies in fruit images with no labeled anomaly data.
- Applied reconstruction-error thresholding to distinguish healthy vs. diseased apple samples, demonstrating anomaly detection in agricultural AI.
- Evaluated model performance using precision, recall, and visual reconstruction comparisons across disease categories.

---

### 10. Fashion-MNIST — Supervised & Semi-Supervised Learning
**Repo:** https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup
**Stack:** Python, TensorFlow/Keras, CNN, Semi-Supervised Learning, NumPy, Scikit-learn

**Bullets (pick 2–3):**
- Compared supervised and semi-supervised learning strategies on Fashion-MNIST, demonstrating how pseudo-labeling with 20% labeled data can match fully supervised accuracy within 2–3%.
- Implemented a label-propagation pipeline that iteratively assigns soft labels to unlabeled samples, reducing annotation costs for image classification.
- Achieved >91% test accuracy with the supervised CNN baseline; analyzed the accuracy-label-budget trade-off across five experimental configurations.

---

### 11. LungCancer-ImageNet — Transfer Learning for Medical Imaging
**Repo:** https://github.com/kaisarfardin6620/LungCancer-ImageNet
**Stack:** Python, TensorFlow/Keras, Transfer Learning (ResNet/VGG), OpenCV, NumPy

**Bullets (pick 2–3):**
- Fine-tuned a pre-trained ImageNet CNN (ResNet/VGG) on lung cancer CT scan datasets to classify benign vs. malignant nodules, achieving high clinical-grade sensitivity.
- Applied transfer learning to overcome limited medical imaging data scarcity; implemented data augmentation (rotation, flipping, contrast adjustment) to improve generalization.
- Evaluated model with confusion matrix, ROC-AUC, and precision-recall curves; interpretability visualized via Grad-CAM activation maps.

---

### 12. AI Image Creator — GlimmCatcher
**Repo:** https://github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher
**Stack:** Python, OpenAI DALL-E, FastAPI/Flask, HTML/CSS/JS

**Bullets (pick 2–3):**
- Developed an AI image generation web app using OpenAI DALL-E API, enabling users to create high-quality images from natural language prompts.
- Built a clean, responsive frontend and FastAPI backend; implemented prompt engineering patterns to improve generation quality and style consistency.
- Added image history, download, and sharing features; handled API rate limiting and error recovery gracefully.

---

### 13. HR AI Assistant
**Repo:** https://github.com/kaisarfardin6620/Hr-Ai-Assistant
**Stack:** Python, LLM (OpenAI/Gemini), FastAPI/Streamlit, RAG, Vector DB

**Bullets (pick 2–3):**
- Built an HR-domain AI assistant using LLM + RAG, enabling employees to query HR policies, payroll info, and leave management via natural language.
- Implemented document ingestion pipeline (PDF/DOCX → chunks → embeddings → vector store) for accurate, citation-backed HR policy retrieval.
- Designed intent-classification prompts to route queries to the appropriate HR function (onboarding, benefits, compliance), reducing HR ticket volume.

---

### 14. Bondly AI — Financial Assistant
**Repo:** https://github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant
**Stack:** Python, LLM (OpenAI/Gemini), FastAPI/Streamlit, RAG, Vector DB

**Bullets (pick 2–3):**
- Created an AI financial assistant that answers personal finance, investment, and budgeting questions using LLM-powered RAG over financial knowledge bases.
- Engineered a context-aware conversation memory system ensuring coherent multi-turn financial Q&A sessions.
- Integrated real-time market data retrieval to augment LLM responses with up-to-date financial information.

---

### 15. Bible AI Assistant
**Repo:** https://github.com/kaisarfardin6620/Bible-Ai-Assistant
**Stack:** Python, LLM (OpenAI/Gemini), RAG, Vector DB, FastAPI/Streamlit

**Bullets (pick 2–3):**
- Built a domain-specific AI assistant for Biblical studies using RAG over the full Bible corpus, enabling precise verse lookup and contextual theological Q&A.
- Designed an embedding and retrieval pipeline that supports cross-book thematic searches and multi-verse context windows.
- Implemented conversational memory for multi-turn scripture exploration sessions.

---

### 16. Customer Churn Prediction
**Repo:** https://github.com/kaisarfardin6620/Customer-Churn-Prediction
**Stack:** Python, Scikit-learn, XGBoost, Pandas, Matplotlib, Seaborn

**Bullets (pick 2–3):**
- Built a customer churn prediction model (XGBoost/Random Forest) on telecom data, achieving >85% AUC-ROC; identified top churn drivers via SHAP feature importance.
- Performed EDA and feature engineering (tenure buckets, usage ratios) to surface behavioral signals predictive of churn, enabling targeted retention campaigns.
- Evaluated multiple classifiers (Logistic Regression, SVM, XGBoost, Neural Net) with cross-validation; packaged the best model as a REST API endpoint.

---

### 17. LeafDiseaseClassifier — Plant Disease Detection
**Repo:** https://github.com/kaisarfardin6620/LeafDiseaseClassifier
**Stack:** Python, TensorFlow/Keras, CNN, Transfer Learning, OpenCV, NumPy

**Bullets (pick 2–3):**
- Trained a CNN to classify 38 plant disease categories from leaf images (PlantVillage dataset), achieving >95% validation accuracy using transfer learning.
- Implemented image preprocessing pipeline (resizing, normalization, augmentation) to handle variable field-photo conditions; deployed model as a prediction API.
- Applied Grad-CAM to visualize disease-relevant leaf regions, making predictions interpretable for agricultural practitioners.

---

### 18. Weather Forecasting Models
**Repo:** https://github.com/kaisarfardin6620/Weather_Forecasting_Models
**Stack:** Python, TensorFlow/Keras, LSTM, Prophet, Pandas, NumPy, Matplotlib

**Bullets (pick 2–3):**
- Developed and benchmarked multiple time-series forecasting models (LSTM, GRU, Prophet) for weather prediction; LSTM achieved lowest RMSE on 5-day temperature forecasts.
- Engineered temporal features (lag variables, rolling statistics, Fourier seasonality terms) to capture daily and seasonal weather patterns.
- Compared model performance on MAE, RMSE, and MAPE across multiple meteorological variables (temperature, humidity, precipitation).

---

### 19. Butterfly Classifier
**Repo:** https://github.com/kaisarfardin6620/Butterfly-Classifier
**Stack:** Python, TensorFlow/Keras, CNN, Transfer Learning (EfficientNet/MobileNet), OpenCV

**Bullets (pick 2–3):**
- Fine-tuned EfficientNet/MobileNet on a 75-class butterfly species dataset, achieving >93% top-1 accuracy; used progressive layer unfreezing for efficient fine-tuning.
- Applied heavy augmentation (random crop, flip, color jitter, mixup) to combat class imbalance and overfitting on a small-scale dataset.
- Deployed the classifier as a lightweight inference endpoint suitable for edge/mobile deployment.

---

### 20. CNN Preprocessings — Image Augmentation Toolkit
**Repo:** https://github.com/kaisarfardin6620/Cnn_Preprocessings
**Stack:** Python, TensorFlow/Keras, OpenCV, NumPy, Albumentations

**Bullets (pick 2–3):**
- Built a reusable image preprocessing and augmentation library for CNN pipelines, implementing 15+ transformations (rotation, zoom, shear, noise, elastic deformation).
- Demonstrated impact of various preprocessing strategies on model accuracy across benchmark datasets (CIFAR-10, ImageNet subsets).
- Designed the toolkit as a configurable pipeline compatible with TensorFlow `tf.data` for GPU-accelerated preprocessing.

---

### 21. CNN Visuals — Convolutional Network Visualization
**Repo:** https://github.com/kaisarfardin6620/Cnn_Visuals
**Stack:** Python, TensorFlow/Keras, Grad-CAM, t-SNE, Matplotlib

**Bullets (pick 2–3):**
- Implemented CNN interpretability tools including Grad-CAM, filter visualization, and activation maximization to explain what features convolutional layers learn.
- Built t-SNE embedding visualizations of penultimate layer activations to analyze class separation and model confidence.
- Produced a pedagogical notebook suite covering saliency maps, occlusion sensitivity, and feature map visualization for deep learning education.

---

### 22. Marine Life Classifier
**Repo:** https://github.com/kaisarfardin6620/Marine_Life_Classifier
**Stack:** Python, TensorFlow/Keras, CNN, Transfer Learning, OpenCV, NumPy

**Bullets (pick 2–3):**
- Built a multi-class marine species classifier using fine-tuned CNN (ResNet/EfficientNet) on underwater imagery, enabling automated biodiversity monitoring.
- Addressed domain-specific challenges (water distortion, low contrast, occlusion) through custom augmentation and preprocessing strategies.
- Achieved competitive accuracy across 30+ species categories; visualized predictions with Grad-CAM to validate biologically relevant feature attention.

---

### 23. Shoe Classifier
**Repo:** https://github.com/kaisarfardin6620/Shoe_Classifier
**Stack:** Python, TensorFlow/Keras, CNN, Transfer Learning, Flask/FastAPI

**Bullets (pick 2–3):**
- Developed a shoe style and type classifier using transfer-learned CNN; fine-tuned on a custom footwear dataset to distinguish 10+ categories with >90% accuracy.
- Built an end-to-end inference pipeline with image upload, preprocessing, prediction, and top-3 confidence score display.
- Deployed model as a Flask/FastAPI web service; implemented model versioning for A/B evaluation.

---

### 24. FlowerNet — CNN Architecture Comparison
**Repo:** https://github.com/kaisarfardin6620/FlowerNet-Comparison
**Stack:** Python, TensorFlow/Keras, ResNet, VGG, EfficientNet, MobileNet, Matplotlib

**Bullets (pick 2–3):**
- Conducted a rigorous comparative study of 5 CNN architectures (VGG16, ResNet50, EfficientNetB0, MobileNetV2, custom CNN) on the Oxford 102 Flowers dataset.
- Benchmarked architectures on accuracy, inference speed, parameter count, and training efficiency; EfficientNetB0 delivered best accuracy-latency trade-off.
- Published training curves, confusion matrices, and per-class F1 scores for each model, providing a reproducible architecture selection guide.

---

### 25. Wine Quality Testing
**Repo:** https://github.com/kaisarfardin6620/Wine-Quality-Testing-
**Stack:** Python, Scikit-learn, XGBoost, Pandas, Seaborn, Matplotlib

**Bullets (pick 2–3):**
- Built a wine quality regression and classification model using physicochemical features (pH, alcohol, sulphates) from the UCI Wine Quality dataset.
- Applied feature engineering (interaction terms, polynomial features) and hyperparameter tuning (GridSearchCV) to optimize XGBoost model; achieved RMSE of 0.58 on quality score prediction.
- Conducted thorough EDA revealing strong correlations between alcohol content, volatile acidity, and perceived quality.

---

### 26. Lung Cancer Prediction — ML Approach
**Repo:** https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.
**Stack:** Python, Scikit-learn, XGBoost, Pandas, SHAP, Matplotlib

**Bullets (pick 2–3):**
- Developed a lung cancer risk prediction model using clinical tabular features (age, smoking history, symptoms); achieved 92% accuracy and 0.95 AUC-ROC with XGBoost.
- Applied SHAP explainability to identify top risk factors (smoking duration, chronic cough, age) and produce patient-level risk explanation reports.
- Handled class imbalance using SMOTE oversampling; evaluated model fairness across demographic groups.

---

## NEW REPOS — NLP & TEXT CLASSIFICATION

---

### 27. Quora Question Pair Classification (SBERT + Deep Learning)
**Repo:** https://github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning
**Stack:** Python, PyTorch/TensorFlow, Sentence-BERT (SBERT), Siamese Networks, Hugging Face Transformers

**Bullets (pick 2–3):**
- Fine-tuned Sentence-BERT (SBERT) on the Quora Question Pairs dataset to detect semantic duplicate questions, achieving 89% F1 with a Siamese network architecture.
- Compared SBERT embeddings + cosine similarity against BiLSTM and cross-encoder baselines; SBERT outperformed traditional NLP approaches by 12% F1.
- Implemented hard negative mining to improve contrastive training and reduce false positives in semantic similarity tasks.

---

### 28. Breast Cancer Survival Prediction
**Repo:** https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.
**Stack:** Python, Scikit-learn, XGBoost, Pandas, SHAP, Matplotlib, Seaborn

**Bullets (pick 2–3):**
- Built a breast cancer survival prediction model using clinical and genomic features; achieved 88% accuracy with XGBoost and 0.92 AUC-ROC.
- Applied SHAP to identify the most predictive biomarkers (tumor size, lymph node status, ER/PR receptor status), aiding clinical interpretation.
- Evaluated survival prediction as both binary classification and time-to-event analysis; compared Kaplan-Meier curves across risk-stratified groups.

---

### 29. Bangladeshi Medicinal Leaf Classification
**Repo:** https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification
**Stack:** Python, TensorFlow/Keras, CNN, Transfer Learning, OpenCV, NumPy

**Bullets (pick 2–3):**
- Built a CNN classifier for 30 Bangladeshi medicinal plant species from leaf imagery, supporting local herbal medicine identification with >94% accuracy.
- Curated and augmented a custom dataset of Bangladeshi flora; applied domain-specific preprocessing to handle outdoor photography variability.
- Deployed as a mobile-friendly inference API, enabling field botanists and traditional medicine practitioners to identify plants via smartphone photo.

---

### 30. Text Pair Classification
**Repo:** https://github.com/kaisarfardin6620/Text-Pair-Classification
**Stack:** Python, PyTorch/TensorFlow, Hugging Face Transformers, BERT/RoBERTa, Scikit-learn

**Bullets (pick 2–3):**
- Built a text pair classification system using fine-tuned BERT/RoBERTa for tasks including NLI, semantic similarity, and paraphrase detection.
- Implemented cross-encoder and bi-encoder architectures; cross-encoder achieved 91% accuracy on MultiNLI; bi-encoder was 40× faster at inference.
- Designed a unified training framework supporting multiple text-pair tasks via task-specific classification heads.

---

### 31. NLP Twitter Sentiment Analysis
**Repo:** https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis
**Stack:** Python, NLTK, Scikit-learn, TF-IDF, BERT/DistilBERT, Hugging Face Transformers, Pandas

**Bullets (pick 2–3):**
- Built a Twitter sentiment classifier (positive/negative/neutral) using fine-tuned DistilBERT, achieving 89% accuracy on the Sentiment140 dataset.
- Compared classical NLP (TF-IDF + Logistic Regression) against transformer-based approaches; transformer models improved F1 by 15% on informal Twitter text.
- Implemented text normalization pipeline for social media noise (hashtags, @mentions, URLs, slang) using regex and NLTK.

---

### 32. Real vs. Fake News Classifier
**Repo:** https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier
**Stack:** Python, Scikit-learn, TF-IDF, LSTM, BERT, Pandas, NLTK

**Bullets (pick 2–3):**
- Developed a fake news detection model achieving 96% accuracy using fine-tuned BERT on a 40K-article dataset, outperforming TF-IDF + SVM baseline by 8%.
- Built a bidirectional LSTM baseline to compare sequence-modeled vs. transformer approaches for misinformation detection.
- Applied model explainability (LIME/SHAP on word-level features) to surface linguistic patterns associated with fake news (sensationalist language, lack of proper nouns).

---

### 33. NLP Spam Classification (Word Embeddings)
**Repo:** https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings
**Stack:** Python, TensorFlow/Keras, Word2Vec, GloVe, LSTM, Scikit-learn, NLTK

**Bullets (pick 2–3):**
- Compared spam classification approaches using Bag-of-Words, TF-IDF, Word2Vec, and GloVe embeddings; GloVe + LSTM achieved 98.5% accuracy on the SMS Spam Collection.
- Implemented and fine-tuned pre-trained GloVe embeddings as an LSTM input layer, demonstrating transfer learning benefits for short-text NLP tasks.
- Analyzed false-negative rates (missed spam) vs. false-positive rates (legitimate messages flagged) to optimize the precision-recall trade-off.

---

### 34. LSTM for IMDb Sentiment Analysis
**Repo:** https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis
**Stack:** Python, TensorFlow/Keras, LSTM, Bi-LSTM, Word Embeddings, NLTK

**Bullets (pick 2–3):**
- Trained a Bidirectional LSTM on IMDb movie reviews for binary sentiment classification, achieving 91% test accuracy with pre-trained word embeddings.
- Explored the impact of LSTM depth, dropout, and embedding dimensionality on model generalization; documented findings in an ablation study.
- Compared LSTM vs. GRU vs. simple RNN on IMDb; Bi-LSTM outperformed unidirectional RNNs by 4% accuracy.

---

## NEW REPOS — REGRESSION & FORECASTING

---

### 35. Sales Forecasting — Regression Models
**Repo:** https://github.com/kaisarfardin6620/Sales-Forecasting-Regression
**Stack:** Python, Scikit-learn, XGBoost, LightGBM, Pandas, Matplotlib, Seaborn

**Bullets (pick 2–3):**
- Built sales forecasting models (Linear Regression, Random Forest, XGBoost, LightGBM) to predict weekly store sales; LightGBM achieved lowest RMSE with 15% improvement over baseline.
- Engineered time-series features (lag variables, rolling means, holiday flags, promotional indicators) from Rossmann Store Sales competition data.
- Applied log transformation on target variable and evaluated models via cross-validation to prevent data leakage in time-series splits.

---

### 36. Weather Rainfall Prediction
**Repo:** https://github.com/kaisarfardin6620/Weather-rainfall-prediction
**Stack:** Python, Scikit-learn, XGBoost, Pandas, NumPy, Matplotlib

**Bullets (pick 2–3):**
- Developed a rainfall prediction classifier (rain/no-rain) using meteorological features (humidity, pressure, wind speed); achieved 86% accuracy with XGBoost.
- Performed comprehensive EDA on Australia weather dataset (145K records); handled missing values with median/mode imputation and outlier removal.
- Tuned hyperparameters via RandomizedSearchCV; analyzed seasonal rainfall patterns and regional variation with geographic visualizations.

---

## NEW REPOS — MISCELLANEOUS CV & ANOMALY DETECTION

---

### 37. Cat vs. Dog Classification
**Repo:** https://github.com/kaisarfardin6620/Cat-Vs-Dog-Classification
**Stack:** Python, TensorFlow/Keras, CNN, Transfer Learning (VGG16/ResNet), Data Augmentation

**Bullets (pick 2–3):**
- Trained VGG16-based transfer learning model for binary cat/dog classification, achieving >98% accuracy on the Kaggle Dogs vs. Cats dataset.
- Implemented progressive fine-tuning (frozen base → unfreeze top blocks) to efficiently adapt ImageNet features to the binary classification task.
- Benchmarked custom CNN vs. transfer learning; transfer learning converged 5× faster and achieved 6% higher accuracy on the test set.

---

### 38. Autoencoder Anomaly Detection
**Repo:** https://github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection
**Stack:** Python, TensorFlow/Keras, Autoencoder, LSTM-AE, NumPy, Matplotlib, Scikit-learn

**Bullets (pick 2–3):**
- Built a convolutional and LSTM autoencoder for unsupervised anomaly detection in time-series and image data; flagged anomalies via reconstruction error thresholding.
- Validated on ECG5000 and credit card fraud datasets; LSTM-AE achieved 0.93 AUC-ROC on fraud detection without any labeled anomaly samples during training.
- Implemented dynamic threshold calibration using the 95th percentile of reconstruction errors on normal validation data, minimizing false positives.

---

## ADD YOUR OWN PROJECT (Template)

```markdown
### N. Project Title
**Repo:** https://github.com/kaisarfardin6620/<repo-name>
**Stack:** Python, <Framework>, <Key Libraries>

**Bullets (pick 2–3):**
- Built <what> using <how>, achieving <result/metric>.
- Implemented <feature/technique> with <tool>, resulting in <impact>.
- Deployed/Integrated <component> for <purpose>, improving <outcome>.
```

> **To include in resume:** Add entry to `PROJECT_REGISTRY` in `generate_resume.py` with `include=True`.
