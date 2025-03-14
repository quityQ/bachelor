"""
dataset module to created the basic datesets from the scraped data
datasets are concatintion of all available data there is no cleaning or preprocessing done
"""
import pandas as pd
import os
import glob


# Function to create dataset from the scraped data
# The function takes the directory name inside the data folder as the argument
def create_dataset(dir, distressed_dir):
    if not (os.path.isdir(f"data/{dir}") and os.path.isdir(f"data/{distressed_dir}")):
        print(f"Directory does not exist")
        return

    df = pd.DataFrame()
    df_distressed = pd.DataFrame()

    file_list = glob.glob(rf".\data\{dir}\*.json")

    dfs = []  # an empty list to store the data frames
    for file in file_list:
        data = pd.read_json(file)
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)
    df['distressed'] = 0

    file_list = glob.glob(rf".\data\{distressed_dir}\*.json")

    dfs = []  # an empty list to store the data frames
    for file in file_list:
        data = pd.read_json(file)
        dfs.append(data)

    df_distressed = pd.concat(dfs, ignore_index=True)
    df_distressed['distressed'] = 1

    df = pd.concat([df, df_distressed], ignore_index=True)

    df.to_csv(f"datasets/{dir}.csv")


"""create_dataset("balance_sheets", "distressed_balance_sheets")
create_dataset("cash_flow_statements", "distressed_cash_flow_statements")
create_dataset("income_statements", "distressed_income_statements")"""


# function to create a full dataset from the individual datasets
def create_full_dataset():
    df = pd.DataFrame()
    df_bs = pd.read_csv("datasets/balance_sheets.csv")
    df_cf = pd.read_csv("datasets/cash_flow_statements.csv")
    df_is = pd.read_csv("datasets/income_statements.csv")

    df = pd.merge(df_bs, df_cf, on=['symbol', 'date'], how='outer')
    df = pd.merge(df, df_is, on=['symbol', 'date'], how='right')

    df.to_csv("datasets/full_raw_dataset.csv")


def clean_full_dataset():
    df = pd.read_csv("datasets/full_raw_dataset.csv")

    # drop unnecessary columns
    df = df.drop(columns=["Unnamed: 0.1", "Unnamed: 0_x", "Unnamed: 0_y", "Unnamed: 0", "cik", "cik_y", "cik_x", "fillingDate", "fillingDate_x", "fillingDate_y",
                          "acceptedDate", "acceptedDate_x", "acceptedDate_y", "link", "link_x", "link_y", "finalLink", "finalLink_x", "finalLink_y", "distressed_y", "distressed_x", "period", "period_x", "period_y"])

    # rename currency columns
    df.rename(columns={"reportedCurrency_x": "currency_balance_sheet", "reportedCurrency_y":
              "currency_cash_flow_statement", "reportedCurrency": "currency_income_statement"}, inplace=True)

    # combine calendarYears to one column
    df['Year'] = df['calendarYear'].combine_first(
        df['calendarYear_x']).combine_first(df['calendarYear_y'])
    df = df.drop(columns=["calendarYear", "calendarYear_x", "calendarYear_y"])

    # rename inventory columns
    df.rename(columns={"inventory_x": "inventory_balance_sheet",
              "inventory_y": "inventory_cash_flow_statement"}, inplace=True)

    # rename netIncome columns
    df.rename(columns={"netIncome_x": "netIncome_cash_flow_statement", "netIncome_y": "netIncome_income_statement",
              "netIncomeRatio": "netIncomeRatio_income_statement"}, inplace=True)

    # rename depreciationAndAmortization columns
    df.rename(columns={"depreciationAndAmortization_x": "depreciationAndAmortization_cash_flow_statement",
              "depreciationAndAmortization_y": "depreciationAndAmortization_income_statement"}, inplace=True)

    df.to_csv("datasets/full_cleaned_dataset.csv")
