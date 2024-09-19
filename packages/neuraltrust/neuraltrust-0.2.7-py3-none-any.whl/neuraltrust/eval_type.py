from enum import Enum

class RagasEvalTypeId(Enum):
    RAGAS_ANSWER_SEMANTIC_SIMILARITY = "RagasAnswerSemanticSimilarity"
    RAGAS_ANSWER_CORRECTNESS = "RagasAnswerCorrectness"

class GroundedEvalTypeId(Enum):
    ANSWER_SIMILARITY = "AnswerSimilarity"
    CONTEXT_SIMILARITY = "ContextSimilarity"

def is_ragas_eval(evaluator_type: str) -> bool:
    return any(evaluator_type == member.value for member in RagasEvalTypeId)

def is_grounded_eval(evaluator_type: str) -> bool:
    return any(evaluator_type == member.value for member in GroundedEvalTypeId)

