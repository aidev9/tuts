import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
load_dotenv()

model = OpenAIModel('gpt-4o', api_key=os.getenv('OPENAI_API_KEY'))
agent = Agent(model=model)

result = agent.run_sync("What is the capital of Mexico?")

print(result.data)