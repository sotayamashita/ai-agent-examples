import sys
from typing import NoReturn

import click
import requests
from rich.console import Console

from src.agents import ReActParadigm, ReWOOParadigm, SimpleReflexAgent, ModelBasedReflexAgent
from src.clients.ollama_client import OllamaClient
from src.examples.goals import GOALS

console = Console()

PARADIGMS = {"react": ReActParadigm, "rewoo": ReWOOParadigm}

AGENT_TYPES = {
    "simple-reflex": SimpleReflexAgent,
    "model-based-reflex": ModelBasedReflexAgent,
    # TODO: Add other agent types after implementation
}


def exit_with_error(message: str) -> NoReturn:
    """Exit the program with an error message"""
    console.print(f"[red]Error:[/] {message}")
    console.print("\nPlease ensure:")
    console.print("1. Ollama is installed (https://ollama.com)")
    console.print("2. Ollama service is running")
    console.print("3. You have pulled at least one model (e.g., 'ollama pull llama2')")
    sys.exit(1)


def get_available_models() -> list[str]:
    """Get list of available models from Ollama"""
    try:
        client = OllamaClient()
        models = client.models()
        if not models:
            exit_with_error("No models found in Ollama")
        return [model.name.split(":")[0] for model in models]
    except requests.exceptions.ConnectionError:
        exit_with_error("Could not connect to Ollama. Is the service running?")
    except Exception as e:
        exit_with_error(f"Failed to fetch models from Ollama: {str(e)}")


def display_goals() -> None:
    """List available example goals"""
    console.print("\n[bold blue]Available Example Goals:[/]")
    for name, goal in GOALS.items():
        console.print(f"\n[bold]{name}[/]")
        console.print(goal)


@click.command()
@click.option(
    "--paradigm",
    type=click.Choice(list(PARADIGMS.keys())),
    default="react",
    help="Select reasoning paradigm",
)
@click.option(
    "--agent-type",
    type=click.Choice(list(AGENT_TYPES.keys())),
    default="simple-reflex",
    help="Select AI agent type",
)
@click.option(
    "--model",
    type=click.Choice(get_available_models()),
    default="llama2",
    help="Select LLM model from available Ollama models",
)
@click.option("--max-steps", default=5, help="Maximum number of execution steps")
@click.option("--verbose", is_flag=True, help="Show detailed logs")
@click.option(
    "--language",
    type=str,
    default="en",
    help="Language for LLM output (e.g., en, ja, zh)",
)
@click.option(
    "--list-goals",
    is_flag=True,
    help="List available example goals",
)
def main(
    paradigm: str,
    agent_type: str,
    model: str,
    max_steps: int,
    verbose: bool,
    language: str,
    list_goals: bool,
) -> None:
    """CLI for AI Agent experimentation

    Allows experimenting with different combinations of reasoning paradigms and agent types.
    """
    if list_goals:
        display_goals()
        return

    console.print(f"[bold blue]Selected Configuration:[/]")
    console.print(f"Paradigm: {paradigm}")
    console.print(f"Agent Type: {agent_type}")
    console.print(f"Model: {model}")
    console.print(f"Max Steps: {max_steps}")
    console.print(f"Verbose: {verbose}")
    console.print(f"Language: {language}")

    # Instantiate paradigm
    paradigm_class = PARADIGMS[paradigm]
    paradigm_instance = paradigm_class(model_name=model, language=language)

    # Instantiate agent
    agent_class = AGENT_TYPES[agent_type]
    agent = agent_class(paradigm=paradigm_instance)

    # Get goal from user
    goal = click.prompt("\nEnter your goal", type=str)

    # Run agent
    agent.run(goal=goal, max_steps=max_steps, verbose=verbose)


if __name__ == "__main__":
    main()
