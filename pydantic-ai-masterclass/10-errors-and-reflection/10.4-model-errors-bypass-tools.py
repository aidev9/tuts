import os
import pprint
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior, capture_run_messages
from pydantic_ai.messages import ModelResponse, ToolCallPart
from pydantic_ai.models.openai import OpenAIModel

# Load the environment variables
load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model, system_prompt="You are a helpful assistant.")

# Define the tool
@agent.tool_plain(retries=0)
def calc_volume(size: int) -> int:  
    if size == 42:
        return size**3
    else:
        print(Fore.RED, f"Invalid size: {size}.")
        raise ModelRetry('Please try again with another size')

# Run the agent
with capture_run_messages() as messages:  
    try:
        result = agent.run_sync('Please get me the volume of a box with size 6.')
    except UnexpectedModelBehavior as e:
        print('An error occurred:', e)
        print('cause:', repr(e.__cause__))
        #> cause: ModelRetry('Please try again.')
        print(Fore.RESET)
        pprint.pprint(messages, indent=0, width=80)
        
        # Filter the ModelResponse messages from all messages
        model_responses = [m for m in messages if isinstance(m, ModelResponse)]

        # For each model response, print the data
        for model_response in model_responses:
            # Get the parts
            parts = model_response.parts
            # Filter the ToolCallPart messages from all parts
            tool_call_parts = [p for p in parts if isinstance(p, ToolCallPart)]
            if tool_call_parts:
                if any(isinstance(m, ModelResponse) for m in messages):
                    result = agent.run_sync('Please get me the volume of a box with size 6. Do not use tools.')
                    print(Fore.GREEN, result.data)
    else:
        print(Fore.GREEN, result.data)