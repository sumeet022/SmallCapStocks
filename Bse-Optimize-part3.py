import pandas as pd

output_path = r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap\TotalMcap.csv"

df = pd.read_csv(output_path)

grouped = df.groupby('code')

for code, group in grouped:
    group['marketCapFull'] = group['marketCapFull'].fillna(method='ffill').fillna(method='bfill')
    df.loc[group.index, 'marketCapFull'] = group['marketCapFull']

df.to_csv(output_path,index=False)