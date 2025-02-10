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
import json
import gradio as gr
from markdown_pdf import MarkdownPdf, Section
from jinja2 import Environment, PackageLoader, select_autoescape
import logging
from models import Address, StockData, Stock, Choice, Decision, Argument, State
import tools

# Load the environment variables
load_dotenv()

env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

ROUNDS = 1

# Initialize the OpenAI model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pro debate agent
pro_agent = Agent[None, Argument](
    model=model,
    result_type=Argument,
    deps_type=Stock,
    system_prompt="You are a stock analyst. Based on the report provided, write an argument for the stock. The argument should be positive and reference the company’s financial information as provided in the report. Respond with extensive details and bullet points. The argument should entice the user to learn more about and ultimately purchase the stock."
)

# Con debate agent
con_agent = Agent[None, Argument](
    model=model,
    result_type=Argument,
    deps_type=Stock,
    system_prompt='You are a stock analyst. Based on the report provided, write an argument against the stock. The argument should be negative and reference the company’s financial information as provided in the report. Respond with extensive details and bullet points. Your argument should dissuade the user from purchasing the stock.'
)

# Reasoning agent
reasoning_agent = Agent(model=model, system_prompt='You are a stock reviewer. Review the arguments for the stock and make a decision if the stock is a buy or skip. Respond by including the sentiment, decision, and explanation. Include both the positive and negative arguments in the decision. Emphasise why the stock is a buy or skip.' ,deps_type=Stock)

# Decision agent
decision_format_agent = Agent(model=model, system_prompt='You are a formatting agent. Take the input provided and respond with a structured response.', result_type=Decision, deps_type=Stock)

async def call_only_once(
    ctx: RunContext[str], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps.num_rounds <= 3:
        return tool_def

@pro_agent.tool(prepare=call_only_once)
@con_agent.tool(prepare=call_only_once)
def get_stock_report(ctx: RunContext[str]) -> str:
    """Fetch the stock report.
    Args:
        ctx: the context object
    """
    ctx.deps.num_rounds += 1
    print (Fore.YELLOW + f"Round {ctx.deps.num_rounds}: Fetching stock report")
    return ctx.deps.report

# Moderator node
@dataclass
class ModeratorNode(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> ProNode:
        if ctx.state.num_rounds <= ROUNDS:
            if ctx.state.num_rounds % 2 == 0:
                logger.info(Fore.GREEN + f"Round {ctx.state.num_rounds}: calling pro_agent")
                return ProNode()
            else:
                logger.info(Fore.RED + f"Round {ctx.state.num_rounds}: calling con_agent")
                return ConNode()
        else:
            prompt = "Review the arguments for the stock and make a decision if the stock is a buy or skip. Respond by including the sentiment, decision, and explanation. Include both the positive and negative arguments in the decision. Emphasise why the stock is a buy or skip."
            logger.info(Fore.YELLOW + f"Round {ctx.state.num_rounds}: calling reasoning_agent")
            result = await reasoning_agent.run(message_history=ctx.state.messages, user_prompt=prompt, deps=ctx.state.stock)
            stripped_data = re.sub(r'<think>.*?</think>', '', result.data, flags=re.DOTALL)
            logger.info(Fore.YELLOW, stripped_data)
            return DecisionNode(stripped_data)

# Pro debate node
@dataclass
class ProNode(BaseNode[State, None, Argument]):
    """ProNode class - runs the pro_agent to generate a positive argument for the stock."""
    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> ModeratorNode:
        prompt = f"For stock {ctx.state.stock.symbol}, use the stock report tool only to conduct research and make a positive argument so people buy it. Cite financial when possible"
        result = await pro_agent.run(prompt, deps=ctx.state.stock, result_type=Argument, message_history=ctx.state.messages)
        if isinstance(result.data, Argument):
            logger.info(Fore.GREEN, result.data.body)
            ctx.state.messages += result.new_messages()
            ctx.state.num_rounds += 1
            return ModeratorNode()

# Con debate node
@dataclass
class ConNode(BaseNode[State, None, Argument]):
    """ConNode class - runs the con_agent to generate a negative argument for the stock."""
    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> ModeratorNode:
        prompt = f"For stock {ctx.state.stock.symbol}, use the stock report tool only to conduct negative research so people do not buy it. Use negative sentiment when reading stock report. Cite financial when possible."
        result = await con_agent.run(prompt, deps=ctx.state.stock, result_type=Argument, message_history=ctx.state.messages)
        if isinstance(result.data, Argument):
            logger.info(Fore.RED, result.data.body)
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
                f'Format the final buy or skip decision for the stock:\n'
                f'{ctx.state.stock}\n'
                f'Decision text: {self.decision}'
            )
        else:
            prompt = (
                f'Format the final buy or skip decision for the stock:\n'
                f'{ctx.state.stock}'
            )

        logger.info(Fore.BLUE + f"Round {ctx.state.num_rounds}: calling decision_format_agent")
        result = await decision_format_agent.run(message_history=ctx.state.messages, user_prompt=prompt, deps=ctx.state.stock)
        return End(result.data)

# Markdown generator
def convert_stockdata_to_markdown(data: StockData) -> str:
    """Convert the stock data to markdown."""
    template = env.get_template("financial_report_template.md")
    return template.render(data=data)

# PDF Writer
def generate_pdf(report: str, out_file_name: str) -> None:
    """Generate a PDF report from the stock report."""
    css = "table, th, td {border: 1px solid black;}"
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(report, paper_size="A1"), user_css=css)

    pdf.save(f"reports/{out_file_name}.pdf")

# Main loop
async def generate_opinion(symbol: str) -> str:
    """The main loop - Generate an opinion on the stock based on the financial report."""
    yf_api = tools.YahooFinanceApi()
    yf_financial_report = yf_api.GetDetailedFinancialInformation(symbol)
    financial_report = convert_stockdata_to_markdown(yf_financial_report)

    # Generate a PDF copy of the financial report
    generate_pdf(financial_report, f'{symbol}_financial_report')

    stock = Stock(
        symbol=symbol,
        report=financial_report,
        keywords=['Balance Sheet', 'Cash Flow', 'Financials', 'Earnings', 'News'],
    )

    state = State(stock)
    graph = Graph(nodes=(ModeratorNode, ProNode, ConNode, DecisionNode))
    graph.mermaid_save('image.jpg', image_type='jpeg', direction='LR', background_color='white', title='Stock Decision Graph')
    decision, _ = await graph.run(ModeratorNode(), state=state, deps=stock)

    response = f"Decision: {decision.decision.value}\n Reasoning: {decision.explanation}"
    if decision.decision == Choice.buy:
        logger.info(Fore.GREEN, response)
    else:
        logger.info(Fore.RED, response)

    # Generate a PDF copy of the buy/skip decision
    generate_pdf(response, f'{symbol}_buyorskip_decision')

    return response

def generate_interface() -> gr.Blocks:
    """Create and configure Gradio interface"""
    gr.close_all()

    with gr.Blocks(title="Stock Advisor AI") as demo:
        gr.Markdown("# Stock Advisor AI - Stock Decision Graph")
        symbol_input = gr.Textbox(
            label="Stock Symbol",
            placeholder="Enter the stock symbol",
            key="symbol",
        )

        execute_button = gr.Button(value="Render Opinion", key="generate_opinion")

        opinion_output = gr.Textbox(
            label="Opinion",
            placeholder="Opinion will be displayed here",
            key="opinion",
        )

        execute_button.click(
            fn=generate_opinion,
            inputs=[symbol_input],
            outputs=[opinion_output],
        )

    return demo

# Run the main function
if __name__ == "__main__":
# Create a Gradio interface
    interface = generate_interface()

    asyncio.run(interface.launch())