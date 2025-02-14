import os
from dotenv import load_dotenv
from colorama import Fore
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dataclasses import dataclass

load_dotenv()
# This example demonstrates how to use system prompts with dependencies in PydanticAI. The use case is a customer service representative for an insurance company. The agent is expected to take the customer's question, classify it appropriately (e.g., billing, technical support, general inquiry), determine if the issue needs to be escalated, and provide a clear and helpful response. 

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

class Policy(BaseModel):
    """Policy model - includes policy number, policy type and policy status"""
    policy_number: int
    policy_type: str
    policy_status: str
    policy_deductable: int
    policy_max_coverage: int
    policy_coverage_remaining: int

# Define the output model
class Customer(BaseModel):
    """Customer model - includes customer ID, full name and email"""
    customer_id: int
    name: str
    email: str
    policy: Policy

class SupportResponse(BaseModel):
    """Support response model - includes customer, response type (answer, forward, escalation), response text and escalation flag"""
    customer: Customer
    response_type: str
    response: str
    escalation: bool

@dataclass
class Deps:
    """Dependencies for the agent"""
    customer: Customer

# Define the agent
agent = Agent(model=model, result_type=SupportResponse, system_prompt="You are a customer service representative for an insurance company. Your task is to take the customer's question, classify it appropriately (e.g., billing, technical support, general inquiry), determine if the issue needs to be escalated, and provide a clear and helpful response. Ensure that your response is polite and addresses the customer's concern effectively. Always include customer's name in your response. End your answer with Ref: customer ID. Get the customer from the provided context.", deps_type=Deps)


@agent.system_prompt
def get_system_prompt(ctx: RunContext[Deps]) -> str:
    return f"The customer is {ctx.deps.customer}."

# Run the agent
try:
    # Create a customer profile
    customer = Customer(customer_id=123, name="Jeremy Irons, Jr. II", email="john.doe@gmail.com", policy=Policy(policy_number=123456, policy_type="Auto", policy_status="Active", policy_deductable=500, policy_max_coverage=10000, policy_coverage_remaining=5000))
    
    # Create dependencies
    deps = Deps(customer=customer)
    
    question = "What is my deductable?"
    result = agent.run_sync(question, deps=deps)
    print(Fore.YELLOW, question)
    print(Fore.GREEN, f"Agent: {result.data.response}")
    print(Fore.GREEN, f"Customer reference: {result.data.customer.customer_id}")
    print(Fore.CYAN, f"Response type: {result.data.response_type}")
    print(Fore.RED, f"Escalation?: {result.data.escalation}")
    print('\n-----------------------------------\n')

    question = "If I already spent $7600, how much more can I be paid?"
    result = agent.run_sync(question, deps=deps)
    print(Fore.YELLOW, question)
    print(Fore.GREEN, f"Agent: {result.data.response}")
    print(Fore.GREEN, f"Customer reference: {result.data.customer.customer_id}")
    print(Fore.CYAN, f"Response type: {result.data.response_type}")
    print(Fore.RED, f"Escalation?: {result.data.escalation}")
    print('\n-----------------------------------\n')

    question = "Can I get a refund for the remaining coverage?"
    result = agent.run_sync(question, deps=deps)
    print(Fore.YELLOW, question)
    print(Fore.GREEN, f"Agent: {result.data.response}")
    print(Fore.GREEN, f"Customer reference: {result.data.customer.customer_id}")
    print(Fore.CYAN, f"Response type: {result.data.response_type}")
    print(Fore.RED, f"Escalation?: {result.data.escalation}")
    print('\n-----------------------------------\n')

    question = "I am not happy with your answers! Let me speak to your manager, please."
    result = agent.run_sync(question, deps=deps)
    print(Fore.YELLOW, question)
    print(Fore.GREEN, f"Agent: {result.data.response}")
    print(Fore.GREEN, f"Customer reference: {result.data.customer.customer_id}")
    print(Fore.CYAN, f"Response type: {result.data.response_type}")
    print(Fore.RED, f"Escalation?: {result.data.escalation}")
    print('\n-----------------------------------\n')
    
except ModelRetry as e:
    print(Fore.RED, e)
except Exception as e:
    print(Fore.RED, e)