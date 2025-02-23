import os
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.messages import (ModelMessage, ModelResponse)
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

system_prompt_research = f"You are a research assistant. Take user's input and provide relevant research."
system_prompt_reviewer = f"You are a research reviewer. Take the research agent's findings and look for areas of improvement. Don't just confirm the findings, but provide extra information."
system_prompt_qa = f"You are a quality assurance assistant. Take the previous agents' findings and summarize the answer into a simplfied language."

# Define the agent
agent_research = Agent(model=model, system_prompt=system_prompt_research)
agent_reviewer = Agent(model=model, system_prompt=system_prompt_reviewer)
agent_qa = Agent(model=model, system_prompt=system_prompt_qa)

# Filter messages by type
def filter_messages_by_type(messages: list[ModelMessage], message_type: ModelMessage) -> list[ModelMessage]:
    return [msg for msg in messages if type(msg) == message_type]

# Define the main loop
def main_loop():
    message_history: list[ModelMessage] = []
    while True:
        user_input = input(">> I am your research asssitant. How can I help you today? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        # Run the research agent
        result = agent_research.run_sync(user_input, deps=user_input, message_history=message_history)
        print(Fore.RED, f"Research: {result.data}\n")
        msg = result.new_messages()
        message_history.extend(msg)

        # Run the reviewer agent
        result = agent_reviewer.run_sync(user_input, deps=user_input, message_history=message_history)
        print(Fore.GREEN, f"Reviewer: {result.data}\n")
        msg = filter_messages_by_type(result.new_messages(), ModelResponse)
        message_history.extend(msg)

        # Run the QA agent
        result = agent_qa.run_sync(user_input, deps=user_input, message_history=message_history)
        print(Fore.WHITE, f"Summary: {result.data}\n")
        msg = filter_messages_by_type(result.new_messages(), ModelResponse)
        message_history.extend(msg)

        # Limit the message history
        # message_history = message_history[-MAX_MESSAGE_HISTORY_LENGTH:]
        print(Fore.YELLOW, f"Message length: {message_history.__len__()}")
        print(Fore.RESET)
# Run the main loop
if __name__ == "__main__":
    main_loop()