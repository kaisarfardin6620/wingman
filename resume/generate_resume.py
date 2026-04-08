#!/usr/bin/env python3
"""
generate_resume.py
==================
Regenerates RESUME_DRAFT.md from the project bullet bank and personal info.

USAGE
-----
  python resume/generate_resume.py

To add a new project
--------------------
1. Add its entry to PROJECT_REGISTRY below (copy/paste the template).
2. Add its bullet bank block to PROJECT_BULLET_BANK.md.
3. Re-run this script.

To remove a project from the resume
-------------------------------------
Set `include=False` on the project entry in PROJECT_REGISTRY.

To add a new repo shared by the user
--------------------------------------
1. Read the repo README / requirements.txt to understand the stack.
2. Add an entry to PROJECT_REGISTRY with the key facts.
3. Write 3–5 bullet options in PROJECT_BULLET_BANK.md.
4. Re-run this script.
"""

import os
import textwrap
from datetime import date

# ---------------------------------------------------------------------------
# PERSONAL INFO — fill these in once
# ---------------------------------------------------------------------------
PERSONAL = {
    "name":        "Kaisar Fardin",
    "role":        "AI Engineer",
    "city":        "Dhaka",
    "country":     "Bangladesh",
    "github":      "https://github.com/kaisarfardin6620",
    "email":       "your.email@example.com",   # ← replace
    "phone":       "+880-XXXX-XXXXXX",         # ← replace
}

EDUCATION = [
    {
        "degree": "MSc in [Your Field]",
        "university": "[Your University]",
        "city": "Dhaka",
        "status": "Ongoing",
    },
    {
        "degree": "BSc in [Your Field]",
        "university": "[Your University]",
        "city": "Dhaka",
        "status": "Completed, [Year]",
    },
]

SKILLS = {
    "Languages":          "Python",
    "Frameworks":         "Django 5, Django REST Framework, FastAPI",
    "AI / LLM":           "OpenAI API (GPT-4o, DALL-E 3, Embeddings), Google GenAI (Gemini), "
                          "Retrieval-Augmented Generation (RAG), Knowledge Graphs, NLP/NLI",
    "Vector / Graph DBs": "Pinecone, Neo4j",
    "Databases":          "PostgreSQL, MongoDB, Redis, SQLite",
    "Async / Real-time":  "Celery, Django Channels, WebSockets, Daphne",
    "Infrastructure":     "Docker, Docker Compose, Nginx, AWS S3, Firebase FCM",
    "Auth & Security":    "JWT (SimpleJWT), Google OAuth2, Apple Sign-In, Email OTP",
    "Tools":              "Git, Swagger / OpenAPI, Postman",
}

OPEN_TO = (
    "New AI Engineering roles in Dhaka or remote. "
    "Interests include LLM systems, RAG pipelines, AI microservices, and production ML backends."
)

# ---------------------------------------------------------------------------
# PROJECT REGISTRY
# ---------------------------------------------------------------------------
# Each entry:
#   name        – display name
#   repo_url    – full GitHub URL
#   stack_tags  – comma-separated tech (shown as inline code block)
#   include     – True/False; set False to hide from resume without deleting
#   bullets     – list of bullet strings; pick the best 2–3 per project
#
# TEMPLATE (copy-paste to add a new project):
# {
#     "name":       "Project Name",
#     "repo_url":   "https://github.com/kaisarfardin6620/<repo>",
#     "stack_tags": "Python · FastAPI · OpenAI · PostgreSQL",
#     "include":    True,
#     "bullets": [
#         "Built X using Y, achieving Z.",
#         "Implemented A with B, resulting in C.",
#     ],
# },

PROJECT_REGISTRY = [
    # -----------------------------------------------------------------------
    # 1. EXPLAINABLE RAG CHATBOT (Research)
    # -----------------------------------------------------------------------
    {
        "name":       "Explainable Hybrid KG-RAG Chatbot *(Research)*",
        "repo_url":   "https://github.com/kaisarfardin6620/explainable-rag-chatbot",
        "stack_tags": "Python · FastAPI · OpenAI GPT-4o · Pinecone · Neo4j · NLI",
        "include":    True,
        "bullets": [
            "Designed a research-grade Hybrid RAG system combining Pinecone vector search "
            "with Neo4j knowledge-graph traversal to reduce LLM hallucinations and provide "
            "claim-level explainability.",
            "Built a post-hoc NLI verification layer that abstains from answering when "
            "confidence falls below 0.4; applied Freeman's Degree Centrality to weight "
            "evidence from authoritative graph entities.",
            "Architected three ablation modes (`hybrid`, `rag_only`, `kg_only`) and a "
            "benchmark automation script generating comparative F1, semantic similarity, "
            "and latency reports — supporting the paper "
            "*\"Hybrid Knowledge Graph–Guided Explainable RAG for Trustworthy QA\"*.",
        ],
    },
    # -----------------------------------------------------------------------
    # 2. MAGICTALE
    # -----------------------------------------------------------------------
    {
        "name":       "MagicTale — AI Children's Storytelling Platform",
        "repo_url":   "https://github.com/kaisarfardin6620/magictale",
        "stack_tags": "Python · Django 5 · Celery · OpenAI GPT-4o · DALL-E 3 · ElevenLabs · WebSockets",
        "include":    True,
        "bullets": [
            "Engineered an async AI content pipeline (Celery + Redis) that generates "
            "personalized stories (GPT-4o), cover illustrations (DALL-E 3), and voice "
            "narration (ElevenLabs TTS) without blocking the HTTP layer.",
            "Implemented real-time story-generation progress over Django Channels "
            "WebSockets; integrated Google OAuth2, Apple Sign-In, FCM push notifications, "
            "and RevenueCat subscription webhooks.",
            "Containerized the full stack (Django/Daphne + Celery + Redis + PostgreSQL + "
            "Nginx) with Docker Compose; auto-generated OpenAPI 3.0 docs via drf-spectacular.",
        ],
    },
    # -----------------------------------------------------------------------
    # 3. REHO AI FINANCE MICROSERVICE
    # -----------------------------------------------------------------------
    {
        "name":       "Reho AI Finance Microservice",
        "repo_url":   "https://github.com/kaisarfardin6620/Reho-AI-Service",
        "stack_tags": "Python · FastAPI · OpenAI GPT-4o · MongoDB (Motor) · Redis · WebSockets",
        "include":    True,
        "bullets": [
            "Built an AI microservice that dynamically injects live user financial data "
            "into the GPT-4o system prompt, enabling context-aware conversational advice "
            "over real-time WebSockets.",
            "Developed admin intelligence endpoints auto-generating user 360° summaries, "
            "spending heatmaps, and debt-to-income risk scores (Low/Medium/High) using GPT-4o.",
            "Scheduled nightly background jobs to pre-compute heavy analytics reports, "
            "significantly reducing daytime dashboard load times via Redis caching.",
        ],
    },
    # -----------------------------------------------------------------------
    # 4. WINGMAN
    # -----------------------------------------------------------------------
    {
        "name":       "Wingman — AI Assistant Backend",
        "repo_url":   "https://github.com/kaisarfardin6620/wingman",
        "stack_tags": "Python · Django 5 · Celery · OpenAI · Google GenAI · WebSockets · PostgreSQL",
        "include":    True,
        "bullets": [
            "Developed a full-featured Django REST API powering an AI chat assistant with "
            "JWT-secured endpoints, real-time WebSocket chat (Django Channels), and "
            "subscription tier management.",
            "Integrated OpenAI and Google GenAI (Gemini) for multi-modal AI responses; "
            "implemented tiktoken-based token counting for accurate usage billing.",
        ],
    },
    # -----------------------------------------------------------------------
    # 5. BENJAMINKLEY — 3D HEAD SCANNER
    # -----------------------------------------------------------------------
    {
        "name":       "Benjaminkley — 3D Head Scanner & Biometric Analysis",
        "repo_url":   "https://github.com/kaisarfardin6620/benjaminkley",
        "stack_tags": "Python · Django 5 · Celery · KeenTools API · trimesh · numpy · AWS S3",
        "include":    True,
        "bullets": [
            "Designed an end-to-end 3D scanning pipeline: uploaded multi-image datasets "
            "to KeenTools API, downloaded `.obj` meshes, and automatically calculated "
            "biometric measurements (head width, circumference, ear-to-ear distance) "
            "using trimesh and numpy.",
            "Implemented async scan processing with Celery + Redis; auto-generated "
            "biometric PDF reports and delivered FCM push notifications on completion; "
            "stored assets on AWS S3.",
        ],
    },
    # -----------------------------------------------------------------------
    # 6. RAI BACKEND
    # -----------------------------------------------------------------------
    {
        "name":       "Rai Backend — AI Community Platform",
        "repo_url":   "https://github.com/kaisarfardin6620/Rai_Backend",
        "stack_tags": "Python · Django 5 · Celery · OpenAI · Google GenAI · WebSockets · PostgreSQL",
        "include":    False,   # set True to include in resume
        "bullets": [
            "Built a scalable Django REST API backend integrating OpenAI and Google GenAI "
            "for an AI-powered community platform, with JWT authentication, subscription "
            "management, and real-time chat via Django Channels.",
            "Implemented asynchronous task handling (Celery + Redis) for background AI "
            "inference and notification delivery; used Django Anymail for transactional "
            "email and Daphne as the ASGI server.",
        ],
    },
    # -----------------------------------------------------------------------
    # 7. DELUX_AI
    # -----------------------------------------------------------------------
    {
        "name":       "DELUX_AI — FastAPI AI Service",
        "repo_url":   "https://github.com/kaisarfardin6620/DELUX_AI",
        "stack_tags": "Python · FastAPI · PostgreSQL (asyncpg) · OpenAI · Redis · JWT · Docker",
        "include":    False,   # set True to include in resume
        "bullets": [
            "Engineered a high-performance async FastAPI service with PostgreSQL (asyncpg), "
            "per-user rate limiting (Redis), structured JSON logging, and JWT-based "
            "authentication.",
            "Integrated OpenAI API for AI inference endpoints; containerized the service "
            "with Docker and Docker Compose.",
        ],
    },
    # -----------------------------------------------------------------------
    # 8. MAIZ-FASTAPI
    # -----------------------------------------------------------------------
    {
        "name":       "Maiz FastAPI — AI Microservice",
        "repo_url":   "https://github.com/kaisarfardin6620/maiz-fastapi",
        "stack_tags": "Python · FastAPI · MongoDB (Motor) · OpenAI · JWT · Docker",
        "include":    False,   # set True to include in resume
        "bullets": [
            "Developed an async FastAPI microservice backed by MongoDB (Motor) and OpenAI "
            "for AI-driven features, secured with JWT authentication and Pydantic data "
            "validation.",
        ],
    },
    # -----------------------------------------------------------------------
    # ADD NEW PROJECTS BELOW THIS LINE
    # Copy the template from the top of this file and paste it here.
    # -----------------------------------------------------------------------
]

# ---------------------------------------------------------------------------
# GENERATOR — no edits needed below this line
# ---------------------------------------------------------------------------

def build_header(p: dict) -> str:
    return textwrap.dedent(f"""\
        # {p['name']}
        **{p['role']}**  
        {p['city']}, {p['country']}  
        GitHub: [{p['github'].replace('https://', '')}]({p['github']}) | Email: {p['email']} | Phone: {p['phone']}
    """)


def build_education(edu_list: list) -> str:
    lines = ["## Education\n"]
    for edu in edu_list:
        lines.append(
            f"**{edu['degree']}** — {edu['university']}, {edu['city']} *({edu['status']})*  "
        )
    return "\n".join(lines)


def build_skills(skills: dict) -> str:
    lines = ["## Technical Skills\n", "| Category | Skills |", "|---|---|"]
    for cat, val in skills.items():
        lines.append(f"| **{cat}** | {val} |")
    return "\n".join(lines)


def build_projects(registry: list) -> str:
    sections = ["## Projects\n"]
    active = [p for p in registry if p.get("include", True)]
    for proj in active:
        header = f"### {proj['name']}"
        stack  = f"`{proj['stack_tags']}`"
        url    = f"[{proj['repo_url'].replace('https://github.com/', 'github.com/')}]({proj['repo_url']})"
        bullets = "\n".join(f"- {b}" for b in proj["bullets"])
        sections.append(f"{header}  \n{stack}  \n{url}\n\n{bullets}")
    return "\n\n---\n\n".join(sections)


def main() -> None:
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    output_path  = os.path.join(script_dir, "RESUME_DRAFT.md")
    today        = date.today().strftime("%B %Y")

    parts = [
        build_header(PERSONAL),
        "---\n",
        build_education(EDUCATION),
        "---\n",
        build_skills(SKILLS),
        "---\n",
        build_projects(PROJECT_REGISTRY),
        "---\n",
        f"## Open to\n{OPEN_TO}",
        "---\n",
        f"*Last updated: {today} — generated by `resume/generate_resume.py`*",
    ]

    content = "\n\n".join(parts)

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(content)

    included = sum(1 for p in PROJECT_REGISTRY if p.get("include", True))
    print(f"✅  RESUME_DRAFT.md written to {output_path}")
    print(f"   Projects included : {included}")
    print(f"   Projects hidden   : {len(PROJECT_REGISTRY) - included}")
    print(f"   Tip: set include=True on any project to add it to the resume.")


if __name__ == "__main__":
    main()
