import json
from typing import Any, Dict, List

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

from .base import BaseParadigm

console = Console()


class Plan(BaseModel):
    """Represent agent's plan"""

    steps: List[str]


class Action(BaseModel):
    """Represent agent's action"""

    name: str
    args: Dict[str, Any]


class Result(BaseModel):
    """Represent action result"""

    content: str


class ReWOOParadigm(BaseParadigm):
    """ReWOO (Reasoning Without Observation) Paradigm"""

    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        self.plan: Plan | None = None

    def run(self, goal: str, max_steps: int = 5, verbose: bool = False) -> None:
        """Run ReWOO Paradigm"""
        console.print(Panel(f"[bold blue]Goal:[/]\n{goal}"))

        # Plan phase
        self.plan = self._create_plan(goal)
        console.print(Panel("[bold green]Plan:[/]", border_style="green"))
        for i, step in enumerate(self.plan.steps, 1):
            console.print(f"{i}. {step}")

        # Execute phase
        for step_num, step in enumerate(self.plan.steps, 1):
            if step_num > max_steps:
                break

            console.print(f"\n[bold]Executing Step {step_num}[/]")

            # Create action
            action = self._create_action(step)
            console.print(
                Panel(
                    f"[bold yellow]Action:[/]\n{action.name}\nArgs: {action.args}",
                    border_style="yellow",
                )
            )

            # Execute action
            result = self._execute_action(action)
            console.print(
                Panel(
                    f"[bold magenta]Result:[/]\n{result.content}",
                    border_style="magenta",
                )
            )

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

        console.print("\n[bold]Execution completed![/]")

    def _create_plan(self, goal: str) -> Plan:
        """Create a plan to achieve the goal"""
        prompt = f"""Goal: {goal}

Create a step-by-step plan to achieve this goal. Respond in JSON format:
{{
    "steps": [
        "Step 1: ...",
        "Step 2: ...",
        ...
    ]
}}

Do not include any other text, only return the JSON object."""

        response = self.llm.generate(self.model_name, prompt)
        try:
            plan_data = json.loads(response)
            plan = Plan(steps=plan_data["steps"])
            return plan
        except json.JSONDecodeError:
            raise ValueError(f"Invalid plan format from LLM: {response}")

    def _create_action(self, step: str) -> Action:
        """Create an action for the given step"""
        prompt = f"""For this step:
{step}

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

    def _execute_action(self, action: Action) -> Result:
        """Execute the action and get result"""
        prompt = f"""After taking this action:
{action.name} with args {action.args}

What would be the result? Respond directly with the result."""

        response = self.llm.generate(self.model_name, prompt)
        result = Result(content=response.strip())
        self.history.append(result)
        return result

    def _build_context(self) -> str:
        """Build context from history"""
        context = []
        for item in self.history:
            if isinstance(item, Action):
                context.append(f"Action: {item.name} ({item.args})")
            elif isinstance(item, Result):
                context.append(f"Result: {item.content}")
        return "\n".join(context)
