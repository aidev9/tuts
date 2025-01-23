# Building Reliable AI Agents with PydanticAI: Result Validator Functions

## Overview

Welcome to the **[PydanticAI Masterclass](https://www.youtube.com/playlist?list=PL2yl5VopECya-fXbIKlGbkv8qgTFVsfwO)**! This series explores the core features of **PydanticAI**, a robust framework for building effective AI agents using simple Python code. In this tutorial, we’ll focus on **Result Validator Functions** and their critical role in increasing the reliability of AI agents. By the end of this session, you'll have the tools and confidence to craft agents tailored to your specific needs.

This repository serves as a companion to the PydanticAI Masterclass and its sixth video tutorial **[Transform You Agents with Result Validator Functions (10X More Reliable Outputs)](https://www.youtube.com/watch?v=2B5uDly91gY)** which introduces the concept of function tools and provides several examples of to effectively use tools to extend the functionality of the LLMs.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/2B5uDly91gY/0.jpg)](https://www.youtube.com/watch?v=2B5uDly91gY)

## Masterclass Modules

- [Part 1: The Best Agent Framework Has Arrived (Coding Tutorial for PydanticAI w/ OpenAI, Ollama, AzureOpenAI)](https://www.youtube.com/watch?v=xVe87QpNE80)
- [Part 2: From Chaos to Clarity: LLM Tracing with Logfire and PydanticAI (Coding Tutorial)](https://www.youtube.com/watch?v=TTNT3rnuZp0)
- [Part 3: 100% Reliable LLM Outputs with Structured Data Outputs (Developer Tutorial)](https://www.youtube.com/watch?v=PXO9_nWZYrc)
- [Part 4: Mastering System Prompts in PydanticAI: The Ultimate Guide (Developer Coding Tutorial)](https://www.youtube.com/watch?v=WQqsiB0xUXk)
- [Part 5: Build More Effective Agents with Function Tools in PydanticAI (Developer Tutorial)](https://www.youtube.com/watch?v=4UN2emXnxN4)
- [Part 6: Transform You Agents with Result Validator Functions (10X More Reliable Outputs)](https://www.youtube.com/watch?v=2B5uDly91gY)
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

## **📌 Overview**

This tutorial demonstrates:

1. **Result Validators**: Post-LLM validation to ensure high-quality outputs.
2. **System Prompts**: Guide the AI’s behavior for domain-specific tasks.
3. **Tools**: Custom tools for runtime context and dependencies.
4. **Retry Mechanisms**: Automatically retry invalid outputs for robust workflows.

By the end, you’ll be confident in designing AI agents that produce structured and validated responses.

---

## **🛠 Prerequisites**

1. **Python 3.8+**
2. Install required dependencies:
   ```bash
   pip install pydantic-ai logfire dotenv colorama
   ```
3. **Set up your API key**:  
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

---

## **💡 Key Features of This Example**

- **Agent Type**: Historian AI Agent
- **Task**: Provides information about a capital city, including:
  - Name
  - Year founded
  - Short history
  - Age comparison with another city
- **Validation**: Ensures the year founded is within acceptable bounds.

---

## **🔍 Code Breakdown**

### **1. Setting Up the Model and Agent**

Define an AI model and the agent responsible for generating outputs:

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

# Define the output model
class Capital(BaseModel):
    name: str
    year_founded: int
    short_history: str
    comparison: str

# Initialize the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(
    model=model,
    result_type=Capital,
    system_prompt=(
        "You are an experienced historian. Provide the capital city's name, "
        "year it was founded, a short history, and a comparison with another city."
    )
)
```

### **2. Adding Tools**

Define tools to inject runtime dependencies dynamically:

```python
@agent.tool
def get_comparison_city(ctx: RunContext[str]) -> str:
    return f"The comparison city is {ctx.deps}"
```

### **3. Validating Outputs**

Add a result validator to ensure outputs meet requirements:

```python
from pydantic_ai import ModelRetry

@agent.result_validator
def validate_result(ctx: RunContext[str], result: Capital) -> Capital:
    if result.year_founded > 1000:
        print(f"Validation failed: Year founded {result.year_founded} is too high.")
        raise ModelRetry("Year founded is too high. Try another country.")
    return result
```

### **4. Running the Agent**

Run the agent synchronously and handle retries or exceptions:

```python
try:
    result = agent.run_sync("What is the capital of the US?", deps="Toronto")
    print("Capital Name:", result.data.name)
    print("Year Founded:", result.data.year_founded)
    print("Short History:", result.data.short_history)
except ModelRetry as e:
    print("Retry Reason:", e)
except Exception as e:
    print("Error:", e)
```

---

## **🧑‍💻 Example Output**

Input Prompt:

```plaintext
What is the capital of the US?
```

Expected Output:

```plaintext
Capital Name: Washington, D.C.
Year Founded: 1790
Short History: Founded as the nation's capital in 1790, it has served as the center of American politics.
Comparison: The comparison city is Toronto. Washington, D.C., is much younger than Toronto.
```

If the year founded exceeds the threshold (e.g., 1000), the validator triggers a retry.

---

## **🌟 Advanced Usage**

- **Retry Mechanisms**: Automatically re-prompt the AI for corrections.
- **Dynamic Tools**: Use additional APIs or databases for enhanced validations.
- **Streaming**: Process large outputs incrementally with PydanticAI’s streaming capabilities.

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
