import os
from colorama import Fore
import logfire
from pydantic_ai import Agent, RunContext, Tool
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

result = code_review_agent.run_sync("Read the code and provide the code quality metrics.", deps=result.data)
print(Fore.CYAN, result.data)