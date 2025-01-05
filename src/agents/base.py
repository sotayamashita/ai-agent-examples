from abc import ABC, abstractmethod
from typing import Optional

from src.clients import OllamaClient


class BaseAgent(ABC):
    """Base class for all AI agents

    This abstract class defines the common interface that all agents must implement.
    It provides basic initialization and abstract methods that need to be overridden.
    """

    def __init__(self):
        """Initialize the base agent with an LLM client"""
        self.llm = OllamaClient()

    @abstractmethod
    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run the agent with the given goal

        Args:
            goal (str): The goal or task for the agent to achieve
            max_steps (int): Maximum number of steps the agent can take
            verbose (bool): Whether to show detailed output
        """
        pass
