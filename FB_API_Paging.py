import os
import json
import urllib
import pprint
import urllib.parse
import urllib.request
import pandas as pd
import ast
import datetime
from datetime import datetime
import numpy

#declare two panda dataframes
df=pd.DataFrame()
df2=pd.DataFrame()

# get Facebook access token
ACCESS_TOKEN ='EAACEdEose0cBAJTIvA6x7qDo58cKvtZARcCkALX0PfZCvpA9d3tLs0yUZBvMLGVIfrahq2REv85k1VlKZCiewMqPUjX6fuGiUsagyuE2AGC1SNuBXdF5CzrgFi4bUqGEC2vNGEVpHLBkIWsiN4jgz7w3k7eeyDw3GRHGxmS2q7IbLWUvmGAQkthFgvBSciYBFSBcvZCQPNwZDZD'
#build the URL for the API endpoint
host = "https://graph.facebook.com"
path = "/me/friends"
params = urllib.parse.urlencode({"access_token": ACCESS_TOKEN})

url = "{host}{path}?{params}&limit=2".format(host=host, path=path, params=params)
print(url)
# open the URL and read the response
resp = urllib.request.urlopen(url).read()


while True:
    
        resp = urllib.request.urlopen(url).read()
        me = json.loads(resp)
        if 'previous'  not in me['paging'].keys():
            #below line extracts only 'data' part from fetched JSON
            ext_only_data=me['data']
            #below line converts dict into pandas dataframe
            df=df.from_dict(ext_only_data, orient='columns')
            print(df)
            #fetch url for next page from current JSON
            url=me['paging']['next']
        else:
            if 'next' in me['paging'].keys():
                print("\n\nrohit")
                print(url)
                resp_1 = urllib.request.urlopen(url).read()
                me = json.loads(resp_1)
                #fetch url for next page from current JSON
                url=me['paging']['next']
                ext_only_data=me['data']
                #below line converts dict into pandas dataframe
                df2=df2.from_dict(ext_only_data, orient='columns')
                print(df2)
                #below line appends two pandas dataframes
                df=df2.append(df, ignore_index=True)
            else:
                 break
#Please put the fresh token from FB graph API before running the code                
#while loop will run till infinity
#First "if" checks if the fetched page is 1st page(as the first page will not
# have a link to previous)
#in outer else we check for subsequent pages until we do not encounter "next"(where we break
# the loop)
                


        


