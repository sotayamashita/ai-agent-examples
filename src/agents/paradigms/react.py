import json
from typing import Any, Dict, List

from pydantic import BaseModel
from rich.console import Console

from .base import BaseParadigm

console = Console()


class Thought(BaseModel):
    """Represent agent's thought"""

    content: str


class Action(BaseModel):
    """Represent agent's action"""

    name: str
    args: Dict[str, Any]


class Observation(BaseModel):
    """Represent observation of the action result"""

    content: str


class ReActParadigm(BaseParadigm):
    """ReACT (Reasoning and Acting) Agent"""

    def __init__(self, model_name: str, language: str = "en"):
        super().__init__(model_name=model_name, language=language)
        self.history: List[Thought | Action | Observation] = []

    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run ReACT Agent"""
        step = 0

        console.print("\n[bold blue]Goal:[/]")
        console.print(goal)
        console.print()

        while step < max_steps:
            step += 1
            console.print(f"\n[bold]Step {step}[/]")

            # Think
            thought = self.think(goal)
            console.print("\n[bold green]Thought:[/]")
            console.print(thought.content)

            # Act
            action = self.act(thought)
            console.print("\n[bold yellow]Action:[/]")
            console.print(f"Name: {action.name}")
            console.print(f"Args: {action.args}")

            # Observe
            observation = self.observe(action)
            console.print("\n[bold magenta]Observation:[/]")
            console.print(observation.content)

            if verbose:
                console.print("\n[bold]Current State:[/]")
                console.print(self._build_context())

            if (
                not input("\nPress Enter to continue, or 'q' to quit: ")
                .lower()
                .startswith("q")
            ):
                continue
            break

        console.print("\n[bold]Agent run completed![/]")

    def think(self, goal: str) -> Thought:
        """Think about the current situation"""
        context = self._build_context()
        prompt = f"""Goal: {goal}

Previous steps:
{context}

Take a deep breath and think about what to do next to achieve the goal step by step. Please respond in {self.language} language. Respond in JSON format:
{{
    "content": "I think ..."
}}

Do not include any other text, only return the JSON object."""

        response = self.llm.generate(self.model_name, prompt)
        try:
            thought_content = json.loads(response)["content"]
            thought = Thought(content=thought_content)
            self.history.append(thought)
            return thought
        except json.JSONDecodeError:
            raise ValueError(f"Invalid thought format from LLM: {response}")

    def act(self, thought: Thought) -> Action:
        """Determine the next action"""
        prompt = f"""Based on this thought:
{thought.content}

What action should be taken? Please respond in {self.language} language. Respond in JSON format:
{{
    "name": "action_name",
    "args": {{
        "arg1": "value1"
    }}
}}

Do not include any other text, only return the JSON object."""

        response = self.llm.generate(self.model_name, prompt)
        try:
            action_data = json.loads(response)
            action = Action(name=action_data["name"], args=action_data["args"])
            self.history.append(action)
            return action
        except json.JSONDecodeError:
            raise ValueError(f"Invalid action format from LLM: {response}")

    def observe(self, action: Action) -> Observation:
        """Observe the result of the action"""
        prompt = f"""After taking this action:
{action.name} with args {action.args}

What would be observed? Please respond in {self.language} language. Respond directly with the observation."""

        response = self.llm.generate(self.model_name, prompt)
        observation = Observation(content=response.strip())
        self.history.append(observation)
        return observation

    def _build_context(self) -> str:
        """Build context from history"""
        context = []
        for item in self.history:
            if isinstance(item, Thought):
                context.append(f"Thought: {item.content}")
            elif isinstance(item, Action):
                context.append(f"Action: {item.name} ({item.args})")
            elif isinstance(item, Observation):
                context.append(f"Observation: {item.content}")
        return "\n".join(context)
