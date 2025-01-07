import sys
from typing import NoReturn

import click
import requests
from rich.console import Console
from InquirerPy import inquirer

from src.agents import ReActParadigm, ReWOOParadigm, SimpleReflexAgent, ModelBasedReflexAgent
from src.clients.ollama_client import OllamaClient

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

def select_paradigm() -> str:
    """Select reasoning paradigm interactively"""
    return inquirer.select(
        message="Select reasoning paradigm:",
        choices=list(PARADIGMS.keys()),
        default="react"
    ).execute()

def select_agent_type() -> str:
    """Select agent type interactively"""
    return inquirer.select(
        message="Select agent type:",
        choices=list(AGENT_TYPES.keys()),
        default="simple-reflex"
    ).execute()

def select_model() -> str:
    """Select model interactively"""
    return inquirer.select(
        message="Select model:",
        choices=get_available_models(),
    ).execute()

def select_language() -> str:
    """Select language interactively"""
    return inquirer.select(
        message="Select language:",
        choices=["en", "ja"],
        default="en"
    ).execute()


@click.command()
@click.option(
    "--paradigm",
    type=click.Choice(list(PARADIGMS.keys())),
    help="Select reasoning paradigm",
)
@click.option(
    "--agent-type",
    type=click.Choice(list(AGENT_TYPES.keys())),
    help="Select AI agent type",
)
@click.option(
    "--model",
    type=click.Choice(get_available_models()),
    help="Select LLM model from available Ollama models",
)
@click.option("--max-steps", default=5, help="Maximum number of execution steps")
@click.option("--verbose", is_flag=True, help="Show detailed logs")
@click.option(
    "--language",
    type=str,
    help="Language for LLM output (e.g., en, ja)",
)
def main(
    paradigm: str,
    agent_type: str,
    model: str,
    max_steps: int,
    verbose: bool,
    language: str,
) -> None:
    """CLI for AI Agent experimentation

    Allows experimenting with different combinations of reasoning paradigms and agent types.
    """
    console.print(f"[bold blue]Selected Configuration:[/]")
    
    # If paradigm is not specified, select interactively
    if not paradigm:
        paradigm = select_paradigm()
    
    # If agent type is not specified, select interactively
    if not agent_type:
        agent_type = select_agent_type()

    # If model is not specified, select interactively
    if not model:
        model = select_model()

    # If language is not specified, select interactively
    if not language:
        language = select_language()
    
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
