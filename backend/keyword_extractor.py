"""JD keyword extraction module."""
import json
import logging

from langchain_openai import ChatOpenAI
from backend.config import MODEL_NAME, TEMPERATURE
from backend.prompts import KEYWORD_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)

_DEFAULT_RESULT = {
    "hard_skills": [],
    "soft_skills": [],
    "certifications": [],
    "experience_requirements": [],
    "education_requirements": [],
    "action_verbs": [],
    "industry_terms": [],
}


def _strip_json_fences(raw: str) -> str:
    """Remove markdown code fences from LLM JSON output."""
    raw = raw.strip()
    if raw.startswith("```"):
        first_newline = raw.find("\n")
        if first_newline != -1:
            raw = raw[first_newline + 1:]
        else:
            raw = raw[3:]
    if raw.rstrip().endswith("```"):
        raw = raw.rstrip()[:-3]
    return raw.strip()


def extract_keywords(jd_text: str) -> dict:
    """Extract structured keywords from a job description."""
    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
    prompt_text = KEYWORD_EXTRACTION_PROMPT.format(jd_text=jd_text)

    logger.info("Extracting keywords from JD...")
    response = llm.invoke(prompt_text)
    raw = _strip_json_fences(response.content)

    try:
        result = json.loads(raw)
        for key, default in _DEFAULT_RESULT.items():
            result.setdefault(key, default)
        return result
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("Keyword extraction response was not valid JSON (%s)", exc)
        return dict(_DEFAULT_RESULT)
