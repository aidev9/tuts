import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class Capital(BaseModel):
    """Capital city model - includes name, year founded, short history of the city and comparison to another city"""
    name: str
    year_founded: int
    short_history: str
    comparison: str

# Define the agent
agent = Agent(model=model, result_type=Capital, system_prompt="You are an experienced historian and you are asked a question about the capital of a country. You are expected to provide the name of the capital city, the year it was founded, and a short history of the city. Provide an age and historical significance comparison of the cities.")

@agent.system_prompt  
def add_comparison_city(ctx: RunContext[str]) -> str:
    return f"The city to compare is {ctx.deps}."

# Run the agent
result = agent.run_sync("What is the capital of the US?", deps="Paris")

print(result.data)