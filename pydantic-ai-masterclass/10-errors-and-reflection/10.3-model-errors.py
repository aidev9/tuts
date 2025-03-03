import os
import pprint
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior, capture_run_messages
from pydantic_ai.models.openai import OpenAIModel

# Load the environment variables
load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model, system_prompt="You are a helpful assistant.")

@agent.tool_plain(retries=5)
def calc_volume(size: int) -> int:  
    if size == 42:
        return size**3
    else:
        print(Fore.RED, f"Invalid size: {size}.")
        raise ModelRetry('Please try again with size=42.')

with capture_run_messages() as messages:  
    try:
        result = agent.run_sync('Please get me the volume of a box with size 6.')
    except UnexpectedModelBehavior as e:
        print('An error occurred:', e)
        #> An error occurred: Tool exceeded max retries count of 1
        print('cause:', repr(e.__cause__))
        #> cause: ModelRetry('Please try again.')
        print(Fore.RESET)
        pprint.pprint(messages, indent=0, width=80)
    else:
        print(Fore.WHITE, result.data)