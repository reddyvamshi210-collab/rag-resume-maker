"""Streamlit web interface for AI Resume Matcher."""
import tempfile
from pathlib import Path

import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

from backend import config  # noqa: E402
from backend.config import require_api_key  # noqa: E402
from backend.loader import extract_text_from_upload  # noqa: E402
from backend.splitter import split_documents  # noqa: E402
from backend.embeddings import get_embeddings  # noqa: E402
from backend.vectorstore import create_vectorstore  # noqa: E402
from backend.retriever import get_retriever  # noqa: E402
from backend.rag_chain import build_rag_chain  # noqa: E402
from backend.scorer import keyword_score  # noqa: E402
from backend.ats_scorer import compute_ats_score  # noqa: E402
from backend.keyword_extractor import extract_keywords  # noqa: E402
from backend.resume_rewriter import rewrite_resume  # noqa: E402
from backend.cover_letter import generate_cover_letter  # noqa: E402
from backend.exporter import export_content  # noqa: E402
from frontend.styles import MAIN_CSS  # noqa: E402


# ── Helpers ──────────────────────────────────────────────────────────────────

def _save_upload(uploaded_file, suffix: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    return tmp.name


def _cleanup(*paths: str) -> None:
    for p in paths:
        if p:
            Path(p).unlink(missing_ok=True)


def _make_docs(text: str, source: str):
    """Create LangChain Document objects from plain text."""
    from langchain.schema import Document
    return [Document(page_content=text, metadata={"source": source})]


# ── SIDEBAR ──────────────────────────────────────────────────────────────────

def render_sidebar():
    """Render the sidebar with input controls and return collected inputs."""
    with st.sidebar:
        st.markdown("# 📄 AI Resume Matcher")
        st.markdown("---")

        st.markdown("### 📎 Upload Resume")
        resume_file = st.file_uploader(
            "PDF or DOCX",
            type=["pdf", "docx"],
            label_visibility="collapsed",
        )

        st.markdown("### 📝 Job Description")
        jd_input_method = st.radio(
            "Input method",
            ["Paste text", "Upload file"],
            horizontal=True,
            label_visibility="collapsed",
        )

        jd_text_input = ""
        jd_file = None
        if jd_input_method == "Paste text":
            jd_text_input = st.text_area(
                "Paste the job description here",
                height=200,
                placeholder="Paste the full job description...",
                label_visibility="collapsed",
            )
        else:
            jd_file = st.file_uploader(
                "TXT or MD file",
                type=["txt", "md"],
                label_visibility="collapsed",
            )

        st.markdown("---")
        st.markdown("### ⚙️ Options")

        template_style = st.selectbox(
            "Resume Template",
            config.RESUME_TEMPLATES,
        )

        company_name = st.text_input("Company Name", placeholder="e.g. Google")
        role_title = st.text_input("Role Title", placeholder="e.g. Senior Python Developer")

        st.markdown("---")

        analyze_btn = st.button(
            "🚀 Analyze & Generate",
            type="primary",
            use_container_width=True,
        )

        return {
            "resume_file": resume_file,
            "jd_text_input": jd_text_input,
            "jd_file": jd_file,
            "jd_input_method": jd_input_method,
            "template_style": template_style,
            "company_name": company_name or "the company",
            "role_title": role_title or "the position",
            "analyze": analyze_btn,
        }


# ── WELCOME ──────────────────────────────────────────────────────────────────

def render_welcome():
    """Render the welcome / landing state."""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">📄 AI Resume Matcher</h1>
        <p style="font-size: 1.2rem; color: #6c757d; max-width: 600px; margin: 0 auto 2rem;">
            AI-powered resume analysis, tailoring, and cover letter generation.
            Upload your resume and paste a job description to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    features = [
        ("🎯", "ATS Score", "Check how well your resume passes ATS filters"),
        ("🔑", "Keywords", "Extract critical keywords from any JD"),
        ("📊", "Gap Analysis", "Identify missing skills and requirements"),
        ("✏️", "Resume Tailor", "AI rewrites your resume for the role"),
        ("💌", "Cover Letter", "Generate a matching cover letter"),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="section-card" style="text-align:center; min-height:180px;">
                <div style="font-size:2.5rem;">{icon}</div>
                <h4 style="margin:0.5rem 0 0.3rem;">{title}</h4>
                <p style="font-size:0.85rem; color:#6c757d;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)


# ── RESULTS ──────────────────────────────────────────────────────────────────

def render_results(resume_text: str, jd_text: str, inputs: dict):
    """Run all analyses and render the tabbed results view."""

    tab_ats, tab_keywords, tab_gap, tab_resume, tab_cover = st.tabs([
        "🎯 ATS Score",
        "🔑 Keywords",
        "📊 Gap Analysis",
        "✏️ Tailored Resume",
        "💌 Cover Letter",
    ])

    # ── ATS Score Tab ────────────────────────────────────────────────────
    with tab_ats:
        with st.spinner("Computing ATS score..."):
            ats = compute_ats_score(resume_text, jd_text)
            kw_score = keyword_score(resume_text, jd_text)

        score = ats.get("ats_score", 0)
        color = "#28a745" if score >= 70 else "#ffc107" if score >= 40 else "#dc3545"

        col_score, col_details = st.columns([1, 2])

        with col_score:
            st.markdown(f"""
            <div class="score-card" style="background: linear-gradient(135deg, {color}cc 0%, {color} 100%);">
                <div class="score-number">{score}%</div>
                <div class="score-label">ATS Compatibility Score</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{kw_score}%</div>
                <div class="metric-label">Keyword Overlap</div>
            </div>
            """, unsafe_allow_html=True)

        with col_details:
            section_scores = ats.get("section_scores", {})
            if section_scores:
                st.markdown("#### Section Breakdown")
                for section, s_score in section_scores.items():
                    label = section.replace("_", " ").title()
                    st.progress(min(s_score, 100) / 100, text=f"{label}: {s_score}%")

            recs = ats.get("recommendations", [])
            if recs:
                st.markdown("#### 💡 Recommendations")
                for r in recs:
                    st.markdown(f"- {r}")

        st.markdown("---")
        col_m, col_x = st.columns(2)
        with col_m:
            st.markdown("#### ✅ Matched Keywords")
            matched = ats.get("matched_keywords", [])
            if matched:
                tags = "".join(
                    f'<span class="keyword-tag matched">{k}</span>' for k in matched
                )
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.info("No matched keywords found")
        with col_x:
            st.markdown("#### ⚠️ Missing Keywords")
            missing = ats.get("missing_keywords", [])
            if missing:
                tags = "".join(
                    f'<span class="keyword-tag missing">{k}</span>' for k in missing
                )
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.success("All keywords matched!")

        fmt_issues = ats.get("formatting_issues", [])
        if fmt_issues:
            with st.expander("🔍 Formatting Issues"):
                for issue in fmt_issues:
                    st.markdown(f"- {issue}")

    # ── Keywords Tab ─────────────────────────────────────────────────────
    with tab_keywords:
        with st.spinner("Extracting keywords..."):
            keywords = extract_keywords(jd_text)

        categories = [
            ("💻 Hard Skills", "hard_skills"),
            ("🤝 Soft Skills", "soft_skills"),
            ("📜 Certifications", "certifications"),
            ("⏳ Experience Requirements", "experience_requirements"),
            ("🎓 Education Requirements", "education_requirements"),
            ("🎬 Action Verbs", "action_verbs"),
            ("🏭 Industry Terms", "industry_terms"),
        ]

        for icon_label, key in categories:
            items = keywords.get(key, [])
            if items:
                st.markdown(f"#### {icon_label}")
                tags = "".join(
                    f'<span class="keyword-tag">{item}</span>' for item in items
                )
                st.markdown(tags, unsafe_allow_html=True)
                st.markdown("")

    # ── Gap Analysis Tab ─────────────────────────────────────────────────
    with tab_gap:
        with st.spinner("Running gap analysis with RAG..."):
            resume_docs = _make_docs(resume_text, "resume")
            jd_docs = _make_docs(jd_text, "jd")
            all_docs = resume_docs + jd_docs
            split_docs = split_documents(all_docs)
            embeddings = get_embeddings()
            vectorstore = create_vectorstore(split_docs, embeddings)
            retriever = get_retriever(vectorstore)
            rag_chain = build_rag_chain(retriever)

            query = (
                "Analyze how well this resume matches the job description. "
                "Give a percentage match score, list matched skills, "
                "identify skill gaps, and provide improvement suggestions."
            )
            response = rag_chain.invoke({"query": query})

        st.markdown("### 📊 AI Gap Analysis")
        st.markdown(response["result"])

        source_docs = response.get("source_documents", [])
        if source_docs:
            with st.expander(f"📚 Source Chunks ({len(source_docs)})"):
                for i, doc in enumerate(source_docs, 1):
                    st.markdown(f"**Chunk {i}**")
                    st.text(doc.page_content[:500])
                    st.divider()

    # ── Tailored Resume Tab ──────────────────────────────────────────────
    with tab_resume:
        with st.spinner(f"Rewriting resume ({inputs['template_style']} style)..."):
            tailored = rewrite_resume(
                resume_text, jd_text, inputs["template_style"]
            )

        st.markdown("### ✏️ Tailored Resume")
        st.markdown(tailored)

        st.markdown("---")
        st.markdown("#### 📥 Download")
        dl1, dl2 = st.columns(2)
        with dl1:
            pdf_bytes = export_content(tailored, "pdf", "Tailored_Resume")
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_bytes,
                file_name="tailored_resume.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        with dl2:
            docx_bytes = export_content(tailored, "docx", "Tailored_Resume")
            st.download_button(
                "⬇️ Download DOCX",
                data=docx_bytes,
                file_name="tailored_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

    # ── Cover Letter Tab ─────────────────────────────────────────────────
    with tab_cover:
        with st.spinner("Generating cover letter..."):
            cover = generate_cover_letter(
                resume_text,
                jd_text,
                inputs["company_name"],
                inputs["role_title"],
            )

        st.markdown("### 💌 Cover Letter")
        st.markdown(cover)

        st.markdown("---")
        st.markdown("#### 📥 Download")
        dl1, dl2 = st.columns(2)
        with dl1:
            pdf_bytes = export_content(cover, "pdf", "Cover_Letter")
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_bytes,
                file_name="cover_letter.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="cover_pdf",
            )
        with dl2:
            docx_bytes = export_content(cover, "docx", "Cover_Letter")
            st.download_button(
                "⬇️ Download DOCX",
                data=docx_bytes,
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="cover_docx",
            )


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    st.markdown(MAIN_CSS, unsafe_allow_html=True)

    inputs = render_sidebar()

    if not inputs["analyze"]:
        render_welcome()
        return

    # Validate API key before doing any work
    try:
        require_api_key()
    except EnvironmentError:
        st.error("⚠️ OPENAI_API_KEY is not set. Add it to your .env file or environment variables.")
        return

    # Validate inputs
    if not inputs["resume_file"]:
        st.error("⚠️ Please upload a resume (PDF or DOCX).")
        return

    jd_text = ""
    if inputs["jd_input_method"] == "Paste text":
        jd_text = inputs["jd_text_input"].strip()
    elif inputs["jd_file"]:
        jd_text = inputs["jd_file"].read().decode("utf-8", errors="replace").strip()

    if not jd_text:
        st.error("⚠️ Please provide a job description.")
        return

    # Save resume to temp file and extract text
    suffix = Path(inputs["resume_file"].name).suffix
    resume_path = _save_upload(inputs["resume_file"], suffix)

    try:
        resume_text = extract_text_from_upload(resume_path)
        if not resume_text.strip():
            st.error("Could not extract text from the uploaded resume.")
            return

        render_results(resume_text, jd_text, inputs)

    except Exception as exc:
        st.error(f"❌ An error occurred: {exc}")
    finally:
        _cleanup(resume_path)


if __name__ == "__main__":
    main()
