# 问题二：景区及酒店的综合评价
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

# 定义核心模型函数 - 熵权法 (Entropy Weight Method)

def entropy_weight_method(d
    
    # 数据归一化
    # 为避免log(0)错误，加上一个极小值
    df_normalized = (df_scores + 1e-10) / (df_scores.sum(axis=0) + 1e-9)
    
    # 计算每个指标的信息熵
    k = -1 / np.log(len(df_scores))
    # p * log(p)，如果p为0，则结果为0
    entropy = k * (df_normalized * np.log(df_normalized)).sum(axis=0)
    
    # 计算信息冗余度 (或差异系数)
    redundancy = 1 - entropy
    
    # 计算各指标的权重 (归一化冗余度)
    weights = redundancy / redundancy.sum()
    
    return weights

def calculate_composite_score(df, score_columns):
    # 提取需要计算权重的分数列
    df_scores = df[score_columns]
    
    # 使用熵权法计算权重
    weights = entropy_weight_method(df_scores)
    
    print("\n计算出的各维度权重:")
    print(weights)
    
    # 计算加权后的综合得分
    # np.dot是矩阵乘法，这里是 df_scores 和 weights 的点积
    composite_score = np.dot(df_scores, weights)
    
    # 将权重和综合得分添加到DataFrame中
    df_with_scores = df.copy()
    for col, weight in weights.items():
        df_with_scores[f'{col}_权重'] = weight
    df_with_scores['综合得分'] = composite_score
    
    # 按综合得分进行排名
    df_with_scores['综合排名'] = df_with_scores['综合得分'].rank(ascending=False, method='min').astype(int)
    
    # 模型评估：计算我们合成的“综合得分”与原始“总得分”的均方误差(MSE)
    # 注意：为了公平比较，我们需要将我们的综合得分重新缩放到与“总得分”相似的范围
    # 这里我们采用简单的线性缩放
    min_orig = df_with_scores['总得分'].min()
    max_orig = df_with_scores['总得分'].max()
    min_comp = df_with_scores['综合得分'].min()
    max_comp = df_with_scores['综合得分'].max()
    
    df_with_scores['缩放后综合得分'] = min_orig + (df_with_scores['综合得分'] - min_comp) * (max_orig - min_orig) / (max_comp - min_comp)
    
    mse = mean_squared_error(df_with_scores['总得分'], df_with_scores['缩放后综合得分'])
    
    return df_with_scores, mse


# 主执行流程

# 定义5个维度的列名
score_dimensions = ['服务得分', '位置得分', '设施得分', '卫生得分', '性价比得分']

# --- 处理景区数据 ---
print("\n--- 开始处理景区综合评价 ---")
try:
    df_spots_scores = pd.read_excel('./data/景区评分.xlsx')
    
    # 调用核心函数进行计算和评估
    df_spots_final, spots_mse = calculate_composite_score(df_spots_scores, score_dimensions)
    
    print("\n景区综合评价最终结果预览:")
    print(df_spots_final[['景区名称', '总得分', '综合得分', '缩放后综合得分', '综合排名']].head())
    print(f"\n景区评价模型的均方误差 (MSE): {spots_mse:.4f}")

except FileNotFoundError:
    print("错误：未在 'data' 文件夹中找到 '景区评分.xlsx'。请检查文件是否存在。")
    df_spots_final = pd.DataFrame()

# --- 处理酒店数据 ---
print("\n--- 开始处理酒店综合评价 ---")
try:
    df_hotels_scores = pd.read_excel('./data/酒店评分.xlsx')

    # 调用核心函数进行计算和评估
    df_hotels_final, hotels_mse = calculate_composite_score(df_hotels_scores, score_dimensions)

    print("\n酒店综合评价最终结果预览:")
    print(df_hotels_final[['酒店名称', '总得分', '综合得分', '缩放后综合得分', '综合排名']].head())
    print(f"\n酒店评价模型的均方误差 (MSE): {hotels_mse:.4f}")

except FileNotFoundError:
    print("错误：未在 'data' 文件夹中找到 '酒店评分.xlsx'。请检查文件是否存在。")
    df_hotels_final = pd.DataFrame()


# 保存结果到指定的Excel文件
output_filename_2 = './output/综合评价表.xlsx'

try:
    with pd.ExcelWriter(output_filename_2) as writer:
        if not df_spots_final.empty:
            df_spots_final.to_excel(writer, sheet_name='景区综合评价', index=False)
        if not df_hotels_final.empty:
            df_hotels_final.to_excel(writer, sheet_name='酒店综合评价', index=False)
    
    print(f"\n处理完成！综合评价结果已成功保存至: {output_filename_2}")

except Exception as e:
    print(f"\n保存文件时出错: {e}")
