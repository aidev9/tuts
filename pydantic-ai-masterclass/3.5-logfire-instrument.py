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

@logfire.instrument('Applying multiply to {x=} and {y=}')
def multiply(x, y):
    return x * y

# Run the agent
with logfire.span('Calling OpenAI gpt-4o-mini') as span:
    try:
        result = agent.run_sync(f"Can you confirm that {multiply(300, 6)} is the result of 300 multiplied by 6? Also, include the answer.")
        span.set_attribute('result', result.data)
    except ValueError as e:
        span.record_exception(e)