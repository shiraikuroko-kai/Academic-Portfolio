# 景区及酒店的特色分析
# ---------------------------------------------------------------------------

# 导入所需库
import pandas as pd
import jieba.analyse
import os


# 定义核心分析函数

def select_tiers(df_ranked, id_column, rank_column):
   
    # 按排名排序
    df_sorted = df_ranked.sort_values(by=rank_column)
    
    total_count = len(df_sorted)
    
    # 高层次：排名前3
    high_tier_ids = df_sorted[id_column].head(3).tolist()
    
    # 中层次：排名在中间的3个
    mid_index = total_count // 2
    mid_tier_ids = df_sorted[id_column].iloc[mid_index-1 : mid_index+2].tolist()
    
    # 低层次：排名最后的3个
    low_tier_ids = df_sorted[id_column].tail(3).tolist()
    
    return {
        '高分层': high_tier_ids,
        '中分层': mid_tier_ids,
        '低分层': low_tier_ids
    }


def analyze_uniqueness(df_reviews, selected_ids, id_column, text_column, top_k=5):

    # 加载停用词
    stop_words_path = './stopwords/hit_stopwords.txt'
    if os.path.exists(stop_words_path):
        jieba.analyse.set_stop_words(stop_words_path)
    
    # 筛选出只包含选定ID的评论
    df_filtered = df_reviews[df_reviews[id_column].isin(selected_ids)].copy()
    
    # 将每个ID的所有评论合并成一个文档
    # 使用.astype(str)确保所有评论都是字符串
    corpus = df_filtered.groupby(id_column)[text_column].apply(lambda x: ' '.join(x.astype(str))).reset_index()
    corpus.rename(columns={text_column: 'full_text'}, inplace=True)
    
    uniqueness_results = {}
    
    print(f"\n开始分析 {len(selected_ids)} 个目标的特色...")
    
    for _, row in corpus.iterrows():
        item_id = row[id_column]
        full_text = row['full_text']
        
        # 使用TF-IDF提取关键词 (不带权重，只取词)
        keywords = jieba.analyse.extract_tags(full_text, topK=top_k, withWeight=False)
        
        uniqueness_results[item_id] = keywords
        print(f"已分析: {item_id} -> 特色: {', '.join(keywords)}")
        
    return uniqueness_results



# 主执行流程

# --- 景区特色分析 ---
print("\n--- 开始进行景区特色分析 ---")
try:
    # 加载问题二的评价结果
    df_spots_ranked = pd.read_excel('./output/综合评价表.xlsx', sheet_name='景区综合评价')
    # 加载原始评论数据
    df_spots_reviews = pd.read_excel('./data/景区评论.xlsx')

    # 1. 筛选高、中、低三个层次的景区
    spot_tiers = select_tiers(df_spots_ranked, '景区名称', '综合排名')
    print("已选定高、中、低分层的景区:")
    print(spot_tiers)
    
    all_selected_spots = spot_tiers['高分层'] + spot_tiers['中分层'] + spot_tiers['低分层']

    # 2. 挖掘特色
    spot_features = analyze_uniqueness(df_spots_reviews, all_selected_spots, '景区名称', '评论内容')
    
    # 3. 整理结果
    spot_feature_list = []
    for tier, ids in spot_tiers.items():
        for item_id in ids:
            features = spot_features.get(item_id, [])
            spot_feature_list.append({
                '层次': tier,
                '景区名称': item_id,
                '特色关键词': ', '.join(features)
            })
    df_spot_feature_results = pd.DataFrame(spot_feature_list)

except FileNotFoundError:
    print("错误：请先确保 'data' 文件夹中有'景区评论.xlsx'和'景区评分.xlsx'，且 'output' 文件夹中有'综合评价表.xlsx'")
    df_spot_feature_results = pd.DataFrame()

# --- 酒店特色分析 ---
print("\n--- 开始进行酒店特色分析 ---")
try:
    # 加载问题二的评价结果
    df_hotels_ranked = pd.read_excel('./output/综合评价表.xlsx', sheet_name='酒店综合评价')
    # 加载原始评论数据
    df_hotels_reviews = pd.read_excel('./data/酒店评论.xlsx')

    # 1. 筛选高、中、低三个层次的酒店
    hotel_tiers = select_tiers(df_hotels_ranked, '酒店名称', '综合排名')
    print("已选定高、中、低分层的酒店:")
    print(hotel_tiers)
    
    all_selected_hotels = hotel_tiers['高分层'] + hotel_tiers['中分层'] + hotel_tiers['低分层']

    # 2. 挖掘特色
    hotel_features = analyze_uniqueness(df_hotels_reviews, all_selected_hotels, '酒店名称', '评论内容')

    # 3. 整理结果
    hotel_feature_list = []
    for tier, ids in hotel_tiers.items():
        for item_id in ids:
            features = hotel_features.get(item_id, [])
            hotel_feature_list.append({
                '层次': tier,
                '酒店名称': item_id,
                '特色关键词': ', '.join(features)
            })
    df_hotel_feature_results = pd.DataFrame(hotel_feature_list)
    
except FileNotFoundError:
    print("错误：请先确保 'data' 文件夹中有'酒店评论.xlsx'和'酒店评分.xlsx'，且 'output' 文件夹中有'综合评价表.xlsx'")
    df_hotel_feature_results = pd.DataFrame()


# 保存结果并展示
output_filename_4 = './output/特色分析表.xlsx'

try:
    with pd.ExcelWriter(output_filename_4) as writer:
        if not df_spot_feature_results.empty:
            print("\n--- 景区特色分析结果 ---")
            print(df_spot_feature_results)
            df_spot_feature_results.to_excel(writer, sheet_name='景区特色分析', index=False)
        
        if not df_hotel_feature_results.empty:
            print("\n--- 酒店特色分析结果 ---")
            print(df_hotel_feature_results)
            df_hotel_feature_results.to_excel(writer, sheet_name='酒店特色分析', index=False)
            
    print(f"\n处理完成！特色分析结果已成功保存至: {output_filename_4}")

except Exception as e:
    print(f"\n保存文件时出错: {e}")
