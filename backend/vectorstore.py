from langchain_community.vectorstores import FAISS


def create_vectorstore(docs: list, embeddings) -> FAISS:
    """Create a FAISS vector store from document chunks."""
    if not docs:
        raise ValueError("No documents provided for vector store creation.")
    return FAISS.from_documents(docs, embeddings)
