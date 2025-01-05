import json
from datetime import datetime
from typing import Any, Dict, List

import requests
from pydantic import BaseModel

from .base import BaseClient


class Model(BaseModel):
    name: str
    model: str
    modified_at: datetime
    size: int
    digest: str
    details: Dict[str, Any]


class OllamaClient(BaseClient):
    """Ollama API Client"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def models(self) -> List[Model]:
        """Get all available models"""
        url = f"{self.base_url}/api/tags"

        response = requests.get(url)
        response.raise_for_status()

        return [
            Model.model_validate(model_data) for model_data in response.json()["models"]
        ]

    def generate(self, model_name: str, prompt: str, system: str = None) -> str:
        """Generate text using Ollama API"""
        url = f"{self.base_url}/api/generate"

        payload = {"model": model_name, "prompt": prompt, "stream": False}

        if system:
            payload["system"] = system

        response = requests.post(url, json=payload)
        response.raise_for_status()

        response_text = response.json()["response"]
        # Remove code block markers if they exist
        response_text = self._remove_code_block_markers(response_text)
        return response_text

    def _remove_code_block_markers(self, text: str) -> str:
        """Remove code block markers with or without language specification from the text.

        Args:
            text: The text to process

        Returns:
            The text with code block markers removed
        """
        # Remove code blocks with language specification (e.g. ```python)
        if text.startswith("```") and text.endswith("```"):
            lines = text.split("\n")
            # Remove first and last line if they only contain ```
            if lines[0].startswith("```") and lines[-1] == "```":
                text = "\n".join(lines[1:-1])
        return text
