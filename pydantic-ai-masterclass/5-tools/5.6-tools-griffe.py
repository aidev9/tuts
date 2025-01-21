import os
from colorama import Fore
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.messages import ModelMessage, ModelResponse
from pydantic_ai.models.function import AgentInfo, FunctionModel
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

agent = Agent()

@agent.tool_plain
def code_quality(raw_code: str, cyclomatic_complexity: float, percent_duplication: float, review: str, notification_list: list[str]) -> str:
    """Code quality tool.

    Args:
        raw_code: raw code contents
        cyclomatic_complexity: how complex the code is
        percent_duplication: how much code is duplicated
        notification_list: list of emails to receive notifications
    """
    return f'{raw_code} {cyclomatic_complexity} {percent_duplication} {notification_list}'

def print_schema(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    tool = info.function_tools[0]
    print(Fore.CYAN, f"Tool name: {tool.name}")
    print(Fore.YELLOW, f"Tool description: {tool.description}")
    print(Fore.RED, f"Tool parameters: {tool.parameters_json_schema}")
    content = messages[-1].parts[0].content
    print(Fore.GREEN, f"Content: {content}")
    return ModelResponse.from_text(content=tool.description)
    
result = agent.run_sync('test run', model=FunctionModel(print_schema))
print(Fore.GREEN, result.data)