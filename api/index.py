"""Vercel serverless API — AI Resume Matcher.

Provides REST endpoints for resume analysis when deployed on Vercel.
The full Streamlit UI is available via Render (see render.yaml).
"""
import os
import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.config import require_api_key
from backend.loader import extract_text_from_upload
from backend.scorer import keyword_score
from backend.ats_scorer import compute_ats_score
from backend.keyword_extractor import extract_keywords
from backend.resume_rewriter import rewrite_resume
from backend.cover_letter import generate_cover_letter
from backend.exporter import export_content

app = FastAPI(title="AI Resume Matcher API", version="1.0.0")

_ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _save_upload(upload: UploadFile) -> str:
    suffix = Path(upload.filename or "file").suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(upload.file.read())
    tmp.close()
    return tmp.name


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "AI Resume Matcher"}


@app.post("/api/ats-score")
async def ats_score(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
):
    require_api_key()
    path = _save_upload(resume)
    try:
        resume_text = extract_text_from_upload(path)
        result = compute_ats_score(resume_text, jd_text)
        result["keyword_overlap"] = keyword_score(resume_text, jd_text)
        return JSONResponse(result)
    finally:
        Path(path).unlink(missing_ok=True)


@app.post("/api/keywords")
async def keywords(jd_text: str = Form(...)):
    require_api_key()
    return JSONResponse(extract_keywords(jd_text))


@app.post("/api/rewrite")
async def rewrite(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    template_style: str = Form("Professional"),
):
    require_api_key()
    path = _save_upload(resume)
    try:
        resume_text = extract_text_from_upload(path)
        result = rewrite_resume(resume_text, jd_text, template_style)
        return JSONResponse({"tailored_resume": result})
    finally:
        Path(path).unlink(missing_ok=True)


@app.post("/api/cover-letter")
async def cover_letter(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    company_name: str = Form("the company"),
    role_title: str = Form("the position"),
):
    require_api_key()
    path = _save_upload(resume)
    try:
        resume_text = extract_text_from_upload(path)
        result = generate_cover_letter(resume_text, jd_text, company_name, role_title)
        return JSONResponse({"cover_letter": result})
    finally:
        Path(path).unlink(missing_ok=True)


@app.post("/api/export")
async def export(
    content: str = Form(...),
    fmt: str = Form("pdf"),
    title: str = Form("Document"),
):
    data = export_content(content, fmt, title)
    media = (
        "application/pdf" if fmt == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    return Response(content=data, media_type=media)
