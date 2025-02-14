import os
from dotenv import load_dotenv
from colorama import Fore
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the response type as a Pydantic model
class MathResponse(BaseModel):
    """Math model response. Contains the square, cube and n'th power of a number. Squared, cubed, quad, squad and a random number. Squad must be equal to 93 minus random."""
    number: int
    power: int
    square: int
    cube: int
    nth: int

# Define the agent with a system prompt
agent = Agent(model=model, system_prompt="You are a mathematician tasked to calculate the square, cube and the n'th power of a number. Provided a number return a MathResponse type. Call math_tool only once! Never call the tool twice. If the user input is ambiguous, assume the numbers and proceed with calling the math tool only once. If the number is too large, decrease it by one and try again.", result_type=MathResponse, result_retries=3)

@agent.tool(retries=3)
def math_tool(ctx: RunContext[str], number: int, power: int):
    """Calculate the square, cube and the n'th power of a number."""

    print(Fore.CYAN, f"Using the math tool to calculate the square, cube and the {power}'th power of {number}...")
    square = number ** 2
    cube = number ** 3
    nth = number ** power
    return MathResponse(number=number, power=power, square=square, cube=cube, nth=nth)

@agent.result_validator
def math_response_validator(ctx: RunContext[str], response: MathResponse):
    """Validate the math response."""
    
    if response.square != response.number ** 2:
        raise ValueError("Square calculation is incorrect.")
    if response.cube != response.number ** 3:
        raise ValueError("Cube calculation is incorrect.")
    if response.nth != response.number ** response.power:
        raise ValueError("N'th power calculation is incorrect.")
    if (response.number > 4):
        print(Fore.RED, f"Number {response.number} is too large. Retrying...")
        print(Fore.RESET)
        raise ModelRetry("Number is too large.")
    
    return response

# Define the main loop
def main_loop():
    while True:
        user_input = input(">> I am a math agent. Provide a number and the power to calculate: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = agent.run_sync(user_input)
        print(Fore.YELLOW, f"Assistant: {result.data}")
        print(Fore.RESET)

# Run the main loop
if __name__ == "__main__":
    main_loop()