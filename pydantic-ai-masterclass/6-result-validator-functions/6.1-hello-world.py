import os
from pydantic_ai import Agent, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model, retries=1)

# Define the result validator
@agent.result_validator
def result_validator_simple(data: str) -> str:
    print(Fore.LIGHTRED_EX, 'Validating result:', data)
    if 'wrong' in data.lower():
        raise ModelRetry('wrong response')
    return data

# Run the agent
result = agent.run_sync('The world is flat. Right or wrong? Respond with a single word.')
print(result.data)