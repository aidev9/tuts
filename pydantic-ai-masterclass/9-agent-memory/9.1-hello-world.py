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

stock = "TESLA"

system_prompt = f"You are an investment portfolio manager specialized in US tech stocks. The user is a 45 year old tech executive with $10M net worth and 5 year aggresive investment window. Your job is to provide investment advice on {stock} stock. The user will never invest more than 5% of their portfolio into any individual stock or ETF. Your job is to guide that decision and suggest a number between 1-5%. Consider the user's profile, investment window, and the stock's performance, market trends, and expert opinions. Consider alternative investments."

# Define the agent
agent = Agent(model=model, system_prompt=system_prompt)
reasoning_agent = Agent(model=ollama_model, system_prompt=system_prompt)

# Run the agent
result_pro = agent.run_sync(user_prompt=f"Provide arguments why I should buy {stock} and how much I should invest.")

messages = result_pro.all_messages()
print(Fore.GREEN, result_pro.data)

result_con = agent.run_sync(
    user_prompt=f"Provide counter arguments why I should not buy {stock} and what to do instead.",
    message_history=result_pro.new_messages(),
)
print(Fore.RED, result_con.data)

combined_messages = result_pro.new_messages() + result_con.new_messages()

result_reasoning = reasoning_agent.run_sync(
    user_prompt=f"Should I buy {stock} stock? Respond with a strong YES or NO, and support your answer with facts and the percent investment. If the answer is yes, what are some of the risks associated? If the answer is no, what are the top 5 alternatives? Include buy percent for each. Balance both the negative and positive arguments and help me make a decision. Try to be netural and only consider user's situation and financial goals.",
    message_history=combined_messages,
)
print(Fore.YELLOW, result_reasoning.data)
