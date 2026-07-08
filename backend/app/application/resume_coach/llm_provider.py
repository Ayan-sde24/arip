"""LLM provider interface to support future OpenAI, Gemini, and Claude integrations."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Common interface for external LLM models."""

    @abstractmethod
    def generate(self, prompt: str, system_instruction: str | None = None) -> str:
        """Generate content from the LLM based on prompt and system instructions.

        Args:
            prompt: User-level input query.
            system_instruction: High-level instructions or system prompt.

        Returns:
            The generated string completion.
        """
        pass


class MockLLMProvider(LLMProvider):
    """Mock LLM Provider for unit testing and deterministic rule-based optimizations."""

    def __init__(self, response_map: dict[str, str] | None = None) -> None:
        self.response_map = response_map or {}

    def generate(self, prompt: str, system_instruction: str | None = None) -> str:
        # Fallback to simple matching if key is in response_map
        for key, value in self.response_map.items():
            if key.lower() in prompt.lower():
                return value

        # Default mock response
        return (
            "Senior Software Engineer with 5+ years of experience "
            "specializing in Python, FastAPI, and Docker microservices."
        )
