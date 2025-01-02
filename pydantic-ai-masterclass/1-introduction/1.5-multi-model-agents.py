import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.ollama import OllamaModel
from colorama import Fore

load_dotenv()
# Create the OpenAI model
openai_model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Create the OpenAI agent
open_ai_agent = Agent(model=openai_model)

# Run the OpenAI agent
result = open_ai_agent.run_sync("What is the capital of the Mexico?")
print(Fore.CYAN, "OpenAI Agent: ", result.data)

# Capture the last message
message_history = result.new_messages()

# Create the Ollama model
ollama_model = OllamaModel(
    model_name='llama3.2:1b',
    base_url='http://0.0.0.0:11434/v1',
)

# Create the Ollama agent
ollama_agent = Agent(model=ollama_model)

# Run the Ollama agent, passing the message history
print(Fore.GREEN, "Ollama Agent: ", ollama_agent.run_sync("Tell me about the history of this city.", message_history=message_history).data)