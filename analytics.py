# %%
import pandas as pd
import json
# %%
df=pd.read_csv("files/20220226",delimiter="|",header=None)
df.columns='a b c'.split()
df.dropna(inplace=True)
df['d']=df['c'].apply(lambda data: json.loads(data)['totalBuyQty'])
df['e']=df['c'].apply(lambda data: json.loads(data)['totalSellQty'])
# %%
df2=df.groupby("b").mean()
df2['f']=df2.d/df2.e
df2.sort_values('f',ascending=False).head(20)
# %%
