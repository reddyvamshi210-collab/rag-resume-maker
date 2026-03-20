"""ATS (Applicant Tracking System) scoring module."""
import json
import logging

from langchain_openai import ChatOpenAI
from backend.config import MODEL_NAME, TEMPERATURE
from backend.prompts import ATS_SCORE_PROMPT

logger = logging.getLogger(__name__)

_DEFAULT_RESULT = {
    "ats_score": 0,
    "matched_keywords": [],
    "missing_keywords": [],
    "formatting_issues": [],
    "section_scores": {},
    "recommendations": [],
}


def _strip_json_fences(raw: str) -> str:
    """Remove markdown code fences from LLM JSON output."""
    raw = raw.strip()
    # Handle ```json or ``` at the start
    if raw.startswith("```"):
        first_newline = raw.find("\n")
        if first_newline != -1:
            raw = raw[first_newline + 1:]
        else:
            raw = raw[3:]
    # Handle trailing ```
    if raw.rstrip().endswith("```"):
        raw = raw.rstrip()[:-3]
    return raw.strip()


def compute_ats_score(resume_text: str, jd_text: str) -> dict:
    """Run ATS scoring analysis and return structured results."""
    llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
    prompt_text = ATS_SCORE_PROMPT.format(
        resume_text=resume_text, jd_text=jd_text
    )

    logger.info("Computing ATS score...")
    response = llm.invoke(prompt_text)
    raw = _strip_json_fences(response.content)

    try:
        result = json.loads(raw)
        # Ensure all expected keys exist
        for key, default in _DEFAULT_RESULT.items():
            result.setdefault(key, default)
        # Clamp score to 0-100
        result["ats_score"] = max(0, min(100, int(result["ats_score"])))
        return result
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        logger.warning("ATS response was not valid JSON (%s), returning fallback", exc)
        fallback = dict(_DEFAULT_RESULT)
        fallback["recommendations"] = [raw[:500] if raw else "Analysis unavailable"]
        return fallback
