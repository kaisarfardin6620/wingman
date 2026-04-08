# How to Update Your Resume

This folder contains everything you need to maintain and regenerate your resume as you add new projects.

---

## Files in this folder

| File | Purpose |
|---|---|
| `RESUME_DRAFT.md` | Your ready-to-use resume — edit contact info, then export to PDF |
| `PROJECT_BULLET_BANK.md` | All resume bullets for every project — pick 2–3 per project |
| `RESUME_TEMPLATE.md` | Blank template with placeholders for name, contact, education |
| `generate_resume.py` | Python script — configure `PROJECT_REGISTRY`, run to rebuild `RESUME_DRAFT.md` |
| `HOW_TO_UPDATE.md` | This file |

---

## Quickstart: update personal info

1. Open `generate_resume.py`.
2. Edit the `PERSONAL` dict near the top:
   ```python
   PERSONAL = {
       "name": "Your Full Name",
       "title": "AI Engineer",
       "location": "Dhaka, Bangladesh",
       "github": "github.com/kaisarfardin6620",
       "email": "your.real.email@example.com",
       "phone": "+880-XXXX-XXXXXX",
   }
   ```
3. Edit the `EDUCATION` list similarly.
4. Run the script:
   ```bash
   python resume/generate_resume.py
   ```
5. Open `RESUME_DRAFT.md` to review.

---

## Show or hide a project on your resume

Every project in `PROJECT_REGISTRY` has an `include` flag:

```python
{
    "name": "My Project",
    ...
    "include": True,   # <- True = show on resume, False = hide
    ...
},
```

- Set `include=True` to show the project.
- Set `include=False` to hide it (it stays in `PROJECT_BULLET_BANK.md`).
- Run `python resume/generate_resume.py` to rebuild `RESUME_DRAFT.md`.

**Keep the resume to 1 page** by setting `include=False` on lower-priority projects.

---

## Add a new project

1. Open `generate_resume.py`.
2. Copy the template comment at the top of `PROJECT_REGISTRY` and add a new entry:
   ```python
   {
       "name":       "My New Project",
       "repo_url":   "https://github.com/kaisarfardin6620/my-new-repo",
       "stack_tags": "Python · FastAPI · OpenAI · PostgreSQL",
       "include":    True,
       "bullets": [
           "Built X using Y, achieving Z.",
           "Implemented A with B, resulting in C.",
           "Deployed D for E, improving F.",
       ],
   },
   ```
3. Also add an entry to `PROJECT_BULLET_BANK.md` for reference.
4. Run `python resume/generate_resume.py`.

---

## Scalability checklist (adding many repos at once)

1. - [ ] Skim each repo's `README.md` and `requirements.txt` to identify the stack.
2. - [ ] Write 3–5 bullet options in `PROJECT_BULLET_BANK.md`.
3. - [ ] Add one entry per project to `PROJECT_REGISTRY` in `generate_resume.py`.
4. - [ ] Run `python resume/generate_resume.py`.
5. - [ ] Review `RESUME_DRAFT.md` — keep to **1 page** by setting `include=False` on lower-priority projects.
6. - [ ] Commit the changes.

---

## Resume priorities (pre-configured in `generate_resume.py`)

1. **AI Engineering focus** — Lead with LLM/RAG/NLP/CV projects.
2. **1 year of experience** — Let project depth speak for itself.
3. **Dhaka, Bangladesh** — Keep location visible; mention "open to remote" at the bottom.
4. **BSc completed, MSc ongoing** — List MSc first (most recent) in Education.
5. **Production quality** — Highlight Docker, async pipelines, auth, deployment.

---

## Current project inventory (38 projects)

### Active on resume (include=True by default)
| # | Project | Type |
|---|---|---|
| 1 | Explainable Hybrid KG-RAG Chatbot | LLM / RAG / Research |
| 2 | MagicTale — AI Storytelling Platform | LLM / Backend |
| 3 | Reho AI Finance Microservice | LLM / FastAPI |
| 4 | Quora Question Pair Classification (SBERT) | NLP / Transformers |
| 5 | LungCancer-ImageNet | CV / Medical AI |

### Available to activate (include=False — flip to True as needed)
| # | Project | Type |
|---|---|---|
| 6 | HR AI Assistant | LLM / RAG |
| 7 | Bondly AI Financial Assistant | LLM / RAG / FinTech |
| 8 | Bible AI Assistant | LLM / RAG |
| 9 | Autoencoder Anomaly Detection | DL / Anomaly |
| 10 | Real vs. Fake News Classifier | NLP / BERT |
| 11 | NLP Twitter Sentiment Analysis | NLP / Transformers |
| 12 | LSTM for IMDb Sentiment | NLP / LSTM |
| 13 | NLP Spam Classification | NLP / Word Embeddings |
| 14 | Text Pair Classification | NLP / BERT/RoBERTa |
| 15 | LeafDiseaseClassifier | CV / Transfer Learning |
| 16 | Bangladeshi Medicinal Leaf Classification | CV / CNN |
| 17 | Marine Life Classifier | CV / CNN |
| 18 | FlowerNet — CNN Architecture Comparison | CV / Research |
| 19 | AppleNet-AE | CV / Autoencoder |
| 20 | Fashion-MNIST Sup/Semi-sup | ML / Semi-supervised |
| 21 | Butterfly Classifier | CV / Transfer Learning |
| 22 | Cat vs. Dog Classification | CV / Transfer Learning |
| 23 | Shoe Classifier | CV / CNN |
| 24 | CNN Preprocessings Toolkit | CV / Toolkit |
| 25 | CNN Visuals | CV / Interpretability |
| 26 | Customer Churn Prediction | ML / Classification |
| 27 | Lung Cancer Prediction (ML) | ML / Healthcare |
| 28 | Breast Cancer Survival Prediction | ML / Healthcare |
| 29 | Wine Quality Testing | ML / Regression |
| 30 | Sales Forecasting Regression | ML / Time Series |
| 31 | Weather Forecasting Models | ML / LSTM / Time Series |
| 32 | Weather Rainfall Prediction | ML / Classification |
| 33 | AI Image Creator (GlimmCatcher) | LLM / DALL-E / Web App |
| 34 | Wingman — AI Assistant Backend | Backend / LLM API |
| 35 | Benjaminkley 3D Scanner | CV / Biometrics |
| 36 | Rai Backend — AI Community Platform | Backend / LLM |
| 37 | MAIZ FastAPI | Backend / AI Service |
| 38 | DELUX AI | Backend / AI Service |

---

## Sharing new repos with Copilot

When you want Copilot to add a new repo, share:
1. The GitHub URL(s).
2. A one-line description of what the project does (optional).
3. Whether to set `include=True` or `include=False` by default.

Copilot will then read the README, write bullet options in `PROJECT_BULLET_BANK.md`, add the entry to `PROJECT_REGISTRY`, re-run the generator, and commit the updated `RESUME_DRAFT.md`.
