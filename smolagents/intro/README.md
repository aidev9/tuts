# smolagents: Tiny Agents, Huge Power!

## Overview

Welcome to the official guide for following along with the **smolagents** video tutorial! This document will help you get started with smolagents, understand key concepts, and run the provided examples. Let’s build lightweight, efficient AI agents together! 🚀

This repository serves as a companion to the PydanticAI Masterclass and its fifth video tutorial **[Too Smol to Be Good? Absolutely Not! Build Your First Agent in 3 Lines of Code](https://www.youtube.com/watch?v=zPlPiGiiI14)** which introduces the concept of function tools and provides several examples of to effectively use tools to extend the functionality of the LLMs.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/zPlPiGiiI14/0.jpg)](https://www.youtube.com/watch?v=zPlPiGiiI14)

## Stay In Touch

Stay ahead in the fast-paced world of AI by subscribing to our newsletter, **[Code the Revolution](https://aidev9.substack.com/)**! From cutting-edge tutorials to breaking industry news, we bring you the insights and tools you need to stay informed and inspired. Whether you're a developer, entrepreneur, or AI enthusiast, our newsletter ensures you're always in the loop. Don’t miss out—join a community that's shaping the future of AI. **[Subscribe now and revolutionize the way you code!](https://aidev9.substack.com/)**

## Looking for Collaborators

Have an idea for an article, video tutorial, a learning project or anything related to AI? Consider collaborating with our growing community of collaborators. Get started today by [posting your idea on our Discord sever](https://discord.gg/eQXBaCvTA9). Together, we are building a strong community of AI Software Developers.

## How to Contribute to This Repository

This repository is maintained by the team at **[AI Software Developers](https://www.youtube.com/@AISoftwareDevelopers)** channel. Contributions are welcome! If you'd like to contribute, please check out the contribution guidelines and submit a PR.

## **What Are smolagents?**

**smolagents** is a lightweight Python library by Hugging Face for building powerful AI agents. With a focus on simplicity and performance, smolagents empowers developers to create agents using minimal code while leveraging the power of open-source and proprietary large language models (LLMs).

Key features include:

- 🌟 Code Agents: Treats code actions as first-class citizens.
- ⚡ Multi-model support: Compatible with OpenAI, Anthropic, and open-source models.
- 🛠️ Integrations: Seamless use of Hugging Face Hub models.
- 📦 Lightweight and easy to use.

---

## **Getting Started**

### **1. Installation**

```bash
pip install smolagents
```

### **2. Import and Setup**

Here’s a minimal example to get you started with smolagents:

```python
from smolagents import LiteLLMModel, CodeAgent

# Define a simple LLM model
model = LiteLLMModel(model="gpt-4-mini")

# Create a Code Agent with guidance
agent = CodeAgent(
    model=model,
    instructions="You are a helpful assistant. Follow the user's input carefully."
)

# Run your first prompt
response = agent.run("Write a Python function to calculate factorial.")
print(response)
```

---

## **Hello, World! Example**

In the tutorial, we walk you through building your first **smolagent** with a practical “Hello, World” example:

```python
from smolagents import LiteLLMModel, CodeAgent

# Initialize the LiteLLMModel
model = LiteLLMModel(model="gpt-4-mini")

# Define the agent
agent = CodeAgent(
    model=model,
    instructions="You are a friendly agent. Respond concisely."
)

# Interact with the agent
output = agent.run("Hello, World!")
print("Agent response:", output)
```

This example demonstrates how to create an agent and use it to process simple prompts.

---

## **Building Multi-Step Agents**

For more complex workflows, smolagents can handle multi-step reasoning and decision-making. Here’s an example:

```python
from smolagents import LiteLLMModel, CodeAgent

# Initialize the model
model = LiteLLMModel(model="gpt-4-mini")

# Create a multi-step agent
agent = CodeAgent(
    model=model,
    instructions="You are an agent that solves math problems step by step."
)

# Multi-step interaction
problem = "Calculate the sum of the squares of the first 5 integers."
steps = agent.run(problem, multi_step=True)
for step in steps:
    print("Step:", step)
```

---

## **Using Open-Source Models**

smolagents also supports open-source models hosted on the Hugging Face Hub:

```python
from smolagents import HFModel, CodeAgent

# Use an open-source model
model = HFModel(model="google/flan-t5-small")

# Create the agent
agent = CodeAgent(
    model=model,
    instructions="Summarize the following text."
)

# Test with input text
text = "Large language models are changing the way we interact with AI."
summary = agent.run(text)
print("Summary:", summary)
```

---

## **Best Practices for Using smolagents**

- Use **Code Agents** for workflows involving code generation, debugging, or code review.
- Leverage **multi-step interactions** for complex problem-solving.
- Experiment with **different models** to find the best fit for your task.
- Use **Hugging Face Hub integrations** for seamless access to open-source models.

---

## **Additional Resources**

- 📖 **Documentation**: [smolagents Docs](https://huggingface.co/docs/smolagents)
- 🎥 **Video Tutorial**: [Watch the Tutorial](https://youtu.be/zPlPiGiiI14)
- 💬 **Community**: [Join the Discord](https://discord.gg/eQXBaCvTA9)

---

## **Next Steps**

1. Install smolagents and try the examples provided in this README.
2. Follow the video tutorial for a step-by-step walkthrough.
3. Explore advanced use cases and multi-agent systems.

Let’s build something amazing with **smolagents**! 🚀

---

## Help and Support

If you encounter issues or have questions, feel free to open an issue in this repository, [ask a question on the Discord sever](https://discord.gg/eQXBaCvTA9) or refer to the [smolagents Documentation](https://huggingface.co/docs/smolagents).

## Thank you

Thank you for contributing to this repository! Your efforts help create a valuable resource for the AI community. If you have any questions, feel free to reach out via [our Discord sever](https://discord.gg/eQXBaCvTA9) or open an issue in this repository. Let’s build a strong AI community together!

## Summary

**smolagents** is a new tool from Hugging Face for building AI agents. Here's a breakdown of what it is and why it matters:

- **What are AI agents?** AI agents are programs where a large language model (LLM) controls the workflow. The level of control an LLM has is described as "agency" which exists on a spectrum. Agents can carry out tasks through a series of steps, which may include thinking, using a tool, and then executing.

- **What makes smolagents special?**
  - **Simplicity:** It's designed to be a simple library, with its core logic fitting into a few thousand lines of code.
  - **Code Agents:** It treats code agents as a priority, which means the agent writes actions in code rather than JSON. This allows for more reliable and precise execution.
- **Hub Integration:** You can share and load tools from the Hugging Face Hub.
- **Flexibility:** It supports many different LLMs, including those hosted on the Hugging Face Hub, as well as models from OpenAI and Anthropic.
- **How do you build an agent using smolagents?** You need at least two things: a list of tools for the agent to use and an LLM to power the agent. You can also add a system prompt and memory.
- **Why use agents?** Agents can significantly improve the results of an LLM application.
- **Open Source Models:** Open-source models are becoming as good as commercial models for agent workflows, providing more access to quality LLM data outputs.
- **Key to building good agents**: Keep the workflow simple, give the LLM better information, use a stronger LLM or give weaker models more guidance.

In short, **smolagents** is a new framework that makes it easier to build powerful AI agents, with a focus on code-based actions for increased reliability and precision. It’s designed to be simple, flexible, and integrates well with other Hugging Face resources.
