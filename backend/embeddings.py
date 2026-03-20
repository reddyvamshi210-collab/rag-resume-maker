from langchain_openai import OpenAIEmbeddings
from backend.config import EMBEDDING_MODEL


def get_embeddings() -> OpenAIEmbeddings:
    """Return the configured OpenAI embedding model."""
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)
