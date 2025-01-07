import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class SystemPrompt(BaseModel):
    """System prompt for an agent to generate helpful responses"""
    prompt: str
    tags: list[str]

# Define the agent
prompt_agent = Agent(model=model, result_type=SystemPrompt, system_prompt="You an expert prompt writer. Create a system prompt to be used for an AI agent that will help a user based on the user's input. Must be very descriptive and include step by step instructions on how the agent can best answer user's question. Do not directly answer the question. Start with 'You are a helpful assistant specialized in...'. Include any relevant tags that will help the AI agent understand the context of the user's input.")

agent = Agent(model=model, system_prompt="Use the system prompt and tags provided to generate a helpful response to the user's input.")

@agent.system_prompt  
def add_prompt(ctx: RunContext[str]) -> str:
    return ctx.deps.prompt

@agent.system_prompt
def add_tags(ctx: RunContext[str]) -> str:
    return f"Use these tags: {ctx.deps.tags}"

# Define the main loop
def main_loop():
    message_history = []
    prompt_generated = False
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if not prompt_generated:
            system_prompt = prompt_agent.run_sync(user_input).data
            print("Prompt:", system_prompt.prompt)
            print("Tags:", system_prompt.tags)
            prompt_generated = True

        # Run the agent
        result = agent.run_sync(user_input, deps=system_prompt, message_history=message_history)
        message_history = result.all_messages()
        print(f"Assistant: {result.data}")

# Run the main loop
if __name__ == "__main__":
    main_loop()