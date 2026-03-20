from backend.config import TOP_K


def get_retriever(vectorstore):
    """Return a similarity-search retriever with configured top-k."""
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )
