# PydanticAI: The Best Agent Framework Has Arrived

## Overview

Welcome to the **[PydanticAI Masterclass](https://www.youtube.com/playlist?list=PL2yl5VopECya-fXbIKlGbkv8qgTFVsfwO)**! This series explores the core features of **PydanticAI**, a robust framework for building effective AI agents using simple Python code. In this tutorial, we’ll focus on **how to create simple agents** through multiple examples with a variety of LLMs. By the end of this session, you'll have the tools and confidence to craft agents tailored to your specific needs.

PydanticAI is a Python framework designed to simplify the process of creating robust and efficient AI agents. Developed by the team behind the popular Pydantic library, it offers powerful tools for building production-ready agent systems while leveraging Python's core strengths.

This repository serves as a companion to the PydanticAI Masterclass and its first video tutorial **[The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](https://www.youtube.com/watch?v=xVe87QpNE80)** which introduces the framework and demonstrates its key features through practical coding examples.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/xVe87QpNE80/0.jpg)](https://www.youtube.com/watch?v=xVe87QpNE80)

## Masterclass Modules

- [Part 1: The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](https://www.youtube.com/watch?v=xVe87QpNE80)
- [Part 2: From Chaos to Clarity: LLM Tracing with Logfire and PydanticAI (Coding Tutorial)](https://www.youtube.com/watch?v=TTNT3rnuZp0)
- [Part 3: 100% Reliable LLM Outputs with Structured Data Outputs (Developer Tutorial)](https://www.youtube.com/watch?v=PXO9_nWZYrc)
- [Part 4: Mastering System Prompts in PydanticAI: The Ultimate Guide (Developer Coding Tutorial)](https://www.youtube.com/watch?v=WQqsiB0xUXk)
- [Part 5: Build More Effective Agents with Function Tools in PydanticAI (Developer Tutorial)](https://www.youtube.com/watch?v=4UN2emXnxN4)
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

## Stay In Touch

Stay ahead in the fast-paced world of AI by subscribing to our newsletter, **[Code the Revolution](https://aidev9.substack.com/)**! From cutting-edge tutorials to breaking industry news, we bring you the insights and tools you need to stay informed and inspired. Whether you're a developer, entrepreneur, or AI enthusiast, our newsletter ensures you're always in the loop. Don’t miss out—join a community that's shaping the future of AI. **[Subscribe now and revolutionize the way you code!](https://aidev9.substack.com/)**

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

agent = Agent(model="gpt-4")
response = agent.run("Hello, World!")
print(response)
```

5. **Multi-Agent Workflows**: Coordinate multiple agents using different models, sharing message history and runtime contexts.

---

## Getting Started

### Installation

To get started, clone the repository and install the dependencies:

```bash
git clone https://github.com/aidev9/tuts.git
cd pydantic-ai-masterclass/1-introduction
pip install -r requirements.txt
```

### Running Your First Agent

1. Create a Python file (e.g., `1.1-hello-world.py`).
2. Copy the example code above
3. Run the script:

```bash
python 1.1-hello-world.py
```

---

## Documentation

For comprehensive guides and reference documentation, visit the [PydanticAI Documentation](https://ai.pydantic.dev).

## Help and Support

If you encounter issues or have questions, feel free to open an issue in this repository, [ask a question on the Discord sever](https://discord.gg/eQXBaCvTA9) or refer to the [PydanticAI Documentation](https://ai.pydantic.dev).

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!

## Video Summary

### PydanticAI: A New Framework for Building AI Agents

This summarizes the key takeaways from the video tutorial "The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)." The tutorial introduces PydanticAI, a Python framework for building AI agents, showcasing its core features and providing practical coding examples.

**Key Themes and Ideas:**

- PydanticAI's origins and goals: PydanticAI builds upon the success of Pydantic, a popular Python library for data validation and parsing, aiming to simplify the process of creating AI agents.
- Framework Features: PydanticAI offers several compelling features:
  - Built by the same team behind Pydantic, ensuring strong typing and validation capabilities.
  - Support for multiple models, including OpenAI, Anthropic, Gemini, Ollama, Google, and Mistral.
  - Seamless integration with Pydantic's logging and debugging tools.
  - Python-centric design, leveraging Python's control flow and composition for agent creation.
  - Comprehensive type checking for robust and reliable code.
  - Powerful dependency injection system for flexible data and service provisioning.
  - Ability to stream and validate LLM outputs in real-time.
  - Support for tools reflection and self-correction.
- Agent workflow: The tutorial describes the core elements of a PydanticAI agent:
  - The agent, represented as a Python object.
  - Calls to various LLMs (Large Language Models).
  - Tools for contextual enhancement.
  - Static and dynamic system prompts.
  - Runtime dependencies for dynamic context injection.

**Important Facts and Examples:**

- Five lines of code for a basic agent: The tutorial demonstrates creating a simple "Hello World" agent using OpenAI's GPT-4 in just five lines of code.
- Support for multiple models: Examples illustrate using OpenAI, Ollama, and Azure OpenAI models, showcasing the framework's flexibility and ability to adapt to different environments.
- Multi-agent flows: The tutorial culminates with an example showcasing two agents, one using OpenAI and another using Ollama, communicating and sharing message history. This demonstrates the potential for building complex agent systems with diverse capabilities.

**Quotes from the Source:**

- Pydantic AI is a new AI agent framework from the same team that brought us Pydantic. It supports many of the features of modern agent frameworks and it aims to simplify the agent creation process.
- Pydantic AI uses plain Python to control the flow of agent data. There's no need for domain specific code or extra classes.
- It is designed to make type checking as useful as possible so it integrates well with static type Checkers like mypy and pyright.
- You can create multiple agents where each agent can operate with its own model exchanging information through message history and a dynamic runtime context.

**Conclusion:**
PydanticAI presents a promising framework for developing robust and efficient AI agents. Its focus on Python, comprehensive typing, and support for various LLMs make it an attractive choice for developers looking to build production-ready agent systems. The tutorial provides a clear and concise introduction to the framework, demonstrating its ease of use and powerful capabilities.
