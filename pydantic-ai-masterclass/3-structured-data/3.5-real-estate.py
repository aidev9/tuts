import datetime
import os
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Define the output models
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class PropertyFeatures(BaseModel):
    bedrooms: int
    bathrooms: int
    square_footage: float
    lot_size: float  # in acres, but we can convert to sqft if needed

class AdditionalInfo(BaseModel):
    price: float
    listing_agent: str
    last_updated: datetime.date

class Property(BaseModel):
    address: Address
    info: AdditionalInfo
    type: str  # Single Family Home
    mls_id: int
    features: PropertyFeatures
    garage_spaces: int

# Define the agent
agent = Agent(model=model, result_type=Property, system_prompt=f'You are a real estate agent specialized in creating and parsing property listings in the US. Parse the following property listing and extract the address, type, MLS ID, features, and garage spaces. The listing is for a single-family home located at 47516 Anchorage Cir, Sterling, VA 20165. The property has 4 bedrooms, 3.5 bathrooms, 2,500 sqft, and a 0.25-acre lot. The listing price is $500,000, and the listing agent is John Doe. The listing was last updated on 2022-03-01.', retries=3)

# Run the agent
result = agent.run_sync("Parse the listing")
logfire.notice('Text parse LLM results: {result}', result = str(result.data))
logfire.info('Result type: {result}', result = type(result.data))

# Function to scrape HTML into markdown
async def html_to_markdown(url, output_path):
    browser = await launch(headless=True)
    requestHeaders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/',
    }
    page = await browser.newPage()
    await stealth(page)  # <-- Here
    await page.setExtraHTTPHeaders(requestHeaders)
    await page.goto(url, {'waitUntil': 'load'})
    content = await page.content()
    soup = BeautifulSoup(content, 'lxml')
    markdown = convert_to_markdown(str(soup))
    # Write the markdown to a file
    with open(output_path, 'w') as f:
        f.write(markdown)
    await browser.close()

# Get the real estate data
# url = 'https://www.redfin.com/VA/Sterling/47516-Anchorage-Cir-20165/home/11931811'
# url = 'https://www.zillow.com/homedetails/845-Sea-Ranch-Dr-Santa-Barbara-CA-93109/15896664_zpid'
url = 'https://www.homes.com/property/1803-fernald-point-ln-santa-barbara-ca/9wr35zkk9mxjq'
output_path = 'data/property.md'
asyncio.new_event_loop().run_until_complete(html_to_markdown(url, output_path))

# Read the markdown file
with open('data/property.md', 'r') as file:
    property_data = file.read()

# Run the agent
result = agent.run_sync(f"Can you extract the following information from the property listing? The raw data is {property_data}")
logfire.notice('Property markdown prompt LLM results: {result}', result = str(result.data))
logfire.info('Result type: {result}', result = type(result.data))