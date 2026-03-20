import re

# Common English stop-words to ignore in keyword matching
_STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "we", "you", "i",
    "they", "he", "she", "it", "this", "that", "these", "those", "am",
    "not", "no", "so", "if", "as", "from", "up", "out", "about", "into",
    "over", "after", "before", "between", "under", "above", "such",
})


def _extract_keywords(text: str) -> set[str]:
    """Extract meaningful lowercase keywords, filtering stop-words."""
    words = set(re.findall(r"\b[a-zA-Z]{2,}\b", text.lower()))
    return words - _STOP_WORDS


def keyword_score(resume_text: str, jd_text: str) -> float:
    """Return the percentage of JD keywords found in the resume (0-100)."""
    jd_keywords = _extract_keywords(jd_text)
    resume_keywords = _extract_keywords(resume_text)

    if not jd_keywords:
        return 0.0

    matched = jd_keywords & resume_keywords
    return round((len(matched) / len(jd_keywords)) * 100, 2)
