import sys
from typing import Dict, List, Optional, Type

import fire
import inquirer
from rich.console import Console

from .agents import ReACTAgent, ReWOOAgent
from .agents.base import BaseAgent
from .clients import OllamaClient
from .clients.ollama_client import Model

console = Console()

# CLI Questions configuration
QUESTIONS = {
    "model_selection": lambda models: inquirer.List(
        "model",
        message="Select a model to use",
        choices=[(f"{model.name}", model.name) for model in models],
    ),
    "agent_selection": lambda agents: inquirer.List(
        "agent",
        message="Select an agent to use",
        choices=[
            (f"{name} - {agent_class.__doc__}", name)
            for name, agent_class in agents.items()
        ],
    ),
    "goal_input": inquirer.Text("goal", message="What is your goal?"),
}


class AgentCLI:
    """Command Line Interface for AI Agents

    This class provides a CLI interface for interacting with different AI agents.
    It supports listing available agents and running them with specified parameters.
    """

    def __init__(self):
        self.agents: Dict[str, Type[BaseAgent]] = {
            "react": ReACTAgent,
            "rewoo": ReWOOAgent,
        }

        self.models: List[Model] = OllamaClient().models()

    def _select_model(self) -> Optional[str]:
        """Prompt user to select a model

        Returns:
            Optional[str]: Selected model name or None if cancelled
        """
        answers = inquirer.prompt([QUESTIONS["model_selection"](self.models)])
        return answers["model"] if answers else None

    def _select_agent(self) -> Optional[str]:
        """Prompt user to select an agent

        Returns:
            Optional[str]: Selected agent name or None if cancelled
        """
        answers = inquirer.prompt([QUESTIONS["agent_selection"](self.agents)])
        return answers["agent"] if answers else None

    def _get_goal(self) -> Optional[str]:
        """Prompt user to input their goal

        Returns:
            Optional[str]: User's goal or None if cancelled
        """
        answers = inquirer.prompt([QUESTIONS["goal_input"]])
        return answers["goal"] if answers else None

    def run(self, max_steps: int = 5, verbose: bool = False) -> None:
        """Run the selected agent with specified parameters

        Args:
            max_steps (int): Maximum number of steps for the agent to take
            verbose (bool): Whether to show detailed output
        """
        try:
            # Select model
            model_name = self._select_model()
            if not model_name:
                console.print("[yellow]Operation cancelled[/]")
                return

            # Select agent
            agent_name = self._select_agent()
            if not agent_name:
                console.print("[yellow]Operation cancelled[/]")
                return

            if agent_name not in self.agents:
                console.print(f"[red]Error:[/] Unknown agent type '{agent_name}'")
                console.print("Available agents:", ", ".join(self.agents.keys()))
                return

            # Get goal
            goal = self._get_goal()
            if not goal:
                console.print("[yellow]Operation cancelled[/]")
                return

            # Initialize and run agent
            agent_class = self.agents[agent_name]
            agent_instance = agent_class(model_name)

            console.print(f"\n[bold]Running {agent_name} agent...[/]")
            agent_instance.run(goal, max_steps, verbose)

        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/]")
            sys.exit(1)
        except Exception as e:
            console.print(f"\n[red]Error:[/] {str(e)}")
            console.print_exception()
            sys.exit(1)


def main() -> None:
    """CLI entry point"""
    try:
        fire.Fire(AgentCLI)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/] {str(e)}")
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
