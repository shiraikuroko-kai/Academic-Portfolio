import jieba
from jieba.analyse import *
import pandas as pd

sent='中文分词是文本处理不可或缺的一步!'
#全模式：把句子中所有可以成词的词语都扫描出来，速度非常快，但是不能解决歧义
seg_list = jieba.cut(sent, cut_all=True)
print('全模式：000','/ '.join(seg_list))
#精确模式：试图将句子最精确地切开，适合文本分析
seg_list = jieba.cut(sent, cut_all=False)
print('精确模式：','/ '.join(seg_list))
seg_list = jieba.cut(sent)
print('默认精确模式：','/ '.join(seg_list))
#搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
seg_list = jieba.cut_for_search(sent)
print('搜索引擎模式：','/ '.join(seg_list))


wfile =r"C:\Users\shino\Desktop\1.txt"
with open(r"C:\Users\shino\Desktop\1.txt",encoding='UTF-8') as f:
    data = f.read()
    for keyword, weight in extract_tags(data, withWeight=True):
        print('%s %r' % (keyword, weight))


data = pd.read_csv(r'C:\Users\shino\Desktop\汇总 (转UTF-8）\汇总\BV1T5411s74c.csv',usecols=['dm_text'])
data = str(data)
for keyword, weight in extract_tags(data, withWeight=True): 
    print('%s %r' % (keyword, weight))
