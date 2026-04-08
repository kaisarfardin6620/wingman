# Resume Generator — How to Customise

This folder contains everything you need to maintain an up-to-date, ATS-friendly resume generated directly from your GitHub projects.

---

## Folder Structure

```
resume/
├── README.md               ← You are here
├── resume_template.md      ← Blank resume skeleton (edit your personal info here)
├── project_bullets.md      ← Bullet-point bank for each project
└── generate_resume.py      ← Script that combines template + bullets → RESUME_DRAFT.md
```

`RESUME_DRAFT.md` lives in the **repo root** and is the output of the generator.

---

## Quick Start

### Prerequisites

- Python 3.8+

### 1 — Fill in your personal details

Open `resume/resume_template.md` and replace every `[placeholder]` with your real information:

- Full name
- Target role
- Email, GitHub, LinkedIn URLs
- Education
- Work experience (if any)

### 2 — Update project bullets (optional)

Open `resume/project_bullets.md` and:

- Replace `(X%)`, `(N users)`, `(X hours/week)` etc. with real metrics where you have them.
- Add or remove bullet points to emphasise different skills for different job applications.
- Add new `## PROJECT: <id>` blocks for future projects.

### 3 — Run the generator

```bash
# From the repo root
python resume/generate_resume.py
```

This regenerates `RESUME_DRAFT.md` in the repo root.

### 4 — Convert to PDF (optional)

Install [Pandoc](https://pandoc.org/) and a LaTeX engine, then run:

```bash
pandoc RESUME_DRAFT.md -o RESUME_DRAFT.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=11pt
```

Or paste the Markdown into [Markdown to PDF](https://md2pdf.netlify.app/) for a quick browser conversion.

---

## Customising for a Specific Job

1. Duplicate `project_bullets.md` → e.g. `project_bullets_ml.md`
2. Edit that copy to re-order or rewrite bullets to match the job description keywords.
3. Run:
   ```bash
   python resume/generate_resume.py --bullets resume/project_bullets_ml.md --output RESUME_ML.md
   ```

---

## Adding a New Project

1. Open `resume/project_bullets.md`.
2. Append a new block following this pattern:

```markdown
---

## PROJECT: your-repo-name

**Name:** Human-Readable Project Name
**URL:** https://github.com/kaisarfardin6620/your-repo-name
**Stack:** Framework · Database · Key Library

- Action verb + what you built + impact/metric placeholder.
- Action verb + technical challenge you solved.
- Action verb + scale or outcome.
```

3. Re-run `python resume/generate_resume.py`.

---

## Tips for ATS Optimisation

- Mirror keywords from the job description in your bullet points (e.g., "REST API", "microservices", "CI/CD").
- Keep bullets to one sentence each: **Action verb → What you did → Result/Metric**.
- Avoid tables if submitting to older ATS parsers; convert the Skills section to a comma-separated list instead.
- Aim for a single page (~600–800 words in the output Markdown).
