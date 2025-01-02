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
class Calculation(BaseModel):
    """Captures the result of a calculation"""
    result: int

# Define the agent
agent = Agent(model=model, result_type=Calculation)

# Run the agent
result = agent.run_sync("What is 100 + 300?")

logfire.notice('Output from LLM: {result}', result = str(result.data))
logfire.info('Result type: {result}', result = type(result.data))
logfire.info('Result: {result}', result = result.data.result)