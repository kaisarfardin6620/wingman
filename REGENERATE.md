# Resume Regeneration Guide

This guide explains how to update and regenerate your resume from the template files in this repository.

---

## Files Overview

| File | Purpose |
|---|---|
| `RESUME_DRAFT.md` | Your current finalized resume draft |
| `resume_template.md` | Blank template with `{{PLACEHOLDER}}` tokens |
| `project_bullets.md` | All projects with bullets, tech stacks, and GitHub links |
| `REGENERATE.md` | This file — instructions for re-generating |

---

## How to Update Your Resume

### Option 1: Edit RESUME_DRAFT.md Directly (Quickest)

Open `RESUME_DRAFT.md` in any text editor and update the relevant sections.
When applying for a new role, tailor the summary and swap out projects from `project_bullets.md` to match the job description.

### Option 2: Use the Template + Python Script

1. Copy `resume_template.md` to a new file (e.g., `my_resume.md`)
2. Replace all `{{PLACEHOLDER}}` tokens with your values
3. Run the generator script:

```bash
python generate_resume.py --template resume_template.md --output my_resume.md
```

### Option 3: CLI One-liner (Requires sed)

```bash
sed \
  -e 's/{{FULL_NAME}}/Abdullah Kaisar Fardin/g' \
  -e 's/{{EMAIL}}/kaisarfardin128@gmail.com/g' \
  -e 's/{{PHONE}}/01708050645/g' \
  -e 's/{{LINKEDIN}}/www.linkedin.com\/in\/abdullah-kaisar-fardin/g' \
  -e 's/{{LOCATION}}/Dhaka, Bangladesh/g' \
  resume_template.md > RESUME_DRAFT.md
```

Add more `-e` flags for summary, skills, and other sections as needed.

---

## Python Generator Script

Save this as `generate_resume.py` in the repository root:

```python
import re
import sys

# Map of placeholder tokens to actual values
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
        "ongoing postgraduate studies in Data Science."
    ),
    "{{LANGUAGES}}": "Python (Advanced), SQL",
    "{{FRAMEWORKS}}": "Django, Django Channels (WebSockets), FastAPI, Celery",
    "{{AI_ML_SKILLS}}": "TensorFlow, MediaPipe (CV), OpenAI (Vision/Audio), LangChain, RAG",
    "{{DATA_ENGINEERING}}": "Neo4j (Graph DB), Pinecone (Vector DB), Redis, PostgreSQL, MongoDB",
    "{{INFRASTRUCTURE}}": "Docker, Nginx, AWS S3, Firebase (FCM), CI/CD Pipelines",
    # Work Experience
    "{{JOB_TITLE_1}}": "Jr AI Developer",
    "{{COMPANY_1}}": "SparkTech Agency",
    "{{LOCATION_1}}": "Dhaka",
    "{{START_DATE_1}}": "Aug 2025",
    "{{END_DATE_1}}": "Present",
    "{{JOB_BULLET_1_1}}": "Architecting asynchronous backend systems using Django and FastAPI, handling concurrent AI inference requests via Celery task queues.",
    "{{JOB_BULLET_1_2}}": "Integrated multimodal AI models (GPT-4o Vision, Whisper Audio) into production workflows, handling file uploads, OCR, and transcription at scale.",
    "{{JOB_BULLET_1_3}}": "Built and maintained file upload and processing pipelines supporting real-time AI-driven data extraction.",
    "{{JOB_TITLE_2}}": "Trainee AI Developer",
    "{{COMPANY_2}}": "SparkTech Agency",
    "{{LOCATION_2}}": "Dhaka",
    "{{START_DATE_2}}": "May 2025",
    "{{END_DATE_2}}": "Aug 2025",
    "{{JOB_BULLET_2_1}}": "Developed modular backend services for data preprocessing and LLM context window management.",
    "{{JOB_BULLET_2_2}}": "Assisted in the containerization (Docker) and deployment of ML services to cloud environments.",
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
        print(f"Warning: {len(remaining)} unfilled placeholders: {remaining}")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Resume written to {output_path}")

if __name__ == "__main__":
    template = sys.argv[1] if len(sys.argv) > 1 else "resume_template.md"
    output = sys.argv[2] if len(sys.argv) > 2 else "RESUME_DRAFT.md"
    generate(template, output)
```

Run it:

```bash
python generate_resume.py resume_template.md RESUME_DRAFT.md
```

---

## How to Add a New Project

1. Open `project_bullets.md`
2. Add your new project under the appropriate category section using the format:

```
### Project Name
Tech: Python, FastAPI, ...
GitHub: https://github.com/yourusername/repo-name
Category: Backend AI
- Bullet describing what you built and the impact.
- Second bullet with technical detail.
```

3. Copy the bullets into `RESUME_DRAFT.md` under the PROJECTS section (or update `REPLACEMENTS` in `generate_resume.py` and re-run).

---

## ATS Formatting Rules (Do Not Break)

- Use plain text only — no tables, graphics, icons, or columns
- Section headers must be ALL CAPS (PROJECTS, EDUCATION, etc.)
- Use simple hyphens (`-`) for bullet points, not special characters
- Keep consistent date formats: `Mon YYYY` or `YYYY`
- One blank line between sections; no blank lines inside bullet lists
- Keep to one page for roles requiring 0-3 years experience; two pages is acceptable for senior roles

---

## Converting to PDF

### Option 1: Pandoc (Recommended)

```bash
pip install pandoc
pandoc RESUME_DRAFT.md -o resume.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

### Option 2: VS Code Extension

Install the "Markdown PDF" extension in VS Code, open `RESUME_DRAFT.md`, and use Command Palette > "Markdown PDF: Export (pdf)".

### Option 3: Online Converter

Paste the content of `RESUME_DRAFT.md` into [Dillinger.io](https://dillinger.io) or [Markdown to PDF](https://md2pdf.netlify.app) and export.
