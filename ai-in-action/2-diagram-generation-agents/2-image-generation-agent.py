import os
from dotenv import load_dotenv
from smolagents import load_tool, CodeAgent, LiteLLMModel, GradioUI

# Load environment variables
load_dotenv()

# Define the model
model = LiteLLMModel(model_id="gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY'))

# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

# Initialize the agent with the image generation tool
agent = CodeAgent(tools=[image_generation_tool], model=model)

# Launch the agent with Gradio UI
GradioUI(agent).launch()