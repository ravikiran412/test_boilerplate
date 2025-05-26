from crewai import LLM
import os

environment = os.environ["ENVIRONMENT"]

class LLMSelector:
    def __init__(self, provider="openai"):
        self.provider = provider.lower()
        self.llm = self._select_llm()

    def _select_llm(self):
        if self.provider == "gemini":
            return LLM(
                model = os.environ["GEMINI_MODEL_2"] if environment == "development" else os.environ["GEMINI_MODEL_2_5"],
                api_key=os.environ["GEMINI_API_KEY"],
                temperature=0.0
            )
        elif self.provider == "openai":
            return LLM(
                model = os.environ["OPENAI_GPT_4_mini"] if environment == "development" else os.environ["OPENAI_GPT_4"],
                temperature=0.7,
                base_url=os.environ["OPENAI_BASE_URL"],
                api_key=os.environ["OPENAI_API_KEY"]
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_llm(self):
        return self.llm
