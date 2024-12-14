import aisuite as ai

from .template.base import LLMClientTemplate

class OpenAIClient(LLMClientTemplate):
    def __init__(self, _api_key: str):
        super().__init__(_api_key=_api_key)

    def _initialize_client(self):
        self.client = ai.Client({"openai": {"api_key": self._api_key}})
        """
        self.model = "openai:gpt-4o"
        """
        self.model = "openai:gpt-3.5-turbo"