from __future__ import annotations as _annotations
from dataclasses import dataclass, field
from enum import Enum
from pydantic_ai.messages import ModelMessage

# Product class
@dataclass
class Stock:
    symbol: str
    report: str
    keywords: list[str]
    num_rounds: int = 0

# Decision enum
class Choice(Enum):
    buy = 'Buy'
    skip = 'Skip'

# Decision model 
@dataclass
class Decision:
    """Decision model - includes sentiment and decision. Sentiment is a value between -100 and 100. Decision is a one-word string value of 'Buy' or 'Skip'. Explanation is a short paragraph explaining the decision."""
    sentiment: int
    decision: Choice # buy or skip
    explanation: str

# Debate argument model
@dataclass
class Argument:
    """Argument model - includes sentiment and body. Sentiment is a value between -100 and 100. Body is a  paragraph explaining the argument for or against the product and provides the reasons."""
    sentiment: int
    body: str

# Graph state
@dataclass
class State:
    stock: Stock
    messages: list[ModelMessage] = field(default_factory=list)
    num_rounds: int = 0
    sentiment: int = 0

# Address class
@dataclass
class Address:
    street_1: str
    street_2: str
    city: str
    state: str
    postal_code: str
    country: str

# Product class
@dataclass
class StockData:
    symbol: str
    industry: str
    sector: str
    company_name: str
    address: Address
    website: str
    balance_sheet: dict
    cash_flow: dict
    financials: dict
    earnings: dict
    news: list

    def generate_markdown_table_header (self, data: dict) -> str:
        """
        Generate a markdown table header from a dictionary
        """
        header = "| |"
        div = "|-----------------|"

        for key in data.keys():
            header += " %s |" % key
            div += "-----------------|"

        header += "\n" + div

        return header
    
    def generate_markdown_table_row (self, data: dict) -> [str]:
        result = []

        for k1 in data[list(data.keys())[0]].keys():
            row = "|" + k1

            for k2 in data.keys():
                row += " | %s " % str(data[k2][k1])

            row += " |"

            result.append(row)

        return result
    
    def generate_markdown_table (self, data: dict) -> str:      
        header = self.generate_markdown_table_header(data)
        rows = self.generate_markdown_table_row(data)
        
        return header + "\n" + "\n".join(rows)
    
    def generate_markdown (self, template) -> str:
        """
        Generate a markdown report from the StockData object
        """
        return template.render(data=self)