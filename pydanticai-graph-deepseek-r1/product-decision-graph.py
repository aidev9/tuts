from __future__ import annotations as _annotations
import os
import re
import requests
import asyncio
from colorama import Fore
from dotenv import load_dotenv
from enum import Enum
from bs4 import BeautifulSoup

from dataclasses import dataclass, field
from typing import Union
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import ToolDefinition
from pydantic_ai.messages import ModelMessage
from pydantic_graph import BaseNode, End, Graph, GraphRunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.ollama import OllamaModel
from tavily import TavilyClient

# Load the environment variables
load_dotenv()

# Initialize the Tavily client
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

# Initialize the OpenAI model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Initialize the Deepseek R1 model on Ollama
reasoning_model = OllamaModel(
    model_name='deepseek-r1',
    base_url='http://0.0.0.0:11434/v1',
)

# Number of rounds for the debate
ROUNDS = 1

# Product class
@dataclass
class Product:
    name: str
    url: str
    keywords: list[str]
    num_rounds: int = 0

# Decision enum
class Choice(Enum):
    buy = 'Buy'
    skip = 'Skip'

# Decision model 
@dataclass
class Decision:
    """Decision model - includes sentiment and decision. Sentiment is a value between -100 and 100. Decision is a one-word string value of 'Buy' or 'Skip'. Explanation is a short paragraph explaining the decision."""
    sentiment: int
    decision: Choice # buy or skip
    explanation: str

# Debate argument model
@dataclass
class Argument:
    """Argument model - includes sentiment and body. Sentiment is a value between -100 and 100. Body is a  paragraph explaining the argument for or against the product and provides the reasons."""
    sentiment: int
    body: str

# Graph state
@dataclass
class State:
    product: Product
    messages: list[ModelMessage] = field(default_factory=list)
    num_rounds: int = 0
    sentiment: int = 0

# Agent definitions

# Pro debate agent
pro_agent = Agent[None, Argument](
    model=model,
    result_type=Argument,
    deps_type=Product,
    system_prompt='You are a product manager for a new product. Write an argument for the product. The argument should be positive and reference the products features, competitive advantages and unique selling points. It should entice the user to learn more about and ultimately purchase the product. Get the product details from the URL provided. Respond with extensive details and bullet points. Use the search tool with positive sentiment to get the search results for positive reviews about the product.'
)

# Con debate agent
con_agent = Agent[None, Argument](
    model=model,
    result_type=Argument,
    deps_type=Product,
    system_prompt='Write an argument against the product. Get the product details from the URL provided. Use the search tool to perform negative sentiment research to support your points. Respond with extensive details and bullet points. Your argument should dissuade potential buyers.'
)

# Reasoning agent
reasoning_agent = Agent(model=reasoning_model, system_prompt='You are a product reviewer. Review the arguments for the product and make a decision if the product is a buy or skip. Respond by including the sentiment, decision, and explanation. Include both the positive and negative arguments in the decision. Emphasise why the product is a buy or skip.' ,deps_type=Product)

# Decision agent
decision_format_agent = Agent(model=model, system_prompt='You are a formatting agent. Take the input provided and respond with a structured response.', result_type=Decision, deps_type=Product)


# Tools
async def call_only_once(
    ctx: RunContext[str], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps.num_rounds <= 3:
        return tool_def

@pro_agent.tool(prepare=call_only_once)
@con_agent.tool(prepare=call_only_once)
def product_search(ctx: RunContext[str], sentiment: str) -> str:
    """Perform search for online reviews for given product and return the results.
    Args:
        ctx: the context object
        sentiment: whther to search for positive or negative reviews
    """
    max_results = 5
    query = f"Find results with {sentiment} sentiment for {ctx.deps.name} with keywords {ctx.deps.keywords}"
    results = tavily_client.search(query, max_results=max_results, days=60)
    ctx.deps.num_rounds += 1
    return results

@pro_agent.tool(prepare=call_only_once)
@con_agent.tool(prepare=call_only_once)
def get_product_details(ctx: RunContext[str]) -> str:
    """Scrape the product URL and process the information.
    Args:
        ctx: the context object
    """
    response = requests.get(ctx.deps.url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    ctx.deps.num_rounds += 1
    return text

# Graph nodes

# Moderator node
@dataclass
class ModeratorNode(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> ProNode:
        if ctx.state.num_rounds <= ROUNDS:
            if ctx.state.num_rounds % 2 == 0:
                print(Fore.GREEN + f"Round {ctx.state.num_rounds}: calling pro_agent")
                return ProNode()
            else:
                print(Fore.RED + f"Round {ctx.state.num_rounds}: calling con_agent")
                return ConNode()
        else:
            prompt = "Review the arguments for the product and make a decision if the product is a buy or skip. Respond by including the sentiment, decision, and explanation. Include both the positive and negative arguments in the decision. Emphasise why the product is a buy or skip."
            print(Fore.YELLOW + f"Round {ctx.state.num_rounds}: calling reasoning_agent")
            result = await reasoning_agent.run(message_history=ctx.state.messages, user_prompt=prompt, deps=ctx.state.product)
            stripped_data = re.sub(r'<think>.*?</think>', '', result.data, flags=re.DOTALL)
            print(Fore.YELLOW, stripped_data)
            return DecisionNode(stripped_data)

# Pro debate node
@dataclass
class ProNode(BaseNode[State, None, Argument]):
    """ProNode class - runs the pro_agent to generate a positive argument for the product."""
    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> ModeratorNode:
        prompt = f"For product {ctx.state.product.name}, use the search tool to conduct research and make a positive argument so people buy it."
        result = await pro_agent.run(prompt, deps=ctx.state.product, result_type=Argument, message_history=ctx.state.messages)
        if isinstance(result.data, Argument):
            print(Fore.GREEN, result.data.body)
            ctx.state.messages += result.new_messages()
            ctx.state.num_rounds += 1
            return ModeratorNode()

# Con debate node
@dataclass
class ConNode(BaseNode[State, None, Argument]):
    """ConNode class - runs the con_agent to generate a negative argument for the product."""
    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> ModeratorNode:
        prompt = f"For product {ctx.state.product.name}, use the search tool to conduct negative research so people do not buy it. Use negative sentiment when calling search tool."
        result = await con_agent.run(prompt, deps=ctx.state.product, result_type=Argument, message_history=ctx.state.messages)
        if isinstance(result.data, Argument):
            print(Fore.RED, result.data.body)
            ctx.state.messages += result.new_messages()
            ctx.state.num_rounds += 1
            return ModeratorNode()

# Decision node 
@dataclass
class DecisionNode(BaseNode[State]):
    decision: str | None = None

    async def run(self, ctx: GraphRunContext[State]) -> ProNode:
        if self.decision:
            prompt = (
                f'Format the final buy or skip decision for product:\n'
                f'{ctx.state.product}\n'
                f'Decision text: {self.decision}'
            )
        else:
            prompt = (
                f'Format the final buy or skip decision for product:\n'
                f'{ctx.state.product}'
            )

        print(Fore.BLUE + f"Round {ctx.state.num_rounds}: calling decision_format_agent")
        result = await decision_format_agent.run(message_history=ctx.state.messages, user_prompt=prompt, deps=ctx.state.product)
        return End(result.data)

# Main loop
async def main():
    
    # Wilson Basketball
    product = Product(
        name='NCAA Evo NXT Game Basketball',
        url='https://www.wilson.com/en-us/product/ncaa-evo-nxt-game-ball-wz10033',
        keywords=['basketball', 'sport', 'indoor', 'game', 'wilson'],
    )

    # MacBook Pro
    # product = Product(
    #     name='MacBook Pro 16 inch',
    #     url='https://www.apple.com/shop/buy-mac/macbook-pro/16-inch',
    #     keywords=['macbook', 'pro', 'laptop', 'apple', 'reviews'],
    # )

    # Lenovo Laptop Case
    # product = Product(
    #     name='Lenovo 15.6” Casual Toploader T210 - Green',
    #     url='https://www.lenovo.com/us/en/p/accessories-and-software/cases-and-bags/briefcases-toploads/gx40q17232',
    #     keywords=['laptop', 'bag', 'green', 'casual', 'lenovo'],
    # )

    state = State(product)
    graph = Graph(nodes=(ModeratorNode, ProNode, ConNode, DecisionNode))
    graph.mermaid_save('image.jpg', image_type='jpeg', direction='LR', background_color='white', title='Product Decision Graph')
    decision, _ = await graph.run(ModeratorNode(), state=state, deps=product)
    if decision.decision == Choice.buy:
        print(Fore.GREEN, f"Decision: {decision.decision.value}\n Reasoning: {decision.explanation}")
    else:
        print(Fore.RED, f"Decision: {decision.decision.value}\n Reasoning: {decision.explanation}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())