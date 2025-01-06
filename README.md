# AI Agent Playground

![Python](https://img.shields.io/badge/python-3.12-blue)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

An experimental playground for learning and exploring different AI Agent paradigms and types. This repository provides a flexible framework for implementing, testing, and understanding various AI agent architectures through hands-on experimentation.

## Prerequisites

- [Ollama](https://ollama.com/) for LLM API
  - Must be installed and running
  - At least one model must be pulled
- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

## Features

- Multiple reasoning paradigms:
  - ReAct (Reasoning and Acting)
  - ReWOO (Reasoning Without Observation)
- Different agent types:
  - Simple Reflex Agent
  - Model-based Reflex Agent
  - More agent types coming soon...
- Dynamic model selection from available Ollama models
- Pre-defined experimental goals for agent testing

## Project Structure

```
src/
├── agents/
│   ├── paradigms/                 # Reasoning paradigm implementations
│   │   ├── base.py                # Base paradigm class
│   │   ├── react.py               # ReAct paradigm
│   │   └── rewoo.py               # ReWOO paradigm
│   └── types/                     # Agent type implementations
│       ├── base.py                # Base agent type class
│       ├── simple_reflex.py       # Simple reflex agent
│       └── model_based_reflex.py  # Model-based reflex agent
├── examples/                      # Example goals and use cases
│   ├── __init__.py                # Examples package initialization
│   └── goals.py                   # Pre-defined goals for testing
├── clients/
│   └── ollama_client.py           # Ollama API client
└── cli.py                         # Command-line interface
```

## Usage

The CLI provides various options to experiment with different combinations of paradigms and agent types:

### Basic Commands

```bash
# List available options and models
poetry run ai-agent --help

# List available experimental goals
poetry run ai-agent --list-goals

# Run with default settings (ReAct paradigm + Simple Reflex agent)
poetry run ai-agent

# Use ReWOO paradigm with a specific model
poetry run ai-agent --paradigm rewoo --model mistral

# Run a specific experimental goal
poetry run ai-agent --paradigm react --agent-type model-based-reflex --goal task_management
```

### Available Options
- `--paradigm`: Choose reasoning paradigm (`react` or `rewoo`)
- `--agent-type`: Choose agent type (`simple-reflex` or `model-based-reflex`)
- `--model`: Select LLM model from available Ollama models
- `--max-steps`: Set maximum number of steps
- `--verbose`: Enable detailed logging
- `--goal`: Select a pre-defined experimental goal
- `--list-goals`: Show available experimental goals

### Programmatic Usage

```python
from src.examples import get_available_goals, get_goal_description

# Get list of available goals
goals = get_available_goals("react", "model_based_reflex")

# Get specific goal description
description = get_goal_description("react", "model_based_reflex", "task_management")
```

### Model Names

When specifying a model name (either in the CLI or in code), you only need to provide the base model name without the version tag. For example:
- Use `llama2` (not `llama2:latest`)
- Use `mistral` (not `mistral:7b`)
- Use `gemma` (not `gemma:7b`)

The CLI will automatically handle the version information internally.

### Troubleshooting

If you encounter errors when starting the CLI, ensure:
1. Ollama is properly installed
2. Ollama service is running
3. You have pulled at least one model using `ollama pull <model-name>`

The CLI will provide specific error messages to help you identify and resolve any issues.

## Reasoning Paradigms

### ReAct (Reasoning and Acting)
- Combines reasoning and acting in a loop
- Think-Act-Observe cycle for step-by-step problem solving
- Suitable for tasks requiring continuous feedback
- Best for: debugging, research, interactive problem-solving

### ReWOO (Reasoning Without Observation)
- Plans actions upfront before execution
- Reduces redundant tool usage
- Efficient for well-defined tasks with clear steps
- Best for: task planning, strategy development, decision analysis

## Agent Types

### Simple Reflex Agent
- Responds immediately to current perception
- No internal state maintenance
- Suitable for straightforward stimulus-response scenarios
- Best for: quick decisions, simple tasks, immediate responses

## Contributing

Feel free to contribute by:
1. Implementing new agent types
2. Adding new reasoning paradigms
3. Improving existing implementations
4. Adding tests and documentation

## Case Studies

See [examples/case-studies](examples/case-studies) for detailed analysis of AI Agent implementations in production services.

## References

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [IBM: What are AI agents?](https://www.ibm.com/think/topics/ai-agents)
  - Japanese translation: [AIエージェントとは](https://www.ibm.com/jp-ja/think/topics/ai-agents)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models](https://arxiv.org/abs/2305.18323)
- [Kaggle Agents](https://www.kaggle.com/whitepaper-agents)

