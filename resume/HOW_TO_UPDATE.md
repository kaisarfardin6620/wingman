# How to Update Your Resume

This folder contains everything you need to maintain and rebuild your resume as you add new projects.

---

## Files in this folder

| File | Purpose |
|---|---|
| `RESUME_DRAFT.md` | ✅ Your ready-to-use resume — edit contact info, then export to PDF |
| `PROJECT_BULLET_BANK.md` | 📦 All resume bullets for every project — pick 2–3 per project |
| `RESUME_TEMPLATE.md` | 🏗 Blank template with placeholders (for starting fresh) |
| `generate_resume.py` | ⚙️ Python script to rebuild `RESUME_DRAFT.md` automatically |
| `HOW_TO_UPDATE.md` | 📖 This file |

---

## Quick start — fill in your contact info

1. Open `RESUME_DRAFT.md`  
2. Replace the placeholder lines at the top:
   - `your.email@example.com` → your real email  
   - `+880-XXXX-XXXXXX` → your phone  
   - `[Your Field]`, `[Your University]`, `[Year]` → your actual degree details  
3. Export to PDF with any Markdown → PDF tool (e.g. VS Code + Markdown PDF extension, Pandoc, Typora, or paste into Overleaf/Google Docs).

---

## How to add a new project to the resume

### Step 1 — Add bullets to `PROJECT_BULLET_BANK.md`

Copy the template at the bottom of the file and fill it in:

```markdown
## N. Project Name
**Repo:** https://github.com/kaisarfardin6620/<repo-name>
**Stack:** Python, FastAPI, OpenAI, ...

**Bullets (pick 2–3):**
- [Action verb] [what you built] using [key tech], achieving [impact/metric].
- [Action verb] [key technical challenge] with [approach], resulting in [outcome].
- [Action verb] [deployment/infra/testing detail] to [goal].
```

### Step 2 — Add the project to `generate_resume.py`

Open `generate_resume.py`, scroll to `PROJECT_REGISTRY`, and add a new entry before the `# ADD NEW PROJECTS BELOW THIS LINE` comment:

```python
{
    "name":       "My New Project — Short Description",
    "repo_url":   "https://github.com/kaisarfardin6620/<repo-name>",
    "stack_tags": "Python · FastAPI · OpenAI · PostgreSQL",
    "include":    True,
    "bullets": [
        "Built X using Y, achieving Z.",
        "Implemented A with B, resulting in C.",
        "Deployed D with E to F.",
    ],
},
```

**Tips for writing strong bullets:**
- Start with an **action verb**: Built, Designed, Engineered, Implemented, Automated, Deployed, Integrated, Optimized.
- Mention **technology**: be specific (e.g. "GPT-4o" not just "AI").
- Quantify where possible: response times, dataset sizes, number of users, percentage improvements.
- Focus on what you *built* and what *impact* it had, not just what the project is.

### Step 3 — Re-run the generator

```bash
python resume/generate_resume.py
```

This overwrites `RESUME_DRAFT.md` with the updated resume.

---

## How to hide a project (without deleting it)

In `generate_resume.py`, set `include=False` on the project entry:

```python
{
    "name":    "...",
    "include": False,   # ← hides from resume but keeps bullets safe
    ...
},
```

Re-run `python resume/generate_resume.py`.

---

## How to update personal info (email, phone, education)

Edit the `PERSONAL` and `EDUCATION` dicts near the top of `generate_resume.py`, then re-run the script.

---

## Scalability checklist

When adding many new repos in one batch:

1. [ ] Skim each repo's `README.md` and `requirements.txt` to identify the stack.
2. [ ] Write 3–5 bullet options in `PROJECT_BULLET_BANK.md`.
3. [ ] Add one entry per project to `PROJECT_REGISTRY` in `generate_resume.py`.
4. [ ] Run `python resume/generate_resume.py`.
5. [ ] Review `RESUME_DRAFT.md` — keep the resume to **1 page** by setting `include=False` on lower-priority projects.
6. [ ] Commit the changes.

---

## Resume priorities (keep these at the top)

The following priorities are pre-configured in `generate_resume.py`:

1. **AI Engineering focus** — Lead with LLM/RAG/Knowledge Graph projects.
2. **1 year of experience** — Do not exaggerate; let the project depth speak for itself.
3. **Dhaka, Bangladesh** — Keep location visible; mention "open to remote" at the bottom.
4. **BSc completed, MSc ongoing** — List MSc first (most recent) in the Education section.
5. **Production quality** — Highlight Docker, async pipelines, auth, and deployment details — these signal production-ready skills.

---

## Sharing new repos with Copilot

When you want Copilot to add a new repo to your resume, share:

1. The GitHub URL(s).
2. A one-line description of what the project does (optional — Copilot will read the README).
3. Whether to `include=True` or `include=False` by default.

Copilot will then:
- Read the README and requirements.txt.
- Write bullet options in `PROJECT_BULLET_BANK.md`.
- Add the entry to `PROJECT_REGISTRY` in `generate_resume.py`.
- Re-run the generator and commit the updated `RESUME_DRAFT.md`.
