# Kaisar Fardin
**AI Engineer**  
Dhaka, Bangladesh  
GitHub: [github.com/kaisarfardin6620](https://github.com/kaisarfardin6620) | Email: your.email@example.com | Phone: +880-XXXX-XXXXXX

---

## Education

**MSc in [Your Field]** — [Your University], Dhaka *(Ongoing)*  
**BSc in [Your Field]** — [Your University], Dhaka *(Completed, [Year])*  

---

## Technical Skills

| Category | Skills |
|---|---|
| **Languages** | Python |
| **AI / LLM** | OpenAI GPT-4o, DALL-E 3, Gemini, RAG, Knowledge Graphs, NLI, Prompt Engineering |
| **ML / DL** | TensorFlow, Keras, PyTorch, Scikit-learn, XGBoost, LightGBM, LSTM, CNN, Transfer Learning |
| **NLP** | Hugging Face Transformers, BERT, SBERT, Word2Vec, GloVe, NLTK, spaCy, TF-IDF |
| **Computer Vision** | OpenCV, Grad-CAM, Image Augmentation, Object Classification, Anomaly Detection |
| **Frameworks** | Django 5, Django REST Framework, FastAPI |
| **Vector / Graph DBs** | Pinecone, Neo4j, ChromaDB |
| **Databases** | PostgreSQL, MongoDB, Redis, SQLite |
| **Async / Real-time** | Celery, Django Channels, WebSockets, Daphne |
| **Infrastructure** | Docker, Docker Compose, Nginx, AWS S3, Firebase FCM |
| **Auth & Security** | JWT (SimpleJWT), Google OAuth2, Apple Sign-In, Email OTP |
| **Tools** | Git, Swagger / OpenAPI, Postman, Jupyter, Matplotlib, Seaborn, SHAP |

---

## Projects

### Explainable Hybrid KG-RAG Chatbot (Research)  
`Python · FastAPI · OpenAI GPT-4o · Pinecone · Neo4j · NLI`  
[github.com/kaisarfardin6620/explainable-rag-chatbot](https://github.com/kaisarfardin6620/explainable-rag-chatbot)

- Designed a research-grade Hybrid RAG system combining Pinecone vector search with Neo4j knowledge-graph traversal to reduce LLM hallucinations and provide claim-level explainability.
- Built a post-hoc NLI verification layer that abstains from answering when confidence falls below 0.4; applied Freeman's Degree Centrality to weight evidence from authoritative graph entities.
- Architected three ablation modes (hybrid, rag_only, kg_only) and a benchmark automation script generating comparative F1, semantic similarity, and latency reports.

---

### MagicTale — AI Children's Storytelling Platform  
`Python · Django 5 · Celery · OpenAI GPT-4o · DALL-E 3 · ElevenLabs · WebSockets`  
[github.com/kaisarfardin6620/magictale](https://github.com/kaisarfardin6620/magictale)

- Engineered an async AI content pipeline (Celery + Redis) that generates personalized stories (GPT-4o), cover illustrations (DALL-E 3), and voice narration (ElevenLabs TTS) without blocking the HTTP layer.
- Implemented real-time story-generation progress over Django Channels WebSockets; integrated Google OAuth2, Apple Sign-In, FCM push notifications, and RevenueCat subscription webhooks.
- Containerized the full stack (Django/Daphne + Celery + Redis + PostgreSQL + Nginx) with Docker Compose.

---

### Reho AI Finance Microservice  
`Python · FastAPI · OpenAI GPT-4o · MongoDB · Redis · WebSockets`  
[github.com/kaisarfardin6620/Reho-AI-Service](https://github.com/kaisarfardin6620/Reho-AI-Service)

- Built an AI microservice that dynamically injects live user financial data into the GPT-4o system prompt, enabling context-aware conversational advice over real-time WebSockets.
- Developed admin intelligence endpoints auto-generating user 360 summaries, spending heatmaps, and debt-to-income risk scores using GPT-4o.
- Scheduled nightly background jobs to pre-compute heavy analytics reports, reducing dashboard load times via Redis caching.

---

### Quora Question Pair Classification (SBERT + Deep Learning)  
`Python · SBERT · Siamese Networks · Hugging Face Transformers · PyTorch`  
[github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning](https://github.com/kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning)

- Fine-tuned Sentence-BERT (SBERT) on the Quora Question Pairs dataset to detect semantic duplicates, achieving 89% F1 with a Siamese network architecture.
- Compared SBERT embeddings + cosine similarity against BiLSTM and cross-encoder baselines; SBERT outperformed traditional NLP approaches by 12% F1.
- Implemented hard negative mining to improve contrastive training and reduce false positives in semantic similarity tasks.

---

### LungCancer-ImageNet — Transfer Learning for Medical Imaging  
`Python · TensorFlow · ResNet/VGG · Transfer Learning · Grad-CAM`  
[github.com/kaisarfardin6620/LungCancer-ImageNet](https://github.com/kaisarfardin6620/LungCancer-ImageNet)

- Fine-tuned a pre-trained ImageNet CNN (ResNet/VGG) on lung cancer CT scan datasets to classify benign vs. malignant nodules.
- Applied transfer learning with data augmentation (rotation, flipping, contrast adjustment) to overcome medical imaging data scarcity.
- Visualized model interpretability via Grad-CAM activation maps; evaluated with ROC-AUC and precision-recall curves.

---

## Additional Projects

Set `include=True` in `generate_resume.py` to activate any of these:

| Project | GitHub |
|---|---|
| HR AI Assistant | [https://github.com/kaisarfardin6620/Hr-Ai-Assistant](https://github.com/kaisarfardin6620/Hr-Ai-Assistant) |
| Bondly AI — Financial Assistant | [https://github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant](https://github.com/kaisarfardin6620/Bondly-Ai_Financial-Assistant) |
| Bible AI Assistant | [https://github.com/kaisarfardin6620/Bible-Ai-Assistant](https://github.com/kaisarfardin6620/Bible-Ai-Assistant) |
| Autoencoder Anomaly Detection | [https://github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection](https://github.com/kaisarfardin6620/Autoencoder-Anomaly-Detection) |
| Real vs. Fake News Classifier | [https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier](https://github.com/kaisarfardin6620/Real-vs.-Fake-News-Classifier) |
| NLP Twitter Sentiment Analysis | [https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis](https://github.com/kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis) |
| LSTM for IMDb Sentiment Analysis | [https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis](https://github.com/kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis) |
| NLP Spam Classification with Word Embeddings | [https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings](https://github.com/kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings) |
| Text Pair Classification | [https://github.com/kaisarfardin6620/Text-Pair-Classification](https://github.com/kaisarfardin6620/Text-Pair-Classification) |
| LeafDiseaseClassifier — Plant Disease Detection | [https://github.com/kaisarfardin6620/LeafDiseaseClassifier](https://github.com/kaisarfardin6620/LeafDiseaseClassifier) |
| Bangladeshi Medicinal Leaf Classification | [https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification](https://github.com/kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification) |
| Marine Life Classifier | [https://github.com/kaisarfardin6620/Marine_Life_Classifier](https://github.com/kaisarfardin6620/Marine_Life_Classifier) |
| FlowerNet — CNN Architecture Comparison | [https://github.com/kaisarfardin6620/FlowerNet-Comparison](https://github.com/kaisarfardin6620/FlowerNet-Comparison) |
| AppleNet-AE — Apple Disease Detection (Autoencoder) | [https://github.com/kaisarfardin6620/AppleNet-AE](https://github.com/kaisarfardin6620/AppleNet-AE) |
| Fashion-MNIST — Supervised and Semi-Supervised Learning | [https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup](https://github.com/kaisarfardin6620/Fashion-Mnist-Sup-Semisup) |
| Butterfly Classifier | [https://github.com/kaisarfardin6620/Butterfly-Classifier](https://github.com/kaisarfardin6620/Butterfly-Classifier) |
| Cat vs. Dog Classification | [https://github.com/kaisarfardin6620/Cat-Vs-Dog-Classification](https://github.com/kaisarfardin6620/Cat-Vs-Dog-Classification) |
| Shoe Classifier | [https://github.com/kaisarfardin6620/Shoe_Classifier](https://github.com/kaisarfardin6620/Shoe_Classifier) |
| CNN Preprocessings — Image Augmentation Toolkit | [https://github.com/kaisarfardin6620/Cnn_Preprocessings](https://github.com/kaisarfardin6620/Cnn_Preprocessings) |
| CNN Visuals — Convolutional Network Visualization | [https://github.com/kaisarfardin6620/Cnn_Visuals](https://github.com/kaisarfardin6620/Cnn_Visuals) |
| Customer Churn Prediction | [https://github.com/kaisarfardin6620/Customer-Churn-Prediction](https://github.com/kaisarfardin6620/Customer-Churn-Prediction) |
| Lung Cancer Prediction using Machine Learning | [https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.](https://github.com/kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.) |
| Breast Cancer Survival Prediction | [https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.](https://github.com/kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.) |
| Wine Quality Testing | [https://github.com/kaisarfardin6620/Wine-Quality-Testing-](https://github.com/kaisarfardin6620/Wine-Quality-Testing-) |
| Sales Forecasting Regression | [https://github.com/kaisarfardin6620/Sales-Forecasting-Regression](https://github.com/kaisarfardin6620/Sales-Forecasting-Regression) |
| Weather Forecasting Models | [https://github.com/kaisarfardin6620/Weather_Forecasting_Models](https://github.com/kaisarfardin6620/Weather_Forecasting_Models) |
| Weather Rainfall Prediction | [https://github.com/kaisarfardin6620/Weather-rainfall-prediction](https://github.com/kaisarfardin6620/Weather-rainfall-prediction) |
| AI Image Creator — GlimmCatcher | [https://github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher](https://github.com/kaisarfardin6620/Ai-Image-Creator-Glimmcatcher) |
| Wingman — AI Assistant Backend | [https://github.com/kaisarfardin6620/wingman](https://github.com/kaisarfardin6620/wingman) |
| Benjaminkley — 3D Head Scanner and Biometric Analysis | [https://github.com/kaisarfardin6620/benjaminkley](https://github.com/kaisarfardin6620/benjaminkley) |
| Rai Backend — AI Community Platform | [https://github.com/kaisarfardin6620/Rai_Backend](https://github.com/kaisarfardin6620/Rai_Backend) |
| MAIZ FastAPI — AI Data Service | [https://github.com/kaisarfardin6620/maiz-fastapi](https://github.com/kaisarfardin6620/maiz-fastapi) |
| DELUX AI — AI Feature Service | [https://github.com/kaisarfardin6620/DELUX_AI](https://github.com/kaisarfardin6620/DELUX_AI) |

---

## Open to
New AI Engineering roles in Dhaka or remote. Interests include LLM systems, RAG pipelines, AI microservices, computer vision, and production ML backends.

---

*Last updated: April 2026 — generated by `resume/generate_resume.py`*