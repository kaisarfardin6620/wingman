#!/usr/bin/env python3
"""
resume/generate_resume.py
=========================
Rebuild RESUME_DRAFT.md from the PROJECT_REGISTRY below.

Usage:
    python resume/generate_resume.py

To add a new project:
1. Add an entry to PROJECT_REGISTRY (copy the template comment below).
2. Set include=True to show it on the resume, or include=False to hide it.
3. Run this script to regenerate RESUME_DRAFT.md.

To change personal info:
- Edit the PERSONAL dict.
- Edit the EDUCATION list.
- Run this script.
"""

from pathlib import Path
import datetime

# ---------------------------------------------------------------------------
# PERSONAL INFO — edit these
# ---------------------------------------------------------------------------
PERSONAL = {
    "name": "Kaisar Fardin",
    "title": "AI Engineer",
    "location": "Dhaka, Bangladesh",
    "github": "github.com/kaisarfardin6620",
    "email": "your.email@example.com",
    "phone": "+880-XXXX-XXXXXX",
}

# ---------------------------------------------------------------------------
# EDUCATION — edit these (most recent first)
# ---------------------------------------------------------------------------
EDUCATION = [
    {
        "degree": "MSc in [Your Field]",
        "university": "[Your University], Dhaka",
        "status": "Ongoing",
    },
    {
        "degree": "BSc in [Your Field]",
        "university": "[Your University], Dhaka",
        "status": "Completed, [Year]",
    },
]

# ---------------------------------------------------------------------------
# SKILLS — edit as needed
# ---------------------------------------------------------------------------
SKILLS = [
    ("Languages", "Python"),
    ("AI / LLM", "OpenAI GPT-4o, DALL-E 3, Gemini, RAG, Knowledge Graphs, NLI, Prompt Engineering"),
    ("ML / DL", "TensorFlow, Keras, PyTorch, Scikit-learn, XGBoost, LightGBM, LSTM, CNN, Transfer Learning"),
    ("NLP", "Hugging Face Transformers, BERT, SBERT, Word2Vec, GloVe, NLTK, spaCy, TF-IDF"),
    ("Computer Vision", "OpenCV, Grad-CAM, Image Augmentation, Object Classification, Anomaly Detection"),
    ("Frameworks", "Django 5, Django REST Framework, FastAPI"),
    ("Vector / Graph DBs", "Pinecone, Neo4j, ChromaDB"),
    ("Databases", "PostgreSQL, MongoDB, Redis, SQLite"),
    ("Async / Real-time", "Celery, Django Channels, WebSockets, Daphne"),
    ("Infrastructure", "Docker, Docker Compose, Nginx, AWS S3, Firebase FCM"),
    ("Auth & Security", "JWT (SimpleJWT), Google OAuth2, Apple Sign-In, Email OTP"),
    ("Tools", "Git, Swagger / OpenAPI, Postman, Jupyter, Matplotlib, Seaborn, SHAP"),
]

# ---------------------------------------------------------------------------
# PROJECT REGISTRY
# ---------------------------------------------------------------------------
# Each entry has:
#   name        - display name on resume
#   repo_url    - full GitHub URL
#   stack_tags  - one-line tech stack (shown as code tag line)
#   include     - True  -> show on resume; False -> hide (keep in bank only)
#   bullets     - list of bullet strings; only first 3 shown on resume
#
# TEMPLATE (copy-paste to add a new project):
# {
#     "name":       "Project Title",
#     "repo_url":   "https://github.com/kaisarfardin6620/<repo>",
#     "stack_tags": "Python - FastAPI - OpenAI - PostgreSQL",
#     "include":    True,
#     "bullets": [
#         "Built X using Y, achieving Z.",
#         "Implemented A with B, resulting in C.",
#         "Deployed D for E, improving F.",
#     ],
# },
# ---------------------------------------------------------------------------

PROJECT_REGISTRY = [
    # -----------------------------------------------------------------------
    # 1. EXPLAINABLE RAG CHATBOT (Research) — HIGH PRIORITY
    # -----------------------------------------------------------------------
    {
        "name": "Explainable Hybrid KG-RAG Chatbot (Research)",
        "repo_url": "https://github.com/kaisarfardin6620/explainable-rag-chatbot",
        "stack_tags": "Python · FastAPI · OpenAI GPT-4o · Pinecone · Neo4j · NLI",
        "include": True,
        "bullets": [
            "Designed a research-grade Hybrid RAG system combining Pinecone vector search "
            "with Neo4j knowledge-graph traversal to reduce LLM hallucinations and provide "
            "claim-level explainability.",
            "Built a post-hoc NLI verification layer that abstains from answering when "
            "confidence falls below 0.4; applied Freeman's Degree Centrality to weight "
            "evidence from authoritative graph entities.",
            "Architected three ablation modes (hybrid, rag_only, kg_only) and a "
            "benchmark automation script generating comparative F1, semantic similarity, "
            "and latency reports.",
        ],
    },
    # -----------------------------------------------------------------------
    # 2. MAGICTALE
    # -----------------------------------------------------------------------
    {
        "name": "MagicTale — AI Children's Storytelling Platform",
        "repo_url": "https://github.com/kaisarfardin6620/magictale",
        "stack_tags": "Python · Django 5 · Celery · OpenAI GPT-4o · DALL-E 3 · ElevenLabs · WebSockets",
        "include": True,
        "bullets": [
            "Engineered an async AI content pipeline (Celery + Redis) that generates "
            "personalized stories (GPT-4o), cover illustrations (DALL-E 3), and voice "
            "narration (ElevenLabs TTS) without blocking the HTTP layer.",
            "Implemented real-time story-generation progress over Django Channels "
            "WebSockets; integrated Google OAuth2, Apple Sign-In, FCM push notifications, "
            "and RevenueCat subscription webhooks.",
            "Containerized the full stack (Django/Daphne + Celery + Redis + PostgreSQL + "
            "Nginx) with Docker Compose.",
        ],
    },
    # -----------------------------------------------------------------------
    # 3. REHO AI FINANCE MICROSERVICE
    # -----------------------------------------------------------------------
    {
        "name": "Reho AI Finance Microservice",
        "repo_url": "https://github.com/kaisarfardin6620/Reho-AI-Service",
        "stack_tags": "Python · FastAPI · OpenAI GPT-4o · MongoDB · Redis · WebSockets",
        "include": True,
        "bullets": [
            "Built an AI microservice that dynamically injects live user financial data "
            "into the GPT-4o system prompt, enabling context-aware conversational advice "
            "over real-time WebSockets.",
            "Developed admin intelligence endpoints auto-generating user 360 summaries, "
            "spending heatmaps, and debt-to-income risk scores using GPT-4o.",
            "Scheduled nightly background jobs to pre-compute heavy analytics reports, "
            "reducing dashboard load times via Redis caching.",
        ],
    },
    # -----------------------------------------------------------------------
    # 4. QUORA QUESTION PAIR (SBERT) — NLP HIGHLIGHT
    # -----------------------------------------------------------------------
    {
        "name": "Quora Question Pair Classification (SBERT + Deep Learning)",
        "repo_url": "https://github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning",
        "stack_tags": "Python · SBERT · Siamese Networks · Hugging Face Transformers · PyTorch",
        "include": True,
        "bullets": [
            "Fine-tuned Sentence-BERT (SBERT) on the Quora Question Pairs dataset to "
            "detect semantic duplicates, achieving 89% F1 with a Siamese network architecture.",
            "Compared SBERT embeddings + cosine similarity against BiLSTM and cross-encoder "
            "baselines; SBERT outperformed traditional NLP approaches by 12% F1.",
            "Implemented hard negative mining to improve contrastive training and reduce "
            "false positives in semantic similarity tasks.",
        ],
    },
    # -----------------------------------------------------------------------
    # 5. LUNG CANCER IMAGENET — MEDICAL CV HIGHLIGHT
    # -----------------------------------------------------------------------
    {
        "name": "LungCancer-ImageNet — Transfer Learning for Medical Imaging",
        "repo_url": "https://github.com/kaisarfardin6620/LungCancer-ImageNet",
        "stack_tags": "Python · TensorFlow · ResNet/VGG · Transfer Learning · Grad-CAM",
        "include": True,
        "bullets": [
            "Fine-tuned a pre-trained ImageNet CNN (ResNet/VGG) on lung cancer CT scan "
            "datasets to classify benign vs. malignant nodules.",
            "Applied transfer learning with data augmentation (rotation, flipping, contrast "
            "adjustment) to overcome medical imaging data scarcity.",
            "Visualized model interpretability via Grad-CAM activation maps; evaluated "
            "with ROC-AUC and precision-recall curves.",
        ],
    },
    # -----------------------------------------------------------------------
    # 6. HR AI ASSISTANT — optional, set include=True to show
    # -----------------------------------------------------------------------
    {
        "name": "HR AI Assistant",
        "repo_url": "https://github.com/kaisarfardin6620/Hr-Ai-Assistant",
        "stack_tags": "Python · LLM (OpenAI/Gemini) · FastAPI · RAG · Vector DB",
        "include": False,
        "bullets": [
            "Built an HR-domain AI assistant using LLM + RAG, enabling employees to "
            "query HR policies, payroll info, and leave management via natural language.",
            "Implemented document ingestion pipeline (PDF/DOCX to chunks to embeddings "
            "to vector store) for accurate, citation-backed HR policy retrieval.",
            "Designed intent-classification prompts to route queries to the appropriate "
            "HR function, reducing HR ticket volume.",
        ],
    },
    # -----------------------------------------------------------------------
    # 7. BONDLY AI FINANCIAL ASSISTANT — optional
    # -----------------------------------------------------------------------
    {
        "name": "Bondly AI — Financial Assistant",
        "repo_url": "https://github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant",
        "stack_tags": "Python · LLM (OpenAI/Gemini) · FastAPI · RAG · Vector DB",
        "include": False,
        "bullets": [
            "Created an AI financial assistant that answers personal finance, investment, "
            "and budgeting questions using LLM-powered RAG over financial knowledge bases.",
            "Engineered a context-aware conversation memory system ensuring coherent "
            "multi-turn financial Q&A sessions.",
            "Integrated real-time market data retrieval to augment LLM responses with "
            "up-to-date financial information.",
        ],
    },
    # -----------------------------------------------------------------------
    # 8. BIBLE AI ASSISTANT — optional
    # -----------------------------------------------------------------------
    {
        "name": "Bible AI Assistant",
        "repo_url": "https://github.com/kaisarfardin6620/Bible-Ai-Assistant",
        "stack_tags": "Python · LLM (OpenAI/Gemini) · RAG · Vector DB · FastAPI",
        "include": False,
        "bullets": [
            "Built a domain-specific AI assistant for Biblical studies using RAG over "
            "the full Bible corpus, enabling precise verse lookup and contextual Q&A.",
            "Designed an embedding and retrieval pipeline that supports cross-book "
            "thematic searches and multi-verse context windows.",
            "Implemented conversational memory for multi-turn scripture exploration.",
        ],
    },
    # -----------------------------------------------------------------------
    # 9. AUTOENCODER ANOMALY DETECTION — optional
    # -----------------------------------------------------------------------
    {
        "name": "Autoencoder Anomaly Detection",
        "repo_url": "https://github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection",
        "stack_tags": "Python · TensorFlow/Keras · Autoencoder · LSTM-AE · Scikit-learn",
        "include": False,
        "bullets": [
            "Built a convolutional and LSTM autoencoder for unsupervised anomaly detection "
            "in time-series and image data; flagged anomalies via reconstruction error thresholding.",
            "Validated on ECG5000 and credit card fraud datasets; LSTM-AE achieved 0.93 "
            "AUC-ROC on fraud detection without any labeled anomaly samples during training.",
            "Implemented dynamic threshold calibration using the 95th percentile of "
            "reconstruction errors on normal validation data, minimizing false positives.",
        ],
    },
    # -----------------------------------------------------------------------
    # 10. REAL VS. FAKE NEWS — optional
    # -----------------------------------------------------------------------
    {
        "name": "Real vs. Fake News Classifier",
        "repo_url": "https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier",
        "stack_tags": "Python · BERT · TF-IDF · LSTM · Pandas · NLTK",
        "include": False,
        "bullets": [
            "Developed a fake news detection model achieving 96% accuracy using fine-tuned "
            "BERT on a 40K-article dataset, outperforming TF-IDF + SVM baseline by 8%.",
            "Built a bidirectional LSTM baseline to compare sequence-modeled vs. "
            "transformer approaches for misinformation detection.",
            "Applied LIME/SHAP to surface linguistic patterns associated with fake news.",
        ],
    },
    # -----------------------------------------------------------------------
    # 11. NLP TWITTER SENTIMENT — optional
    # -----------------------------------------------------------------------
    {
        "name": "NLP Twitter Sentiment Analysis",
        "repo_url": "https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis",
        "stack_tags": "Python · DistilBERT · TF-IDF · Hugging Face · NLTK · Pandas",
        "include": False,
        "bullets": [
            "Built a Twitter sentiment classifier (positive/negative/neutral) using "
            "fine-tuned DistilBERT, achieving 89% accuracy on the Sentiment140 dataset.",
            "Compared classical NLP (TF-IDF + Logistic Regression) against transformer "
            "models; transformers improved F1 by 15% on informal Twitter text.",
            "Implemented text normalization pipeline for social media noise (hashtags, "
            "mentions, URLs, slang) using regex and NLTK.",
        ],
    },
    # -----------------------------------------------------------------------
    # 12. LSTM IMDB SENTIMENT — optional
    # -----------------------------------------------------------------------
    {
        "name": "LSTM for IMDb Sentiment Analysis",
        "repo_url": "https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis",
        "stack_tags": "Python · TensorFlow/Keras · Bi-LSTM · Word Embeddings · NLTK",
        "include": False,
        "bullets": [
            "Trained a Bidirectional LSTM on IMDb movie reviews for binary sentiment "
            "classification, achieving 91% test accuracy with pre-trained word embeddings.",
            "Explored the impact of LSTM depth, dropout, and embedding dimensionality "
            "on model generalization; documented findings in an ablation study.",
            "Compared LSTM vs. GRU vs. simple RNN; Bi-LSTM outperformed unidirectional "
            "RNNs by 4% accuracy.",
        ],
    },
    # -----------------------------------------------------------------------
    # 13. NLP SPAM CLASSIFICATION — optional
    # -----------------------------------------------------------------------
    {
        "name": "NLP Spam Classification with Word Embeddings",
        "repo_url": "https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings",
        "stack_tags": "Python · TensorFlow/Keras · Word2Vec · GloVe · LSTM · NLTK",
        "include": False,
        "bullets": [
            "Compared spam classification approaches using BoW, TF-IDF, Word2Vec, and "
            "GloVe; GloVe + LSTM achieved 98.5% accuracy on the SMS Spam Collection.",
            "Implemented pre-trained GloVe embeddings as LSTM input layer, demonstrating "
            "transfer learning benefits for short-text NLP tasks.",
            "Analyzed false-negative vs. false-positive rates to optimize the "
            "precision-recall trade-off for production spam filtering.",
        ],
    },
    # -----------------------------------------------------------------------
    # 14. TEXT PAIR CLASSIFICATION — optional
    # -----------------------------------------------------------------------
    {
        "name": "Text Pair Classification",
        "repo_url": "https://github.com/kaisarfardin6620/Text-Pair-Classification",
        "stack_tags": "Python · BERT/RoBERTa · Hugging Face · PyTorch · Scikit-learn",
        "include": False,
        "bullets": [
            "Built a text pair classification system using fine-tuned BERT/RoBERTa for "
            "NLI, semantic similarity, and paraphrase detection.",
            "Implemented cross-encoder and bi-encoder architectures; cross-encoder achieved "
            "91% accuracy on MultiNLI; bi-encoder was 40x faster at inference.",
            "Designed a unified training framework supporting multiple text-pair tasks "
            "via task-specific classification heads.",
        ],
    },
    # -----------------------------------------------------------------------
    # 15. LEAF DISEASE CLASSIFIER — optional
    # -----------------------------------------------------------------------
    {
        "name": "LeafDiseaseClassifier — Plant Disease Detection",
        "repo_url": "https://github.com/kaisarfardin6620/LeafDiseaseClassifier",
        "stack_tags": "Python · TensorFlow/Keras · CNN · Transfer Learning · OpenCV",
        "include": False,
        "bullets": [
            "Trained a CNN to classify 38 plant disease categories from leaf images "
            "(PlantVillage dataset), achieving >95% validation accuracy using transfer learning.",
            "Implemented image preprocessing pipeline (resizing, normalization, augmentation) "
            "to handle variable field-photo conditions; deployed model as a prediction API.",
            "Applied Grad-CAM to visualize disease-relevant leaf regions, making predictions "
            "interpretable for agricultural practitioners.",
        ],
    },
    # -----------------------------------------------------------------------
    # 16. BANGLADESHI MEDICINAL LEAF — optional
    # -----------------------------------------------------------------------
    {
        "name": "Bangladeshi Medicinal Leaf Classification",
        "repo_url": "https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification",
        "stack_tags": "Python · TensorFlow/Keras · CNN · Transfer Learning · OpenCV",
        "include": False,
        "bullets": [
            "Built a CNN classifier for 30 Bangladeshi medicinal plant species from leaf "
            "imagery, supporting local herbal medicine identification with >94% accuracy.",
            "Curated and augmented a custom dataset of Bangladeshi flora; applied "
            "domain-specific preprocessing to handle outdoor photography variability.",
            "Deployed as a mobile-friendly inference API for field botanists and "
            "traditional medicine practitioners.",
        ],
    },
    # -----------------------------------------------------------------------
    # 17. MARINE LIFE CLASSIFIER — optional
    # -----------------------------------------------------------------------
    {
        "name": "Marine Life Classifier",
        "repo_url": "https://github.com/kaisarfardin6620/Marine_Life_Classifier",
        "stack_tags": "Python · TensorFlow/Keras · CNN · Transfer Learning · OpenCV",
        "include": False,
        "bullets": [
            "Built a multi-class marine species classifier using fine-tuned CNN on "
            "underwater imagery, enabling automated biodiversity monitoring.",
            "Addressed domain-specific challenges (water distortion, low contrast, "
            "occlusion) through custom augmentation strategies.",
            "Achieved competitive accuracy across 30+ species categories; validated "
            "with Grad-CAM to confirm biologically relevant feature attention.",
        ],
    },
    # -----------------------------------------------------------------------
    # 18. FLOWERNET COMPARISON — optional
    # -----------------------------------------------------------------------
    {
        "name": "FlowerNet — CNN Architecture Comparison",
        "repo_url": "https://github.com/kaisarfardin6620/FlowerNet-Comparison",
        "stack_tags": "Python · TensorFlow/Keras · ResNet · VGG · EfficientNet · MobileNet",
        "include": False,
        "bullets": [
            "Conducted a comparative study of 5 CNN architectures (VGG16, ResNet50, "
            "EfficientNetB0, MobileNetV2, custom CNN) on the Oxford 102 Flowers dataset.",
            "Benchmarked architectures on accuracy, inference speed, and parameter count; "
            "EfficientNetB0 delivered the best accuracy-latency trade-off.",
            "Published training curves, confusion matrices, and per-class F1 scores for "
            "each model as a reproducible architecture selection guide.",
        ],
    },
    # -----------------------------------------------------------------------
    # 19. APPLENET AE — optional
    # -----------------------------------------------------------------------
    {
        "name": "AppleNet-AE — Apple Disease Detection (Autoencoder)",
        "repo_url": "https://github.com/kaisarfardin6620/AppleNet-AE",
        "stack_tags": "Python · TensorFlow/Keras · CNN · Autoencoder · NumPy",
        "include": False,
        "bullets": [
            "Built a convolutional autoencoder for apple disease detection using "
            "unsupervised feature learning to identify anomalies in fruit images.",
            "Applied reconstruction-error thresholding to distinguish healthy vs. "
            "diseased apple samples, demonstrating anomaly detection in agricultural AI.",
            "Evaluated performance using precision, recall, and visual reconstruction "
            "comparisons across disease categories.",
        ],
    },
    # -----------------------------------------------------------------------
    # 20. FASHION MNIST SUP/SEMISUP — optional
    # -----------------------------------------------------------------------
    {
        "name": "Fashion-MNIST — Supervised and Semi-Supervised Learning",
        "repo_url": "https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup",
        "stack_tags": "Python · TensorFlow/Keras · CNN · Semi-Supervised Learning · Scikit-learn",
        "include": False,
        "bullets": [
            "Compared supervised and semi-supervised learning strategies on Fashion-MNIST; "
            "pseudo-labeling with 20% labeled data matched fully supervised accuracy within 2-3%.",
            "Implemented a label-propagation pipeline that iteratively assigns soft labels "
            "to unlabeled samples, reducing annotation costs.",
            "Achieved >91% test accuracy with the supervised CNN baseline; analyzed the "
            "accuracy-label-budget trade-off across five experimental configurations.",
        ],
    },
    # -----------------------------------------------------------------------
    # 21. BUTTERFLY CLASSIFIER — optional
    # -----------------------------------------------------------------------
    {
        "name": "Butterfly Classifier",
        "repo_url": "https://github.com/kaisarfardin6620/Butterfly-Classifier",
        "stack_tags": "Python · TensorFlow/Keras · EfficientNet/MobileNet · Transfer Learning",
        "include": False,
        "bullets": [
            "Fine-tuned EfficientNet/MobileNet on a 75-class butterfly species dataset, "
            "achieving >93% top-1 accuracy with progressive layer unfreezing.",
            "Applied heavy augmentation (random crop, flip, color jitter, mixup) to "
            "combat class imbalance and overfitting on a small-scale dataset.",
            "Deployed as a lightweight inference endpoint suitable for edge/mobile deployment.",
        ],
    },
    # -----------------------------------------------------------------------
    # 22. CAT VS DOG — optional
    # -----------------------------------------------------------------------
    {
        "name": "Cat vs. Dog Classification",
        "repo_url": "https://github.com/kaisarfardin6620/Cat-Vs-Dog-Classification",
        "stack_tags": "Python · TensorFlow/Keras · VGG16/ResNet · Transfer Learning",
        "include": False,
        "bullets": [
            "Trained VGG16-based transfer learning model for binary cat/dog classification, "
            "achieving >98% accuracy on the Kaggle Dogs vs. Cats dataset.",
            "Implemented progressive fine-tuning (frozen base then unfreeze top blocks) "
            "to efficiently adapt ImageNet features to the binary classification task.",
            "Benchmarked custom CNN vs. transfer learning; transfer learning converged "
            "5x faster and achieved 6% higher accuracy.",
        ],
    },
    # -----------------------------------------------------------------------
    # 23. SHOE CLASSIFIER — optional
    # -----------------------------------------------------------------------
    {
        "name": "Shoe Classifier",
        "repo_url": "https://github.com/kaisarfardin6620/Shoe_Classifier",
        "stack_tags": "Python · TensorFlow/Keras · CNN · Transfer Learning · Flask/FastAPI",
        "include": False,
        "bullets": [
            "Developed a shoe style and type classifier using transfer-learned CNN, "
            "distinguishing 10+ categories with >90% accuracy.",
            "Built end-to-end inference pipeline with image upload, preprocessing, "
            "prediction, and top-3 confidence score display.",
            "Deployed model as a Flask/FastAPI web service with model versioning for A/B evaluation.",
        ],
    },
    # -----------------------------------------------------------------------
    # 24. CNN PREPROCESSINGS — optional
    # -----------------------------------------------------------------------
    {
        "name": "CNN Preprocessings — Image Augmentation Toolkit",
        "repo_url": "https://github.com/kaisarfardin6620/Cnn_Preprocessings",
        "stack_tags": "Python · TensorFlow/Keras · OpenCV · NumPy · Albumentations",
        "include": False,
        "bullets": [
            "Built a reusable image preprocessing and augmentation library for CNN "
            "pipelines, implementing 15+ transformations (rotation, zoom, shear, noise, "
            "elastic deformation).",
            "Demonstrated impact of various preprocessing strategies on model accuracy "
            "across benchmark datasets (CIFAR-10, ImageNet subsets).",
            "Designed as a configurable pipeline compatible with TensorFlow tf.data "
            "for GPU-accelerated preprocessing.",
        ],
    },
    # -----------------------------------------------------------------------
    # 25. CNN VISUALS — optional
    # -----------------------------------------------------------------------
    {
        "name": "CNN Visuals — Convolutional Network Visualization",
        "repo_url": "https://github.com/kaisarfardin6620/Cnn_Visuals",
        "stack_tags": "Python · TensorFlow/Keras · Grad-CAM · t-SNE · Matplotlib",
        "include": False,
        "bullets": [
            "Implemented CNN interpretability tools including Grad-CAM, filter visualization, "
            "and activation maximization to explain what features convolutional layers learn.",
            "Built t-SNE embedding visualizations of penultimate layer activations to "
            "analyze class separation and model confidence.",
            "Produced a pedagogical notebook suite covering saliency maps, occlusion "
            "sensitivity, and feature map visualization.",
        ],
    },
    # -----------------------------------------------------------------------
    # 26. CUSTOMER CHURN PREDICTION — optional
    # -----------------------------------------------------------------------
    {
        "name": "Customer Churn Prediction",
        "repo_url": "https://github.com/kaisarfardin6620/Customer-Churn-Prediction",
        "stack_tags": "Python · Scikit-learn · XGBoost · SHAP · Pandas · Matplotlib",
        "include": False,
        "bullets": [
            "Built a customer churn prediction model (XGBoost/Random Forest) on telecom "
            "data, achieving >85% AUC-ROC; identified top churn drivers via SHAP feature importance.",
            "Performed EDA and feature engineering (tenure buckets, usage ratios) to surface "
            "behavioral signals predictive of churn.",
            "Evaluated multiple classifiers with cross-validation; packaged best model as "
            "a REST API endpoint.",
        ],
    },
    # -----------------------------------------------------------------------
    # 27. LUNG CANCER PREDICTION (ML) — optional
    # -----------------------------------------------------------------------
    {
        "name": "Lung Cancer Prediction using Machine Learning",
        "repo_url": "https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.",
        "stack_tags": "Python · Scikit-learn · XGBoost · SHAP · Pandas · Matplotlib",
        "include": False,
        "bullets": [
            "Developed a lung cancer risk prediction model using clinical tabular features; "
            "achieved 92% accuracy and 0.95 AUC-ROC with XGBoost.",
            "Applied SHAP explainability to identify top risk factors (smoking duration, "
            "chronic cough, age) and produce patient-level risk explanations.",
            "Handled class imbalance using SMOTE oversampling; evaluated model fairness "
            "across demographic groups.",
        ],
    },
    # -----------------------------------------------------------------------
    # 28. BREAST CANCER SURVIVAL — optional
    # -----------------------------------------------------------------------
    {
        "name": "Breast Cancer Survival Prediction",
        "repo_url": "https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.",
        "stack_tags": "Python · Scikit-learn · XGBoost · SHAP · Pandas · Seaborn",
        "include": False,
        "bullets": [
            "Built a breast cancer survival prediction model using clinical and genomic "
            "features; achieved 88% accuracy with XGBoost and 0.92 AUC-ROC.",
            "Applied SHAP to identify the most predictive biomarkers (tumor size, lymph "
            "node status, ER/PR receptor status).",
            "Compared binary classification and time-to-event analysis; analyzed "
            "Kaplan-Meier curves across risk-stratified groups.",
        ],
    },
    # -----------------------------------------------------------------------
    # 29. WINE QUALITY — optional
    # -----------------------------------------------------------------------
    {
        "name": "Wine Quality Testing",
        "repo_url": "https://github.com/kaisarfardin6620/Wine-Quality-Testing-",
        "stack_tags": "Python · Scikit-learn · XGBoost · Pandas · Seaborn · Matplotlib",
        "include": False,
        "bullets": [
            "Built a wine quality regression and classification model using physicochemical "
            "features from the UCI Wine Quality dataset.",
            "Applied feature engineering (interaction terms, polynomial features) and "
            "hyperparameter tuning (GridSearchCV); achieved RMSE of 0.58 on quality score.",
            "Conducted thorough EDA revealing strong correlations between alcohol content, "
            "volatile acidity, and perceived quality.",
        ],
    },
    # -----------------------------------------------------------------------
    # 30. SALES FORECASTING — optional
    # -----------------------------------------------------------------------
    {
        "name": "Sales Forecasting Regression",
        "repo_url": "https://github.com/kaisarfardin6620/Sales-Forecasting-Regression",
        "stack_tags": "Python · Scikit-learn · XGBoost · LightGBM · Pandas · Matplotlib",
        "include": False,
        "bullets": [
            "Built sales forecasting models (Linear Regression, Random Forest, XGBoost, "
            "LightGBM) to predict weekly store sales; LightGBM achieved lowest RMSE.",
            "Engineered time-series features (lag variables, rolling means, holiday flags, "
            "promotional indicators) from Rossmann Store Sales data.",
            "Applied log transformation on target variable and time-series cross-validation "
            "to prevent data leakage.",
        ],
    },
    # -----------------------------------------------------------------------
    # 31. WEATHER FORECASTING MODELS — optional
    # -----------------------------------------------------------------------
    {
        "name": "Weather Forecasting Models",
        "repo_url": "https://github.com/kaisarfardin6620/Weather_Forecasting_Models",
        "stack_tags": "Python · TensorFlow/Keras · LSTM · Prophet · Pandas · Matplotlib",
        "include": False,
        "bullets": [
            "Developed and benchmarked multiple time-series forecasting models (LSTM, GRU, "
            "Prophet) for weather prediction; LSTM achieved lowest RMSE on 5-day forecasts.",
            "Engineered temporal features (lag variables, rolling statistics, Fourier "
            "seasonality terms) to capture daily and seasonal patterns.",
            "Compared model performance on MAE, RMSE, and MAPE across multiple "
            "meteorological variables.",
        ],
    },
    # -----------------------------------------------------------------------
    # 32. WEATHER RAINFALL PREDICTION — optional
    # -----------------------------------------------------------------------
    {
        "name": "Weather Rainfall Prediction",
        "repo_url": "https://github.com/kaisarfardin6620/Weather-rainfall-prediction",
        "stack_tags": "Python · Scikit-learn · XGBoost · Pandas · NumPy · Matplotlib",
        "include": False,
        "bullets": [
            "Developed a rainfall prediction classifier (rain/no-rain) using meteorological "
            "features; achieved 86% accuracy with XGBoost.",
            "Performed comprehensive EDA on Australia weather dataset (145K records); "
            "handled missing values with median/mode imputation and outlier removal.",
            "Tuned hyperparameters via RandomizedSearchCV; analyzed seasonal patterns "
            "with geographic visualizations.",
        ],
    },
    # -----------------------------------------------------------------------
    # 33. AI IMAGE CREATOR (GLIMMCATCHER) — optional
    # -----------------------------------------------------------------------
    {
        "name": "AI Image Creator — GlimmCatcher",
        "repo_url": "https://github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher",
        "stack_tags": "Python · OpenAI DALL-E · FastAPI/Flask · HTML/CSS/JS",
        "include": False,
        "bullets": [
            "Developed an AI image generation web app using OpenAI DALL-E API, enabling "
            "users to create high-quality images from natural language prompts.",
            "Built a clean, responsive frontend and FastAPI backend; implemented prompt "
            "engineering patterns to improve generation quality.",
            "Added image history, download, and sharing features; handled API rate "
            "limiting and error recovery gracefully.",
        ],
    },
    # -----------------------------------------------------------------------
    # 34. WINGMAN AI ASSISTANT BACKEND — optional
    # -----------------------------------------------------------------------
    {
        "name": "Wingman — AI Assistant Backend",
        "repo_url": "https://github.com/kaisarfardin6620/wingman",
        "stack_tags": "Python · Django 5 · Celery · OpenAI · Google GenAI · WebSockets · PostgreSQL",
        "include": False,
        "bullets": [
            "Developed a full-featured Django REST API backend powering an AI chat assistant "
            "with JWT-secured endpoints, real-time WebSocket chat (Django Channels), and "
            "subscription tier management.",
            "Integrated OpenAI and Google GenAI (Gemini) for multi-modal AI responses; "
            "implemented tiktoken-based token counting for accurate usage billing.",
            "Built an async task pipeline with Celery + Redis for background AI processing.",
        ],
    },
    # -----------------------------------------------------------------------
    # 35. BENJAMINKLEY 3D SCANNER — optional
    # -----------------------------------------------------------------------
    {
        "name": "Benjaminkley — 3D Head Scanner and Biometric Analysis",
        "repo_url": "https://github.com/kaisarfardin6620/benjaminkley",
        "stack_tags": "Python · Django 5 · Celery · KeenTools API · trimesh · numpy · AWS S3",
        "include": False,
        "bullets": [
            "Designed an end-to-end 3D scanning pipeline: uploads multi-image datasets to "
            "KeenTools API for 3D reconstruction, downloads .obj meshes, and calculates "
            "biometric measurements using trimesh and numpy.",
            "Implemented async scan processing with Celery + Redis; auto-generated biometric "
            "PDF reports and delivered FCM push notifications; stored assets on AWS S3.",
            "Built role-based access control (Admin, Doctor, Provider, Client) with email "
            "OTP verification and JWT authentication.",
        ],
    },
    # -----------------------------------------------------------------------
    # 36. RAI BACKEND — optional
    # -----------------------------------------------------------------------
    {
        "name": "Rai Backend — AI Community Platform",
        "repo_url": "https://github.com/kaisarfardin6620/Rai_Backend",
        "stack_tags": "Python · Django 5 · DRF · Celery · Redis · PostgreSQL · OpenAI · Docker",
        "include": False,
        "bullets": [
            "Built a scalable AI-powered community platform backend with real-time chat, "
            "notifications, and role-based user management.",
            "Integrated OpenAI for AI-assisted content moderation and personalized "
            "recommendations; implemented async task processing with Celery + Redis.",
            "Designed RESTful APIs supporting mobile and web clients; containerized with "
            "Docker Compose.",
        ],
    },
    # -----------------------------------------------------------------------
    # 37. MAIZ FASTAPI — optional
    # -----------------------------------------------------------------------
    {
        "name": "MAIZ FastAPI — AI Data Service",
        "repo_url": "https://github.com/kaisarfardin6620/maiz-fastapi",
        "stack_tags": "Python · FastAPI · OpenAI · PostgreSQL · Docker",
        "include": False,
        "bullets": [
            "Engineered a high-performance FastAPI microservice for AI-driven data processing, "
            "exposing RESTful endpoints consumed by mobile and web frontends.",
            "Integrated OpenAI API for intelligent data analysis; implemented async I/O "
            "patterns for low-latency response times.",
        ],
    },
    # -----------------------------------------------------------------------
    # 38. DELUX AI — optional
    # -----------------------------------------------------------------------
    {
        "name": "DELUX AI — AI Feature Service",
        "repo_url": "https://github.com/kaisarfardin6620/DELUX_AI",
        "stack_tags": "Python · FastAPI/Django · OpenAI · PostgreSQL · Docker",
        "include": False,
        "bullets": [
            "Developed an AI service layer providing intelligent features (recommendations, "
            "content generation) to client applications via clean REST APIs.",
            "Implemented multi-model AI integration with OpenAI; designed for horizontal "
            "scaling with Docker containerization.",
        ],
    },
]

# ---------------------------------------------------------------------------
# GENERATOR — do not edit below this line unless you know what you are doing
# ---------------------------------------------------------------------------

def build_resume():
    out = []

    # Header
    g = PERSONAL["github"]
    out.append(f"# {PERSONAL['name']}")
    out.append(f"**{PERSONAL['title']}**  ")
    out.append(f"{PERSONAL['location']}  ")
    out.append(
        f"GitHub: [{g}](https://{g}) | "
        f"Email: {PERSONAL['email']} | "
        f"Phone: {PERSONAL['phone']}"
    )
    out.append("")
    out.append("---")
    out.append("")

    # Education
    out.append("## Education")
    out.append("")
    for edu in EDUCATION:
        status = edu["status"]
        out.append(f"**{edu['degree']}** — {edu['university']} *({status})*  ")
    out.append("")
    out.append("---")
    out.append("")

    # Skills
    out.append("## Technical Skills")
    out.append("")
    out.append("| Category | Skills |")
    out.append("|---|---|")
    for cat, skills in SKILLS:
        out.append(f"| **{cat}** | {skills} |")
    out.append("")
    out.append("---")
    out.append("")

    # Projects (included only)
    included = [p for p in PROJECT_REGISTRY if p.get("include")]
    out.append("## Projects")
    out.append("")

    for proj in included:
        repo = proj["repo_url"]
        short = repo.replace("https://", "")
        out.append(f"### {proj['name']}  ")
        out.append(f"`{proj['stack_tags']}`  ")
        out.append(f"[{short}]({repo})")
        out.append("")
        for bullet in proj["bullets"][:3]:
            out.append(f"- {bullet}")
        out.append("")
        out.append("---")
        out.append("")

    # Additional projects table
    excluded = [p for p in PROJECT_REGISTRY if not p.get("include")]
    if excluded:
        out.append("## Additional Projects")
        out.append("")
        out.append("Set `include=True` in `generate_resume.py` to activate any of these:")
        out.append("")
        out.append("| Project | GitHub |")
        out.append("|---|---|")
        for proj in excluded:
            name = proj["name"]
            url = proj["repo_url"]
            out.append(f"| {name} | [{url}]({url}) |")
        out.append("")
        out.append("---")
        out.append("")

    # Footer
    out.append("## Open to")
    out.append(
        "New AI Engineering roles in Dhaka or remote. "
        "Interests include LLM systems, RAG pipelines, AI microservices, "
        "computer vision, and production ML backends."
    )
    out.append("")
    out.append("---")
    out.append("")
    month = datetime.datetime.now().strftime("%B %Y")
    out.append(f"*Last updated: {month} — generated by `resume/generate_resume.py`*")

    return "\n".join(out)


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    output_path = script_dir / "RESUME_DRAFT.md"
    content = build_resume()
    output_path.write_text(content, encoding="utf-8")
    included_count = sum(1 for p in PROJECT_REGISTRY if p.get("include"))
    print(f"RESUME_DRAFT.md written to {output_path}")
    print(f"  Projects shown: {included_count}/{len(PROJECT_REGISTRY)}")
    print("  Edit 'include' flags in PROJECT_REGISTRY to change which projects appear.")
