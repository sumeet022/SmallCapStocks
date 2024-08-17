import pandas as pd
from datetime import datetime

output_path = r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap\TotalMcap.csv"

df = pd.read_csv(output_path)

grouped = df.groupby('code')

for code, group in grouped:
    group['marketCapFull'] = group['marketCapFull'].ffill().bfill()
    df.loc[group.index, 'marketCapFull'] = group['marketCapFull']

df.to_csv(output_path,index=False)


def calculate_rolling_avg(group):
    group['rolling_avg_10_days'] = group['marketCapFull'].rolling(window=10).mean()
    return group

# Convert the column to datetime
df['updatedOn'] = pd.to_datetime(df['updatedOn'], format='%d %b %y | %I:%M %p')
# Format the datetime to only include the date
df['updatedOn'] = df['updatedOn'].dt.strftime('%d %b %y')
df = df[['code', 'companyName', 'updatedOn', 'marketCapFull']]
df_unique = df.drop_duplicates(subset=['code', 'companyName', 'updatedOn', 'marketCapFull'],keep='first').reset_index(drop=True)
df_unique = df_unique[['code', 'companyName', 'updatedOn', 'marketCapFull']]
# a_grouped_sorted = a_unique.sort_values(by=['code','updatedOn']).reset_index(drop=True)
# a_grouped_sorted
df_unique['updatedOn'] = pd.to_datetime(df_unique['updatedOn'],errors='coerce')
df_grouped_sorted = df_unique.groupby('code',group_keys=False).apply(lambda x: x.sort_values('updatedOn',ignore_index=True)).reset_index(drop=True)
df_grouped_sorted = df_grouped_sorted.groupby('code',group_keys=False).apply(calculate_rolling_avg)
df_grouped_sorted.to_csv(r'C:\Users\sumeet\Desktop\LargeDeals\MarketCap\TotalMcap-ma.csv')
df.to_csv(output_path,index=False)