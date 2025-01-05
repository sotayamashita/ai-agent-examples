from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.clients.ollama_client import OllamaClient


class BaseParadigm(ABC):
    """Base class for reasoning paradigms"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.history: List[Any] = []
        self.llm = OllamaClient()

    @abstractmethod
    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run the paradigm"""
        pass

    @abstractmethod
    def _build_context(self) -> str:
        """Build context from history"""
        pass
