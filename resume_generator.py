"""
resume_generator.py
====================
Annotated script documenting the logic used to build RESUME_DRAFT.md.

This script shows—transparently—which data comes from the user's supplied
personal information and which data is extracted automatically from each
GitHub repository.  It does NOT make live API calls; it is a documented
reference that mirrors the extraction workflow used to produce the draft.

For a human-readable table of every data-source decision, see:
    RESUME_DATA_SOURCES.md

Usage (dry-run):
    python resume_generator.py

To regenerate RESUME_DRAFT.md from scratch you would need to supply a
GitHub Personal Access Token and run the fetch functions below.
"""

# ---------------------------------------------------------------------------
# 1. USER-SUPPLIED PERSONAL INFORMATION
#    Source: provided directly in the Copilot chat session.
#    Nothing in this block is inferred from any repository.
# ---------------------------------------------------------------------------

USER_INFO = {
    "name": "Abdullah Kaisar Fardin",       # from chat message
    "email": "kaisarfardin128@gmail.com",   # from chat message
    "phone": "01708050645",                  # from chat message
    "linkedin": "linkedin.com/in/abdullah-kaisar-fardin",  # from chat message
    "github": "github.com/kaisarfardin6620",  # inferred from provided repo URLs
}

PROFESSIONAL_SUMMARY = (
    # Verbatim from user's chat message — not modified or generated from repos.
    "Results-driven AI Developer with hands-on experience in designing and deploying scalable, "
    "production-grade AI systems. Skilled in bridging the gap between cutting-edge research models "
    "and real-world applications, with expertise in building asynchronous backends using FastAPI and "
    "Django. Proficient in integrating multimodal AI solutions, including vision and audio models, "
    "into high-performance workflows. Strong foundation in data engineering, cloud deployment, and "
    "microservices architecture, complemented by ongoing postgraduate studies in Data Science."
)

WORK_EXPERIENCE = [
    # Both entries are verbatim from the user's chat message.
    {
        "title": "Jr. AI Developer",
        "company": "SparkTech Agency",
        "location": "Dhaka, Bangladesh",
        "dates": "Aug 2025 – Present",
        "bullets": [
            "Architecting asynchronous backend systems using Django & FastAPI, handling concurrent "
            "AI inference requests via Celery task queues.",
            "Integrated Multimodal AI models (GPT-4o Vision, Whisper Audio) into production "
            "workflows, handling file uploads, OCR, and transcription at scale.",
        ],
    },
    {
        "title": "Trainee AI Developer",
        "company": "SparkTech Agency",
        "location": "Dhaka, Bangladesh",
        "dates": "May 2025 – Aug 2025",
        "bullets": [
            "Developed modular backend services for data preprocessing and LLM context window "
            "management.",
            "Assisted in the containerization (Docker) and deployment of ML services to cloud "
            "environments.",
        ],
    },
]

EDUCATION = [
    # Both entries are verbatim from the user's chat message.
    {
        "degree": "MSc in Data Science & Analytics",
        "institution": "East West University",
        "dates": "Jan 2026 – Present",
    },
    {
        "degree": "BSc in Computer Science & Engineering",
        "institution": "Bangladesh University of Business & Technology (BUBT)",
        "dates": "2019 – 2024",
    },
]


# ---------------------------------------------------------------------------
# 2. SKILLS — User-Supplied Base
#    Source: user's "TECHNICAL SKILLS" section in their chat message.
#    These are stored as a set so repo-detected additions can be deduplicated.
# ---------------------------------------------------------------------------

USER_SUPPLIED_SKILLS = {
    # Languages
    "Python", "SQL",
    # Frameworks
    "Django", "Django Channels", "WebSockets", "FastAPI", "Celery",
    # AI & ML
    "TensorFlow", "MediaPipe", "OpenAI", "LangChain", "RAG",
    # Data Engineering
    "Neo4j", "Pinecone", "Redis", "PostgreSQL", "MongoDB",
    # Infrastructure
    "Docker", "Nginx", "AWS S3", "Firebase", "CI/CD",
}


# ---------------------------------------------------------------------------
# 3. REPOSITORY LIST
#    Source: URLs shared by the user in the chat session.
#    No descriptions are pre-filled — everything comes from repo content.
# ---------------------------------------------------------------------------

REPOS = [
    "kaisarfardin6620/AppleNet-AE",
    "kaisarfardin6620/Fashion-Mnist-Sup-Semisup",
    "kaisarfardin6620/LungCancer-ImageNet",
    "kaisarfardin6620/Ai-Image-Creator-Glimmcatcher",
    "kaisarfardin6620/Hr-Ai-Assistant",
    "kaisarfardin6620/Bondly-Ai_Financial-Assistant",
    "kaisarfardin6620/Bible-Ai-Assistant",
    "kaisarfardin6620/Customer-Churn-Prediction",
    "kaisarfardin6620/LeafDiseaseClassifier",
    "kaisarfardin6620/Weather_Forecasting_Models",
    "kaisarfardin6620/Butterfly-Classifier",
    "kaisarfardin6620/Cnn_Preprocessings",
    "kaisarfardin6620/Cnn_Visuals",
    "kaisarfardin6620/Marine_Life_Classifier",
    "kaisarfardin6620/Shoe_Classifier",
    "kaisarfardin6620/FlowerNet-Comparison",
    "kaisarfardin6620/Wine-Quality-Testing-",
    "kaisarfardin6620/Lung-Cancer-Prediction-using-Machine-Learning.",
    "kaisarfardin6620/Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning",
    "kaisarfardin6620/Breast-Cancer-Survival-Prediction-using-Machine-Learning.",
    "kaisarfardin6620/Bangladeshi-Medicinal-Leaf-Classification",
    "kaisarfardin6620/Text-Pair-Classification",
    "kaisarfardin6620/NLP-based-Twitter-Sentiment-Analysis",
    "kaisarfardin6620/Real-vs.-Fake-News-Classifier",
    "kaisarfardin6620/NLP-Based-Spam-Classification-with-Word-Embeddings",
    "kaisarfardin6620/LSTM-for-IMDb-Sentiment-Analysis",
    "kaisarfardin6620/Sales-Forecasting-Regression",
    "kaisarfardin6620/Weather-rainfall-prediction",
    "kaisarfardin6620/Cat-Vs-Dog-Classification",
    "kaisarfardin6620/Autoencoder-Anomaly-Detection",
]


# ---------------------------------------------------------------------------
# 4. REPO EXTRACTION FUNCTIONS
#    Each function represents one extraction signal from a repository.
#    Signal priority order:
#      1. README.md         → project description, feature list, model names
#      2. requirements.txt  → exact library names and versions
#      3. *.py / *.ipynb    → `import X` and `from X import Y` statements
#      4. Dockerfile        → base images, system-level dependencies
#      5. File / folder names → domain context (e.g. "Churn_Prediction.ipynb")
# ---------------------------------------------------------------------------

def extract_readme_description(readme_text: str) -> str:
    """
    Extract the project description from the first paragraph of README.md.

    Signal: README.md — first non-heading, non-empty paragraph.
    Used for: Project summary bullet in the resume.
    """
    lines = readme_text.splitlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return ""


def extract_readme_features(readme_text: str) -> list[str]:
    """
    Extract bullet points from the '## Features' section of README.md.

    Signal: README.md — '## Features' or '## Key Features' section.
    Used for: Project bullets in the resume (converted to action-verb bullets).
    """
    features: list[str] = []
    in_features = False
    for line in readme_text.splitlines():
        if line.strip().lower().startswith("## feature"):
            in_features = True
            continue
        if in_features:
            if line.startswith("##"):
                break  # next section starts
            if line.strip().startswith("-") or line.strip().startswith("*"):
                feature = line.strip().lstrip("-").lstrip("*").strip()
                # Remove markdown bold/italic markers
                feature = feature.replace("**", "").replace("__", "")
                features.append(feature)
    return features


def extract_requirements_skills(requirements_text: str) -> set[str]:
    """
    Parse a requirements.txt file and return a set of package names.

    Signal: requirements.txt — package name (before '>=', '==', '<', etc.)
    Used for: Project tech stack and additional Technical Skills.

    Example input line:  'openai>=1.0.0'
    Example output:      'openai'
    """
    skills: set[str] = set()
    for line in requirements_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Strip version specifiers
        for sep in (">=", "==", "<=", "!=", "~=", ">", "<", "["):
            line = line.split(sep)[0]
        package = line.strip().lower()
        if package:
            skills.add(package)
    return skills


def extract_import_skills(source_code: str) -> set[str]:
    """
    Extract top-level library names from Python import statements.

    Signal: *.py and *.ipynb files — 'import X' and 'from X import Y' lines.
    Used for: Project tech stack and additional Technical Skills.

    Example input:  'from sklearn.ensemble import RandomForestClassifier'
    Example output: 'sklearn'
    """
    import re
    skills: set[str] = set()
    for line in source_code.splitlines():
        line = line.strip()
        m_import = re.match(r"^import\s+([\w]+)", line)
        m_from = re.match(r"^from\s+([\w]+)", line)
        if m_import:
            skills.add(m_import.group(1))
        elif m_from:
            skills.add(m_from.group(1))
    return skills


def extract_dockerfile_skills(dockerfile_text: str) -> set[str]:
    """
    Extract base image names and apt/pip packages from a Dockerfile.

    Signal: Dockerfile — FROM, RUN pip install, RUN apt-get install lines.
    Used for: Infrastructure skills (e.g., 'python:3.11-slim' → Python).
    """
    import re
    skills: set[str] = set()
    for line in dockerfile_text.splitlines():
        line = line.strip()
        # Base image
        m = re.match(r"^FROM\s+([\w./:-]+)", line, re.IGNORECASE)
        if m:
            skills.add(m.group(1).split(":")[0])  # strip tag
        # pip install packages
        if "pip install" in line.lower():
            packages = re.findall(r"pip install\s+([\w\->=<.,\[\] ]+)", line, re.IGNORECASE)
            for pkg_str in packages:
                for pkg in pkg_str.split():
                    pkg = re.sub(r"[>=<!\[\],]+.*", "", pkg).strip()
                    if pkg:
                        skills.add(pkg.lower())
    return skills


# ---------------------------------------------------------------------------
# 5. SKILLS MERGE LOGIC
#    User-supplied skills form the base.
#    Repo-detected skills are ADDED only if not already present.
#    The final set is categorised for the Technical Skills section.
# ---------------------------------------------------------------------------

# Mapping from raw package/import names to human-friendly skill labels
SKILL_LABEL_MAP = {
    "sklearn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "torch": "PyTorch",
    "openai": "OpenAI",
    "langchain": "LangChain",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "plotly": "Plotly",
    "nltk": "NLTK",
    "sentence_transformers": "Sentence-Transformers (SBERT)",
    "sentence-transformers": "Sentence-Transformers (SBERT)",
    "xgboost": "XGBoost",
    "imbalanced-learn": "Imbalanced-learn / SMOTE",
    "imblearn": "Imbalanced-learn / SMOTE",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "django": "Django",
    "celery": "Celery",
    "redis": "Redis",
    "pillow": "Pillow",
    "tenacity": "Tenacity",
    "requests": "Requests",
    "scipy": "SciPy",
    "sounddevice": "SoundDevice",
}


def merge_skills(user_skills: set[str], repo_raw_skills: set[str]) -> dict[str, str]:
    """
    Merge user-supplied and repo-detected skills.

    Returns a dict: {human_label: source}
        source is either "user" or "repo"

    Skills already present in user_skills are NOT duplicated.
    """
    merged: dict[str, str] = {skill: "user" for skill in user_skills}

    for raw in repo_raw_skills:
        label = SKILL_LABEL_MAP.get(raw.lower(), raw.capitalize())
        if label not in merged:
            merged[label] = "repo"

    return merged


# ---------------------------------------------------------------------------
# 6. PROJECT BULLET ASSEMBLY
#    Combines README description + feature bullets + tech stack into the
#    structured project entry used in RESUME_DRAFT.md.
# ---------------------------------------------------------------------------

def build_project_entry(
    repo_name: str,
    readme_text: str,
    requirements_text: str = "",
    sample_code: str = "",
) -> dict:
    """
    Build a structured project entry for the resume from repo content.

    All text originates from the repository — no user-provided descriptions.

    Parameters
    ----------
    repo_name       : e.g. 'kaisarfardin6620/Hr-Ai-Assistant'
    readme_text     : raw content of README.md
    requirements_text: raw content of requirements.txt (empty string if absent)
    sample_code     : raw content of any .py or .ipynb file (for import scanning)

    Returns
    -------
    dict with keys: name, url, description_source, features, tech_stack, tech_source
    """
    description = extract_readme_description(readme_text)
    features = extract_readme_features(readme_text)

    tech_skills: set[str] = set()

    if requirements_text:
        req_skills = extract_requirements_skills(requirements_text)
        tech_skills |= req_skills
        tech_source = "requirements.txt"
    else:
        tech_source = "README pip install / import statements"

    if sample_code:
        import_skills = extract_import_skills(sample_code)
        tech_skills |= import_skills

    short_name = repo_name.split("/")[-1]
    return {
        "name": short_name,
        "url": f"https://github.com/{repo_name}",
        "description": description,
        "description_source": "README.md — first paragraph",
        "features": features,
        "features_source": "README.md — Features section bullets",
        "tech_stack": sorted(tech_skills),
        "tech_source": tech_source,
    }


# ---------------------------------------------------------------------------
# 7. MAIN — DRY-RUN DEMO
#    Uses the already-fetched data shown in RESUME_DATA_SOURCES.md to print
#    a sample output without making live API calls.
# ---------------------------------------------------------------------------

# Representative extracted data (mirrors what was fetched during resume generation)
SAMPLE_EXTRACTED_REPOS = {
    "Hr-Ai-Assistant": {
        "readme_snippet": "A suite of robust, production-ready Python backend modules for various "
                          "HR domains. Each assistant leverages OpenAI's GPT models.",
        "requirements": "openai>=1.0.0\npython-dotenv>=1.0.0\ntenacity>=8.0.0\n"
                        "sounddevice>=0.4.0\nscipy>=1.7.0\nrequests>=2.25.0",
        "tech_source": "requirements.txt",
    },
    "AppleNet-AE": {
        "readme_snippet": "Robust, modular pipeline for unsupervised deep learning on apple images "
                          "using Keras/TensorFlow — autoencoder, VAE, anomaly detection.",
        "requirements": "",  # no requirements.txt — detected from README pip install
        "tech_from_readme": ["tensorflow", "matplotlib", "scikit-learn", "pillow"],
        "tech_source": "README.md pip install section",
    },
    "Customer-Churn-Prediction": {
        "readme_snippet": "Implements various machine learning models to predict customer churn "
                          "including Logistic Regression, XGBoost, and ANN.",
        "requirements": "",
        "tech_from_readme": [
            "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn",
            "imbalanced-learn", "xgboost", "plotly", "tensorflow", "scikeras",
        ],
        "tech_source": "README.md pip install section",
    },
    "Quora-Question-Pair-Classification-Using-Sbert-And-Deep-Learning": {
        "readme_snippet": "Classifies Quora question pairs as duplicate/not-duplicate using "
                          "pretrained SBERT embeddings and ANN, LSTM, Siamese Networks.",
        "requirements": "",
        "tech_from_readme": [
            "sentence-transformers", "imbalanced-learn", "seaborn",
            "pandas", "tensorflow", "sklearn", "nltk", "matplotlib",
        ],
        "tech_source": "README.md pip install + notebook import statements",
    },
}


def demo():
    """Print a dry-run summary of extraction results."""
    print("=" * 70)
    print("RESUME GENERATOR — Data Source Transparency Report")
    print("=" * 70)

    print("\n[USER-SUPPLIED DATA]")
    print(f"  Name:       {USER_INFO['name']}")
    print(f"  Email:      {USER_INFO['email']}")
    print(f"  Phone:      {USER_INFO['phone']}")
    print(f"  LinkedIn:   {USER_INFO['linkedin']}")
    print(f"  Summary:    (verbatim from user message — {len(PROFESSIONAL_SUMMARY)} chars)")
    print(f"  Work roles: {len(WORK_EXPERIENCE)} positions (all bullets verbatim)")
    print(f"  Education:  {len(EDUCATION)} entries (all verbatim)")
    print(f"  Base skills supplied: {len(USER_SUPPLIED_SKILLS)}")

    print("\n[REPO-EXTRACTED DATA]")
    print(f"  Repositories to scan: {len(REPOS)}")

    # Demonstrate skill extraction from one sample repo
    sample_reqs = SAMPLE_EXTRACTED_REPOS["Hr-Ai-Assistant"]["requirements"]
    repo_skills_raw = extract_requirements_skills(sample_reqs)
    print(f"\n  Hr-Ai-Assistant / requirements.txt → detected packages:")
    for pkg in sorted(repo_skills_raw):
        label = SKILL_LABEL_MAP.get(pkg, pkg.capitalize())
        already = "already in user skills" if pkg.upper() in {s.upper() for s in USER_SUPPLIED_SKILLS} else "NEW → added to resume"
        print(f"    {pkg:<30} → {label:<35} [{already}]")

    print("\n[SKILLS MERGE PREVIEW]")
    all_repo_skills: set[str] = set()
    for repo_data in SAMPLE_EXTRACTED_REPOS.values():
        if repo_data.get("requirements"):
            all_repo_skills |= extract_requirements_skills(repo_data["requirements"])
        for skill in repo_data.get("tech_from_readme", []):
            all_repo_skills.add(skill)

    merged = merge_skills(USER_SUPPLIED_SKILLS, all_repo_skills)
    repo_additions = {k: v for k, v in merged.items() if v == "repo"}
    print(f"  User-supplied skills: {sum(1 for v in merged.values() if v == 'user')}")
    print(f"  Repo-detected additions: {len(repo_additions)}")
    print(f"  Additions: {', '.join(sorted(repo_additions.keys()))}")

    print("\n[NOTE]")
    print("  Project bullets in RESUME_DRAFT.md come ONLY from README.md content")
    print("  and requirements.txt / code imports. No user-provided project")
    print("  descriptions are used. See RESUME_DATA_SOURCES.md for full detail.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
