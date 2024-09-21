import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context

from mimir.config import config
from mimir.utils.common import save_list_to_json_file, Logger


logger = Logger("create_qna")


def create_qna(
    total_questions: int,
    dir_path: str,
    qna_file_path: str,
    distributions: dict = {simple: 0.5, reasoning: 0.25, multi_context: 0.25},
):
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set")

    assert sum(distributions.values()) > 0.999, "Distributions should sum to 1.0"
    assert sum(distributions.values()) < 1.001, "Distributions should sum to 1.0"
    assert simple in distributions, "simple distribution is required"
    assert reasoning in distributions, "reasoning distribution is required"
    assert multi_context in distributions, "multi_context distribution is required"

    assert os.path.exists(dir_path), f"Directory {dir_path} does not exist"
    assert os.path.isdir(dir_path), f"{dir_path} is not a directory"
    # assert os.path.exists(qna_file_path), f"File {qna_file_path} already exists"

    loader = DirectoryLoader(dir_path)
    documents = loader.load()

    for document in documents:
        document.metadata["filename"] = document.metadata["source"]

    # generator with openai models
    generator_llm = ChatOpenAI(model=config["GENERATOR_MODEL"])
    critic_llm = ChatOpenAI(model=config["CRITIC_MODEL"])
    embeddings = OpenAIEmbeddings()

    generator = TestsetGenerator.from_langchain(generator_llm, critic_llm, embeddings)

    # generate testset
    testset = generator.generate_with_langchain_docs(
        documents,
        test_size=total_questions,
        distributions=distributions,
    )

    test_items = testset.test_data

    logger.info(
        f"Generated testset item have following schema: \n\n{test_items[0].schema}"
    )

    data = []
    for item in test_items:
        data.append(
            {
                "question": item.question,
                "ground_truth": item.ground_truth,
                "contexts": item.contexts,
                "metadata": item.metadata,
            }
        )

    logger.info(f"Saving QnA data to: {qna_file_path}")
    save_list_to_json_file(data, qna_file_path)
    logger.info("Done creating QnA data")
