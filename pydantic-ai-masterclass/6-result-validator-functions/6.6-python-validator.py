import os
import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from langchain_experimental.utilities import PythonREPL
from colorama import Fore

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model, system_prompt="Generate Python code based on user input. Return executable code only.")

@agent.result_validator
def validate_result(ctx: RunContext[str], result_data) -> str:
    print(Fore.YELLOW, f"Evaluating Python code: {result_data}")
    try:
        repl = PythonREPL()
        result = repl.run(result_data)
        print(Fore.GREEN, "Function result: ", result)
    except BaseException as e:
        print(Fore.RED, f"Failed to execute. Error: {repr(e)}")
        raise ValueError(f"Failed to execute. Error: {repr(e)}")
    return result_data

# Run the agent
try:
    result = agent.run_sync("Create a Python function that calculates the cube of a number. Run the function with the number 12.")
    print(Fore.MAGENTA, "Code result: ", result.data)
except ModelRetry as e:
    print(Fore.RED, e)
except Exception as e:
    print(Fore.RED, e)