"""Resume rewriting / tailoring module."""
import logging

from langchain_openai import ChatOpenAI
from backend.config import MODEL_NAME
from backend.prompts import RESUME_REWRITE_PROMPT

logger = logging.getLogger(__name__)


def rewrite_resume(
    resume_text: str,
    jd_text: str,
    template_style: str = "Professional",
) -> str:
    """Rewrite a resume tailored to the given JD and template style."""
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0.4)
    prompt_text = RESUME_REWRITE_PROMPT.format(
        resume_text=resume_text,
        jd_text=jd_text,
        template_style=template_style,
    )

    logger.info("Rewriting resume with style=%s ...", template_style)
    response = llm.invoke(prompt_text)
    return response.content.strip()
