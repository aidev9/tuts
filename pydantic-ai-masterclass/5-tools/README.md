# Build More Effective Agents with Function Tools in PydanticAI

## Overview

Welcome to the **[PydanticAI Masterclass](https://www.youtube.com/playlist?list=PL2yl5VopECya-fXbIKlGbkv8qgTFVsfwO)**! This series explores the core features of **PydanticAI**, a robust framework for building effective AI agents using simple Python code. In this tutorial, we’ll focus on **Function Tools** and their critical role in extending the functionality of AI agents when using LLMs. By the end of this session, you'll have the tools and confidence to craft agents tailored to your specific needs.

This repository serves as a companion to the PydanticAI Masterclass and its fifth video tutorial **[Build More Effective Agents with Function Tools in PydanticAI (Developer Coding Tutorial)](https://www.youtube.com/watch?v=4UN2emXnxN4)** which introduces the concept of function tools and provides several examples of to effectively use tools to extend the functionality of the LLMs.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/4UN2emXnxN4/0.jpg)](https://www.youtube.com/watch?v=4UN2emXnxN4)

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

## About PydanticAI

**PydanticAI** is a Python-based framework designed to simplify the development of AI agents. It builds upon the strengths of **Pydantic**—a data validation library—and extends its functionality to streamline the creation of intelligent systems. Key features include:

- **System Prompt Management**: Intuitive tools for defining static and dynamic prompts.
- **Seamless Integration**: Easily connect agents to APIs, databases, and external tools.
- **Customizability**: Fine-tune agent behavior to align with specific tasks and contexts.
- **Flexibility**: Support for multi-agent systems and dynamic workflows.

With **PydanticAI**, you can focus on crafting intelligent, task-oriented agents without getting bogged down by boilerplate code.

---

# PydanticAI: Building AI Agents with Python

## Table of Contents

1. [Introduction](#introduction)
2. [Core Concepts](#core-concepts)
   - [Static System Prompts](#static-system-prompts)
   - [Dynamic System Prompts](#dynamic-system-prompts)
   - [Tools and Context](#tools-and-context)
3. [Setup and Prerequisites](#setup-and-prerequisites)
4. [Getting Started](#getting-started)
   - [Hello, World!](#hello-world)
   - [Plain Tools Agent](#plain-tools-agent)
5. [Advanced Examples](#advanced-examples)
   - [Tools with Context](#tools-with-context)
   - [Passing Tools to Agents](#passing-tools-to-agents)
   - [Prepare Parameter Usage](#prepare-parameter-usage)
   - [Testing Tools with Function Models](#testing-tools-with-function-models)
6. [Conclusion](#conclusion)
7. [Resources](#resources)

---

## Introduction

Welcome to the developer documentation for PydanticAI, a powerful framework for creating AI agents in Python. This guide will provide a comprehensive overview of PydanticAI's features, including practical coding examples, to help you confidently build AI agents tailored to your needs.

---

## Core Concepts

### Static System Prompts

Static system prompts allow you to define fixed behaviors and contexts for your agents. These prompts are ideal for scenarios where the agent's behavior doesn't need to change dynamically.

### Dynamic System Prompts

Dynamic system prompts are more flexible, enabling runtime adjustments to an agent's behavior based on context or other inputs. This approach is particularly useful for complex workflows where adaptability is key.

### Tools and Context

Tools in PydanticAI act as helper functions to provide additional context or perform operations that are either impractical or impossible for an AI model to handle directly. Tools can:

- Inject critical information during runtime.
- Make agent behavior more deterministic.
- Retrieve external data or compute results.

---

## Setup and Prerequisites

Before diving into the examples, ensure you have the following:

- Python 3.8 or higher
- Installed libraries, including PydanticAI:
  ```bash
  pip install -r requirements.txt
  ```
- An OpenAI API key (for LLM-based examples) added to .env

---

## Getting Started

### Hello, World!

A simple example to introduce the basics of PydanticAI function tools

#### Code Example

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))

# Define the agent
agent = Agent(model=model, tools=[roll_die])
result = agent.run_sync('My guess is 4')
print(result.data)
```

#### Output Example

```
Your guess was 4. The die roll result is 5. Close, but not quite!
```

---

### Plain Tools Agent

Create agents with multiple tools for more functionality.

#### Code Example

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model)

# Tool to add two numbers
@agent.tool_plain
def add(a:int, b:int) -> int:
    """Adds two numbers"""
    print(Fore.CYAN, f"Calling tool add with params {a} and {b}...")
    return a + b

# Tool to determine if an integer is a prime number
@agent.tool_plain
def is_prime(a:int) -> bool:
    """Determines whether an integer is a prime number"""

    print(Fore.GREEN, f"Calling tool is_prime with param {a}...")
    if a <= 1:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True

result = agent.run_sync('17 + 74 is a prime number')
print(Fore.RED, result.data)
```

#### Output Example

```
The sum of 17 and 74 is 91, which is not a prime number.
```

---

## Advanced Examples

### Tools with Context

Tools can access context passed between agents, tools, and prompts.

#### Code Example

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class Capital(BaseModel):
    """"Capital city model - includes the name, year founded, short history of the city and a comparison to another city"""
    name: str
    year_founded: int
    short_history: str
    comparison: str

# Define the agent
agent = Agent(model=model, result_type=Capital, system_prompt="You are an experienced historian and you are asked a question about the capital of a country. You are expected to provide the name of the capital city, the year it was founded, and a short history of the city. Compare the the city to the  city provided by the comparison tool. Always call the comparison tool to get the comparison city.")

# Tool to get the comparison city
@agent.tool(retries=2)
def get_comparison_city(ctx: RunContext[str]) -> str:
    return f"The comparison city is {ctx.deps}"

# Run the agent
result = agent.run_sync("Capital of the US", deps="Paris")
```

#### Output Example

```
The capital of the US is Washington, D.C. It was founded in 1790. Compared to Paris, Washington, D.C. is newer but equally significant.
```

---

### Passing Tools to Agents

Pass tools explicitly to agents during runtime.

#### Code Example

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class CodeQuality(BaseModel):
    """Code Quality metrics"""
    cyclomatic_complexity: float
    percent_duplication: float
    review: str

# Tool get the source code
def get_source_code(ctx: RunContext[str]) -> str:
    """Get the source code"""
    return f"The source code is {ctx.deps}"

# Tool get the industry standards
def get_industry_standards() -> CodeQuality:
    """Get the industry standards for code quality"""
    return CodeQuality(cyclomatic_complexity=5.0, percent_duplication=10.0, review="These are the industry standards")

# Coding agent
coding_agent = Agent(model=model, system_prompt="You an experienced software developer. Write code accorting to the user's requirements. Return only the source code.")

# Code review agent
code_review_agent = Agent(model=model, tools=[Tool(get_source_code, takes_ctx=True), Tool(get_industry_standards, takes_ctx=False)], result_type=CodeQuality, system_prompt="You an experienced software architect and code reviewer. You are reviewing a codebase to ensure quality standards are met. You need to provide the code quality metrics for the codebase and a review of the codebase comparing it to the industry standards.")

# Run the agents
result = coding_agent.run_sync("Create a method in Python that calculates the 30-yr fixed mortgage rates and returns an amortization table.")
print(Fore.YELLOW, result.data)
```

---

### Prepare Parameter Usage

Use the `prepare` parameter to control tool execution.

#### Code Example

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class CodeQuality(BaseModel):
    """Code Quality metrics"""
    cyclomatic_complexity: float
    percent_duplication: float
    review: str

# Coding agent
coding_agent = Agent(model=model, system_prompt="You an experienced software developer. Write code accorting to the user's requirements. Return only the source code.")

# Code review agent
code_review_agent = Agent(model=model, result_type=CodeQuality, system_prompt="You an experienced software architect and code reviewer. You are reviewing a codebase to ensure quality standards are met. You need to provide the code quality metrics for the codebase and a review of the codebase comparing it to the industry standards.")

# Notifications agent
notifications_agent = Agent(model=model, system_prompt="You are a notification agent. You need to send a notification to the user based on the code quality metrics and the industry standards.")

# Tool get the source code
@coding_agent.tool
def get_source_code(ctx: RunContext[str]) -> str:
    """Get the source code"""
    return f"The source code is {ctx.deps}"

# Tool get the industry standards
@coding_agent.tool
def get_industry_standards() -> CodeQuality:
    """Get the industry standards for code quality"""
    return CodeQuality(cyclomatic_complexity=5.0, percent_duplication=10.0, review="These are the industry standards")

async def if_below_industry_standards(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps.cyclomatic_complexity > 2:
        return tool_def

# Tool to sent notifications
@notifications_agent.tool(prepare=if_below_industry_standards)
def send_notification(ctx: RunContext[CodeQuality]) -> str:
    """Send a notification"""
    print(Fore.YELLOW, f"Notification sent: {ctx.deps.review}")
    return f"Notification sent: {ctx.deps.review}"

# Run the agents
result = coding_agent.run_sync("Create a method in Python that calculates the 30-yr fixed mortgage rates and returns an amortization table.")
print(Fore.YELLOW, result.data)

result = code_review_agent.run_sync("Read the code and provide the code quality metrics.", deps=result.data)
print(Fore.CYAN, result.data)

result = notifications_agent.run_sync("Send a notification based on the code quality metrics and the industry standards.", deps=result.data)
print(Fore.RED, result.data)
```

---

### Testing Tools with Function Models

Use function models for testing tool functionality without an LLM.

#### Code Example

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

agent = Agent()

@agent.tool_plain
def code_quality(raw_code: str, cyclomatic_complexity: float, percent_duplication: float, review: str, notification_list: list[str]) -> str:
    """Code quality tool.

    Args:
        raw_code: raw code contents
        cyclomatic_complexity: how complex the code is
        percent_duplication: how much code is duplicated
        notification_list: list of emails to receive notifications
    """
    return f'{raw_code} {cyclomatic_complexity} {percent_duplication} {notification_list}'

def print_schema(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    tool = info.function_tools[0]
    print(Fore.CYAN, f"Tool name: {tool.name}")
    print(Fore.YELLOW, f"Tool description: {tool.description}")
    print(Fore.RED, f"Tool parameters: {tool.parameters_json_schema}")
    content = messages[-1].parts[0].content
    print(Fore.GREEN, f"Content: {content}")
    return ModelResponse.from_text(content=tool.description)

result = agent.run_sync('test run', model=FunctionModel(print_schema))
print(Fore.GREEN, result.data)
```

---

## Conclusion

PydanticAI simplifies the creation of AI agents with tools, context, and dynamic prompts. Its flexibility and Pythonic approach make it an excellent choice for developers exploring AI-powered workflows.

---

## Resources

- [PydanticAI GitHub Repository](https://github.com/pydantic/pydantic-ai)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Discord Community](https://discord.gg/eQXBaCvTA9)
- [Full Video Masterclass](https://www.youtube.com/playlist?list=PL2yl5VopECya-fXbIKlGbkv8qgTFVsfwO)

---

## Documentation

For questions or support, visit the [PydanticAI Documentation](https://ai.pydantic.dev).

## Help and Support

If you encounter issues or have questions, feel free to open an issue in this repository, [ask a question on the Discord sever](https://discord.gg/eQXBaCvTA9) or refer to the [PydanticAI Documentation](https://ai.pydantic.dev).

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!

## Summary

# PydanticAI Masterclass Tutorial: Building AI Agents with Python

## Overview

This tutorial provides a comprehensive introduction to PydanticAI, a powerful framework for building AI agents using Python. It covers the core features of PydanticAI and demonstrates how to create effective agents with simple Python code. By the end of this tutorial, you'll have the knowledge and confidence to build your own intelligent agents.

## Key Concepts

- **Tools**: Tools are crucial in PydanticAI. They provide models with additional information to enhance their responses. This is particularly beneficial when it's impractical to include all the necessary context in the system prompt or when you need to make agent behavior more deterministic.
- **Agent.tool Decorator**: PydanticAI offers various ways to register function tools within agents, including using decorators like `@agent.tool`. This decorator allows you to easily define and integrate tools into your agent workflows.
- **"Prepare" Parameter**: This unique parameter gives developers fine-grained control over when and if a specific tool is used in an agent flow. This level of control enhances the flexibility and reliability of your agents.
- **Testing with Function Model**: PydanticAI allows you to use a "function model" instead of a full language model (LLM) for testing purposes. This enables you to verify the functionality of your tools and ensure they are called with the correct parameters.

## Tutorial Structure

The tutorial presents six practical examples that progressively increase in complexity:

1. **Hello World**: This introductory example demonstrates the basic structure of a PydanticAI agent and the use of a simple tool.
2. **Plain Tools Agent**: This example introduces the concept of "plain tools" and how to define and use multiple tools within an agent without relying on context.
3. **Tools with Context**: This example explores how to pass context among agents, tools, and other components, allowing tools to access and utilize relevant information from the workflow.
4. **Passing Tools as Keywords**: This example demonstrates how to pass tools to agents using the "tools" keyword, offering flexibility in tool registration and usage.
5. **Using the "Prepare" Parameter**: This example highlights the power of the "prepare" parameter, allowing developers to define conditions for when a tool should be executed.
6. **Tools in Testing**: This example utilizes the "function model" and the Griff library to test the functionality of tools and ensure they are called correctly during development.

## Key Differentiators

Here are some key differentiators of PydanticAI compared to other agent frameworks:

- **Fine-grained control over tool execution with the "prepare" parameter:** This allows developers to define specific conditions for when a tool should be used, giving them more control over the agent's workflow compared to frameworks where agents autonomously decide tool usage.
- **Emphasis on "plain Python" functions for tool implementation:** This simplifies tool creation and integration, as developers can leverage existing Python code and libraries without needing to learn framework-specific methods.
- **Seamless integration of tools with context passing:** PydanticAI allows for smooth information flow between agents, tools, and other components, ensuring tools have access to relevant context for improved decision-making.
- **Focus on testability:** PydanticAI provides features like the "function model" and integration with libraries like Griffe to facilitate test-driven development, enabling thorough testing of tool functionality and agent behavior.

## Conclusion

This tutorial provides a hands-on learning experience for developers interested in building AI agents with Python using the PydanticAI framework.
