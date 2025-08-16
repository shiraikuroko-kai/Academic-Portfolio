# 问题三：网评文本的有效性分析 (版本：优化用户体验)
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np
from snownlp import SnowNLP
import jieba.posseg as pseg # 用于词性标注
import os
from tqdm import tqdm # 导入tqdm库

# 初始化tqdm，使其能与pandas的apply方法配合使用
tqdm.pandas()

# 确保输出文件夹存在
if not os.path.exists('output'):
    os.makedirs('output')
    print("已创建 'output' 文件夹。")


# 定义核心分析函数
def analyze_review_effectiveness(df, text_column):
    
    # 指标1: 文本长度 (此计算非常快，无需进度条)
    df['文本长度'] = df[text_column].astype(str).apply(len)
    print("指标1：文本长度 -> 计算完成。")

    # --- 情感强度计算 (加入tqdm进度条) ---
    def get_sentiment_strength(text):
        try:
            sentiment_score = SnowNLP(text).sentiments
            return abs(sentiment_score - 0.5)
        except ZeroDivisionError:
            return 0
    
    print("指标2：情感强度 -> 开始计算 (这可能需要几分钟)...")
    # 使用 .progress_apply() 来自动显示进度条
    df['情感强度'] = df[text_column].astype(str).progress_apply(get_sentiment_strength)
    print("指标2：情感强度 -> 计算完成。")

    # --- 信息密度计算 (加入tqdm进度条) ---
    def get_information_density(text):
        words = pseg.cut(text)
        nv_count = 0 # 名词和动词的数量
        total_words = 0
        for word, flag in words:
            if flag.startswith('n') or flag.startswith('v'):
                nv_count += 1
            total_words += 1
        return nv_count / total_words if total_words > 0 else 0

    print("指标3：信息密度 -> 开始计算 (这可能需要几分钟)...")
    # 再次使用 .progress_apply()
    df['信息密度'] = df[text_column].astype(str).progress_apply(get_information_density)
    print("指标3：信息密度 -> 计算完成。")
    
    # --- 归一化与综合评分 ---
    def min_max_normalize(series):
        # 避免因分母为0而产生的NaN或Inf错误
        if series.max() == series.min():
            return pd.Series(0.0, index=series.index)
        return (series - series.min()) / (series.max() - series.min())
    
    df['文本长度_归一化'] = min_max_normalize(df['文本长度'])
    df['情感强度_归一化'] = min_max_normalize(df['情感强度'])
    df['信息密度_归一化'] = min_max_normalize(df['信息密度'])
    print("所有指标归一化处理完成。")
    
    # 计算综合得分
    weights = {'length': 0.33, 'sentiment': 0.34, 'density': 0.33}
    df['有效性综合得分'] = (df['文本长度_归一化'] * weights['length'] + 
                           df['情感强度_归一化'] * weights['sentiment'] + 
                           df['信息密度_归一化'] * weights['density'])
    
    print("有效性综合得分计算完成。")

    return df.sort_values(by='有效性综合得分', ascending=False)


# 主执行流程

# --- 处理景区数据 ---
print("\n--- 开始分析景区评论有效性 ---")
try:
    df_spots = pd.read_excel('./data/景区评论.xlsx')
    
    # 调用核心函数进行分析
    df_spots_effectiveness = analyze_review_effectiveness(df_spots, '评论内容')
    
    print("\n景区评论有效性分析结果预览 (得分最高的前5条):")
    print(df_spots_effectiveness[['景区名称', '评论内容', '有效性综合得分']].head())

except FileNotFoundError:
    print("错误：未在 'data' 文件夹中找到 '景区评论.xlsx'。请检查文件是否存在。")
    df_spots_effectiveness = pd.DataFrame()

# --- 处理酒店数据 ---
print("\n--- 开始分析酒店评论有效性 ---")
try:
    df_hotels = pd.read_excel('./data/酒店评论.xlsx')

    # 调用核心函数进行分析
    df_hotels_effectiveness = analyze_review_effectiveness(df_hotels, '评论内容')

    print("\n酒店评论有效性分析结果预览 (得分最高的前5条):")
    print(df_hotels_effectiveness[['酒店名称', '评论内容', '有效性综合得分']].head())

except FileNotFoundError:
    print("错误：未在 'data' 文件夹中找到 '酒店评论.xlsx'。请检查文件是否存在。")
    df_hotels_effectiveness = pd.DataFrame()


# 保存结果到指定的Excel文件
output_filename_3 = './output/评论有效性分析表.xlsx'

try:
    with pd.ExcelWriter(output_filename_3) as writer:
        if not df_spots_effectiveness.empty:
            df_spots_effectiveness.to_excel(writer, sheet_name='景区评论有效性', index=False)
        if not df_hotels_effectiveness.empty:
            df_hotels_effectiveness.to_excel(writer, sheet_name='酒店评论有效性', index=False)
    
    print(f"\n处理完成！评论有效性分析结果已成功保存至: {output_filename_3}")

except Exception as e:
    print(f"\n保存文件时出错: {e}")
