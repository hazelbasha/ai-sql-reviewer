# src/qwen_judge.py

from deepeval.models import DeepEvalBaseLLM
from ollama import chat

class QwenJudge(DeepEvalBaseLLM):

    def load_model(self):
        return "qwen2.5-coder:7b"

    def generate(self, prompt: str) -> str:
        response = chat(
            model="qwen2.5-coder:7b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "qwen2.5-coder:7b"