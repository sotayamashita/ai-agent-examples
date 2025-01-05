from typing import Any

from .base import BaseAgentType


class SimpleReflexAgent(BaseAgentType):
    """Simple Reflex Agent implementation"""

    def process_result(self, result: Any) -> Any:
        """Process result immediately without maintaining state"""
        # Simple reflexエージェントは状態を持たず、
        # 現在の知覚（結果）に基づいて即座に反応します
        return result
