import os
import logfire
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class Capital(BaseModel):
    """Capital city model - includes name and short history of the city"""
    name: str
    year_founded: int
    short_history: str
    comparison: str

# Define the agent
agent = Agent(model=model, result_type=Capital, system_prompt="You are an experienced historian and you are asked a question about the capital of a country. You are expected to provide the name of the capital city, the year it was founded, a short history of the city and a comparison of the city age to the age of the city provided by the tool.")

@agent.tool
def get_comparison_city(ctx: RunContext[str]) -> str:
    return f"The comparison city is {ctx.deps}"

@agent.result_validator
def validate_result(ctx: RunContext[str], result: Capital) -> Capital:
    if (result.year_founded > 1000):
        print(Fore.YELLOW, f"Prompt: {ctx.prompt}")
        print(Fore.YELLOW, f"Dependencies: {ctx.deps}")
        print(Fore.MAGENTA, f"Evaluating: {result.name}")
        print(Fore.MAGENTA, f"Comparison: {result.comparison}")
        print(Fore.RED, f"Validation failed: Year founded {result.year_founded} is too high. Try another country.")
        raise ModelRetry("Year founded is too high. Try another country.")
    return result

# Run the agent
try:
    result = agent.run_sync("What is the capital of the US?", deps="Toronto")
    print(Fore.RED, result.data.name)
    print(Fore.GREEN, result.data.year_founded)
    print(Fore.CYAN, result.data.short_history)
except ModelRetry as e:
    print(Fore.RED, e)
except Exception as e:
    print(Fore.RED, e)