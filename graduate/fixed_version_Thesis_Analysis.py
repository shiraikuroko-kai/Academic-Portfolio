import pandas as pd
import numpy as np
import re
import jieba
import jieba.posseg as pseg
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import warnings
from gensim import corpora, models
from tqdm import tqdm

# 初始化设置
warnings.filterwarnings("ignore", category=DeprecationWarning) 
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False
tqdm.pandas()

print(">>> 库导入完成。\n")

# ===========================================================================

# --- 数据加载与预处理 ---
print(">>> 步骤 2: 加载并预处理数据...")

try:
    # 假设您的真实数据保存在这两个文件中
    df_hhl = pd.read_csv('./data/黄鹤楼_reviews.csv')
    df_gf = pd.read_csv('./data/龟峰_reviews.csv')
    
    # 添加来源标识并合并
    df_hhl['景点名称'] = '黄鹤楼'
    df_gf['景点名称'] = '龟峰'
    df = pd.concat([df_hhl, df_gf], ignore_index=True)
    
    # 基础清洗
    df.dropna(subset=['content', 'date'], inplace=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce') # errors='coerce'会将无法解析的日期变为NaT
    df.dropna(subset=['date'], inplace=True) # 删除无法解析的日期行
    df['content'] = df['content'].astype(str)
    
    print(f"--> 数据加载与预处理成功。总计 {len(df)} 条有效评论。")
    print("--> 数据样本预览:")
    print(df.sample(5))

except FileNotFoundError:
    print("!!! 错误：请确保在'/data/'文件夹下，存在'黄鹤楼_reviews.csv'和'龟峰_reviews.csv'这两个数据文件。")
    df = pd.DataFrame() # 创建空DataFrame以避免后续报错

print("\n")
    
# ===========================================================================

# --- 情感演化分析 ---
if not df.empty:
    print(">>> 步骤 3: 开始进行情感演化分析 (此过程可能需要几分钟)...")

    # 计算情感分数，并使用tqdm显示进度条
    df['sentiment'] = df['content'].progress_apply(lambda x: SnowNLP(x).sentiments)

    # 按月对每个景点进行分组，并计算月平均情感
    df_monthly_sentiment = df.set_index('date').groupby(['景点名称', pd.Grouper(freq='M')])['sentiment'].mean().reset_index()

    # 绘制情感演化图
    plt.figure(figsize=(15, 7))
    for name, group in df_monthly_sentiment.groupby('景点名称'):
        plt.plot(group['date'], group['sentiment'], marker='o', linestyle='-', label=name)

    plt.title('黄鹤楼 vs 龟峰：游客月平均情感演化趋势', fontsize=16)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('情感得分 (0=负面, 1=正面)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    print("--> 情感演化图已生成，请在下方查看。")
    plt.show()
else:
    print(">>> 步骤 3: 跳过情感演化分析（因为数据加载失败）。")
    
print("\n")
    
# ===========================================================================

# --- 主题建模与对比---
if not df.empty:
    print(">>> 步骤 4: 开始进行LDA主题建模...")

    # 加载停用词
    try:
        with open('./stopwords/hit_stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = [line.strip() for line in f.readlines()]
        print("--> 停用词加载成功。")
    except FileNotFoundError:
        print("!!! 警告：未找到停用词文件，模型效果可能受影响。")
        stopwords = []

    # 定义文本预处理函数
    def preprocess_for_lda(text):
        # 使用词性标注，只保留名词和动词
        words = pseg.cut(text)
        return [word for word, flag in words if (flag.startswith('n') or flag.startswith('v')) and word not in stopwords and len(word) > 1]

    # 定义LDA模型训练和打印函数
    def train_and_print_topics(corpus, num_topics=4, num_words=5):
        dictionary = corpora.Dictionary(corpus)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in corpus]
        ldamodel = models.LdaModel(doc_term_matrix, num_topics=num_topics, id2word=dictionary, passes=25, random_state=42)
        
        print(f"\n--> 提取出的 {num_topics} 个核心主题:")
        topics = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
        for idx, topic in topics:
            print(f"    主题 #{idx+1}: {topic}")
        return ldamodel

    # --- 黄鹤楼主题分析 ---
    print("\n--- 正在分析【黄鹤楼】的核心主题 ---")
    hhl_corpus = df[df['景点名称'] == '黄鹤楼']['content'].progress_apply(preprocess_for_lda).tolist()
    train_and_print_topics(hhl_corpus)

    # --- 龟峰主题分析 ---
    print("\n--- 正在分析【龟峰】的核心主题 ---")
    gf_corpus = df[df['景点名称'] == '龟峰']['content'].progress_apply(preprocess_for_lda).tolist()
    train_and_print_topics(gf_corpus)
else:
    print(">>> 步骤 4: 跳过主题建模分析（因为数据加载失败）。")
print("\n>>> 所有分析已执行完毕。")
# ===========================================================================
