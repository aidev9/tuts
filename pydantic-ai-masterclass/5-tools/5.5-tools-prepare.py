import os
from colorama import Fore
import logfire
from typing import Union
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.tools import ToolDefinition
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

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