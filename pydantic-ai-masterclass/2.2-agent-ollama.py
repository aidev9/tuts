from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from colorama import Fore

ollama_model = OllamaModel(
    model_name='llama3.2:1b',
    base_url='http://0.0.0.0:11434/v1',
)

# Create the Agent
agent = Agent(model=ollama_model)

# Run the agent
result = agent.run_sync("What is the capital of the United States?")
print(Fore.RED, result.data)