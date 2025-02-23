import os
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import (ModelMessage)
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
system_prompt = "You are a helpful assistant."

# Define the agent
agent = Agent(model=model, system_prompt=system_prompt)

# Define the main loop
def main_loop():
    message_history: list[ModelMessage] = []
    MAX_MESSAGE_HISTORY_LENGTH = 5

    while True:
        user_input = input(">> I am your asssitant. How can I help you today? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = agent.run_sync(user_input, deps=user_input, message_history=message_history)
        print(Fore.WHITE, result.data)
        msg = result.new_messages()
        message_history.extend(msg)

        # Limit the message history
        message_history = message_history[-MAX_MESSAGE_HISTORY_LENGTH:]
        print(Fore.YELLOW, f"Message length: {message_history.__len__()}")
        print(Fore.RESET)
# Run the main loop
if __name__ == "__main__":
    main_loop()