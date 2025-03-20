import os
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
agent = Agent(model=model, system_prompt="You are a helpful assistant")

def get_response(user_input: str) -> str:
    return agent.run_sync(user_input)

def get_response_with_history(user_input: str, history: list) -> str:
    response = agent.run_sync(user_input)
    return response.data

# Define the main loop
def main_loop():
    while True:
        user_input = input(">> I am your asssitant. How can I help you today? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = get_response(user_input)
        print(Fore.WHITE, result.data)
        
# Run the main loop
if __name__ == "__main__":
    main_loop()