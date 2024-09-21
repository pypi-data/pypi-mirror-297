import os

from ragas import evaluate

from mimir.utils.parser import create_dataset_for_eval
from mimir.utils.common import Logger
from mimir.utils.chart import create_chart
from mimir.config import config


logger = Logger(__name__)


def eval_rag(qna_file_path, qna_rag_file_path, should_create_chart=True):
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set")

    assert os.path.exists(qna_file_path), f"File {qna_file_path} does not exist"
    assert os.path.exists(qna_rag_file_path), f"File {qna_rag_file_path} does not exist"

    dataset = create_dataset_for_eval(qna_file_path, qna_rag_file_path)

    logger.info("Evaluating RAG Model")

    result = evaluate(
        dataset,
        metrics=config["metrics"],
        embeddings=config["EMBEDDER"],
        llm=config["EVALUATOR_MODEL"],
    )

    logger.info("\n\n" + "=" * 80 + f"\n\nResults: {result}\n\n" + "=" * 80 + "\n\n")

    if should_create_chart:
        create_chart(result)
