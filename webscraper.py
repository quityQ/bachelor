"""
Webscraper for the Website https://site.financialmodelingprep.com/ and companiesmarketcap.com

finacialmodeelingprep provides Income statement, cashflowo statement and balance sheet for many companies
Each can be downloaded as a csv file, the following code should help ease the process of downloading the files
The free tier of the API only provides US-Data, we wish to download data for Swiss companies

companiesmarketcap provides historical data of the marketcap of companies
the data must be scraped from the website
"""

import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

"""
The following functions are used to download the income statement, cash flow statement and balance sheet of companies
The data is stored in the data folder in the respective subfolders as json files
"""
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
    
    companies = pd.read_csv("data\equity_issuers.csv", delimiter=";", encoding = "ISO-8859-1") #encoding is necessary to match the encoding of the source file
    
    for i, row in companies.iterrows():
        ticker = row["Symbol"] + ".SW" #add .SW since FMP stores swiss comapneis as such
        name = row["Company"]
        
        get_income_statement(ticker, name)
        get_cash_flow_statement(ticker, name)
        get_balance_sheet_statement(ticker, name)

"""
The following funcitons are used to download the income statement, cash flow statement and balance sheet of companies that are from the distressed source file
These are separated just to make saving them to another place easier
"""

def get_distressed_income_statement(ticker, name):
    url = f"https://marketplace.financialmodelingprep.com/public/income-statement/{ticker}?period=annual&limit=4&apikey="
        
    response = requests.get(url)
    
    with open(f"data\distressed_income_statements\{name}_income_statement.json", "w") as f:
        json.dump(response.json(), f)

def get_distressed_cash_flow_statement(ticker, name):
    url= f"https://marketplace.financialmodelingprep.com/public/cash-flow-statement/{ticker}?period=annual&limit=4&apikey="

    response = requests.get(url)

    with open(f"data\distressed_cash_flow_statements\{name}_cash_flow_statement.json", "w") as f:
        json.dump(response.json(), f)

def get_distressed_balance_sheet_statement(ticker, name):
    url = f"https://marketplace.financialmodelingprep.com/public/balance-sheet-statement/{ticker}?period=annual&limit=4&apikey="

    response = requests.get(url)

    with open(rf"data\distressed_balance_sheets\{name}_balance_sheet_statement.json", "w") as f: #rf so that \b isnt interpreted as a backspace
        json.dump(response.json(), f)

def get_distressed_statements():

    companies = pd.read_csv("data\distressed_companies.csv", delimiter=";", encoding = "ISO-8859-1")

    for i, row in companies.iterrows():
        ticker = row["Symbol"] + ".SW"
        name = row["Company"]

        get_distressed_income_statement(ticker, name)
        get_distressed_cash_flow_statement(ticker, name)
        get_distressed_balance_sheet_statement(ticker, name)

"""
The following functions are used to download the marketcap of companies
The data is stored in the data folder as csv files
"""

def get_marketcap(filename):
    
    companies = pd.read_csv(f"data\{filename}", delimiter=";", encoding = "ISO-8859-1")
    cleancompanies = companies.dropna(subset=["marketcap_url"]) 
    
    for i, row in cleancompanies.iterrows():
        url = row["marketcap_url"]
        name = row["Symbol"]
        marketcap_scraper(url, name)
        
def marketcap_scraper(url, name):
    response = requests.get(url)   

    if response.status_code != 200:
        print("Failed to connect")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'table'})
            
    rows = []
    for row in table.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        if len(cells) > 0:
            rows.append([cell.text.strip() for cell in cells])
            
    df = pd.DataFrame(rows)
        
    df.to_csv(f"data/market_caps/{name}_market_cap.csv", header=None, index=None)