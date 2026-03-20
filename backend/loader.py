from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document

SUPPORTED_RESUME_EXTENSIONS = {".pdf", ".docx"}
SUPPORTED_JD_EXTENSIONS = {".txt", ".md"}


def _validate_file(path: str, allowed_extensions: set[str]) -> Path:
    """Verify a file exists and has an allowed extension."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    if p.suffix.lower() not in allowed_extensions:
        raise ValueError(
            f"Unsupported file type '{p.suffix}'. "
            f"Allowed: {allowed_extensions}"
        )
    return p


def _load_docx(path: str) -> list[Document]:
    """Load a DOCX file and return LangChain Documents."""
    import docx2txt
    text = docx2txt.process(path)
    if not text or not text.strip():
        raise ValueError(f"No content extracted from DOCX: {path}")
    return [Document(page_content=text, metadata={"source": path})]


def load_resume(path: str) -> list:
    """Load a resume PDF or DOCX and return LangChain Documents."""
    validated = _validate_file(path, SUPPORTED_RESUME_EXTENSIONS)
    if validated.suffix.lower() == ".docx":
        return _load_docx(str(validated))
    loader = PyPDFLoader(str(validated))
    docs = loader.load()
    if not docs:
        raise ValueError(f"No content extracted from resume: {validated}")
    return docs


def load_job_description(path: str) -> list:
    """Load a job description text file and return LangChain Documents."""
    validated = _validate_file(path, SUPPORTED_JD_EXTENSIONS)
    loader = TextLoader(str(validated), encoding="utf-8")
    docs = loader.load()
    if not docs:
        raise ValueError(f"No content extracted from JD: {validated}")
    return docs


def extract_text_from_upload(path: str) -> str:
    """Extract plain text from a PDF or DOCX resume file."""
    p = Path(path)
    if p.suffix.lower() == ".docx":
        import docx2txt
        return docx2txt.process(path) or ""
    elif p.suffix.lower() == ".pdf":
        loader = PyPDFLoader(path)
        docs = loader.load()
        return "\n".join(d.page_content for d in docs)
    raise ValueError(f"Unsupported file type: {p.suffix}")
