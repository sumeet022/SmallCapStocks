import os
import pandas as pd

folder_path = r'C:\Users\sumeet\Desktop\LargeDeals\MarketCap\TotalMcap'

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    df['updatedOn'] = df['updatedOn'].fillna(method='ffill')
    df.to_csv(file_path, index=False)

dataframes = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]

combined_df = pd.concat(dataframes, ignore_index=True)

output_path = r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap\TotalMcap.csv"

combined_df.to_csv(output_path, index=False)