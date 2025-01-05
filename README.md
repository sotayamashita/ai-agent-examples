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
  - More agent types coming soon...
- Dynamic model selection from available Ollama models

## Project Structure

```
src/
├── agents/
│   ├── paradigms/            # Reasoning paradigm implementations
│   │   ├── base.py           # Base paradigm class
│   │   ├── react.py          # ReAct paradigm
│   │   └── rewoo.py          # ReWOO paradigm
│   └── types/                # Agent type implementations
│       ├── base.py           # Base agent type class
│       └── simple_reflex.py  # Simple reflex agent
├── clients/
│   └── ollama_client.py      # Ollama API client
└── cli.py                    # Command-line interface
```

## Installation

1. Install and start Ollama:
   - Visit [Ollama's official website](https://ollama.com/) for the latest installation instructions
   - Start the Ollama service
   - Pull at least one model e.g. `ollama pull llama2`
   - For other available models, check [Ollama Model Library](https://ollama.com/search)
2. Clone this repository
3. Install dependencies with `poetry install`

## Usage

The CLI provides various options to experiment with different combinations of paradigms and agent types:

```bash
# List available options and models
poetry run ai-agent --help

# Run with default settings (ReAct paradigm + Simple Reflex agent)
poetry run ai-agent

# Use ReWOO paradigm with a specific model (just specify model name without version)
poetry run ai-agent --paradigm rewoo --model mistral

# Show detailed logs
poetry run ai-agent --verbose

# Full configuration
poetry run ai-agent --paradigm react --agent-type simple-reflex --model llama2 --max-steps 10 --verbose
```

Available options:
- `--paradigm`: Choose reasoning paradigm (`react` or `rewoo`)
- `--agent-type`: Choose agent type (`simple-reflex`)
- `--model`: Select LLM model from available Ollama models (specify model name without version)
- `--max-steps`: Set maximum number of steps
- `--verbose`: Enable detailed logging

### Example Usage Scenarios

Here are some practical examples of how to use the AI Agent with different goals:

#### 1. Task Planning and Organization
```bash
poetry run ai-agent --paradigm rewoo --model llama2

Enter your goal: Help me plan my workday. I have a team meeting at 10am, three urgent emails to respond to, a project deadline tomorrow, and I need to prepare for a client presentation next week.
```
ReWOO paradigm is suitable here as it plans all steps upfront.

#### 2. Problem Analysis and Debugging
```bash
poetry run ai-agent --paradigm react --model mistral

Enter your goal: My Python web application is returning a 500 error when users try to upload files larger than 2MB. Help me identify potential causes and solutions.
```
ReAct paradigm works well here as it can think and adapt based on each observation.

#### 3. Research and Information Gathering
```bash
poetry run ai-agent --paradigm react --model llama2 --verbose

Enter your goal: I need to research and compare different cloud providers (AWS, Azure, GCP) for hosting a machine learning application. Focus on pricing, scalability, and ML-specific services.
```
Verbose mode helps track the agent's thought process during research.

#### 4. Decision Making
```bash
poetry run ai-agent --paradigm rewoo --model mistral --max-steps 8

Enter your goal: Help me evaluate whether to migrate our application from a monolithic architecture to microservices. Consider team size (15 developers), current pain points (deployment delays, scaling issues), and business growth plans.
```
Extended steps allow for thorough analysis of complex decisions.

#### 5. Code Review and Improvement
```bash
poetry run ai-agent --paradigm react --model llama2

Enter your goal: Review my React component that handles user authentication. Look for security vulnerabilities, performance issues, and suggest best practices for improvement.
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

## References

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [IBM: What are AI agents?](https://www.ibm.com/think/topics/ai-agents)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- [ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models](https://arxiv.org/abs/2305.18323)
