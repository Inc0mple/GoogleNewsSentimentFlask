from GoogleNews import GoogleNews
import pandas as pd
import newspaper

googlenews = GoogleNews(lang='en',start='02/28/2013')
googlenews.get_news('Malaysia')
result=googlenews.result()
df=pd.DataFrame(result)
df.to_csv("output.csv",index=False)
print(df.head())

googlenews.clear()