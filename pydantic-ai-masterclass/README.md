# PydanticAI Masterclass

## Overview

PydanticAI is a Python framework designed to simplify the process of creating robust and efficient AI agents. Developed by the team behind the popular Pydantic library, it offers powerful tools for building production-ready agent systems while leveraging Python's core strengths.

This repository serves as a companion to the PydanticAI Masterclass and it's corresponding video tutorials.

The first video tutorial is **[The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](https://www.youtube.com/watch?v=xVe87QpNE80)** where we introduce the framework and demonstrate key features through practical coding examples.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/xVe87QpNE80/0.jpg)](https://www.youtube.com/watch?v=xVe87QpNE80)

## Masterclass Modules

- [Part 1: The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](https://www.youtube.com/watch?v=xVe87QpNE80)
- [Part 2: From Chaos to Clarity: LLM Tracing with Logfire and PydanticAI (Coding Tutorial)](https://www.youtube.com/watch?v=TTNT3rnuZp0)
- [Part 3: 100% Reliable LLM Outputs with Structured Data Outputs (Developer Tutorial)](https://www.youtube.com/watch?v=PXO9_nWZYrc)
- [Part 4: Mastering System Prompts in PydanticAI: The Ultimate Guide (Developer Coding Tutorial)](https://www.youtube.com/watch?v=WQqsiB0xUXk)
- Part 5: Build More Effective Agents with Function Tools in PydanticAI (Developer Tutorial)
- Part 6: Improve the Accuracy of AI Agents with Result Validator Functions (Developer Tutorial)
- Part 7: Simplify Agent Workflows with Dependency Injection in PydanticAI (Developer Tutorial)
- Part 8: Advanced Retry Strategies for High-Performance AI Agents in PydanticAI (Developer Tutorial)
- Part 9: Better Context Retention with Agent Memory in PydanticAI (Developer Tutorial)
- Part 10: Building Resilient Agents: Best Practices for Handling Model Errors in PydanticAI (Developer Tutorial)
- Part 11: Better User Experience with Streaming Outputs in PydanticAI (Developer Tutorial)
- Part 12: Achieving Precision and Efficiency with Advanced Model Settings (Developer Tutorial)
- Part 13: Multi-Model Agents in PydanticAI: Unlocking Next-Gen AI Capabilities (Developer Tutorial)
- Part 14: Mastering RAG in PydanticAI: Better AI Agents with Real-Time Data (Developer Tutorial)
- Part 15: Masterclass Final Project: AI Resume Writing with Multiple Agents (Developer Tutorial)

## Looking for Collaborators

Have an idea for an article, video tutorial, a learning project or anything related to AI? Consider collaborating with our growing community of collaborators. Get started today by [posting your idea on our Discord sever](https://discord.gg/eQXBaCvTA9). Together, we are building a strong community of AI Software Developers.

## How to Contribute to This Repository

This repository is maintained by the team at **[AI Software Developers](https://www.youtube.com/@AISoftwareDevelopers)** channel. Contributions are welcome! If you'd like to contribute, please check out the contribution guidelines and submit a PR.

## Why PydanticAI?

PydanticAI is built on the following principles:

- **Strong Typing**: Ensures robust and reliable code through comprehensive type checking.
- **Ease of Use**: Uses plain Python for control flow and agent creation, eliminating the need for domain-specific languages.
- **Flexibility**: Supports multiple LLMs, including OpenAI, Anthropic, Gemini, Ollama, Google, and Mistral.
- **Advanced Features**:
  - Dependency injection for dynamic data and service provisioning.
  - Real-time streaming and validation of LLM outputs.
  - Tools reflection and self-correction for enhanced functionality.
- **Integration**: Seamlessly integrates with Pydantic’s existing logging and debugging tools.

---

## Key Features

1. **Multi-Model Support**: Easily switch between LLMs like OpenAI, Ollama, and Azure OpenAI.
2. **Python-Centric Design**: Leverages Python’s control flow and composition for agent creation.
3. **Dynamic Runtime Context**: Enables agents to exchange information and adapt to changing contexts.
4. **Simplified Agent Creation**: Build a basic agent in just five lines of code.

Example:

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel('gpt-4o-mini')
agent = Agent(model=model)

print(agent.run_sync("What is the capital of the United States?").data)
```

5. **Multi-Agent Workflows**: Coordinate multiple agents using different models, sharing message history and runtime contexts.

---

## Getting Started

### GitHub Modules

- [Part 1: The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](1-introduction/README.md)
- [Part 2: From Chaos to Clarity: LLM Tracing with Logfire and PydanticAI (Coding Tutorial)](2-logfire/README.md)

---

## Documentation

For comprehensive guides and reference documentation, visit the [PydanticAI Documentation](https://ai.pydantic.dev).

## Help and Support

If you encounter issues or have questions, feel free to open an issue in this repository, [ask a question on the Discord sever](https://discord.gg/eQXBaCvTA9) or refer to the [PydanticAI Documentation](https://ai.pydantic.dev).

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!
