# AI Agent Example

![Python](https://img.shields.io/badge/python-3.12-blue)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


## Reasoning paradigms

- [x] ReACT ReAct (Reasoning and Action)
- [ ] ReWOO ReWOO (Reasoning WithOut Observation)

## Prerequisites

- [ollama](https://ollama.com/l)
- Python 3.12 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-agent
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

1. Activate the Poetry shell:
   ```bash
   poetry shell
   ```

2. Download model with ollama:
   ```bash
   ollama pull mistral
   ```

   Note: You can see any other model supported by ollama by visiting [ollama models](https://ollama.com/search)

3. Run the AI agent:
   ```bash
   python -m src.cli run
   ```

## References

- [What are AI agents?](https://www.ibm.com/think/topics/ai-agents)
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [Agents](https://www.kaggle.com/whitepaper-agents)
- [Practices for Governing Agentic AI Systems, December 14, 2023]([https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf](https://openai.com/index/practices-for-governing-agentic-ai-systems/))
