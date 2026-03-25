<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:1f6feb&height=180&section=header&text=AI%20Resume%20Matcher&fontSize=42&fontColor=58a6ff&animation=fadeIn&fontAlignY=32&desc=AI-Powered%20Resume%20Optimization%20Platform&descSize=16&descColor=8b949e&descAlignY=52" width="100%" />

<br>

[![Python](https://img.shields.io/badge/Python-3.11-0d1117?style=for-the-badge&logo=python&logoColor=3776AB)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-0d1117?style=for-the-badge&logo=chainlink&logoColor=1C3C3C)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-0d1117?style=for-the-badge&logo=openai&logoColor=412991)](https://openai.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-0d1117?style=for-the-badge&logo=meta&logoColor=0467DF)](https://github.com/facebookresearch/faiss)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-0d1117?style=for-the-badge&logo=streamlit&logoColor=FF4B4B)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-0d1117?style=for-the-badge&logo=fastapi&logoColor=009688)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-0d1117?style=for-the-badge&logo=opensourceinitiative&logoColor=58a6ff)](LICENSE)

</div>

---

## 📌 Overview

This repository contains **two ML projects** built around intelligent resume analysis using **Retrieval-Augmented Generation (RAG)**:

| # | Project | Description | Entry Point |
|---|---------|-------------|-------------|
| **1** | **Simple RAG Pipeline** | Foundational RAG demo — loads a resume + job description, chunks documents, builds a FAISS vector store, and uses an LLM to analyze resume-JD fit | `app.py` / `cli.py` |
| **2** | **Full AI Resume Matcher Suite** | Production-ready web app with ATS scoring, keyword analysis, gap analysis, resume tailoring, and cover letter generation — deployed on Render & Vercel | `frontend/app.py` / `api/index.py` |

Both projects share the same `backend/` module, demonstrating progression from a basic RAG pipeline to the complete AI Resume Matcher platform.

---

## 🚀 Features

### Project 1 — RAG Pipeline (Foundation)

- Load resume (PDF/DOCX) and job description (TXT/MD)
- Split documents into optimized chunks (800 tokens, 100 overlap)
- Generate embeddings using OpenAI `text-embedding-3-small`
- Build FAISS vector store for semantic similarity search
- Query via LangChain `RetrievalQA` chain for fit analysis
- CLI support with `--resume` and `--jd` arguments

### Project 2 — AI Resume Matcher (Full Suite)

<table>
<tr>
<td width="50%">

**🎯 ATS Scoring**
- ATS compatibility score (0–100%)
- Section-by-section breakdown (contact, experience, skills, education, keywords)
- Matched & missing keywords with color tags
- Formatting issue detection
- Top 5 ATS optimization recommendations

</td>
<td width="50%">

**🔑 Keyword Extraction**
- Structured keyword extraction from job descriptions
- 7 categories: hard skills, soft skills, certifications, experience, education, action verbs, industry terms
- Visual keyword tag display

</td>
</tr>
<tr>
<td width="50%">

**📊 RAG Gap Analysis**
- Semantic match percentage
- Matched skills vs. skill gaps
- Improvement suggestions with source chunks
- Powered by FAISS vector similarity + LLM reasoning

</td>
<td width="50%">

**✏️ Resume Tailoring**
- AI rewrites resume optimized for the target JD
- 4 template styles: Professional, Modern, Minimal, Creative
- Preserves factual data while optimizing keywords & phrasing
- ATS-friendly output (no tables/columns)

</td>
</tr>
<tr>
<td colspan="2" align="center">

**💌 Cover Letter Generation**
- Personalized cover letter for specific company/role
- References actual resume experiences + JD requirements
- 3–4 paragraphs (~300–400 words)
- Export as PDF or DOCX

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
ai-resume-matcher/
│
├── app.py                  # Project 1: Simple RAG pipeline demo
├── cli.py                  # Project 1: CLI interface (--resume, --jd)
├── config.py               # Root config
│
├── backend/                # Shared ML backend (14 modules)
│   ├── loader.py           # Resume (PDF/DOCX) & JD (TXT/MD) file loading
│   ├── splitter.py         # RecursiveCharacterTextSplitter (chunk_size=800)
│   ├── embeddings.py       # OpenAI text-embedding-3-small
│   ├── vectorstore.py      # FAISS vector store creation
│   ├── retriever.py        # Similarity search retriever (top_k=3)
│   ├── rag_chain.py        # RetrievalQA chain with custom prompts
│   ├── scorer.py           # Keyword overlap scoring (set intersection)
│   ├── ats_scorer.py       # LLM-based ATS scoring with JSON output
│   ├── keyword_extractor.py# LLM keyword categorization from JD
│   ├── resume_rewriter.py  # LLM resume tailoring for specific JD
│   ├── cover_letter.py     # LLM cover letter generation
│   ├── exporter.py         # Markdown → PDF (ReportLab) & DOCX export
│   ├── prompts.py          # 5 prompt templates (RAG, ATS, Keywords, Resume, Cover Letter)
│   └── config.py           # Environment variables & defaults
│
├── frontend/               # Project 2: Streamlit Web UI
│   ├── app.py              # 5-tab interface (ATS, Keywords, Gap, Resume, Cover Letter)
│   └── styles.py           # CSS (gradients, cards, responsive layout)
│
├── api/                    # Project 2: FastAPI REST API
│   └── index.py            # 6 endpoints (health, ats-score, keywords, rewrite, cover-letter, export)
│
├── data/                   # Sample data
│   └── job_description.txt # Sample JD (Python Developer + ML/LangChain)
│
├── tests/                  # Unit tests
│   └── test_pipelines.py   # Tests for scorer, splitter, loader validation
│
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config (Streamlit)
├── vercel.json             # Vercel deployment config (FastAPI)
├── Procfile                # Heroku deployment config
└── runtime.txt             # Python 3.11.9
```

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **LLM** | OpenAI `gpt-4o-mini` (configurable) |
| **Embeddings** | OpenAI `text-embedding-3-small` |
| **RAG Framework** | LangChain (chains, loaders, splitters, retrievers) |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Tokenizer** | tiktoken |
| **Web UI** | Streamlit |
| **REST API** | FastAPI + Uvicorn |
| **Doc Processing** | pypdf, python-docx, docx2txt |
| **Doc Generation** | ReportLab (PDF), python-docx (DOCX) |
| **Testing** | pytest |
| **Language** | Python 3.11 |

</div>

---

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key

### 1. Clone & Install

```bash
git clone https://github.com/reddyvamshi210-collab/ai-resume-matcher.git
cd ai-resume-matcher
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run

#### Option A: Simple RAG Pipeline (Project 1)

```bash
# Using CLI with custom files
python cli.py --resume path/to/resume.pdf --jd path/to/job_description.txt

# Using default sample data
python app.py
```

#### Option B: Full Web App (Project 2)

```bash
# Streamlit UI
streamlit run frontend/app.py

# FastAPI REST API
uvicorn api.index:app --reload
```

---

## ⚙️ Configuration

All settings can be configured via environment variables or `backend/config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | OpenAI API authentication key |
| `MODEL_NAME` | `gpt-4o-mini` | LLM model to use |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `CHUNK_SIZE` | `800` | Document chunk size (tokens) |
| `CHUNK_OVERLAP` | `100` | Overlap between chunks |
| `TOP_K` | `3` | Number of retrieved chunks for RAG |
| `TEMPERATURE` | `0.2` | LLM temperature (lower = more consistent) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (API only) |

---

## 🌐 API Endpoints

| Method | Endpoint | Parameters | Response |
|--------|----------|-----------|----------|
| `GET` | `/api/health` | — | `{"status": "ok", "app": "AI Resume Matcher"}` |
| `POST` | `/api/ats-score` | `resume` (file), `jd_text` (form) | ATS score, keywords, formatting issues, recommendations |
| `POST` | `/api/keywords` | `jd_text` (form) | Categorized keywords (7 categories) |
| `POST` | `/api/rewrite` | `resume` (file), `jd_text`, `template_style` | Tailored resume in markdown |
| `POST` | `/api/cover-letter` | `resume` (file), `jd_text`, `company_name`, `role_title` | Cover letter in markdown |
| `POST` | `/api/export` | `content` (form), `fmt` (pdf/docx), `title` | Binary PDF or DOCX file |

---

## 🧪 Testing

```bash
pytest tests/test_pipelines.py -v
```

Tests cover:
- Keyword scoring (perfect match, zero match, empty inputs, stop-words, partial match)
- Document splitting (chunk creation, content preservation)
- File validation (missing files, wrong extensions, valid files)
- JD loading from sample data

---

## 🚢 Deployment

### Render (Streamlit UI)

Configured via `render.yaml`:
```yaml
- type: web
  runtime: python
  buildCommand: pip install -r requirements.txt
  startCommand: streamlit run frontend/app.py --server.port $PORT
  envVars:
    - key: OPENAI_API_KEY
```

### Vercel (FastAPI API)

Configured via `vercel.json`:
```json
{
  "builds": [{"src": "api/index.py", "use": "@vercel/python"}],
  "routes": [{"src": "/api/(.*)", "dest": "api/index.py"}]
}
```

### Heroku

Configured via `Procfile`:
```
web: streamlit run frontend/app.py
```

---

## 🔄 How It Works

```
                    ┌─────────────┐
                    │   Resume    │  (PDF / DOCX)
                    │   Upload    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Loader    │  pypdf / python-docx
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Splitter   │  800 tokens, 100 overlap
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼───┐ ┌──────▼──────┐
       │  Embeddings  │ │ JD   │ │  FAISS      │
       │  (OpenAI)    │ │ Text │ │  VectorStore│
       └──────┬──────┘ └──┬───┘ └──────┬──────┘
              │            │            │
              └────────────┼────────────┘
                           │
              ┌────────────▼────────────┐
              │     RetrievalQA Chain    │
              │  (LangChain + GPT-4o)   │
              └────────────┬────────────┘
                           │
         ┌─────────┬───────┼───────┬──────────┐
         │         │       │       │          │
      ┌──▼──┐  ┌──▼──┐ ┌──▼──┐ ┌──▼──┐  ┌───▼───┐
      │ ATS │  │ Key │ │ Gap │ │Tail │  │Cover  │
      │Score│  │words│ │Anal.│ │ored │  │Letter │
      └─────┘  └─────┘ └─────┘ │Resu.│  └───────┘
                                └─────┘
```

---

## 📁 Sample Data

The repo includes a sample job description in `data/job_description.txt` for testing:

> We are looking for a **Python Developer** with experience in Machine Learning, LangChain, Vector Databases, OpenAI API, and FAISS.

To test, place your resume as `data/resume.pdf` and run:
```bash
python app.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with** ❤️ **by [Vamshi Reddy](https://github.com/reddyvamshi210-collab)**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:1f6feb&height=100&section=footer" width="100%" />

</div>
