# Logfire: Observability Made Easy for AI Agents

## Overview

Logfire is a powerful observability platform built on OpenTelemetry, designed to provide seamless monitoring and debugging for modern applications, including AI agents built using PydanticAI. Developed by the creators of Pydantic, Logfire offers unparalleled support for tracing and debugging, ensuring reliability even when working with the unpredictability of Large Language Models (LLMs).

This repository serves as a companion to the PydanticAI Masterclass and it's second video tutorial **[From Chaos to Clarity: LLM Tracing with Logfire and PydanticAI (Coding Tutorial)](<(https://www.youtube.com/watch?v=TTNT3rnuZp0)>)** which introduces the Logfire toolset and demonstrates key features through practical examples.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/TTNT3rnuZp0/0.jpg)](https://www.youtube.com/watch?v=TTNT3rnuZp0)

## Masterclass Modules

- [Part 1: The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](<(https://www.youtube.com/watch?v=xVe87QpNE80)>)
- [Part 2: From Chaos to Clarity: LLM Tracing with Logfire and PydanticAI (Coding Tutorial)](<(https://www.youtube.com/watch?v=TTNT3rnuZp0)>)

## Looking for Collaborators

Have a burning idea for an article, video tutorial, a learning project or anything related to AI? Consider collaborating with our growing community of collaborators. Get started today by [posting your idea on our Discord sever](https://discord.gg/eQXBaCvTA9). Together, we are building a strong community of AI Software Developers.

## How to Contribute to This Repository

This repository is maintained by the team at **[AI Software Developers](https://www.youtube.com/@AISoftwareDevelopers)** channel. Contributions are welcome! If you'd like to contribute, please check out the contribution guidelines and submit a PR.

## Why Use Logfire?

Building and maintaining AI agents can be challenging, especially when dealing with the unpredictability of LLMs. Logfire provides:

- A robust tracing system for better debugging.
- Insightful metrics to monitor and improve agent reliability.
- Structured data support for effective troubleshooting.

---

## Key Features

- **Cross-Language Support**: Monitor applications across various programming languages, not just Python or PydanticAI.
- **Structured Input/Output**: Leverage structured data for efficient observability and debugging.
- **Seamless Integration**: Built with Python in mind, supporting Python-based projects effortlessly.
- **Log Levels**: Fine-grained control over logging levels for better insights.
- **OpenTelemetry**: Supports open standards for tracing and observability.
- **SQL Querying**: Query logs using SQL for advanced filtering and analysis.
- **Method Instrumentation**: Easily track method-level performance and arguments.

## Examples

### 1. Hello, World!

Send a simple "info" statement to Logfire:

```python
import logfire

# Configure logfire
logfire.configure()

# Send a log
logfire.info('Hello, {name}!', name='world')
```

### 2. Using Spans

Organize logs by context using spans:

```python
import os
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model)

# Run the agent
with logfire.span('Calling OpenAI gpt-4o-mini') as span:
    result = agent.run_sync("What is the capital of the US?")
    span.set_attribute('result', result.data)
    logfire.info('{result=}', result=result.data)
```

### 3. Log Levels

Demonstrate various log levels:

```python
with logfire.span('Calling OpenAI gpt-4o-mini') as span:
    result = agent.run_sync("What is the capital of the US?")
    logfire.notice('{result=}', result=result.data)
    logfire.info('{result=}', result=result.data)
    logfire.debug('{result=}', result=result.data)
    logfire.warn('{result=}', result=result.data)
    logfire.error('{result=}', result=result.data)
    logfire.fatal('{result=}', result=result.data)
```

### 4. Logging Exceptions

Handle exceptions gracefully and log them:

```python
try:
    raise ValueError("Example exception")
except ValueError as e:
    error(f"Exception occurred: {e}")
```

### 5. Method Instrumentation

Instrument methods to log their inputs and outputs:

```python
from logfire import instrument

@instrument
def multiply(a, b):
    return a * b

print(multiply(5, 10))
```

---

## Getting Started

Follow these steps to set up Logfire for your project:

1. **Create a Developer Account**: Sign up at [Logfire](https://logfire.pydantic.dev).
2. **Install the SDK**: Run the following command to install Logfire:
   ```bash
   pip install logfire
   ```
3. **Authenticate**: Use the `logfire auth` command to authenticate. This will create a `.toml` file under your user directory.
   ```bash
   logfire auth
   ```
4. **Set Up a Project**: Configure your project using the command:
   ```bash
   logfire project use [project-name]
   ```

---

## Documentation

For questions or support, visit the [Logfire Documentation](https://logfire.pydantic.dev/docs).

## Help and Support

If you encounter issues or have questions, feel free to open an issue in this repository, [ask a question on the Discord sever](https://discord.gg/eQXBaCvTA9) or refer to the [Logfire Documentation](https://logfire.pydantic.dev/docs).

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!

## Video Summary

### Logfire: Observability Made Easy for AI Agents

Logfire is a powerful observability platform built on OpenTelemetry, designed to provide seamless monitoring and debugging for modern applications, including AI agents built using PydanticAI. Developed by the creators of Pydantic, Logfire offers unparalleled support for tracing and debugging, ensuring reliability even when working with the unpredictability of Large Language Models (LLMs).

The video is a Masterllass on PydanticAI, a new framework for building AI agents. This installment focuses on Logfire, an observability platform built on OpenTelemetry by the same team that created Pydantic. Logfire supports monitoring any application, not just Python or Pydantic AI. It is important to have a solid tracing and debugging system like Logfire when building agents because LLMs are notoriously unreliable.

**The video then provides a step-by-step guide on setting up Logfire for development:**

- Create a developer account at logfire.pydantic.dev.
- Install the SDK with the command "pip install logfire".
- Authenticate with "logfire auth". This creates a tomel file under the user.
- Set up a project with "logfire project use \[project name]".

**The video demonstrates various Logfire features through coding examples, including:**

- **Hello, World!**: This simple example sends an "info" statement to Logfire. It involves importing Logfire, calling "logfire.doc.configure", and sending data with "logfire.info".
- **Span**: This feature organizes logs by context. The example creates a span using "logfire.span", runs the agent within the span, and logs the result.
- **Log Levels**: The example demonstrates different log levels, including notice, info, debug, warning, error, and fatal. Each level uses different coloring for easy identification in the terminal and Logfire's dashboard.
- **Exceptions**: This example showcases how to log exceptions, which are common when working with LLMs. It involves using a try-catch block to run the LLM call and raise an error. The video highlights how to use SQL queries in Logfire to filter exceptions.
- **Instrumenting**: This feature instruments methods by placing "@logfire.instrument" before the method definition. The example instruments a simple multiplication method and logs its arguments and result.

The video concludes by summarizing the key features of Logfire, including its simplicity, Python integration, structured input/output capabilities, support for OpenTelemetry and structured data, and SQL query capabilities.
