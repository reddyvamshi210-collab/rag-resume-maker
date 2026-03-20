from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from backend.config import MODEL_NAME, TEMPERATURE
from backend.prompts import RAG_PROMPT


def build_rag_chain(retriever) -> RetrievalQA:
    """Build a RetrievalQA chain using the custom prompt."""
    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={"prompt": RAG_PROMPT},
    )
