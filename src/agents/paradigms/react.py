import json
from typing import Any, Dict, List

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

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

    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        self.history: List[Thought | Action | Observation] = []

    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run ReACT Agent"""
        step = 0

        console.print(Panel(f"[bold blue]Goal:[/]\n{goal}"))

        while step < max_steps:
            step += 1
            console.print(f"\n[bold]Step {step}[/]")

            # Think
            thought = self.think(goal)
            console.print(
                Panel(
                    f"[bold green]Thought:[/]\n{thought.content}", border_style="green"
                )
            )

            # Act
            action = self.act(thought)
            console.print(
                Panel(
                    f"[bold yellow]Action:[/]\n{action.name}\nArgs: {action.args}",
                    border_style="yellow",
                )
            )

            # Observe
            observation = self.observe(action)
            console.print(
                Panel(
                    f"[bold magenta]Observation:[/]\n{observation.content}",
                    border_style="magenta",
                )
            )

            if verbose:
                console.print("\n[bold]Current State:[/]")
                console.print(self._build_context())

            # 次のステップの確認
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

Take a deep breath and think about what to do next to achieve the goal step by step. Respond in JSON format:
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

What action should be taken? Respond in JSON format:
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

What would be observed? Respond directly with the observation."""

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
