import os
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model)

# Tool to add two numbers
@agent.tool_plain
def add(a:int, b:int) -> int:
    """Adds two numbers"""
    print(Fore.CYAN, f"Calling tool add with params {a} and {b}...")
    return a + b

# Tool to determine if an integer is a prime number
@agent.tool_plain
def is_prime(a:int) -> bool:
    """Determines whether an integer is a prime number"""
    
    print(Fore.GREEN, f"Calling tool is_prime with param {a}...")
    if a <= 1:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True

result = agent.run_sync('17 + 74 is a prime number')
print(Fore.RED, result.data)