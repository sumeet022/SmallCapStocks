from bsedata.bse import BSE
import pandas as pd

# n.info()

b = BSE()
q = b.getQuote('500002')
print(q)
