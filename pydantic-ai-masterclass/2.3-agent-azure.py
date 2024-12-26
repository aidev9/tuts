from pydantic_ai import Agent
from openai import AsyncAzureOpenAI
from pydantic_ai.models.openai import OpenAIModel
import os
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
)

# Create the Model
model = OpenAIModel('gpt-4o-mini', openai_client=client)

# Create the Agent
agent = Agent(model=model)

# Run the agent
print(Fore.RED, agent.run_sync("What is the capital of the United States?").data)