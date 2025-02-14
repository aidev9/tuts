import os
from dotenv import load_dotenv
from colorama import Fore
from pydantic_ai import Agent, RunContext, ModelRetry
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dataclasses import dataclass

load_dotenv()
# This example demonstrates how to use tools with dependencies in PydanticAI. The use case is a loan officer agent evaluating the credit-worthiness of an applicant and approving or denying a loan application. The agent is expected to take the applicant's information, evaluate the credit score, determine the loan amount, and provide a clear and helpful response.

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
    """Customer model - includes customer ID, full name, email, age, income, credit score, zip code, assets and debts."""
    customer_id: int
    name: str
    email: str
    age: int
    annual_income: int
    credit_score: int
    zip_code: int
    assets: int
    current_debts: int
    employment_status: str
    length_credit_history: int
    payment_history: str
    purpose: str
    loan_amount_requested: int
    collateral: str
    additional_info: str

class LoanDecision(BaseModel):
    """Support response model - includes customer, response type (Approved, Denied), response text, loan amount and term in months."""
    customer: Customer
    response_type: str
    response: str
    loan_amount: int
    term: int

@dataclass
class Deps:
    """Dependencies for the agent"""
    customer: Customer

# Define the agent
agent = Agent(model=model, result_type=LoanDecision, system_prompt="You are a loan officer for a lending institution. Your task is to take the customer's profile, use the credit risk tool to get a risk profile and determine if the requested loan should be approved. Provide a clear and helpful response. Ensure that your response is polite and addresses the customer's loan application effectively. Always include customer's name in your response. End your answer with Ref: Applicaiton ID. Get the customer from the provided context and the risk profile from the tools provided.", deps_type=Deps)

@agent.tool(retries=2)
async def get_customer_risk_profile(ctx: RunContext[Deps]) -> str:
    """Get the customer's risk profile based on provided information."""

    # Call the llm to get the customer's risk profile
    agent = Agent(model=model, result_type=str, system_prompt="Take the customer profile and return a risk profile for a loan application. The customer profile will be provided in the context.", deps_type=Deps)
    
    @agent.system_prompt
    def get_system_prompt(ctx: RunContext[str]) -> str:
        return f"The customer profile is {ctx.deps.customer}."
    
    result = await agent.run("Get the customer's risk profile.", deps=ctx.deps)
    print(Fore.BLUE, f"Customer risk profile: {result.data}")
    return f"The customer risk profile is: {result.data}"


# Run the agent
try:
    # Create a customer profile
    customer = Customer(customer_id=123, name="Michaela Resilient", email="m.resilient@gmail.com", age=35, annual_income=50000, credit_score=700, zip_code=20000, assets=30000, current_debts=50000, employment_status="Full-time", length_credit_history=10, payment_history="Good", purpose="Home improvement", loan_amount_requested=1000000, collateral="Home", additional_info="No recent credit inquiries")
    
    # Create dependencies
    deps = Deps(customer=customer)

    question = "Please evaluate the customer's loan application."
    result = agent.run_sync(question, deps=deps)

    print('\n-----------------------------------\n')
    print(Fore.GREEN, f"Agent: {result.data.response}")
    color = Fore.GREEN if result.data.response_type == "Approved" else Fore.RED
    print(color, f"Response type: {result.data.response_type}")
    print(color, f"Loan amount: {result.data.loan_amount}")
    print(color, f"Loan term (mos): {result.data.term}")
    print('\n-----------------------------------\n')

except ModelRetry as e:
    print(Fore.RED, e)
except Exception as e:
    print(Fore.RED, e)