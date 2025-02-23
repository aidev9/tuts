import os
import pickle
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

# Write messages to file
def write_memory(memory: list[ModelMessage], file_path: str):
    with open(file_path, 'wb') as f:
        pickle.dump(memory, f)

# Read messages from file
def read_memory(file_path: str) -> list[ModelMessage]:
    memory = []
    with open(file_path, 'rb') as f:
        memory = pickle.load(f)
    return memory

# Delete messages file
def delete_memory(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

# Define the main loop
def main_loop():
    MEMORY_FILE_PATH = "./memory.pickle"
    MAX_MESSAGE_HISTORY_LENGTH = 5

    try:
        message_history: list[ModelMessage] = read_memory(MEMORY_FILE_PATH)
    except:
        message_history: list[ModelMessage] = []

    while True:
        user_input = input(">> I am your asssitant. How can I help you today? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if user_input.lower() in ["clear", "reset"]:
            print("Clearing memory...")
            delete_memory(MEMORY_FILE_PATH)
            message_history = []
            continue

        # Run the agent
        result = agent.run_sync(user_input, deps=user_input, message_history=message_history)
        print(Fore.WHITE, result.data)
        msg = result.new_messages()
        message_history.extend(msg)
        
        # Limit the message history
        # message_history = message_history[-MAX_MESSAGE_HISTORY_LENGTH:]
        write_memory(message_history, MEMORY_FILE_PATH)
        print(Fore.YELLOW, f"Message length: {message_history.__len__()}")
        print(Fore.RESET)
# Run the main loop
if __name__ == "__main__":
    main_loop()