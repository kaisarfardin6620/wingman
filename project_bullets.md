# Project Bullets
# All projects with descriptions, tech stack, and GitHub links.
# Pick the most relevant ones for your target role and paste into resume_template.md.
# For AI/Backend Engineer roles: prioritize Backend AI, then NLP, then CV.

---

## BACKEND / PRODUCTION AI PROJECTS

### Explainable Hybrid KG-RAG Chatbot
Tech: FastAPI, Neo4j, Pinecone, OpenAI GPT-4o, Python
GitHub: https://github.com/kaisarfardin6620/explainable-rag-chatbot
Category: Backend AI, Research
- Engineered a research-grade hybrid RAG system combining vector search (Pinecone) with knowledge graph reasoning (Neo4j) to mitigate hallucinations and improve answer trustworthiness.
- Implemented claim-level NLI verification and graph centrality scoring to produce structured reasoning chains and citations for every response.
- Built ablation modes (rag_only, kg_only, hybrid) with automated benchmarking pipeline measuring F1, semantic similarity, and latency.

### MagicTale AI Storytelling Platform
Tech: Django, Celery, Redis, WebSockets, OpenAI GPT-4o, DALL-E 3, ElevenLabs, Firebase, Docker
GitHub: https://github.com/kaisarfardin6620/magictale
Category: Backend AI, Multimodal
- Developed a production-grade async storytelling backend that generates personalized children's stories, AI cover illustrations (DALL-E 3), and voice narration (ElevenLabs) via a Celery pipeline.
- Implemented real-time progress updates over Django Channels WebSockets and push notifications via Firebase Cloud Messaging.
- Integrated RevenueCat webhooks for subscription management and supported Google/Apple OAuth2 social login.

### Reho AI Finance Microservice
Tech: FastAPI, OpenAI GPT-4o, MongoDB, Redis, Docker, Nginx
GitHub: https://github.com/kaisarfardin6620/Reho-AI-Service
Category: Backend AI, Microservices
- Built an async AI microservice providing context-aware financial chat, admin dashboard intelligence, and automated spending analysis by querying real user MongoDB transaction data.
- Engineered background scheduled jobs for nightly report pre-computation, reducing dashboard load times significantly.
- Implemented 50/30/20 budget analysis, debt strategy comparison (Avalanche vs. Snowball), and risk scoring for individual users.

### Wingman AI Chat Platform
Tech: Django, Django Channels, WebSockets, OpenAI, Redis, PostgreSQL, Docker
GitHub: https://github.com/kaisarfardin6620/wingman
Category: Backend AI, Real-time
- Designed and deployed a full-stack conversational AI platform with real-time WebSocket chat, user authentication, and subscription management.
- Built modular Django apps (authentication, chat, dashboard, subscription) behind Nginx with Docker containerization.

### Rai Backend (Django AI Platform)
Tech: Django, Docker, Nginx, PostgreSQL
GitHub: https://github.com/kaisarfardin6620/Rai_Backend
Category: Backend AI
- Built a multi-app Django backend with AI inference modules, community features, subscription management, and support ticketing, deployed via Docker Compose with Nginx.

### Maiz FastAPI Backend
Tech: FastAPI, Python, Docker
GitHub: https://github.com/kaisarfardin6620/maiz-fastapi
Category: Backend AI
- Developed a modular FastAPI application with structured app layout following production best practices for routing, dependency injection, and configuration management.

### DELUX AI FastAPI Service
Tech: FastAPI, Docker, PostgreSQL, Redis
GitHub: https://github.com/kaisarfardin6620/DELUX_AI
Category: Backend AI
- Implemented a containerized FastAPI service with JWT authentication, rate limiting, structured logging, and database management for AI-powered endpoints.

### benjaminkley Backend
Tech: Django/FastAPI, Python, Docker
GitHub: https://github.com/kaisarfardin6620/benjaminkley
Category: Backend AI

---

## AI ASSISTANT / CONVERSATIONAL AI PROJECTS

### HR AI Assistant Suite
Tech: Python, OpenAI GPT, Flask
GitHub: https://github.com/kaisarfardin6620/Hr-Ai-Assistant
Category: Conversational AI
- Developed a modular suite of production-ready HR AI backends covering Compensation, Compliance, Talent Acquisition, and Organizational Development domains with conversation history and caching.
- Supports both typed and transcribed (voice) input; ready for integration with Flask or FastAPI REST APIs.

### Bondly AI Financial Coach
Tech: Python, OpenAI GPT
GitHub: https://github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant
Category: Conversational AI
- Engineered an emotionally intelligent financial coaching backend with dynamic context injection, micro-consent for sensitive topics, and adaptive tone based on user mood and financial profile.

### Bible AI Assistant
Tech: Python, OpenAI GPT
GitHub: https://github.com/kaisarfardin6620/Bible-Ai-Assistant
Category: Conversational AI
- Built a domain-specific AI assistant for Biblical Q&A with structured prompting and context management.

### Glimmcatcher AI Image Creator
Tech: Python, OpenAI DALL-E
GitHub: https://github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher
Category: Generative AI
- Built an AI image generation assistant with an interactive CLI allowing users to generate, analyze, and save creative images using OpenAI image models.

---

## COMPUTER VISION / IMAGE CLASSIFICATION PROJECTS

### Bangladeshi Medicinal Leaf Classifier
Tech: Python, TensorFlow, CNN
GitHub: https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification
Category: CV, Healthcare AI
- Built and trained a CNN to classify Bangladeshi medicinal plant leaves, achieving high accuracy on a custom curated dataset relevant to local biodiversity.

### LungCancer ImageNet Classifier
Tech: Python, TensorFlow, Transfer Learning
GitHub: https://github.com/kaisarfardin6620/LungCancer-ImageNet
Category: CV, Healthcare AI
- Applied transfer learning on a lung cancer histopathology image dataset, fine-tuning ImageNet pretrained models for binary and multi-class cancer detection.

### Marine Life Classifier
Tech: Python, TensorFlow, CNN
GitHub: https://github.com/kaisarfardin6620/Marine_Life_Classifier
Category: CV
- Developed a multi-class CNN image classifier to identify marine species from underwater photographs.

### AppleNet Autoencoder (AE)
Tech: Python, TensorFlow, Autoencoder
GitHub: https://github.com/kaisarfardin6620/AppleNet-AE
Category: CV, Unsupervised Learning
- Implemented an autoencoder-based feature learning model on apple disease image data for anomaly detection and classification tasks.

### Leaf Disease Classifier
Tech: Python, TensorFlow, CNN
GitHub: https://github.com/kaisarfardin6620/LeafDiseaseClassifier
Category: CV, Agricultural AI
- Trained a CNN to detect and classify leaf diseases across multiple plant species, supporting early crop disease detection.

### FlowerNet Comparison
Tech: Python, TensorFlow, Transfer Learning
GitHub: https://github.com/kaisarfardin6620/FlowerNet-Comparison
Category: CV
- Benchmarked multiple CNN architectures (VGG, ResNet, MobileNet) on a flower classification dataset to compare accuracy and inference speed trade-offs.

### Fashion MNIST (Supervised + Semi-supervised)
Tech: Python, TensorFlow, Semi-supervised Learning
GitHub: https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup
Category: CV
- Compared fully supervised and semi-supervised learning strategies on Fashion MNIST, analyzing accuracy improvements when labeled data is limited.

### Cat vs Dog Classification
Tech: Python, TensorFlow, CNN
GitHub: https://github.com/kaisarfardin6620/Cat-Vs-Dog-Classification
Category: CV
- Built a binary image classifier distinguishing cats from dogs using convolutional networks with data augmentation.

### Butterfly Classifier
Tech: Python, TensorFlow, CNN
GitHub: https://github.com/kaisarfardin6620/Butterfly-Classifier
Category: CV
- Trained a fine-grained butterfly species classifier using CNN feature extraction and data augmentation techniques.

### Shoe Classifier
Tech: Python, TensorFlow, CNN
GitHub: https://github.com/kaisarfardin6620/Shoe_Classifier
Category: CV
- Built a product classification model for shoe categories, applicable to e-commerce catalog automation.

### CNN Preprocessing Techniques
Tech: Python, TensorFlow
GitHub: https://github.com/kaisarfardin6620/Cnn_Preprocessings
Category: CV, Educational
- Documented and implemented common CNN preprocessing pipelines (normalization, augmentation, resizing) as reusable modules.

### CNN Visualization Techniques
Tech: Python, TensorFlow, Grad-CAM
GitHub: https://github.com/kaisarfardin6620/Cnn_Visuals
Category: CV, XAI
- Implemented CNN interpretability techniques (Grad-CAM, feature map visualization) to explain model predictions for image classification tasks.

### Autoencoder Anomaly Detection
Tech: Python, TensorFlow, Autoencoder
GitHub: https://github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection
Category: Unsupervised Learning
- Implemented an unsupervised autoencoder-based anomaly detection system, reconstructing normal patterns and flagging anomalies via reconstruction error thresholding.

---

## NLP PROJECTS

### Quora Question Pair Classification (SBERT + Deep Learning)
Tech: Python, SBERT, TensorFlow, NLP
GitHub: https://github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning
Category: NLP, Semantic Similarity
- Combined Sentence-BERT embeddings with a deep learning classifier to determine semantic equivalence of Quora question pairs, outperforming baseline NLP approaches.

### NLP Twitter Sentiment Analysis
Tech: Python, NLTK, Scikit-learn, Deep Learning
GitHub: https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis
Category: NLP, Sentiment Analysis
- Built an end-to-end NLP pipeline for multi-class Twitter sentiment classification with preprocessing, feature extraction, and model comparison.

### Real vs Fake News Classifier
Tech: Python, NLP, Scikit-learn, TF-IDF
GitHub: https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier
Category: NLP, Misinformation Detection
- Developed a fake news detection classifier using TF-IDF features and ML models with comparative evaluation.

### NLP Spam Classification (Word Embeddings)
Tech: Python, Word2Vec, TensorFlow, NLP
GitHub: https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings
Category: NLP
- Implemented spam detection using word embedding representations and deep learning classifiers, comparing against traditional bag-of-words baselines.

### LSTM IMDb Sentiment Analysis
Tech: Python, TensorFlow, LSTM
GitHub: https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis
Category: NLP, Sequence Modeling
- Trained LSTM-based sequence models on the IMDb dataset for binary sentiment classification, experimenting with embedding strategies and regularization.

### Text Pair Classification
Tech: Python, NLP, TensorFlow
GitHub: https://github.com/kaisarfardin6620/Text-Pair-Classification
Category: NLP, Semantic Similarity
- Built a text pair classification system using sentence encoders and similarity metrics for natural language inference tasks.

---

## MACHINE LEARNING PROJECTS

### Customer Churn Prediction
Tech: Python, Scikit-learn, XGBoost, Pandas
GitHub: https://github.com/kaisarfardin6620/Customer-Churn-Prediction
Category: ML, Business AI
- Developed a supervised ML pipeline to predict customer churn using feature engineering, class balancing, and ensemble methods with full model evaluation metrics.

### Breast Cancer Survival Prediction
Tech: Python, Scikit-learn, Pandas
GitHub: https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.
Category: ML, Healthcare AI
- Built and compared multiple ML classifiers for breast cancer survival prediction with cross-validation, ROC-AUC evaluation, and feature importance analysis.

### Lung Cancer Prediction (ML)
Tech: Python, Scikit-learn, Pandas
GitHub: https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.
Category: ML, Healthcare AI
- Applied supervised ML classification to lung cancer prediction from clinical tabular data with hyperparameter tuning and model selection.

### Sales Forecasting Regression
Tech: Python, Scikit-learn, Pandas, Regression
GitHub: https://github.com/kaisarfardin6620/Sales-Forecasting-Regression
Category: ML, Time Series
- Built regression models for retail sales forecasting, incorporating feature engineering, lag variables, and cross-validation for time series data.

### Weather Forecasting Models
Tech: Python, Scikit-learn, Time Series
GitHub: https://github.com/kaisarfardin6620/Weather_Forecasting_Models
Category: ML, Time Series
- Developed and compared multiple forecasting models (linear regression, random forest, gradient boosting) for weather prediction tasks.

### Weather Rainfall Prediction
Tech: Python, Scikit-learn, Pandas
GitHub: https://github.com/kaisarfardin6620/Weather-rainfall-prediction
Category: ML
- Predicted rainfall probability and intensity using classification and regression ML models on meteorological datasets.

### Wine Quality Testing
Tech: Python, Scikit-learn, Pandas
GitHub: https://github.com/kaisarfardin6620/Wine-Quality-Testing-
Category: ML
- Built ML models to predict wine quality ratings from physicochemical properties, comparing classification and regression approaches.
