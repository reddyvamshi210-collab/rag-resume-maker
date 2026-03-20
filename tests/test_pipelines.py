"""Unit tests for the AI Resume Matcher pipeline."""
from pathlib import Path

import pytest

from backend.scorer import keyword_score, _extract_keywords
from backend.splitter import split_documents
from backend.loader import _validate_file, load_job_description


# ──────────────────────────────────────────────
# scorer tests
# ──────────────────────────────────────────────

class TestKeywordScore:
    def test_perfect_match(self):
        text = "Python Machine Learning LangChain"
        assert keyword_score(text, text) == 100.0

    def test_zero_match(self):
        resume = "Java Spring Hibernate"
        jd = "Python Machine Learning"
        score = keyword_score(resume, jd)
        assert 0 <= score < 100

    def test_empty_jd_returns_zero(self):
        assert keyword_score("Python developer", "") == 0.0

    def test_empty_resume_returns_zero(self):
        assert keyword_score("", "Python developer") == 0.0

    def test_stop_words_excluded(self):
        keywords = _extract_keywords("the and or is a an")
        assert len(keywords) == 0

    def test_partial_match(self):
        resume = "Python LangChain Docker"
        jd = "Python LangChain Kubernetes"
        score = keyword_score(resume, jd)
        assert 50 <= score <= 80


# ──────────────────────────────────────────────
# splitter tests
# ──────────────────────────────────────────────

class TestSplitter:
    def test_split_returns_chunks(self):
        from langchain.schema import Document
        long_text = "word " * 500
        docs = [Document(page_content=long_text)]
        chunks = split_documents(docs)
        assert len(chunks) > 1

    def test_split_preserves_content(self):
        from langchain.schema import Document
        text = "Hello world"
        docs = [Document(page_content=text)]
        chunks = split_documents(docs)
        combined = " ".join(c.page_content for c in chunks)
        assert "Hello" in combined


# ──────────────────────────────────────────────
# loader validation tests
# ──────────────────────────────────────────────

class TestLoaderValidation:
    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            _validate_file("nonexistent.pdf", {".pdf"})

    def test_wrong_extension_raises(self, tmp_path):
        bad = tmp_path / "test.docx"
        bad.write_text("content")
        with pytest.raises(ValueError, match="Unsupported file type"):
            _validate_file(str(bad), {".pdf"})

    def test_valid_file_passes(self, tmp_path):
        good = tmp_path / "test.txt"
        good.write_text("some content")
        result = _validate_file(str(good), {".txt"})
        assert result == good

    def test_docx_extension_accepted(self, tmp_path):
        docx_file = tmp_path / "test.docx"
        docx_file.write_text("content")
        result = _validate_file(str(docx_file), {".pdf", ".docx"})
        assert result == docx_file

    def test_load_jd_from_real_file(self):
        jd_path = Path(__file__).resolve().parent.parent / "data" / "job_description.txt"
        if jd_path.exists():
            docs = load_job_description(str(jd_path))
            assert len(docs) >= 1
            assert "Python" in docs[0].page_content


# ──────────────────────────────────────────────
# config tests
# ──────────────────────────────────────────────

class TestConfig:
    def test_config_values_loaded(self):
        from backend import config
        assert config.CHUNK_SIZE > 0
        assert config.CHUNK_OVERLAP >= 0
        assert config.TOP_K >= 1
        assert config.MODEL_NAME
        assert config.EMBEDDING_MODEL

    def test_resume_templates_defined(self):
        from backend import config
        assert len(config.RESUME_TEMPLATES) >= 3
        assert "Professional" in config.RESUME_TEMPLATES


# ──────────────────────────────────────────────
# exporter tests
# ──────────────────────────────────────────────

class TestExporter:
    def test_docx_export_returns_bytes(self):
        from backend.exporter import markdown_to_docx
        md = "# Title\n\n- Item 1\n- Item 2\n\n**Bold text** and *italic*."
        result = markdown_to_docx(md)
        assert isinstance(result, bytes)
        assert len(result) > 100

    def test_pdf_export_returns_bytes(self):
        from backend.exporter import markdown_to_pdf
        md = "# Title\n\n- Item 1\n- Item 2\n\nSome paragraph text."
        result = markdown_to_pdf(md)
        assert isinstance(result, bytes)
        assert result[:5] == b"%PDF-"

    def test_export_content_pdf(self):
        from backend.exporter import export_content
        md = "Hello world"
        result = export_content(md, "pdf")
        assert result[:5] == b"%PDF-"

    def test_export_content_docx(self):
        from backend.exporter import export_content
        md = "Hello world"
        result = export_content(md, "docx")
        assert isinstance(result, bytes)
        # DOCX files start with PK (ZIP format)
        assert result[:2] == b"PK"


# ──────────────────────────────────────────────
# prompt template tests
# ──────────────────────────────────────────────

class TestPrompts:
    def test_all_prompts_importable(self):
        from backend.prompts import (
            RAG_PROMPT,
            ATS_SCORE_PROMPT,
            KEYWORD_EXTRACTION_PROMPT,
            RESUME_REWRITE_PROMPT,
            COVER_LETTER_PROMPT,
        )
        assert RAG_PROMPT is not None
        assert ATS_SCORE_PROMPT is not None

    def test_ats_prompt_has_required_variables(self):
        from backend.prompts import ATS_SCORE_PROMPT
        assert "resume_text" in ATS_SCORE_PROMPT.input_variables
        assert "jd_text" in ATS_SCORE_PROMPT.input_variables

    def test_resume_rewrite_prompt_has_template_style(self):
        from backend.prompts import RESUME_REWRITE_PROMPT
        assert "template_style" in RESUME_REWRITE_PROMPT.input_variables
