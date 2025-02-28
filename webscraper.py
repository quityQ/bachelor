"""
Webscraper for the Website https://site.financialmodelingprep.com/
finacialmodeelingprep provides Income statement, cashflowo statement and balance sheet for many companies
Each can be downloaded as a csv file, the following code should help ease the process of downloading the files

The free tier of the API only provides US-Data, we wish to download data for Swiss companies
"""

import requests
import json
import csv
import pandas as pd
import os

def get_income_statement(ticker, name):
    url = f"https://marketplace.financialmodelingprep.com/public/income-statement/{ticker}?period=annual&limit=4&apikey="
        
    response = requests.get(url)
    
    with open(f"data\income_statements\{name}_income_statement.json", "w") as f:
        json.dump(response.json(), f)
        
def get_cash_flow_statement(ticker, name):
    url= f"https://marketplace.financialmodelingprep.com/public/cash-flow-statement/{ticker}?period=annual&limit=4&apikey="
    
    response = requests.get(url)
    
    with open(f"data\cash_flow_statements\{name}_cash_flow_statement.json", "w") as f:
        json.dump(response.json(), f)

def get_balance_sheet_statement(ticker, name):
    url = f"https://marketplace.financialmodelingprep.com/public/balance-sheet-statement/{ticker}?period=annual&limit=4&apikey="
    
    response = requests.get(url)
    
    with open(rf"data\balance_sheets\{name}_balance_sheet_statement.json", "w") as f: #rf so that \b isnt interpreted as a backspace
        json.dump(response.json(), f)

def get_statements():
    
    companies = pd.read_csv("data\companies.csv", delimiter=";")
    
    for i, row in companies.iterrows():
        ticker = row["ticker"]
        name = row["name"]
        
        get_income_statement(ticker, name)
        get_cash_flow_statement(ticker, name)
        get_balance_sheet_statement(ticker, name)
        
        

    
get_statements()