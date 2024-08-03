import os
import glob
import pandas as pd
import re
from datetime import datetime, timedelta
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance as yf


end_date = datetime.now()
start_date = end_date - timedelta(days=7)


def get_security_code(security_name):
    result = df_merge.loc[df_merge['NAME OF COMPANY'] == security_name, 'SYMBOL']
    if not result.empty:
        return result.iloc[0]
    else:
        return "None"

def add_ns_suffix(value):
    return value + ".ns"

#function to get the price 
def fetch_end_of_day_price(ticker_symbol):
    try:
        stock_data = yf.download(ticker_symbol, period='1d')
        end_of_day_price = stock_data['Close'].iloc[-1]
        return end_of_day_price
    except Exception as e:
        print(f'unable to fetch{ticker_symbol}')
        return 0


def read_files():
    n = pd.read_csv(r"C:\Users\sumeet\Desktop\LargeDeals\NseLargeDeals")
    ClientSheet = pd.read_csv(r"C:\Users\sumeet\Desktop\LargeDeals\ClientNames.csv")
    sme_equity_df = pd.read_csv(r"C:\Users\sumeet\Desktop\LargeDeals\sme_equity.csv")
    equity_df = pd.read_csv(r"C:\Users\sumeet\Desktop\LargeDeals\equity.csv")
    
    return n,ClientSheet,sme_equity_df,equity_df

def tranformSheets(n,sme_equity_df,equity_df):
    n['date'] = pd.to_datetime(n['date'], format='%d-%b-%Y')
    n['date'] = n['date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    n['date']=n['date'].apply(lambda x:x.replace('-','/'))
    n = n.drop_duplicates()
    new_column_names = {
    'deal Date': 'date',
    'security NAME':'security_name',
    'buY/SELL': 'type',
    'quantity TRADED':'quantity',
    'trade PRICE/ WEIGHTED. AVG. PRICE':'price',
    'client NAME':'client_name'
    # Add more mappings as needed
    }
    # Use the rename() method to rename columns
    n = n.rename(columns=new_column_names)
    ####
    nse = n.iloc[:,[0,2,3,4,5,6]]
    # nse.info()
    nse['price'] = nse['price'].apply(lambda x: re.sub(r'[^\d.]', '', x))
    nse['price'] = nse['price'].astype(float)
    df_sme = sme_equity_df.iloc[:, :-5]
    df_equity = equity_df.iloc[:, :-6]

    new_column_names_for_stocks = {
    'NAME_OF_COMPANY': 'NAME OF COMPANY'
    }

    df_sme = df_sme.rename(columns=new_column_names_for_stocks)

    return nse,df_sme,df_equity


n,ClientSheet,sme_equity_df,equity_df = read_files()
nse,df_sme,df_equity = tranformSheets(n,sme_equity_df,equity_df)
df_merge = pd.concat([df_sme, df_equity], axis=0)

# This part is to filter out unique elements where the people only brought and sold the shares not on the same day

filtered_df = nse[~nse.groupby(['date', 'client_name'])['type'].transform(lambda x: x.nunique() == 2)]

# Now, filter out rows for each client where they bought and sold on the same day
result_df = filtered_df.groupby(['date','client_name']).filter(lambda x: len(x) < 2)

result_df['New code'] = result_df['security_name'].apply(get_security_code)
result_df['New code'] = result_df['New code'].apply(add_ns_suffix)#to add .ns to rate from yfinance
# result_df['last_price'] = result_df['New code'].apply(fetch_end_of_day_price) # to get the price from yfinance

# result_df_a = result_df[result_df['last_price']>=result_df['price']]

LessThan10_GreaterThan5 = result_df[(result_df['price'] > 5) & (result_df['price'] < 10)]
LessThan5_GreaterThan4 = result_df[(result_df['price'] < 5) & (result_df['price'] > 4)]
LessThan4_GreaterThan3 = result_df[(result_df['price'] < 4) & (result_df['price'] > 3)]
LessThan3_GreaterThan2 = result_df[(result_df['price'] < 3) & (result_df['price'] > 2)]
LessThan2 = result_df[(result_df['price'] < 2)]
LessThan20_GreaterThan10 = result_df[(result_df['price'] > 10) & (result_df['price'] < 20)]
LessThan30_GreaterThan20 = result_df[(result_df['price'] > 20) & (result_df['price'] < 30)]
GreaterThan30 = result_df[(result_df['price'] > 30)]
result_df['date'] = pd.to_datetime(result_df['date'])
LessThan10_GreaterThan5_1week = result_df[(result_df['price'] > 5) & (result_df['price'] < 10) & (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
LessThan5_GreaterThan4_1week = result_df[(result_df['price'] < 5) & (result_df['price'] > 4) & (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
LessThan4_GreaterThan3_1week = result_df[(result_df['price'] < 4) & (result_df['price'] > 3)& (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
LessThan3_GreaterThan2_1week = result_df[(result_df['price'] < 3) & (result_df['price'] > 2)& (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
LessThan2_1week = result_df[(result_df['price'] < 2)& (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
LessThan20_GreaterThan10_1week = result_df[(result_df['price'] > 10) & (result_df['price'] < 20)& (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
LessThan30_GreaterThan20_1week = result_df[(result_df['price'] > 20) & (result_df['price'] < 30)& (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
GreaterThan30_1week = result_df[(result_df['price'] > 30)& (result_df['date'] >= start_date) & (result_df['date'] <= end_date)]
TruestedNames = result_df[result_df['client_name'].isin(ClientSheet['Client_Name'])]

def generate_dataframe():
    return result_df

print(result_df)
# result_df_a.to_csv(r'C:\Users\sumeet\Desktop\LargeDeals\price.csv')

# a = result_df[result_df['New code']=='None.ns']
# print(a)

# a.shape
