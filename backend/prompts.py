from langchain.prompts import PromptTemplate

# ── Analysis Prompt ──────────────────────────────────────────────────────────
_ANALYSIS_TEMPLATE = """You are an expert AI hiring assistant.

Using ONLY the retrieved resume and job description context below, perform
the following analysis:

1. **Match Score** — Give a percentage (0-100%) indicating how well the
   resume matches the job description.
2. **Matched Skills** — List the skills/qualifications that appear in both
   the resume and the job description.
3. **Skill Gaps** — List the required skills/qualifications that are missing
   from the resume.
4. **Improvement Suggestions** — Provide 3-5 actionable suggestions for
   the candidate to improve their resume for this role.
5. **Overall Summary** — A concise paragraph summarising the fit.

Context:
{context}

Question:
{question}

Provide a well-structured, professional analysis."""

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=_ANALYSIS_TEMPLATE,
)

# ── ATS Score Prompt ─────────────────────────────────────────────────────────
ATS_SCORE_PROMPT = PromptTemplate(
    input_variables=["resume_text", "jd_text"],
    template="""You are an ATS (Applicant Tracking System) scoring engine.

Analyze the resume against the job description and return a JSON object with
EXACTLY these keys (no markdown, no explanation outside the JSON):

{{
  "ats_score": <integer 0-100>,
  "matched_keywords": [<list of matched keywords/phrases>],
  "missing_keywords": [<list of missing but required keywords/phrases>],
  "formatting_issues": [<list of ATS formatting problems found>],
  "section_scores": {{
    "contact_info": <0-100>,
    "work_experience": <0-100>,
    "skills": <0-100>,
    "education": <0-100>,
    "keywords_match": <0-100>
  }},
  "recommendations": [<top 5 actionable ATS optimization tips>]
}}

Resume:
{resume_text}

Job Description:
{jd_text}

Return ONLY valid JSON.""",
)

# ── Keyword Extraction Prompt ────────────────────────────────────────────────
KEYWORD_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["jd_text"],
    template="""You are a keyword extraction specialist for job descriptions.

Analyze the following job description and extract keywords organized into
categories. Return a JSON object with EXACTLY these keys:

{{
  "hard_skills": [<technical skills, tools, languages, frameworks>],
  "soft_skills": [<communication, leadership, teamwork, etc.>],
  "certifications": [<any mentioned certifications or licenses>],
  "experience_requirements": [<years of experience, specific domains>],
  "education_requirements": [<degrees, fields of study>],
  "action_verbs": [<strong action verbs used in the JD>],
  "industry_terms": [<domain-specific terminology>]
}}

Job Description:
{jd_text}

Return ONLY valid JSON.""",
)

# ── Resume Rewrite Prompt ────────────────────────────────────────────────────
RESUME_REWRITE_PROMPT = PromptTemplate(
    input_variables=["resume_text", "jd_text", "template_style"],
    template="""You are a professional resume writer and career coach.

Your task is to rewrite/tailor the given resume so it is optimized for the
target job description. Follow the "{template_style}" resume template style.

Rules:
- Keep ALL factual information (names, dates, companies, degrees) UNCHANGED.
- Rewrite bullet points to incorporate keywords from the JD.
- Quantify achievements where possible.
- Reorder sections to highlight the most relevant experience first.
- Use strong action verbs that match the JD language.
- Ensure the resume is ATS-friendly (no tables, columns, or graphics).
- Keep it concise (ideally 1-2 pages worth of content).

Template styles:
- Professional: Traditional format, conservative language, clear sections.
- Modern: Clean layout emphasis, contemporary language, skills-forward.
- Minimal: Ultra-concise, essential info only, maximum white space.
- Creative: Personality-forward, narrative style, unique section headers.

Original Resume:
{resume_text}

Target Job Description:
{jd_text}

Write the complete tailored resume in well-structured markdown format.
Use proper headings (##), bullet points, and bold for emphasis.""",
)

# ── Cover Letter Prompt ──────────────────────────────────────────────────────
COVER_LETTER_PROMPT = PromptTemplate(
    input_variables=["resume_text", "jd_text", "company_name", "role_title"],
    template="""You are a professional cover letter writer.

Write a compelling, personalized cover letter for the candidate applying to
the "{role_title}" position at "{company_name}".

Rules:
- Draw specific experiences and achievements from the resume.
- Reference specific requirements from the job description.
- Show enthusiasm and cultural fit.
- Keep it to 3-4 paragraphs (roughly 300-400 words).
- Use a professional but personable tone.
- Include a strong opening hook and a clear call-to-action closing.
- Do NOT fabricate any experience — only use what's in the resume.

Resume:
{resume_text}

Job Description:
{jd_text}

Write the complete cover letter in markdown format.""",
)
