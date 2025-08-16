import pandas as pd
from snownlp import SnowNLP

df = pd.read_excel(r"C:\Users\shino\Desktop\毕业论文\评论数据\HA.xlsx")
def get_sentiment_cn(df):
    s = SnowNLP(df)
    return s.sentiments

df["sentiment"] = df.comments.apply(get_sentiment_cn)
df.head()
round(df.sentiment.mean(),2)   #返回情感得分的均值
pos=0
neg=0
for i in df.sentiment:
    if i >=0.5:
        pos +=1
    else:
        neg +=1
print(f"积极的评论占比：{round(pos/len(df.comments)*100,2)}%")
print(f"消极的评论占比：{round(neg/len(df.comments)*100,2)}%")
