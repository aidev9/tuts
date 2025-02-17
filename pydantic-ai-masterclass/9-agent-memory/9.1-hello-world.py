import os
from datetime import date
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
ollama_model = OpenAIModel(model_name='deepseek-r1', base_url='http://localhost:11434/v1')

system_prompt = "You are a shopify store manager with digital marketing experience"

# Define the agent
agent = Agent(model=model, system_prompt=system_prompt)
reasoning_agent = Agent(model=ollama_model, system_prompt="Consider the arguments provided and help the user make a decision.")

# Run the agent
result1 = agent.run_sync(user_prompt="Create a Presidents's Day Marketing campaign for matresses and bed liners.")

messages = result1.all_messages()
print(Fore.GREEN, result1.data)

result2 = agent.run_sync(
    'Provide counter arguments why this strategy will fail.',
    message_history=result1.new_messages(),
)
print(Fore.RED, result2.data)

combined_messages = result1.new_messages() + result2.new_messages()

result3 = reasoning_agent.run_sync(
    'Should I run the marketing campaign? Respond with yes or no and if yes, how to overcome the challenges. If no, how to change the campaign to make it successful.',
    message_history=combined_messages,
)
print(Fore.YELLOW, result3.data)
