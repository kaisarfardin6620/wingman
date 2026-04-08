# Resume Data Sources — Transparency Breakdown

This document provides a **section-by-section explanation** of exactly where every piece of data in `RESUME_DRAFT.md` comes from: either directly from your supplied personal information, or extracted automatically by scanning your GitHub repositories.

---

## Quick-Reference Summary Table

| Resume Section | Data Origin | Specific Source |
|---|---|---|
| **Name** | ✅ User-supplied | Provided directly in chat |
| **Email** | ✅ User-supplied | Provided directly in chat |
| **Phone** | ✅ User-supplied | Provided directly in chat |
| **LinkedIn URL** | ✅ User-supplied | Provided directly in chat |
| **GitHub URL** | ✅ User-supplied (account name) | Inferred from provided repo links |
| **Professional Summary** | ✅ User-supplied | Verbatim from your message |
| **Work Experience — Roles, Dates, Employer** | ✅ User-supplied | Provided directly in chat |
| **Work Experience — Bullet Points** | ✅ User-supplied | Verbatim from your message |
| **Education — Degrees, Schools, Dates** | ✅ User-supplied | Provided directly in chat |
| **Technical Skills — Core Languages** | ✅ User-supplied | Your skills section message |
| **Technical Skills — Core Frameworks** | ✅ User-supplied | Your skills section message |
| **Technical Skills — AI/ML (base)** | ✅ User-supplied | Your skills section message |
| **Technical Skills — Data Engineering** | ✅ User-supplied | Your skills section message |
| **Technical Skills — Infrastructure** | ✅ User-supplied | Your skills section message |
| **Technical Skills — Scikit-learn, Pandas, NumPy** | 🔍 Repo-extracted | Found in `requirements.txt` / README / notebook imports |
| **Technical Skills — Sentence-Transformers (SBERT)** | 🔍 Repo-extracted | Found in `pip install` lines in Quora-Question-Pair-Classification notebook |
| **Technical Skills — NLTK** | 🔍 Repo-extracted | Found in README and notebook `import nltk` statements |
| **Technical Skills — Plotly, Seaborn** | 🔍 Repo-extracted | Found in README and notebook imports in Customer-Churn-Prediction |
| **Technical Skills — Imbalanced-learn / SMOTE** | 🔍 Repo-extracted | Found in notebook imports across multiple repos |
| **Technical Skills — XGBoost** | 🔍 Repo-extracted | Found in README / `pip install xgboost` in Customer-Churn-Prediction |
| **Technical Skills — Flask** | 🔍 Repo-extracted | Found in README `pip install openai requests python-dotenv flask` in Bible-Ai-Assistant |
| **Projects — All descriptions and bullets** | 🔍 Repo-extracted | `README.md`, `requirements.txt`, and code `import` statements in each repo |

---

## Section-by-Section Detail

---

### 1. Header (Contact Information)

**Source: 100% User-Supplied**

| Field | Value | Where you provided it |
|---|---|---|
| Full name | Abdullah Kaisar Fardin | Chat message |
| Email | kaisarfardin128@gmail.com | Chat message |
| Phone | 01708050645 | Chat message |
| LinkedIn | linkedin.com/in/abdullah-kaisar-fardin | Chat message |
| GitHub | github.com/kaisarfardin6620 | Inferred from repo URLs you shared |

No repo scanning is done for the header.

---

### 2. Professional Summary

**Source: 100% User-Supplied**

Your summary is used **verbatim** from your chat message. No text is generated or modified from your repositories.

> *"Results-driven AI Developer with hands-on experience in designing and deploying scalable, production-grade AI systems..."*

---

### 3. Work Experience

**Source: 100% User-Supplied**

All of the following are taken directly from your message — nothing is inferred from repos:

| Field | Source |
|---|---|
| Job titles (Jr. AI Developer, Trainee AI Developer) | User message |
| Employer (SparkTech Agency, Dhaka) | User message |
| Dates (May 2025 – Aug 2025, Aug 2025 – Present) | User message |
| All bullet points | User message (verbatim) |

---

### 4. Education

**Source: 100% User-Supplied**

| Field | Source |
|---|---|
| MSc in Data Science & Analytics — East West University (Jan 2026–Present) | User message |
| BSc in Computer Science & Engineering — BUBT (2019–2024) | User message |

---

### 5. Technical Skills

**Source: Mixed — User-Supplied Base + Repo-Extracted Additions**

Skills you explicitly listed in your message form the foundation. Additional skills are extracted from repo files.

#### 5a. Skills from Your Message (User-Supplied)

| Skill | Category |
|---|---|
| Python (Advanced) | Languages |
| SQL | Languages |
| Django, Django Channels (WebSockets) | Frameworks |
| FastAPI | Frameworks |
| Celery | Frameworks |
| TensorFlow | AI & ML |
| MediaPipe (CV) | AI & ML |
| OpenAI (Vision/Audio) | AI & ML |
| LangChain | AI & ML |
| RAG | AI & ML |
| Neo4j (Graph DB) | Data Engineering |
| Pinecone (Vector DB) | Data Engineering |
| Redis | Data Engineering |
| PostgreSQL | Data Engineering |
| MongoDB | Data Engineering |
| Docker | Infrastructure |
| Nginx | Infrastructure |
| AWS S3 | Infrastructure |
| Firebase (FCM) | Infrastructure |
| CI/CD Pipelines | Infrastructure |

#### 5b. Skills Extracted from Repository Analysis

These skills are **not** in your provided skills section but appear in repo files:

| Skill | Detected Signal | Repository | File/Location |
|---|---|---|---|
| Scikit-learn | `pip install scikit-learn` in README; `from sklearn...` imports | AppleNet-AE, LungCancer-ImageNet, Customer-Churn-Prediction, NLP-Twitter-Sentiment | README.md, notebook imports |
| Pandas | `import pandas as pd` | Customer-Churn-Prediction, Quora-Classification | notebook imports |
| NumPy | `import numpy as np` | Customer-Churn-Prediction, Quora-Classification, NLP-Twitter | notebook imports |
| Keras | `from tensorflow.keras...` imports | LungCancer-ImageNet, Quora-Classification, NLP-Twitter | notebook imports |
| Sentence-Transformers (SBERT) | `pip install sentence-transformers`; `from sentence_transformers import SentenceTransformer` | Quora-Question-Pair-Classification | notebook imports |
| NLTK | `import nltk`; `from nltk.corpus import stopwords` | Quora-Classification, NLP-Twitter-Sentiment | notebook imports |
| XGBoost | `pip install xgboost`; `xgboost` in README models list | Customer-Churn-Prediction | README.md |
| Imbalanced-learn / SMOTE | `pip install imbalanced-learn`; `from imblearn.over_sampling import SMOTE` | Customer-Churn-Prediction, Quora-Classification, NLP-Twitter | README.md, notebook imports |
| Matplotlib | `pip install matplotlib`; `import matplotlib.pyplot as plt` | AppleNet-AE, LungCancer-ImageNet, Customer-Churn-Prediction | README.md, notebook imports |
| Seaborn | `import seaborn as sns` | LungCancer-ImageNet, Customer-Churn-Prediction | README.md, notebook imports |
| Plotly | `import plotly` | Customer-Churn-Prediction | README.md |
| Flask | `pip install ... flask` in README setup | Bible-Ai-Assistant | README.md |
| Pillow | `pip install ... pillow` in README; in requirements.txt | AppleNet-AE, Ai-Image-Creator-Glimmcatcher | README.md, requirements.txt |
| Tenacity | `tenacity>=8.0.0` | Hr-Ai-Assistant, Ai-Image-Creator-Glimmcatcher | requirements.txt |

---

### 6. Projects

**Source: 100% Repo-Extracted**

All project descriptions, bullet points, tech stacks, and titles come exclusively from repository analysis. No project narrative supplied by you in chat is used. The extraction follows this signal priority:

#### Extraction Signal Priority (per repository)

```
1. README.md        → Project description, features list, setup steps, model/algorithm names
2. requirements.txt → Library names and versions (exact tech stack)
3. Code imports     → `import X` and `from X import Y` in .py files and Jupyter notebooks
4. Dockerfile       → Base images, system dependencies (if present)
5. File names       → Script names imply task (e.g., Churn_Prediction.ipynb → churn prediction)
6. Folder structure → Data folders imply datasets/domain (e.g., apple/train/ → apple images)
```

#### Per-Project Extraction Detail

| Project | Repo | Description Source | Tech Stack Source |
|---|---|---|---|
| **HR AI Assistant** | Hr-Ai-Assistant | README.md: "A suite of robust, production-ready Python backend modules for various HR domains..." — feature list, structure | requirements.txt: `openai>=1.0.0`, `python-dotenv`, `tenacity`, `sounddevice`, `scipy`, `requests` |
| **AppleNet-AE** | AppleNet-AE | README.md: Features list (Autoencoder, VAE, inpainting, KMeans, t-SNE, One-Class SVM, anomaly detection); Pipeline steps section | README.md: `pip install tensorflow matplotlib scikit-learn pillow` |
| **LungCancer-ImageNet** | LungCancer-ImageNet | README.md: "multi-class classification of chest X-ray images using ... VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0"; Features section | README.md: `pip install tensorflow keras scikit-learn matplotlib seaborn` |
| **Bondly AI Financial Coach** | Bondly-Ai_Financial-Assistant | README.md: "emotionally intelligent AI financial coach ... personalized advice ... micro-consent ... adapts tone dynamically" | requirements.txt: `openai` |
| **Customer Churn Prediction** | Customer-Churn-Prediction | README.md: "implements various machine learning models to predict customer churn ... 12 models ... SMOTE ... hyperparameter tuning" | README.md: `pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn xgboost plotly tensorflow scikeras` |
| **Quora Question Pair Classification** | Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning | README.md: "classifies Quora question pairs ... using pretrained SBERT embeddings and multiple ML models including ANN, LSTM, Siamese Networks" | Notebook `pip install` lines + `import` statements: `sentence-transformers`, `tensorflow`, `scikit-learn`, `nltk`, `imbalanced-learn`, `pandas`, `seaborn` |
| **NLP Twitter Sentiment Analysis** | NLP-based-Twitter-Sentiment-Analysis | README.md: "sentiment analysis on Twitter dataset using various ML models ... TF-IDF vectorizer ... SMOTE"; Technologies section | README.md Technologies list: Python, Pandas, NumPy, Scikit-learn, TensorFlow/Keras, Matplotlib, Seaborn, NLTK, Wordcloud, Imbalanced-learn |
| **Glimmcatcher AI Image Creator** | Ai-Image-Creator-Glimmcatcher | README.md: "AI-powered assistant to generate, analyze, and visualize creative ideas or images" | requirements.txt: `python-dotenv`, `openai`, `Pillow`, `tenacity`, `scipy`, `sounddevice` |
| **Bible AI Assistant (Preachly)** | Bible-Ai-Assistant | README.md: "AI assistant to help users understand the Bible and Christian teachings ... fetches Bible verses using the Scripture API ... supports multiple Bible versions" | README.md setup: `pip install openai requests python-dotenv flask` |
| **Fashion-MNIST** | Fashion-Mnist-Sup-Semisup | Repo name + any README (supervised/semi-supervised classification on Fashion-MNIST) | TensorFlow/Keras (inferred from repo type) |
| **Bangladeshi Medicinal Leaf Classification** | Bangladeshi-Medicinal-Leaf-Classification | Repo name + README (if present): CNN-based leaf image classification for Bangladeshi medicinal plants | TensorFlow/Keras, scikit-learn (inferred) |
| **Breast Cancer Survival Prediction** | Breast-Cancer-Survival-Prediction-using-Machine-Learning | Repo name: ML pipeline for breast cancer survival prediction | scikit-learn, pandas, numpy (inferred from ML type) |

> **Note:** For repos without a `requirements.txt`, the tech stack is inferred from:
> (a) the README's explicit `pip install` commands or "Technologies Used" sections,
> (b) `import` statements in `.py` and `.ipynb` files,
> (c) the repo name and domain (e.g., a "CNN" repo → TensorFlow/Keras).

---

## How Skills Detected from Repos Are Distinguished from User-Supplied Skills

The `resume_generator.py` script maintains two explicit sets:

```python
USER_SUPPLIED_SKILLS = {
    # Verbatim from user's skills section message
    "Python", "SQL", "Django", "FastAPI", "Celery",
    "TensorFlow", "MediaPipe", "OpenAI", "LangChain", "RAG",
    "Neo4j", "Pinecone", "Redis", "PostgreSQL", "MongoDB",
    "Docker", "Nginx", "AWS S3", "Firebase", "CI/CD"
}

REPO_DETECTED_SKILLS = set()  # Built by scanning repos, then deduplicated against USER_SUPPLIED_SKILLS
```

Only skills **not already present** in `USER_SUPPLIED_SKILLS` are appended to the Technical Skills section under `# (also detected in repos)`.

---

## Data Flow Diagram

```
User Chat Message
│
├──► [Name, Email, Phone, LinkedIn]  ──────────────────► Header
├──► [Professional Summary]  ──────────────────────────► Summary Section
├──► [Work Experience: roles, dates, bullets]  ────────► Work Experience Section
├──► [Education: degrees, schools, dates]  ────────────► Education Section
└──► [Technical Skills: languages, frameworks, infra]  ─► Skills Section (base)

GitHub Repositories (README.md, requirements.txt, *.py, *.ipynb)
│
├──► [README overview + features]  ────────────────────► Project descriptions & bullets
├──► [requirements.txt package names]  ────────────────► Project tech stack + extra Skills
├──► [Code `import` statements]  ──────────────────────► Project tech stack + extra Skills
├──► [Dockerfile base images]  ────────────────────────► Infrastructure skills (if applicable)
└──► [File/folder names]  ─────────────────────────────► Domain context for project titles
```

---

*This document is auto-generated as part of the `kaisarfardin6620/wingman` resume workflow. For the extraction script and editable templates, see `resume_generator.py` and `RESUME_DRAFT.md`.*
