import os
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model)

# Run the agent
with logfire.span('Calling OpenAI gpt-4o-mini') as span:
    result = agent.run_sync("What is the capital of the US?")
    logfire.notice('{result=}', result=result.data)
    logfire.info('{result=}', result=result.data)
    logfire.debug('{result=}', result=result.data)
    logfire.warn('{result=}', result=result.data)
    logfire.error('{result=}', result=result.data)
    logfire.fatal('{result=}', result=result.data)