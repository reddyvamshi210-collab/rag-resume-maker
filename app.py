import os
import os

print("Resume size:", os.path.getsize("data/resume.pdf"))
print("JD size:", os.path.getsize("data/job_description.txt"))
import logging
from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS

# Your project modules
from src.loader import load_resume, load_job_description
from src.splitter import split_documents
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.retriever import get_retriever
from src.rag_chain import build_rag_chain


# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    try:
        logging.info("Loading documents...")

        resume_docs = load_resume("data/resume.pdf")
        jd_docs = load_job_description("data/job_description.txt")

        all_docs = resume_docs + jd_docs

        logging.info("Splitting documents...")
        split_docs = split_documents(all_docs)

        logging.info("Creating embeddings...")
        embeddings = get_embeddings()

        logging.info("Building vector store...")
        vectorstore = create_vectorstore(split_docs, embeddings)

        retriever = get_retriever(vectorstore)

        logging.info("Building RAG chain...")
        rag_chain = build_rag_chain(retriever)

        query = "Analyze how well this resume matches the job description. Give match score and missing skills."

        logging.info("Generating analysis...")
        response = rag_chain.invoke({"input": query})

        print("\n================ RAG ANALYSIS ================\n")
        print(response["answer"])
        print("\n=============================================\n")

    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == "__main__":
    main()