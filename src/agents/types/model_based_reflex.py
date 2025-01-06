from typing import Any, Dict

from .base import BaseAgentType


class ModelBasedReflexAgent(BaseAgentType):
    """Model-based Reflex Agent implementation"""

    def __init__(self, paradigm):
        super().__init__(paradigm)
        # Initialize internal model (state)
        self.model: Dict[str, Any] = {
            "environment_state": {},  # Track environment state
            "action_history": [],     # History of executed actions
            "performance_metrics": {   # Performance metrics
                "actions_taken": 0,
                "goals_achieved": 0
            }
        }

    def update_model(self, percept: Any) -> None:
        """
        Update internal model
        Args:
            percept: Perception information from environment
        """
        # Update environment state
        if isinstance(percept, dict):
            self.model["environment_state"].update(percept)
        
        # Update performance metrics
        self.model["performance_metrics"]["actions_taken"] += 1

    def process_result(self, result: Any) -> Any:
        """
        Model-based agent processing logic
        1. Receive perception information
        2. Update internal model
        3. Record action history
        4. Process and return results
        """
        # Update internal model based on perception
        self.update_model(result)

        # Record action history
        self.model["action_history"].append(result)

        # Evaluate goal achievement (e.g., when specific conditions are met)
        if self._is_goal_achieved(result):
            self.model["performance_metrics"]["goals_achieved"] += 1

        # Process results considering internal model
        processed_result = self._process_with_model(result)
        
        return processed_result

    def _is_goal_achieved(self, result: Any) -> bool:
        """
        Evaluate if goal is achieved
        Actual implementation should define specific goal achievement conditions
        """
        # As a simple example, consider goal achieved if result is dict with 'goal_achieved' key as True
        if isinstance(result, dict) and result.get('goal_achieved'):
            return True
        return False

    def _process_with_model(self, result: Any) -> Any:
        """
        Process results considering internal model
        Actual implementation should process/modify results based on model state
        """
        # Process results based on internal model state
        if isinstance(result, dict):
            # Add model state to results
            result.update({
                "model_state": self.model["environment_state"],
                "actions_taken": self.model["performance_metrics"]["actions_taken"],
                "goals_achieved": self.model["performance_metrics"]["goals_achieved"]
            })
        return result