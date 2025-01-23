import os
import logfire
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))
agent = Agent(model=model, deps_type=str)

# Define the result validator
@agent.result_validator
async def result_validator_deps(ctx: RunContext[str], data: str) -> str:
    print(Fore.YELLOW, 'Deps:', ctx.deps)
    print(Fore.RED, 'Data:', data)
    num_deps = int(ctx.deps)
    num_data = int(data)
    if num_deps != num_data:
        raise ModelRetry('wrong response')
    return data

# Run the agent
result = agent.run_sync('30*40 is what? Respond with the result only.', deps='1201')
print(result.data)