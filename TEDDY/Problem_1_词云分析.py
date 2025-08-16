# 问题一：景区及酒店印象分析
# ---------------------------------------------------------------------------
import pandas as pd
import jieba
import jieba.analyse
import os

# 确保输出文件夹存在
if not os.path.exists('output'):
    os.makedirs('output')
    print("已创建 'output' 文件夹。")


# 定义核心分析函数
def get_top_keywords(df, id_column, text_column, top_k=20):
    
    # 定义停用词文件的路径 (使用相对路径)
    stop_words_path = './stopwords/hit_stopwords.txt'
    
    # 加载停用词文件
    # 这里我们确认文件存在，如果不存在则给出提示
    if os.path.exists(stop_words_path):
        jieba.analyse.set_stop_words(stop_words_path)
        print(f"已成功加载停用词文件: {stop_words_path}")
    else:
        print(f"警告：未找到停用词文件于 '{stop_words_path}'。将不使用自定义停用词。")

    # 按目的地ID进行分组
    # 在分组前，确保ID列没有空值，并将评论转为字符串避免错误
    df.dropna(subset=[id_column], inplace=True)
    df[text_column] = df[text_column].astype(str)
    
    grouped = df.groupby(id_column)
    
    results = {}
    
    print(f"开始处理 {len(grouped)} 个独立的目的地...")
    
    total_items = len(grouped)
    current_item = 0
    
    for name, group in grouped:
        current_item += 1
        # 将该目的地的所有评论合并成一个长字符串
        full_text = ' '.join(group[text_column])
        
        # 使用TF-IDF算法提取关键词及其权重
        # extract_tags函数返回的是一个列表，每个元素是(关键词, 权重)
        keywords = jieba.analyse.extract_tags(full_text, topK=top_k, withWeight=True)
        
        results[name] = keywords
        # 打印进度，避免长时间无响应
        print(f"进度: {current_item}/{total_items} | 已处理: {name}")
        
    print("所有目的地处理完成。")
    return results


# 主执行流程

# --- 处理景区数据 ---
print("\n--- 开始处理景区数据 ---")
# 使用相对路径读取数据
try:
    df_spots = pd.read_excel('./data/景区评论.xlsx')

    # 调用核心函数进行分析
    spot_keywords = get_top_keywords(df_spots, '景区名称', '评论内容')

    # 将结果转换为格式化的DataFrame
    spot_results_list = []
    for spot_id, keywords in spot_keywords.items():
        for keyword, weight in keywords:
            spot_results_list.append({'评论热词': keyword, '热度(TF-IDF)': weight, '景区ID': spot_id})

    df_spot_results = pd.DataFrame(spot_results_list)
    print("\n景区印象词云表预览:")
    print(df_spot_results.head())

except FileNotFoundError:
    print("错误：未在 'data' 文件夹中找到 '景区评论.xlsx'。请检查文件是否存在。")
    df_spot_results = pd.DataFrame() # 创建一个空的DataFrame以避免后续错误


# --- 处理酒店数据 ---
print("\n--- 开始处理酒店数据 ---")
try:
    df_hotels = pd.read_excel('./data/酒店评论.xlsx')

    # 调用核心函数进行分析
    hotel_keywords = get_top_keywords(df_hotels, '酒店名称', '评论内容')

    # 将结果转换为格式化的DataFrame
    hotel_results_list = []
    for hotel_id, keywords in hotel_keywords.items():
        for keyword, weight in keywords:
            hotel_results_list.append({'评论热词': keyword, '热度(TF-IDF)': weight, '酒店ID': hotel_id})

    df_hotel_results = pd.DataFrame(hotel_results_list)
    print("\n酒店印象词云表预览:")
    print(df_hotel_results.head())

except FileNotFoundError:
    print("请检查数据文件")
    df_hotel_results = pd.DataFrame() # 创建一个空的DataFrame以避免后续错误


# 保存结果到指定的Excel文件
output_filename = './output/印象词云表.xlsx'

# 使用pandas的ExcelWriter，将两个结果保存在同一个Excel文件的不同Sheet中
try:
    with pd.ExcelWriter(output_filename) as writer:
        if not df_spot_results.empty:
            df_spot_results.to_excel(writer, sheet_name='景区印象词', index=False)
        if not df_hotel_results.empty:
            df_hotel_results.to_excel(writer, sheet_name='酒店印象词', index=False)
    
    print(f"\n结果已成功保存至: {output_filename}")

except Exception as e:
    print(f"\n保存文件时出错: {e}")
