from bsedata.bse import BSE
import pandas as pd
import re

n = pd.read_csv(r"C:\Users\sumeet\Desktop\LargeDeals\MarketCap\BseStocks.csv")

n['code']=n['code'].astype('str')


# n.info()

b = BSE()

def get_date(x,b):
    try:
        q = b.getQuote(x)
        c=q['updatedOn']
        return c
    except Exception as e:
        return 'n/a'
def get_marketCapFull(x,b):
    try:    
        q = b.getQuote(x)
        d=q['marketCapFull']
        return d
    except Exception as e:
        return 'n/a'
    
def get_marketCapFreeFloat(x,b):
    try:
        q = b.getQuote(x)
        e=q['marketCapFreeFloat']
        return e
    except Exception as e:
        return 'n/a'
    
def substitute_example(input_text):
    if isinstance(input_text, str):  # Check if the value is a string
        return input_text.replace("Cr.", "")
    else:
        return None
    

# Example for REGEXREPLACE-like functionality
def regex_replace_example(input_text):
    if isinstance(input_text, str):  # Check if the value is a string
        return re.sub(r"[^0-9.]", "", input_text)
    else:
        return None
    

n['updatedOn'] = n['code'].apply(lambda x: pd.Series(get_date(x,b)))
n['marketCapFull'] = n['code'].apply(lambda x: pd.Series(get_marketCapFull(x,b)))
n['marketCapFreeFloat'] = n['code'].apply(lambda x: pd.Series(get_marketCapFreeFloat(x,b)))
n['marketCapFull'] = n['marketCapFull'].apply(substitute_example)
n['marketCapFull'] = n['marketCapFull'].apply(regex_replace_example)

print(n.head())
# print(market_cap)
# a[['Date', 'marketCapFull', 'marketCapFreeFloat']] = market_cap

# n[['Date', 'marketCapFull', 'marketCapFreeFloat']] = n['code'].apply(lambda x: get_marketCap(x))

n.to_csv(r'C:\Users\sumeet\Desktop\LargeDeals\BseStocks-11.csv')



# b = BSE()
# # b = BSE(update_codes = True)
# q = b.getQuote('500002')
# print(q)
# print(q['marketCapFull'])
# print(q['updatedOn'])
# print(q['marketCapFreeFloat'])
# b.updateScripCodes()
# stocks = b.getScripCodes()

# stocks = pd.DataFrame(stocks,index=[0])
# stocks.to_csv(r'C:\Users\sumeet\Desktop\LargeDeals\BseStocks.csv')

