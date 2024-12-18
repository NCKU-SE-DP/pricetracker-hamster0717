class LLMClientInitializeException(Exception):
    """
    Raised when the LLM client fails to initialize.
    """
    def __init__(self, message: str):
        super().__init__(message)


class EvaluationFailure(Exception):
    """
    Raised when the evaluation process fails.
    """
    def __init__(self, message: str):
        super().__init__(message)
class InvalidAiInputParamException(Exception):
    """
    Raised when the input parameters to an AI function or model are invalid.
    """
    def __init__(self, message: str = "Invalid input parameters for AI processing"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"InvalidAiInputParamException: {self.message}"


class InternalServerErrorException(Exception):
    """
    Raised when an internal server error occurs in the AI system.
    """
    def __init__(self, message: str = "An internal server error occurred"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"InternalServerErrorException: {self.message}"