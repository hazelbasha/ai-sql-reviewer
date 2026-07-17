from deepeval.metrics import GEval
from deepeval.test_case import (
    LLMTestCase,
    LLMTestCaseParams
)

accuracy_metric = GEval(
    name="SQL Review Accuracy",

    evaluation_steps=[
        "Check whether important SQL issues are identified",
        "Penalize hallucinated issues",
        "Verify recommendations are actionable",
        "Verify severity assessment is appropriate"
    ],

    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT
    ],

    threshold=0.8
)