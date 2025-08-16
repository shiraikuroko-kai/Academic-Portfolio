from snownlp import SnowNLP
# 文本
text = u'好文，已收藏，学习的道路上一起进步，也期待你的关注与支持！'
text1= u'学术垃圾，已拉黑，不如不学，我要点踩再退出！'
# 分析
s = SnowNLP(text)
c = SnowNLP(text1)
# 输出情绪为积极的概率
print(s.sentiments)
print(c.sentiments)


def is_positive(text):
    # 将文本编码为unicode
    s = SnowNLP(text)

    if s.sentiments < 0.8:
        return False
    else:
        return True

# 测试函数
if is_positive(u"还不点个收藏，关注！"):
    print("文本很积极！")

#解析繁体字    
s = SnowNLP(u"繁體字")
print(s.han)

#将文字用标点符号分割，返回列表。
s = SnowNLP(u"学习的道路上一起进步，加油！")
print(s.sentences)

#返回文本的关键词，可以指定返回数量。这里引用了一部分某度百科对“自然语言处理”的解释：
text = u"""自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
           它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
           自然语言处理是一门融语言学、计算机科学、数学于一体的科学。"""
s = SnowNLP(text)
print(s.keywords(5))  # 输出5个关键词



#使用例
import pandas as pd
from snownlp import SnowNLP
data = pd.read_csv(r'C:\Users\shino\Desktop\汇总 (转UTF-8）\汇总\BV1T5411s74c.csv',usecols=['dm_text'])
data = str(data)
s = SnowNLP(data)
print(s.keywords(10))#关键词的数量
