from abc import ABC, abstractmethod
from typing import Any

from ..paradigms.base import BaseParadigm


class BaseAgentType(ABC):
    """Base class for agent types"""

    def __init__(self, paradigm: BaseParadigm):
        self.paradigm = paradigm

    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run the agent with the specified paradigm"""
        self.paradigm.run(goal, max_steps, verbose)

    @abstractmethod
    def process_result(self, result: Any) -> Any:
        """Process the result based on agent type specific logic"""
        pass
