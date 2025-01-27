# Multi-Agent Product Decision Graph with PydanticAI and DeepSeek R1

## Overview

This project demonstrates an implementation of a multi-agent graph using the **PydanticAI** framework. The setup includes several interconnected agents and tools working together to simulate a product buy/skip debate. The final decision is made by leveraging the **DeepSeek R1** reasoning model. While this reasoning model does not support function calling and structured outputs, this example demonstrates ways of overcoming these limitations by using creative workflows.

This repository serves as a companion to the video tutorial **[Multi-Agent Product Decision Graph with PydanticAI and DeepSeek R1](https://www.youtube.com/watch?v=r1pymNaji1E)** which introduces the concept of function tools and provides several examples of to effectively use tools to extend the functionality of the LLMs.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/r1pymNaji1E/0.jpg)](https://www.youtube.com/watch?v=r1pymNaji1E)

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

The core functionality revolves around debating whether to recommend purchasing a product. This is achieved through the following agents:

1. **Pro Agent**: Argues in favor of the product, using positive sentiment research.
2. **Con Agent**: Argues against the product, using negative sentiment research.
3. **Moderator Agent**: Manages the debate rounds and alternates between the Pro and Con agents.
4. **Reasoning Agent**: Uses **DeepSeek R1** to analyze all arguments and make the final buy/skip decision.
5. **Decision Formatting Agent**: Formats the reasoning agent's output into a structured decision model.

### Key Tools and Features:

- **Tavily Search**: Used by the Pro and Con agents to fetch real-world product reviews.
- **BeautifulSoup**: Scrapes and processes product details from the provided URL.
- **PydanticAI Graph**: Implements a structured graph to manage state and agent interactions.
- **DeepSeek R1**: Handles reasoning and decision-making, overcoming its inability to use tools or produce structured output by providing curated inputs.

---

---

## Workflow

1. **Product Initialization**: The product name, URL, and keywords are defined, along with the total number of debate rounds.

2. **Debate Rounds**:

   - The **Moderator Agent** alternates between the Pro and Con agents, managing the flow of arguments.
   - Both agents use the **Tavily Search tool** and product details to strengthen their cases.

3. **Reasoning**:

   - After all rounds are complete, the arguments are passed to the **Reasoning Agent**, which uses DeepSeek R1 to compute the final decision (Buy or Skip).

4. **Decision Formatting**:
   - The decision is formatted into a structured model with sentiment, decision, and explanation fields.

---

## Key Components

### Agents

1. **Pro Agent**:

   - Generates a positive argument for the product.
   - Uses Tavily Search with a positive sentiment filter.

2. **Con Agent**:

   - Generates a negative argument against the product.
   - Uses Tavily Search with a negative sentiment filter.

3. **Reasoning Agent**:

   - Analyzes all arguments and produces a decision based on sentiment and reasoning.

4. **Decision Formatting Agent**:
   - Structures the decision into a consistent format for output.

### Graph Nodes

- **ModeratorNode**: Alternates between ProNode and ConNode based on the current round.
- **ProNode**: Executes the Pro Agent to generate a positive argument.
- **ConNode**: Executes the Con Agent to generate a negative argument.
- **DecisionNode**: Uses the Reasoning Agent to make the final decision and passes it to the Decision Formatting Agent.

### Tools

1. **Tavily Search**:

   - Fetches online reviews for the product.
   - Filters results based on sentiment (positive/negative).

2. **Web Scraping**:
   - Uses BeautifulSoup to scrape product details from the provided URL.

---

## Limitations of DeepSeek R1 and Overcoming Them

### Limitations:

1. Cannot use tools like Tavily Search directly.
2. Does not produce structured output by default.

### Solutions:

1. **Preprocessed Inputs**: The ModeratorNode ensures that curated inputs (arguments from Pro/Con agents) are passed to DeepSeek R1.
2. **Post-Processing**: The Decision Formatting Agent structures the raw output from DeepSeek R1 into a Pydantic-compliant format.

---

## Example Use Case

The following product is used as an example:

**Product**: NCAA Evo NXT Game Basketball  
**URL**: [Wilson Product Page](https://www.wilson.com/en-us/product/ncaa-evo-nxt-game-ball-wz10033)  
**Keywords**: `basketball`, `sport`, `indoor`, `game`, `wilson`

The agents debate whether this basketball is worth purchasing, analyze the arguments, and provide a structured recommendation.

---

## How to Run

### Prerequisites

1. **Python 3.8+**
2. **Environment Variables**:
   - `TAVILY_API_KEY`: API key for Tavily.
   - `OPENAI_API_KEY`: API key for OpenAI GPT-4o.
3. **Install Required Libraries**:
   ```bash
   pip install pydantic-ai tavily beautifulsoup4 colorama
   ```
4. **Ollama Setup**:
   - Install Ollama: [Ollama Installation Guide](https://github.com/ollama/ollama)
   - Download the `deepseek-r1:latest` model:
     ```bash
     ollama run deepseek-r1:latest
     ```

### Running the Script

```bash
python product-decision-graph.py
```

---

## Outputs

The final output will include:

1. **Buy/Skip Decision**: Indicates whether the product is recommended.
2. **Sentiment Score**: Ranges from -100 to 100.
3. **Reasoning**: Explains why the product is recommended or not.

---

## Example Output

```plaintext
Decision: Buy
Sentiment: 85
Reasoning: The product is well-suited for indoor games, with excellent grip and durability. Positive user reviews highlight its performance in competitive settings.
```

---

## Extending the Graph

1. **Add More Agents**:
   - Include additional agents for specific perspectives (e.g., environmental impact).
2. **Enhance Tools**:
   - Integrate more advanced search or scraping tools.
3. **Dynamic Rounds**:
   - Allow the number of debate rounds to vary based on product complexity.
4. **Search for Other Products**:
   - Add another product by including the product name, link to a description website and keywords that describe the product. The script can be updated to weigh in keywords, according to their importance

---

## Troubleshooting

1. **Tavily Search Errors**:
   - Ensure your API key is valid and check rate limits.
2. **BeautifulSoup Parsing Issues**:
   - Verify that the product URL is accessible and contains valid HTML.
3. **Ollama (DeepSeek R1) Connectivity**:
   - Confirm the base URL and ensure the local Ollama (DeepSeek R1) server is running.

---

## Acknowledgments

- **PydanticAI Team**: For providing the framework to simplify agent creation.
- **DeepSeek Team**: For enabling advanced reasoning capabilities.
- **Tavily**: For seamless integration with search tools.

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
