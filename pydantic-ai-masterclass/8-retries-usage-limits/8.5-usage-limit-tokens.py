import os
from dotenv import load_dotenv
from colorama import Fore
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.usage import UsageLimits

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent with a system prompt
agent = Agent(model=model, system_prompt="You are a highly skilled haiku poet. When asked write a short haiku matching user's prompt.")

response_tokens_limit = 50
total_tokens_limit = 50

result_sync = agent.run_sync(
    'Robots will not rule the world.',
    usage_limits=UsageLimits(response_tokens_limit=response_tokens_limit),
)
print(Fore.GREEN, result_sync.data)
print(Fore.RED, result_sync.usage())
print(Fore.RESET)

try:
    result_sync = agent.run_sync(
        'Cherry blossoms bloom.',
        usage_limits=UsageLimits(response_tokens_limit=response_tokens_limit, total_tokens_limit=total_tokens_limit),
    )
    print(Fore.CYAN, result_sync.data)
    print(Fore.RED, result_sync.usage())
    print(Fore.RESET)
except UsageLimitExceeded as e:
    print(e)