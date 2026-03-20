"""CLI entry point for AI Resume Matcher."""
import argparse
import logging
import sys

from backend import config
from backend.config import require_api_key
from backend.loader import load_resume, load_job_description
from backend.splitter import split_documents
from backend.embeddings import get_embeddings
from backend.vectorstore import create_vectorstore
from backend.retriever import get_retriever
from backend.rag_chain import build_rag_chain
from backend.scorer import keyword_score

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def run_analysis(resume_path: str, jd_path: str) -> dict:
    """Run the full RAG analysis pipeline and return results."""
    logger.info("Loading documents...")
    resume_docs = load_resume(resume_path)
    jd_docs = load_job_description(jd_path)
    all_docs = resume_docs + jd_docs

    logger.info("Splitting %d documents into chunks...", len(all_docs))
    split_docs = split_documents(all_docs)
    logger.info("Created %d chunks.", len(split_docs))

    logger.info("Creating embeddings & vector store...")
    embeddings = get_embeddings()
    vectorstore = create_vectorstore(split_docs, embeddings)
    retriever = get_retriever(vectorstore)

    logger.info("Building RAG chain (model=%s)...", config.MODEL_NAME)
    rag_chain = build_rag_chain(retriever)

    query = (
        "Analyze how well this resume matches the job description. "
        "Give a percentage match score, list matched skills, "
        "identify skill gaps, and provide improvement suggestions."
    )

    logger.info("Generating analysis...")
    response = rag_chain.invoke({"query": query})

    resume_text = " ".join(d.page_content for d in resume_docs)
    jd_text = " ".join(d.page_content for d in jd_docs)
    kw_score = keyword_score(resume_text, jd_text)

    return {
        "answer": response["result"],
        "source_documents": response.get("source_documents", []),
        "keyword_score": kw_score,
    }


def main() -> None:
    setup_logging()

    parser = argparse.ArgumentParser(description="AI Resume Matcher")
    parser.add_argument(
        "--resume", default="data/resume.pdf",
        help="Path to the resume PDF (default: data/resume.pdf)",
    )
    parser.add_argument(
        "--jd", default="data/job_description.txt",
        help="Path to the job description text file (default: data/job_description.txt)",
    )
    args = parser.parse_args()

    try:
        require_api_key()
        result = run_analysis(args.resume, args.jd)

        print("\n" + "=" * 50)
        print("  AI RESUME MATCHER — ANALYSIS")
        print("=" * 50)
        print(f"\nKeyword Overlap Score: {result['keyword_score']}%\n")
        print(result["answer"])
        print("\n" + "=" * 50 + "\n")

    except EnvironmentError as exc:
        logger.error("%s", exc)
        sys.exit(1)
    except FileNotFoundError as exc:
        logger.error("File not found: %s", exc)
        sys.exit(1)
    except Exception:
        logger.exception("Analysis failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
