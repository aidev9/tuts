import os
from typing import List, Optional
from colorama import Fore
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.openai import OpenAIModel, OpenAIModelSettings

# Load environment variables
load_dotenv()

# Initialize the OpenAI models
model = OpenAIModel(
    model_name="o3-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_settings = OpenAIModelSettings(
    max_completion_tokens=500,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    
    # Constrains effort on reasoning for reasoning models. Supported values: low, medium, and high. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response
    openai_reasoning_effort="low",

    # A unique identifier representing the end-user, which can help OpenAI monitor and detect abuse
    user="user",

    # Temperature setting for the model. Does not apply to reasoning models
    # temperature=0.7,
)

# Response type - Pydantic model of a Customer Service Agent woring for an online store
class CSRResponse(BaseModel):
    response: str = Field(description="The assistant's response to the customer")
    order_status: Optional[str] = Field(description="Status of the customer's order", default=None)
    refund_status: Optional[str] = Field(description="Status of the customer's refund", default=None)
    estimated_delivery: Optional[str] = Field(description="Estimated delivery date for the order", default=None)
    customer_satisfaction: Optional[str] = Field(description="Customer satisfaction rating", default=None)
    follow_up_questions: Optional[List[str]] = Field(description="Follow-up questions for the customer", default=None)

# Create the agents
agent = Agent(model=model, result_type=CSRResponse)

@agent.system_prompt
def system_prompt() -> str:
    return """You are a professional and empathetic customer service agent for an online retail store. Your role is to assist customers with their inquiries, resolve issues, and ensure a positive shopping experience. When responding to customers:

    1. Always address the customer politely and professionally
    2. Provide clear and concise answers to their questions
    3. Offer solutions to their problems or escalate if necessary
    4. Use a friendly and understanding tone
    5. Include relevant details such as order status, refund status, or estimated delivery dates
    6. Ask follow-up questions if more information is needed to assist them better

    Always structure your response using the CSRResponse model, which includes:
    - A clear and helpful response
    - Order status (if applicable)
    - Refund status (if applicable)
    - Estimated delivery date (if applicable)
    - Customer satisfaction rating (if applicable)
    - Follow-up questions (if applicable)
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