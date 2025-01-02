from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
model = OpenAIModel('gpt-4o-mini')
agent = Agent(model=model)
print(agent.run_sync("What is the capital of the United States?").data)