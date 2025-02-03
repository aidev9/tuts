from __future__ import annotations as _annotations
from dataclasses import dataclass, field
from typing import Union
import yfinance as yf
import json
import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from models import Address, StockData
# Load the environment variables
load_dotenv()

symbol = "MSFT"

dat = yf.Ticker(symbol)
result = None

if dat:
    result = StockData(
        symbol=dat.info['symbol'],
        industry=dat.info['industry'],
        sector=dat.info['sector'],
        company_name=dat.info['longName'],
        address=Address(
            street_1=dat.info['address1'],
            street_2=None,
            city=dat.info['city'],
            state=dat.info['state'],
            postal_code=dat.info['zip'],
            country=dat.info['country'],
        ),
        website=dat.info['website'],
        balance_sheet=dat.get_balance_sheet(as_dict=True, pretty=False),
        cash_flow=dat.get_cash_flow(as_dict=True, pretty=False),
        financials=dat.get_financials(as_dict=True, pretty=False),
        earnings=dat.get_income_stmt(as_dict=True),
        news=dat.get_news()
    )

    if 'address2' in dat.info.keys():
        result.address.street_2 = dat.info['address2']

else:
    print("No data found for %s" % symbol)

print(result)