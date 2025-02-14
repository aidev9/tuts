import os
from dotenv import load_dotenv
from colorama import Fore
from pydantic_ai import Agent, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
import logfire

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent with a system prompt
agent = Agent(model=model, system_prompt="You are an AI knowledge summary agent. Summarize the key points from the provided text. Ensure the summary is concise and captures the main ideas accurately. Any time you get a response, call the `infinite_retry_tool` to produce another response.", retries=2)

# Define a system prompt with dependency injection
@agent.tool_plain(retries=3)
def infinite_retry_tool() -> int:
    print(Fore.RED + "Usage limit exceeded. Please try again later.")
    raise ModelRetry('Please try again.')

# Define the main loop
def main_loop():
    while True:
        user_input = input(">> I am a summary agent. What should I summarize? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = agent.run_sync(user_input)
        print(Fore.CYAN, f"Assistant: {result.data}")

# Run the main loop
if __name__ == "__main__":
    main_loop()