# RESUME TEMPLATE — Abdullah Kaisar Fardin
# HOW TO USE THIS FILE:
#   1. Fill in every field marked with [FILL: ...]
#   2. Remove or add bullet points as needed
#   3. Run the optional update script (resume_update.py) to regenerate RESUME_DRAFT.md
#   4. Keep all section headings EXACTLY as shown for ATS compliance
#   5. Do NOT add images, tables, columns, or special formatting characters

# ============================================================
# SECTION 1: CONTACT INFORMATION
# ============================================================
FULL_NAME      = "Abdullah Kaisar Fardin"
EMAIL          = "[FILL: your-email@example.com]"
PHONE          = "[FILL: +880-XXXXXXXXXX]"
LINKEDIN       = "[FILL: https://www.linkedin.com/in/your-profile]"
GITHUB         = "https://github.com/kaisarfardin6620"
LOCATION       = "Dhaka, Bangladesh"

# ============================================================
# SECTION 2: PROFESSIONAL SUMMARY
# (Edit the text below. Keep it 3–5 sentences. Include your target role.)
# ============================================================
SUMMARY = """
AI Engineer with approximately 1 year of hands-on experience designing and deploying
intelligent backend systems, LLM integrations, and machine learning pipelines.
Proven ability to build production-grade AI microservices (FastAPI, Django),
implement Retrieval-Augmented Generation (RAG) architectures, and apply deep learning
across computer vision and NLP tasks. Currently pursuing an M.Sc. degree while
contributing to research-oriented AI projects. Passionate about explainable, scalable,
and trustworthy AI systems.
"""

# ============================================================
# SECTION 3: SKILLS (edit lists freely)
# ============================================================
SKILLS = {
    "Programming Languages": ["Python", "SQL"],
    "AI / Machine Learning": [
        "Large Language Models (LLMs)", "Retrieval-Augmented Generation (RAG)",
        "Knowledge Graphs", "Natural Language Processing (NLP)", "Computer Vision",
        "CNN", "Transfer Learning", "Autoencoders", "Anomaly Detection",
        "Sentiment Analysis", "Text Classification", "LSTM", "Siamese Networks"
    ],
    "Frameworks & Libraries": [
        "FastAPI", "Django", "Django REST Framework (DRF)", "TensorFlow", "Keras",
        "scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "NLTK",
        "sentence-transformers (SBERT)", "XGBoost", "Celery"
    ],
    "AI / LLM APIs": [
        "OpenAI API (GPT-4o, DALL-E 3)", "ElevenLabs Text-to-Speech",
        "Firebase Cloud Messaging"
    ],
    "Databases": [
        "PostgreSQL", "MongoDB", "Redis", "Neo4j (Graph Database)",
        "Pinecone (Vector Database)", "SQLite"
    ],
    "DevOps & Infrastructure": [
        "Docker", "Docker Compose", "Nginx", "Git", "GitHub",
        "WebSockets", "Uvicorn", "Gunicorn", "Daphne"
    ],
    "Other Tools": [
        "Swagger / OpenAPI", "Jupyter Notebook", "Google Colab", "Postman"
    ]
}

# ============================================================
# SECTION 4: EDUCATION
# (Add or edit entries. Most recent first.)
# ============================================================
EDUCATION = [
    {
        "degree":      "Master of Science (M.Sc.)",
        "field":       "[FILL: Computer Science / Artificial Intelligence / Data Science]",
        "university":  "[FILL: University Name]",
        "location":    "Dhaka, Bangladesh",
        "status":      "In Progress",
        "graduation":  "[FILL: Expected Year, e.g., 2026]"
    },
    {
        "degree":      "Bachelor of Science (B.Sc.)",
        "field":       "[FILL: Computer Science / Electrical Engineering / etc.]",
        "university":  "[FILL: University Name]",
        "location":    "Dhaka, Bangladesh",
        "status":      "Completed",
        "graduation":  "[FILL: Year, e.g., 2023]"
    }
]

# ============================================================
# SECTION 5: WORK EXPERIENCE
# (Add internships, jobs, or freelance work. Most recent first.)
# (Remove the entire EXPERIENCE block if you have no formal experience.)
# ============================================================
EXPERIENCE = [
    {
        "title":       "[FILL: Job Title / Internship Title]",
        "company":     "[FILL: Company Name]",
        "location":    "[FILL: City, Country / Remote]",
        "start":       "[FILL: Month Year, e.g., Jan 2024]",
        "end":         "[FILL: Month Year or Present]",
        "bullets": [
            "[FILL: Describe your primary responsibility and impact here.]",
            "[FILL: Mention tools, technologies, or frameworks used.]",
            "[FILL: Quantify impact where possible, e.g., 'Improved accuracy by X%'.]"
        ]
    }
    # Add more entries as needed:
    # {
    #     "title":    "[FILL: Previous Job Title]",
    #     "company":  "[FILL: Company Name]",
    #     ...
    # }
]

# ============================================================
# SECTION 6: FEATURED PROJECTS
# (These appear prominently. Keep to your top 5–7 for ATS / 1-page goal.)
# (All other projects appear in the "Additional Projects" line.)
# ============================================================
FEATURED_PROJECTS = [
    {
        "name":    "Explainable Hybrid KG-RAG Chatbot",
        "tech":    "Python, FastAPI, OpenAI GPT-4o, Pinecone, Neo4j, NLI",
        "github":  "https://github.com/kaisarfardin6620/explainable-rag-chatbot",
        "bullets": [
            "Built a hybrid RAG system combining vector search (Pinecone) and knowledge graph reasoning (Neo4j) to reduce LLM hallucinations.",
            "Implemented automatic KG construction from PDFs using LLM-based entity and relationship extraction.",
            "Designed a post-hoc NLI claim-verification layer with a confidence-based refusal mechanism.",
            "Applied Freeman's Degree Centrality to weight evidence from authoritative graph nodes.",
            "Built ablation-ready modes (rag_only, kg_only, hybrid); associated with research paper 'Hybrid KG-Guided Explainable RAG for Trustworthy QA'."
        ]
    },
    {
        "name":    "MagicTale AI Backend",
        "tech":    "Python, Django 5, DRF, Celery, Redis, WebSockets, PostgreSQL, OpenAI GPT-4o, DALL-E 3, ElevenLabs, Firebase, Docker",
        "github":  "https://github.com/kaisarfardin6620/magictale",
        "bullets": [
            "Engineered a production-grade async AI storytelling platform integrating GPT-4o (text), DALL-E 3 (images), and ElevenLabs (audio) in a 3-stage pipeline.",
            "Delivered real-time story generation progress via Django Channels WebSockets.",
            "Integrated Google OAuth2, Apple Sign-In, and JWT with Pwned Passwords API validation.",
            "Automated FCM push notifications on story completion; managed subscriptions via RevenueCat webhooks.",
            "Deployed with Docker Compose, Nginx, Celery workers, and Daphne ASGI server."
        ]
    },
    {
        "name":    "Reho AI Finance Microservice",
        "tech":    "Python, FastAPI, OpenAI GPT-4o, MongoDB, Redis, WebSockets, Docker",
        "github":  "https://github.com/kaisarfardin6620/Reho-AI-Service",
        "bullets": [
            "Developed an AI intelligence layer for a finance management system with real-time WebSocket chat powered by GPT-4o.",
            "Built dynamic context injection fetching live user financial data (income, expenses, debts) before each LLM response.",
            "Designed admin dashboard with AI user summaries, spending heatmaps, debt-to-income risk assessment, and anonymized peer comparisons.",
            "Implemented nightly pre-computation of heavy analytics via scheduled background jobs to minimize dashboard load times."
        ]
    },
    {
        "name":    "Wingman AI Backend",
        "tech":    "Python, Django 5, DRF, Celery, Redis, PostgreSQL, OpenAI, WebSockets, Docker, Nginx",
        "github":  "https://github.com/kaisarfardin6620/wingman",
        "bullets": [
            "Built a scalable Django backend with AI-powered real-time chat, JWT authentication, and subscription management.",
            "Integrated Celery + Redis for async task processing and Django Channels for WebSocket communication.",
            "Deployed via Docker Compose with Nginx for production-ready static file handling and CORS management."
        ]
    },
    {
        "name":    "HR AI Assistant Suite",
        "tech":    "Python, OpenAI GPT API",
        "github":  "https://github.com/kaisarfardin6620/Hr-Ai-Assistant",
        "bullets": [
            "Built 8 modular domain-specific AI assistants (Compensation, Compliance, Talent Acquisition, Organizational Development, etc.) using OpenAI GPT.",
            "Implemented per-user conversation history, input sanitization, caching, and structured logging for production use.",
            "Designed for seamless integration with Flask or FastAPI REST APIs."
        ]
    },
    {
        "name":    "Customer Churn Prediction",
        "tech":    "Python, scikit-learn, XGBoost, TensorFlow/Keras, Pandas, Seaborn, SMOTE",
        "github":  "https://github.com/kaisarfardin6620/Customer-Churn-Prediction",
        "bullets": [
            "Trained and compared 12+ ML models (Logistic Regression, Random Forest, XGBoost, SVM, Gradient Boosting, Voting/Stacking Classifiers, ANN) for bank churn prediction.",
            "Applied SMOTE for class imbalance; performed hyperparameter tuning with GridSearchCV and StratifiedKFold cross-validation.",
            "Evaluated with ROC-AUC, Precision, Recall, F1-Score, and Confusion Matrices; visualized with Plotly and Seaborn."
        ]
    },
    {
        "name":    "Lung Cancer Chest X-Ray Classification",
        "tech":    "Python, TensorFlow/Keras, CNN, VGG16, ResNet50, InceptionV3, MobileNetV2, EfficientNetB0",
        "github":  "https://github.com/kaisarfardin6620/LungCancer-ImageNet",
        "bullets": [
            "Built a multi-class chest X-ray classifier distinguishing adenocarcinoma, large cell carcinoma, squamous cell carcinoma, and normal cases.",
            "Applied two-stage transfer learning fine-tuning across 5 architectures with automatic class weight balancing and data augmentation."
        ]
    }
]

# ============================================================
# SECTION 7: ADDITIONAL PROJECTS (one-liners, shown as a summary block)
# ============================================================
ADDITIONAL_PROJECTS = [
    "Bangladeshi Medicinal Leaf Classification — CNN transfer learning (VGG16, ResNet50, etc.) for medicinal plant identification.",
    "NLP Twitter Sentiment Analysis — SVM, Random Forest, ANN with TF-IDF and SMOTE.",
    "Quora Question Pair Classification — SBERT embeddings with ANN, LSTM, and Siamese Networks.",
    "Autoencoder Anomaly Detection / AppleNet-AE — VAE, denoising autoencoder, t-SNE, One-Class SVM.",
    "Real vs. Fake News Classifier — NLP misinformation detection pipeline.",
    "LSTM for IMDb Sentiment Analysis — Sequence classification with LSTM.",
    "Sales Forecasting Regression — End-to-end regression pipeline for business forecasting.",
    "AI Image Creator (Glimmcatcher) — DALL-E powered image generation CLI tool.",
    "Bondly AI Financial Assistant, Bible AI Assistant — Domain-specific GPT-powered conversational assistants.",
    "Other classifiers: Marine Life, Butterfly, Shoe, FlowerNet, Fashion-MNIST (supervised/semi-supervised), Breast Cancer Survival, Wine Quality, Weather Forecasting, Cat vs. Dog."
]
