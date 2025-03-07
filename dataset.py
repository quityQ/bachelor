"""
dataset module to created the basic dateset from the scraped data
datasets are concatintion of all available data there no cleaning or preprocessing done

"""
import pandas as pd
import os
import glob


# Function to create dataset from the scraped data
# The function takes the directory name inside the data folder as the argument
def create_dataset(dir):
    if not os.path.isdir(f"data/{dir}"):
        print(f"Directory {dir} does not exist")
        return
    
    df = pd.DataFrame()

    file_list = glob.glob(rf".\data\{dir}\*.json")

    dfs = [] # an empty list to store the data frames
    for file in file_list:
        data = pd.read_json(file)
        dfs.append(data)

    df = pd.concat(dfs, ignore_index=True)

    df.to_csv(f"datasets/{dir}.csv")
    

create_dataset("balance_sheets")
create_dataset("cash_flow_statements")
create_dataset("income_statements")