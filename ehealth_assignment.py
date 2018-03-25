import pandas as pd
import ast
import datetime
from datetime import datetime
df_full=pd.DataFrame()
df=pd.DataFrame()
m=pd.read_csv('C:\Personal\Python\data.csv',parse_dates=True, dayfirst=True)
partial=(m['Purchase'])
leng=len(partial.index)
print(leng)
for i in range(0,leng-1):
     #partial[i]=ast.literal_eval(partial[i])
     df=pd.DataFrame(ast.literal_eval(partial[i]))
     df['InvoiceNo'] = m['InvoiceNo'][i]
     df_full=pd.concat([df_full,df],ignore_index='true')
#print(df_full

# cleanse 'Date Column'

for i in range(0,leng-1):
    isbn=m['Date'][i]
    if isbn.isdigit():
        isbn = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(isbn) - 2)
        m['Date'][i]=pd.to_datetime(isbn)
    else:
        m['Date'][i]=pd.to_datetime(isbn)
