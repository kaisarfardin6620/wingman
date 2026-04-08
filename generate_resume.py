#!/usr/bin/env python3
"""
Resume generator: fills {{PLACEHOLDER}} tokens in resume_template.md
and writes the result to RESUME_DRAFT.md (or a path you specify).

Usage:
    python generate_resume.py
    python generate_resume.py resume_template.md RESUME_DRAFT.md
"""
import re
import sys

# ---------------------------------------------------------------------------
# Edit the values below to update your resume, then re-run the script.
# ---------------------------------------------------------------------------
REPLACEMENTS = {
    "{{FULL_NAME}}": "Abdullah Kaisar Fardin",
    "{{EMAIL}}": "kaisarfardin128@gmail.com",
    "{{PHONE}}": "01708050645",
    "{{LINKEDIN}}": "www.linkedin.com/in/abdullah-kaisar-fardin",
    "{{LOCATION}}": "Dhaka, Bangladesh",
    "{{PROFESSIONAL_SUMMARY}}": (
        "Results-driven AI Developer with hands-on experience in designing and deploying "
        "scalable, production-grade AI systems. Skilled in bridging the gap between cutting-edge "
        "research models and real-world applications, with expertise in building asynchronous "
        "backends using FastAPI and Django. Proficient in integrating multimodal AI solutions, "
        "including vision and audio models, into high-performance workflows. Strong foundation in "
        "data engineering, cloud deployment, and microservices architecture, complemented by "
        "ongoing postgraduate studies in Data Science. Passionate about delivering efficient, "
        "intelligent systems that solve complex business problems at scale."
    ),
    # Technical Skills
    "{{LANGUAGES}}": "Python (Advanced), SQL",
    "{{FRAMEWORKS}}": "Django, Django Channels (WebSockets), FastAPI, Celery",
    "{{AI_ML_SKILLS}}": "TensorFlow, MediaPipe (CV), OpenAI (Vision/Audio), LangChain, RAG",
    "{{DATA_ENGINEERING}}": "Neo4j (Graph DB), Pinecone (Vector DB), Redis, PostgreSQL, MongoDB",
    "{{INFRASTRUCTURE}}": "Docker, Nginx, AWS S3, Firebase (FCM), CI/CD Pipelines",
    # Work Experience — Job 1
    "{{JOB_TITLE_1}}": "Jr AI Developer",
    "{{COMPANY_1}}": "SparkTech Agency",
    "{{LOCATION_1}}": "Dhaka",
    "{{START_DATE_1}}": "Aug 2025",
    "{{END_DATE_1}}": "Present",
    "{{JOB_BULLET_1_1}}": (
        "Architecting asynchronous backend systems using Django and FastAPI, "
        "handling concurrent AI inference requests via Celery task queues."
    ),
    "{{JOB_BULLET_1_2}}": (
        "Integrated multimodal AI models (GPT-4o Vision, Whisper Audio) into production "
        "workflows, handling file uploads, OCR, and transcription at scale."
    ),
    "{{JOB_BULLET_1_3}}": (
        "Built and maintained file upload and processing pipelines supporting "
        "real-time AI-driven data extraction."
    ),
    # Work Experience — Job 2
    "{{JOB_TITLE_2}}": "Trainee AI Developer",
    "{{COMPANY_2}}": "SparkTech Agency",
    "{{LOCATION_2}}": "Dhaka",
    "{{START_DATE_2}}": "May 2025",
    "{{END_DATE_2}}": "Aug 2025",
    "{{JOB_BULLET_2_1}}": (
        "Developed modular backend services for data preprocessing "
        "and LLM context window management."
    ),
    "{{JOB_BULLET_2_2}}": (
        "Assisted in the containerization (Docker) and deployment "
        "of ML services to cloud environments."
    ),
    # Projects — adjust or add from project_bullets.md as needed
    "{{PROJECT_NAME_1}}": "Explainable Hybrid KG-RAG Chatbot",
    "{{PROJECT_TECH_1}}": "FastAPI, Neo4j, Pinecone, OpenAI GPT-4o, Python",
    "{{PROJECT_URL_1}}": "https://github.com/kaisarfardin6620/explainable-rag-chatbot",
    "{{PROJECT_BULLET_1_1}}": (
        "Engineered a research-grade hybrid RAG system combining vector search (Pinecone) "
        "with knowledge graph reasoning (Neo4j) to mitigate hallucinations."
    ),
    "{{PROJECT_BULLET_1_2}}": (
        "Implemented claim-level NLI verification and graph centrality scoring to produce "
        "structured reasoning chains and citations for every response."
    ),
    "{{PROJECT_BULLET_1_3}}": (
        "Built ablation modes (rag_only, kg_only, hybrid) with automated benchmarking "
        "pipeline measuring F1, semantic similarity, and latency."
    ),
    "{{PROJECT_NAME_2}}": "MagicTale AI Storytelling Platform",
    "{{PROJECT_TECH_2}}": "Django, Celery, Redis, OpenAI GPT-4o, DALL-E 3, ElevenLabs, Docker",
    "{{PROJECT_URL_2}}": "https://github.com/kaisarfardin6620/magictale",
    "{{PROJECT_BULLET_2_1}}": (
        "Built a production-grade async backend generating personalized children's stories, "
        "DALL-E 3 cover illustrations, and ElevenLabs voice narration via a Celery pipeline."
    ),
    "{{PROJECT_BULLET_2_2}}": (
        "Delivered real-time progress updates over Django Channels WebSockets with "
        "Firebase push notifications on completion."
    ),
    # Education
    "{{DEGREE_1}}": "MSc in Data Science and Analytics",
    "{{INSTITUTION_1}}": "East West University",
    "{{LOCATION_EDUCATION_1}}": "Dhaka",
    "{{EDU_START_1}}": "Jan 2026",
    "{{EDU_END_1}}": "Present",
    "{{DEGREE_2}}": "BSc in Computer Science and Engineering",
    "{{INSTITUTION_2}}": "Bangladesh University of Business and Technology",
    "{{LOCATION_EDUCATION_2}}": "Dhaka",
    "{{EDU_START_2}}": "2019",
    "{{EDU_END_2}}": "2024",
}


def generate(template_path: str, output_path: str) -> None:
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    for placeholder, value in REPLACEMENTS.items():
        content = content.replace(placeholder, value)

    remaining = re.findall(r"\{\{[A-Z_0-9]+\}\}", content)
    if remaining:
        print(f"Warning: {len(remaining)} unfilled placeholder(s) remain: {remaining}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Resume written to: {output_path}")


if __name__ == "__main__":
    template = sys.argv[1] if len(sys.argv) > 1 else "resume_template.md"
    output = sys.argv[2] if len(sys.argv) > 2 else "RESUME_DRAFT.md"
    generate(template, output)
