# Mastering System Prompts in PydanticAI: The Ultimate Guide (Developer Coding Tutorial)

## Overview

Welcome to the **[PydanticAI Masterclass](https://www.youtube.com/playlist?list=PL2yl5VopECya-fXbIKlGbkv8qgTFVsfwO)**! This series explores the core features of **PydanticAI**, a robust framework for building effective AI agents using simple Python code. In this tutorial, we’ll focus on **System Prompts** and their critical role in shaping the behavior, personality, and scope of AI agents. By the end of this session, you'll have the tools and confidence to craft agents tailored to your specific needs.

This repository serves as a companion to the PydanticAI Masterclass and its fourth video tutorial **[Mastering System Prompts in PydanticAI: The Ultimate Guide (Developer Coding Tutorial)](https://www.youtube.com/watch?v=WQqsiB0xUXk)** which introduces the `result_type` parameter through practical examples.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/WQqsiB0xUXk/0.jpg)](https://www.youtube.com/watch?v=WQqsiB0xUXk)

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

## Table of Contents

1. [About PydanticAI](#about-pydanticai)
2. [What Are System Prompts?](#what-are-system-prompts)
   - [Static System Prompts](#static-system-prompts)
   - [Dynamic System Prompts](#dynamic-system-prompts)
3. [Why Are System Prompts Important?](#why-are-system-prompts-important)
4. [Coding Examples](#coding-examples)
   - [Hello, World!](#hello-world)
   - [Simple Coder Agent](#simple-coder-agent)
   - [Advanced Coder Agent](#advanced-coder-agent)
   - [Invoice-Writing Agent](#invoice-writing-agent)
   - [Basic Dynamic Prompt](#basic-dynamic-prompt)
   - [Advanced Dynamic Prompt](#advanced-dynamic-prompt)
   - [Bonus: Hello, World Improved!](#bonus-hello-world-improved)
5. [Summary](#summary)
6. [Resources](#resources)
7. [What's Next?](#whats-next)
8. [Stay Connected](#stay-connected)

---

## About PydanticAI

**PydanticAI** is a Python-based framework designed to simplify the development of AI agents. It builds upon the strengths of **Pydantic**—a data validation library—and extends its functionality to streamline the creation of intelligent systems. Key features include:

- **System Prompt Management**: Intuitive tools for defining static and dynamic prompts.
- **Seamless Integration**: Easily connect agents to APIs, databases, and external tools.
- **Customizability**: Fine-tune agent behavior to align with specific tasks and contexts.
- **Flexibility**: Support for multi-agent systems and dynamic workflows.

With **PydanticAI**, you can focus on crafting intelligent, task-oriented agents without getting bogged down by boilerplate code.

---

## What Are System Prompts?

System prompts are the **blueprint** or **initial instructions** for an AI agent. They define the agent's personality, behavior, and scope, ensuring that it operates within the intended context. In **PydanticAI**, there are two types of system prompts:

### Static System Prompts

Static system prompts are predefined and remain constant throughout the agent's operation. They are:

- **Known beforehand** and set at initialization.
- Passed as a parameter (`system_prompt`) in the Agent constructor.

Example:

```python
from pydantic_ai import Agent

agent = Agent(
    system_prompt="You are a helpful assistant specialized in resume writing."
)
```

### Dynamic System Prompts

Dynamic system prompts are context-sensitive and generated at runtime based on the agent's environment or user input. They are defined using functions decorated with `@agent.system_prompt`.

Example:

```python
from pydantic_ai import Agent

agent = Agent()

@agent.system_prompt
def dynamic_prompt(context):
    return f"You are solving the task: {context['task_name']}"
```

An agent can combine both static and dynamic prompts. At runtime, these prompts are appended in the order they are defined, creating a comprehensive instruction set for the agent.

---

## Why Are System Prompts Important?

System prompts are often overlooked but are **critical** to an agent's success. Here's why:

1. **Define Agent Personality**: A well-crafted system prompt determines the tone and style of an agent's responses.
2. **Set Behavioral Boundaries**: Prompts can limit or expand what an agent can do, ensuring it stays on task.
3. **Improve Output Quality**: The prompt provides context that enhances the relevance and accuracy of the agent's responses.
4. **Enable Task-Specific Customization**: Dynamic prompts allow the agent to adapt to changing requirements and runtime context.

Even though system prompts are just strings (or sequences of strings concatenated), their design can make or break an agent's functionality.

---

## Coding Examples

In this masterclass, we’ll work through six examples to demonstrate the use of system prompts:

### Hello, World!

Start with a simple example to familiarize yourself with agent creation and basic system prompts.

```python
# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model, system_prompt="You are an experienced business coach and startup mentor specializing in guiding technology startups from ideation to achieving sustained growth and profitability. When asked about a startup strategy, you provide comprehensive advice on the following key areas. Include all points from the list below in your response, with detailed instructions and actionable insights:")

# Run the agent
result = agent.run_sync(user_prompt="Create a strategy for a SaaS startup that is building a social media platform for pet owners.")
```

### Simple Coder Agent

Introduce a system prompt to guide the agent in writing basic Python code.

```python
system_prompt = "You an experienced React developer. Create code that meets user's requirements."

# Define the agent
agent = Agent(model=model, system_prompt=system_prompt)

# Run the agent
result = agent.run_sync(user_prompt="Create a functional React component that displays a user profile with the following details: name, email, and profile picture. Must use Zustand for state management and TailwindCSS for styling.")
```

### Advanced Coder Agent

Enhance the previous agent with a detailed system prompt to handle more complex tasks.

```python
system_prompt = """You are an experienced React developer tasked with creating reusable, scalable, and high-performance components. Your primary goal is to ensure that each component adheres to the latest best practices in React development.

Please follow these guidelines when developing each component:

1. **Component Naming:** Use descriptive names for your components (e.g., `UserProfile`, `ProjectList`) that clearly indicate their purpose.
2. **Props Management:**
   - Define props with appropriate types using TypeScript or PropTypes to ensure type safety and clarity.
   - Pass only necessary props down from parent components to avoid unnecessary re-renders.
3. **State Management:** Use React's built-in state management (e.g., `useState`) for local component states, and consider context APIs or Redux for global state if needed.
4. **Lifecycle Methods:**
   - Utilize functional components with hooks (`useEffect`, `useContext`, etc.) instead of class-based components to take advantage of modern React features.
5. **Performance Optimization:**
   - Implement memoization techniques (e.g., `React.memo`) for pure components that don't need re-renders on prop changes.
   - Use virtual lists or pagination for large datasets to improve rendering performance.
6. **Styling:** Apply consistent styling using CSS-in-JS solutions like styled-components, emotion, or classnames. Avoid inline styles unless absolutely necessary.
7. **Accessibility:**
   - Ensure that components are accessible by following WCAG guidelines and using appropriate ARIA attributes where needed.
8. **Documentation:**
   - Create clear and concise documentation for each component, including usage examples, props descriptions, and any other relevant information.
   - Create a style guide or component library to maintain consistency across the application.
   - Create a README file for each component with installation instructions, usage guidelines, and other relevant details.
9. **Testing:** Write unit tests for your components using testing frameworks like Jest or React Testing Library to ensure they function correctly under various scenarios.
10. **Code Organization:**
    - Keep related files organized in a consistent directory structure (e.g., `components/`, `hooks/`).
    - Use meaningful folder names and subfolders if necessary to maintain clarity.
11.   **Error Handling:**
    - Implement error boundaries to catch and handle errors within your components gracefully.
12. **Logging:**
    - Use appropriate logging mechanisms (e.g., `console.log`, `sentry`) to track component behavior and debug issues effectively.
13.   **Performance Monitoring:**
    - Integrate performance monitoring tools (e.g., React Profiler, Lighthouse) to identify and address performance bottlenecks in your components.
14. **Security:**
    - Sanitize user inputs and avoid direct DOM manipulation to prevent security vulnerabilities like XSS attacks.
15. **Code Comments:**
    - Add comments to explain complex logic, algorithms, or workarounds in your components for better code readability.

**Additional Notes:**
- Ensure that all components are modular, allowing for easy reuse across different parts of the application.
- Maintain clean code with proper indentation, spacing, and comments where appropriate.
- Follow best practices in error handling and logging within your components.

Return the component code, styled with TailwindCSS, that meets the requirements outlined above. You can use Zustand for state management in your components. Return the Zustand store code. Return the README file for the component with installation instructions, usage guidelines, and other relevant details."""

# Define the agent
agent = Agent(model=model, system_prompt=system_prompt)

# Run the agent
result = agent.run_sync(user_prompt="Create a functional React component that displays a user profile with the following details: name, email, and profile picture. Must use Zustand for state management and TailwindCSS for styling.")
```

### Invoice-Writing Agent

Learn how to inject variables into static prompts for tailored outputs, such as generating invoices.

### Basic Dynamic Prompt

Explore dynamic system prompts and how they adjust based on runtime context.

### Advanced Dynamic Prompt

Dive deeper into dynamic prompts with complex examples that require intricate logic.

### Bonus: Hello, World Improved!

A twist on the classic "Hello, World!" example that showcases agents generating their own dynamic system prompts at runtime.

---

## Summary

- **System Prompts Matter**: They are the foundation of effective AI agents.
- **Static vs. Dynamic Prompts**: Use both to achieve the best results.
- **Practice Makes Perfect**: The examples provided will help you master prompt crafting and improve agent outcomes.

---

## Documentation

For questions or support, visit the [PydanticAI Documentation](https://ai.pydantic.dev).

## Help and Support

If you encounter issues or have questions, feel free to open an issue in this repository, [ask a question on the Discord sever](https://discord.gg/eQXBaCvTA9) or refer to the [PydanticAI Documentation](https://ai.pydantic.dev).

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!

## PydanticAI Masterclass: Structured Outputs for Reliable AI Applications

This is a summary from a YouTube tutorial on how to use **PydanticAI** to build AI agents. The video focuses on **creating custom system prompts**, which are instructions that shape the personality and behavior of an AI agent.

### Types of System Prompts

There are two types of system prompts:

- **Static Prompts:** Defined when the agent is created using the `system_prompt` parameter of the `Agent` constructor.
- **Dynamic Prompts:** Change depending on the situation and are defined using functions decorated with `@agent.system_prompt`.

An agent can use both static and dynamic prompts, which are appended in the order they are defined at runtime.

### Importance of System Prompts

System prompts are critical because they act as a blueprint for the AI agent, defining its **personality, behavior, and scope**. While they appear as simple strings, crafting effective prompts is crucial for achieving desired results.

The tutorial covers six examples:

- Hello, World!
- Simple Coder Agent
- Advanced Coder Agent
- Invoice-Writing Agent
- Basic Dynamic Prompt
- Advanced Dynamic Prompt

These examples start with basic concepts and progress to more complex agents, showcasing the importance of detailed prompts and the effective use of static and dynamic prompts. There's also a bonus "Hello, World Improved!" example included in the tutorial.

### Key Takeaways

The tutorial emphasizes that **well-written system prompts significantly impact the outputs of AI agents**. **Combining static and dynamic prompts** allows for more effective and nuanced agent behavior.

### Looking Ahead

The next video in the series will explore the use of **tools to extend the functionality of AI agents**, enabling them to perform more complex tasks.
