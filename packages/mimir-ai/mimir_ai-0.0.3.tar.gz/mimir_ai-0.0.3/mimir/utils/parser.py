import json

from datasets import Dataset

from mimir.utils.common import Logger


logger = Logger(__name__)


def create_dataset_for_eval(testdata_file_path, rag_qna_file_path):
    with open(testdata_file_path, "r") as f:
        with open(rag_qna_file_path, "r") as f2:
            test_data = json.load(f)
            rag_qna = json.load(f2)

            test_data_map = {item["question"]: item for item in test_data}
            rag_qna_map = {item["question"]: item for item in rag_qna}

            common_questions = list(set(test_data_map.keys()) & set(rag_qna_map.keys()))

            data = {
                "question": common_questions,
                "answer": [],
                "contexts": [],
                "ground_truth": [],
            }
            for question in common_questions:
                data["answer"].append(rag_qna_map[question]["answer"])
                data["contexts"].append(test_data_map[question]["contexts"])
                data["ground_truth"].append(test_data_map[question]["ground_truth"])

            dataset = Dataset.from_dict(data)
            logger.info(f"Created dataset for evaluation with {len(dataset)} examples")
            return dataset
