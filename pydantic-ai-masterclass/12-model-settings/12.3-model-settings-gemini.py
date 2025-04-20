import os
from typing import List, Optional
from colorama import Fore
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings

# Load environment variables
load_dotenv()

# Initialize the OpenAI models
model = GeminiModel(
    model_name="gemini-2.5-pro-exp-03-25",
    api_key=os.getenv("GEMINI_API_KEY"),
)

model_settings = GeminiModelSettings(
    temperature=1.0,
    gemini_safety_settings=[
        {
            'category': 'HARM_CATEGORY_HARASSMENT',
            'threshold': 'BLOCK_LOW_AND_ABOVE',
        },
        {
            'category': 'HARM_CATEGORY_HATE_SPEECH',
            'threshold': 'BLOCK_LOW_AND_ABOVE',
        },
    ],
)

# Response type - Pydantic model of a promotional response for any given brand
class BrandChatbotResponse(BaseModel):
    response: str = Field(..., description="The complete answer to the user's question in the brand's voice and style")
    brand_guidelines_followed: List[str] = Field(..., description="Specific brand guidelines and values reflected in the response")
    personality_traits: List[str] = Field(..., description="Brand personality traits evident in the response")
    suggested_products: Optional[List[str]] = Field(None, description="Suggested products or services relevant to the user's query")
    next_steps: Optional[List[str]] = Field(None, description="Suggested next steps or follow-up actions for the user")



# Create the agents
agent = Agent(model=model, result_type=BrandChatbotResponse)

@agent.system_prompt
def system_prompt() -> str:
    return """You are a skilled brand ambassador representing a company to potential customers. Your role is to engage with users, answer their questions, and promote the brand while maintaining its distinct voice and values. For each response:

    1. Maintain the brand's unique voice, tone, and personality consistently
    2. Follow established brand guidelines and values
    3. Provide helpful information about products or services
    4. Recommend relevant products when appropriate
    5. Suggest clear next steps or actions for the user
    6. Be authentic, engaging, and persuasive without being pushy

    Always structure your response using the BrandChatbotResponse model, which includes:
    - A complete response in the brand's voice and style
    - List of specific brand guidelines followed in the response
    - Brand personality traits evident in your response
    - Relevant product suggestions (when applicable) 
    - Recommended next steps for the user (when applicable)
    """

# Define the main loop
def main_loop():
    while True:
        user_input = input(">> I am your customer service agent. How can I assist you today? ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        # Run the agent
        result = agent.run_sync(user_input, model_settings=model_settings)
        if isinstance(result, UnexpectedModelBehavior):
            print(Fore.RED, "Error:", result.error)
            continue
        print(Fore.CYAN, f"Assistant: {result.data}")

# Run the main loop
if __name__ == "__main__":
    main_loop()