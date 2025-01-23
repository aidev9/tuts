import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from colorama import Fore

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class BaseNumber(BaseModel):
    """Number model representing a digit in base 10, binary and hexadecimal formats."""
    num_dec: int
    num_bin: str
    num_hex: str

# Define the agent
agent = Agent(model=model, result_type=BaseNumber, system_prompt="Generate a random number.", retries=1)

# Define the decimal result validator
@agent.result_validator
def validate_result_dec(ctx: RunContext[str], result: BaseNumber) -> BaseNumber:
    print(Fore.MAGENTA, f"Evaluating DEC: {result.num_dec}")
    if (result.num_dec > 500):
        print(Fore.RED, f"Validation failed: Number {result.num_dec} is too high. Try another number.")
        raise ModelRetry("Number is too high. Try another number.")
    return result

# Define the binary result validator
@agent.result_validator
def validate_result_bin(ctx: RunContext[str], result: BaseNumber) -> BaseNumber:
    print(Fore.MAGENTA, f"Evaluating BIN: {result.num_bin}")
    # Convert the binary number to decimal
    num_dec = int(result.num_bin, 2)
    if (num_dec > 500):
        print(Fore.RED, f"Validation failed: Number {result.num_bin} is too high. Try another number.")
        raise ModelRetry("Number is too high. Try another number.")
    return result

# Define the hexadecimal result validator
@agent.result_validator
def validate_result_hex(ctx: RunContext[str], result: BaseNumber) -> BaseNumber:
    print(Fore.MAGENTA, f"Evaluating HEX: {result.num_hex}")
    # Convert the hexadecimal number to decimal
    num_dec = int(result.num_hex, 16)
    if (num_dec > 500):
        print(Fore.RED, f"Validation failed: Number {result.num_hex} is too high. Try another number.")
        raise ModelRetry("Number is too high. Try another number.")
    return result

# Run the agent
try:
    result = agent.run_sync("Generate a number")
except ModelRetry as e:
    print(Fore.RED, e)
except Exception as e:
    print(Fore.RED, e)