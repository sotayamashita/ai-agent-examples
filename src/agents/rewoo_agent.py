from rich.console import Console
from rich.panel import Panel

from src.clients import OllamaClient

from .base import BaseAgent

console = Console()


class ReWOOAgent(BaseAgent):
    """ReWOO (Reasoning WithOut Observation) Agent"""

    def __init__(self, model_name: str):
        super().__init__(model_name)

    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run ReWOO Agent

        Args:
            goal (str): The goal or task for the agent to achieve
            max_steps (int): Maximum number of steps the agent can take
            verbose (bool): Whether to show detailed output
        """
        raise NotImplementedError("ReWOO Agent is not implemented yet")
