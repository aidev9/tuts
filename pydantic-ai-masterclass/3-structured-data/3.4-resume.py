import os
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output model
class Experience(BaseModel):
    company: str = Field(..., description="The name of the company.")
    position: str = Field(..., description="The job title held at the company.")
    start_date: str = Field(..., description="The date when you started working at the company.")
    end_date: str = Field(..., description="The date when you left the company. If still employed, use 'Present'.")

class Education(BaseModel):
    institution_name: str = Field(..., description="The name of the educational institution.")
    degree: str = Field(..., description="The degree obtained from the institution.")
    start_date: str = Field(..., description="The date when you started attending school at the institution.")
    end_date: str = Field(..., description="The date when you graduated. If still enrolled, use 'Present'.")

class Resume(BaseModel):
    full_name: str = Field(..., description="The full name of the person on the resume.")
    contact_email: str = Field(..., description="The email address for contacting the person.")
    phone_number: str = Field(..., description="The phone number for contacting the person.")
    
    summary: str = Field(..., description="A brief summary of the person's career highlights.")

    experience: list[Experience] = Field([], description="List of experiences held by the person.")
    education: list[Education] = Field([], description="List of educational institutions attended by the person.")
    
    skills: list[str] = Field([], description="Skills possessed by the person.")
    certifications: list[str] = Field([], description="Certifications obtained by the person.")

# Define the agent
agent = Agent(model=model, result_type=Resume, system_prompt=f'You are a technical writer and an HR expert specialized in writing resumes. Write a resume for a Software Engineer with 20 years of progressive experience, mostly on the US West Coast, spanning companies such as Google, Netflix and Tesla. Make it look good for recruiters and hiring managers. It must pass ATS systems and be visually appealing. Include a summary, experience, education, skills, and certifications. Include a minimum of 10 work experiences with real companies. The resume must be at least 5 pages long. Include critical details on projects and responsibilities during employment.')

# Run the agent
result = agent.run_sync("Wrtie a resume.")
logfire.notice('Results from LLM: {result}', result = str(result.data))
logfire.info('Result type: {result}', result = type(result.data))

# Read the markdown file
with open('data/resume.md', 'r') as file:
    resume_data = file.read()

# Run the agent
result = agent.run_sync(f"Can you extract the following information from the resume? The raw data is {resume_data}")
logfire.notice('Resume markdown prompt LLM results: {result}', result = str(result.data))
logfire.info('Result type: {result}', result = type(result.data))