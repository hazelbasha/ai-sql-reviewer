from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from src.qwen_judge import QwenJudge

judge_model = QwenJudge()

accuracy_metric = GEval(
    name="SQL Review Accuracy",
    evaluation_steps=[
        "Check whether important SQL issues are identified",
        "Penalize hallucinated issues",
        "Verify recommendations are actionable"
    ],
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT
    ],
    threshold=0.8,
    model=judge_model
)