import os
from typing import List, Optional
from colorama import Fore
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.settings import ModelSettings

# Load environment variables
load_dotenv()

# Warning: only supported by certain models. Please check the model documentation.
model_settings = ModelSettings(
    
    # The maximum number of tokens to generate before stopping
    max_tokens=500,

    # Amount of randomness injected into the response. Use temperature closer to 0.0 for analytical / multiple choice, and closer to a model's maximum temperature for creative and generative tasks. Warning: even with temperature 0.0, the results will not be fully deterministic.
    temperature=1.0,
    
    # An alternative to temperature, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. Use temperature or top_p, but not both.
    top_p=0.9,

    # Timeout for a request, in seconds
    timeout=10,

    # Whether to allow parallel tool calls.
    parallel_tool_calls=False,

    # The random seed to use for the model, theoretically allowing for more deterministic results
    seed=12839239870083700,

    # Penalize new tokens based on whether they have appeared in the text so far
    presence_penalty=0.0,

    # Penalize new tokens based on their existing frequency in the text so far
    frequency_penalty=0.0,

    # Modify the likelihood of specified tokens appearing in the completion
    # Remove 'irrational', 'addition' and 'solve' from the model's vocabulary
    # Add 'amazing' to the model's vocabulary
    # logit_bias={5856:-100, 17722:-100, 15339:100, 8467:100, 129830:-100}
    # ' irrational' = 129830:-100
    # ' addition' = 5856:-100
    # ' solve' = 17722:-100
    # ' amazing' = 8467:100
    logit_bias={129830:-100, 15339:100, 8467:100, 5856:-100, 17722:-100}
)

class MathResponse(BaseModel):
    explanation: str = Field(description="Step by step explanation of the solution")
    answer: float = Field(description="The final numerical answer")
    steps: List[str] = Field(description="List of steps taken to solve the problem")
    difficulty_level: str = Field(description="Estimated difficulty level of the problem")
    practice_problems: Optional[List[str]] = Field(description="Similar practice problems for the student", default=None)

# Initialize the OpenAI models
tutor_model = OpenAIModel(
    model_name="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Create the agents
math_tutor = Agent(model=tutor_model, result_type=MathResponse, model_settings=model_settings)

@math_tutor.tool_plain
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@math_tutor.tool_plain
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@math_tutor.tool_plain
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@math_tutor.tool_plain
def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b

@math_tutor.system_prompt
def system_prompt() -> str:
    return """You are a friendly and patient math tutor for primary school students. Your role is to help them understand 
    mathematical concepts and solve problems step by step. When responding to questions:

    1. Always break down the problem into simple, easy-to-understand steps
    2. Use clear, age-appropriate language
    3. Provide positive encouragement
    4. Include the final answer
    5. Suggest similar practice problems when appropriate
    6. Estimate the difficulty level of the problem

    You have access to basic mathematical operations through tools: add, subtract, multiply, and divide.
    Use these tools to perform calculations and show your work.

    Always structure your response using the MathResponse model, which includes:
    - A detailed explanation
    - The final numerical answer
    - Step-by-step solution
    - Difficulty level
    - Optional practice problems
    """

# Define the main loop
def main_loop():
    while True:
        user_input = input(">> I am a math tutor agent. What can I help you practice? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = math_tutor.run_sync(user_input)
        print(Fore.CYAN, f"Assistant: {result.data}")

# Run the main loop
if __name__ == "__main__":
    main_loop()