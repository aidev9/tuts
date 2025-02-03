# Investment Report using Pydantic, AI and Yahoo Finance

## Overview

This project demonstrates an implementation of a multi-agent graph using the **PydanticAI** framework. The setup includes several interconnected agents and tools working together to simulate a product buy/skip debate. The final decision is made by leveraging the **DeepSeek R1** reasoning model. While this reasoning model does not support function calling and structured outputs, this example demonstrates ways of overcoming these limitations by using creative workflows.

This repository serves as a companion to the video tutorial **[Multi-Agent Product Decision Graph with PydanticAI and DeepSeek R1](https://www.youtube.com/watch?v=r1pymNaji1E)** which introduces the concept of function tools and provides several examples of to effectively use tools to extend the functionality of the LLMs.


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


---


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
   - See the .env.sample file
3. **Install Required Libraries**:
   ```bash
   $ pip install -r requirements.txt
   ```
4. **Ollama Setup**:
   - Install Ollama: [Ollama Installation Guide](https://github.com/ollama/ollama)
   - Download the `deepseek-r1:latest` model:
     ```bash
     ollama run deepseek-r1:latest
     ```

### Running the Script

```bash
python x.py
```

---

## Outputs

The final output will include:

1. TBD

---

## Example Output

```plaintext
report here
```

---
## Further Explortation
Make sure to checkout the yfinance GitHub [repository](https://github.com/ranaroussi/yfinance/tree/main) and [documentation](https://ranaroussi.github.io/yfinance/index.html). This library provides a rich interface to the Yahoo Finance API. We only scratched the surface with this project.
---

## Resources
- [yfinance GitHub Repository](https://github.com/ranaroussi/yfinance/tree/main)
- [yfinance Documentation Page](https://ranaroussi.github.io/yfinance/index.html)
- [PydanticAI GitHub Repository](https://github.com/pydantic/pydantic-ai)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Discord Community](https://discord.gg/eQXBaCvTA9)
- [Full Video Masterclass](https://www.youtube.com/playlist?list=PL2yl5VopECya-fXbIKlGbkv8qgTFVsfwO)

---

