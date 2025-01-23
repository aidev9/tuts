import os
from dotenv import load_dotenv
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel

# Load environment variables
load_dotenv()

# Define the model
model = LiteLLMModel(model_id="gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY'))

# Initialize the agent with the DuckDuckGo search tool
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

# Run the agent
agent.run("Who is the president of the United States?")