import jieba  
import jieba.posseg
import jieba.analyse


#设置停用词库
jieba.load_userdict(r'自行设置')#加载外部 用户词典
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  # 停用词List的创建
    return stopwords
    
# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist(r'C:\Users\shino\Desktop\1.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
#                 outstr += " "
    return outstr
    
# 词性标注
def pos_sentence(sentence):
    sentence_seged = jieba.posseg.cut(sentence)
    outstr = ''
    for x in sentence_seged:
        outstr += "{}/{}  ".format(x.word, x.flag)
    return outstr
    
    

inputs = open(r'C:\Users\shino\Desktop\1.txt', 'r', encoding='utf-8')  # 这里加载待分词文本注意路径是相对路径,转成utf-8格式
outputs = open(r'C:\Users\shino\Desktop\1.txt', 'w', encoding='utf-8')  # 这里加载待装入文本注意路径是相对路径，转成utf-8格式
for line in inputs:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    pos_seg = pos_sentence(line_seg)
    outputs.write(pos_seg + '\n')
outputs.close()
inputs.close()
print("分词完毕")
