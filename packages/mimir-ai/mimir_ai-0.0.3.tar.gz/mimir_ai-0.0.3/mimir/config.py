from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from ragas import metrics


config = {
    "GENERATOR_MODEL": "gpt-4o",
    "CRITIC_MODEL": "gpt-4o",
    "EVALUATOR_MODEL": ChatOpenAI(model="gpt-4o"),
    "EMBEDDER": OpenAIEmbeddings(model="text-embedding-3-large"),
    "metrics": [
        metrics.answer_relevancy,
        metrics.answer_correctness,
        metrics.answer_relevancy,
        metrics.answer_similarity,
        metrics.context_entity_recall,
        metrics.context_precision,
        metrics.context_recall,
        metrics.context_utilization,
        metrics.faithfulness,
        metrics.noise_sensitivity_irrelevant,
        metrics.noise_sensitivity_relevant,
        metrics.rubrics_score_with_reference,
        metrics.rubrics_score_without_reference,
        # metrics.summarization_score,
    ],
}
