import abc
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
from enum import Enum

class MessageInterface(BaseModel):
    """
    message for LLM
    """
    system_content: str = Field(...)
    user_content: str = Field(...)

    @property
    def to_dict(self):
        value = [
            {"role": "system", "content": f"{self.system_content}"},
            {"role": "user", "content": f"{self.user_content}"},
        ]
        return value
    
from enum import Enum

class Relevance(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def evaluate_relevance_level(cls, response: str) -> str:
        """
        驗證輸入字符串是否為有效的 Relevance 
        """
        valid_values = {cls.HIGH, cls.MEDIUM, cls.LOW}
        response_lower = response.lower()
        if response_lower in valid_values:
            return response_lower
        else:
            raise ValueError(f"Invalid relevance evaluation value: {response}")


        

class LLMClientBase(metaclass=abc.ABCMeta):
    """
    Abstract defining the structure for an LLM client.
    """
    openai_client: OpenAI | None  

    @abc.abstractmethod
    def _generate(self, messages: MessageInterface) -> str:
        """
        response based on the prompt.
        :param messages: MessageInterface
        :return: The generated text response from the LLM API.
        """
        pass