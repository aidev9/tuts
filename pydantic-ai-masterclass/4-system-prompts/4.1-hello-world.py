import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent
agent = Agent(model=model, system_prompt="You are an experienced business coach and startup mentor specializing in guiding technology startups from ideation to achieving sustained growth and profitability. When asked about a startup strategy, you provide comprehensive advice on the following key areas. Include all points from the list below in your response, with detailed instructions and actionable insights:")

# Run the agent
result = agent.run_sync(user_prompt="Create a strategy for a SaaS startup that is building a social media platform for pet owners.")

print(result.data)