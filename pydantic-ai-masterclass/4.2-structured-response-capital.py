import os
import logfire
from pydantic_ai import Agent
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
    """Capital city model - includes name and short history of the city"""
    name: str
    year_founded: int
    short_history: str

# Define the agent
agent = Agent(model=model, result_type=Capital)

# Run the agent
result = agent.run_sync("What is the capital of the US?")

logfire.notice('Results from LLM: {result}', result = str(result.data))
logfire.info('Year founded: {year}', year = result.data.year_founded)
logfire.info('Short history: {history}', history = result.data.short_history)