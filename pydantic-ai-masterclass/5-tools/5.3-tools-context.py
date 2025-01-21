import os
from colorama import Fore
import logfire
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class Capital(BaseModel):
    """"Capital city model - includes the name, year founded, short history of the city and a comparison to another city"""
    name: str
    year_founded: int
    short_history: str
    comparison: str

# Define the agent
agent = Agent(model=model, result_type=Capital, system_prompt="You are an experienced historian and you are asked a question about the capital of a country. You are expected to provide the name of the capital city, the year it was founded, and a short history of the city. Compare the the city to the  city provided by the comparison tool. Always call the comparison tool to get the comparison city.")

# Tool to get the comparison city
@agent.tool(retries=2)
def get_comparison_city(ctx: RunContext[str]) -> str:
    return f"The comparison city is {ctx.deps}"

# Run the agent
result = agent.run_sync("Capital of the US", deps="Paris")

# Print the results
print(Fore.RED, result.data.name)
print(Fore.GREEN, result.data.year_founded)
print(Fore.CYAN, result.data.short_history)
print(Fore.YELLOW, result.data.comparison)