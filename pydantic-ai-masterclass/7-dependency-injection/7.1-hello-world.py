import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()
# This example demonstrates how to use dependency injection in Pydantic AI to pass additional context to the system prompt. Here, we define a system prompt that uses dependency injection to pass the user's industry specialization to the system prompt. The system prompt then uses this information to provide a more personalized response to the user.

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the agent with a system prompt
agent = Agent(model=model, system_prompt="You are an experienced career coach. Guide the user as they transition from a tradtional career to one where AI plays a greater role. Use the industry specialization provided by the user to provide a 10 steps plan for a career overhaul. Refer to the industry in your answer.", deps_type=str)

# Define a system prompt with dependency injection
@agent.system_prompt
def get_industry(ctx: RunContext[str]) -> str:
    return f"Your industry specialization is in {ctx.deps}."

# Define the main loop
def main_loop():
    while True:
        user_input = input(">> I am your career coach. Please provide an industry specialization: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = agent.run_sync("Provide a 10 steps plan for a career overhaul.", deps=user_input)
        print(f"Career advice: {result.data}")

# Run the main loop
if __name__ == "__main__":
    main_loop()