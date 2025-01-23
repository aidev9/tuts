import datetime
import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, tool, GradioUI
import mermaid as md
from mermaid.graph import Graph
from PIL import Image

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model = LiteLLMModel(model_id="gpt-4o-mini", api_key=api_key, temperature=0)

@tool
def mermaid_render_tool(mermaid_str: str) -> str:
    """
    This is a tool that saves a mermaid diagram as a png file.
    It returns the image.

    Args:
        mermaid_str: The Mermaid diagram string.
    """

    sequence = Graph(title='Diagram', script=mermaid_str)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f"./output/diagram_{timestamp}.png"
    md.Mermaid(sequence).to_png(file_path)
    image_path = os.path.abspath(file_path)
    return Image.open(image_path)

agent = CodeAgent(tools=[mermaid_render_tool], model=model)
GradioUI(agent).launch()