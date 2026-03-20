"""Cover letter generation module."""
import logging

from langchain_openai import ChatOpenAI
from backend.config import MODEL_NAME
from backend.prompts import COVER_LETTER_PROMPT

logger = logging.getLogger(__name__)


def generate_cover_letter(
    resume_text: str,
    jd_text: str,
    company_name: str = "the company",
    role_title: str = "the position",
) -> str:
    """Generate a tailored cover letter."""
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.5)
    prompt_text = COVER_LETTER_PROMPT.format(
        resume_text=resume_text,
        jd_text=jd_text,
        company_name=company_name,
        role_title=role_title,
    )

    logger.info("Generating cover letter for %s at %s...", role_title, company_name)
    response = llm.invoke(prompt_text)
    return response.content.strip()
