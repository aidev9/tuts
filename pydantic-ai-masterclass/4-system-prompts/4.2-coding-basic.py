import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

system_prompt = "You an experienced React developer. Create code that meets user's requirements."

# Define the agent
agent = Agent(model=model, system_prompt=system_prompt)

# Run the agent
result = agent.run_sync(user_prompt="Create a functional React component that displays a user profile with the following details: name, email, and profile picture. Must use Zustand for state management and TailwindCSS for styling.")

print(result.data)