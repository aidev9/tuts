import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, tool
from huggingface_hub import list_models

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model = LiteLLMModel(model_id="gpt-4o-mini", api_key=api_key)

@tool
def model_download_tool(task: str) -> str:
    """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint.

    Args:
        task: The task for which to get the download count.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    return most_downloaded_model.id

agent = CodeAgent(tools=[model_download_tool], model=model)

agent.run(
    "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub?"
)