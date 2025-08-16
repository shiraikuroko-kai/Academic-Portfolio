# --- 导入库与加载数据 ---

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 加载数据
try:
    df_students = pd.read_csv('./data/students.csv')
    df_projects = pd.read_csv('./data/projects.csv')
    print("数据加载")
    print(f"共加载 {len(df_students)} 名学生, {len(df_projects)} 个项目。")
except FileNotFoundError:
    print("请检查数据文件")

# 展示数据样本
print("\n学生数据样本:")
print(df_students.head())
print("\n项目数据样本:")
print(df_projects.head())


# --- 数据预处理与特征工程 ---

# TF-IDF算法要求输入的文本是以空格分隔的字符串。
# 然而标签数据已经是逗号分隔的，因此需要将其转换一下。
# 同时学生的'skills'和'interests'两个属性需要合并并创建一个'profile'字段，代表学生的完整画像。

# 填充可能存在的空值（NaN）
df_students['skills'] = df_students['skills'].fillna('')
df_students['interests'] = df_students['interests'].fillna('')
df_projects['required_skills'] = df_projects['required_skills'].fillna('')

# 合并学生技能和兴趣，并替换逗号为空格
df_students['profile_text'] = df_students['skills'] + ',' + df_students['interests']
df_students['profile_text'] = df_students['profile_text'].str.replace(',', ' ')

# 替换项目所需技能的逗号为空格
df_projects['required_skills_text'] = df_projects['required_skills'].str.replace(',', ' ')

print("数据预处理完成")
print("\n处理后的学生数据样本:")
print(df_students[['student_id', 'profile_text']].head())


# --- 构建TF-IDF模型与计算相似度矩阵 ---

# 初始化一个TF-IDF向量化器
# 它将学习我们所有标签的词汇表，并计算每个标签的TF-IDF权重
tfidf_vectorizer = TfidfVectorizer()

# --- 为“项目推荐”构建模型 ---
# 将所有学生的画像和项目的技能要求合并，以构建一个统一的词汇空间
corpus_projects = pd.concat([df_students['profile_text'], df_projects['required_skills_text']], ignore_index=True)
tfidf_matrix_projects = tfidf_vectorizer.fit_transform(corpus_projects)

# 将矩阵拆分回学生和项目两部分
student_vectors = tfidf_matrix_projects[:len(df_students)]
project_vectors = tfidf_matrix_projects[len(df_students):]

# 计算学生与项目之间的余弦相似度
# 结果是一个 (学生数量 x 项目数量) 的矩阵
student_project_similarity = cosine_similarity(student_vectors, project_vectors)
print("学生-项目 相似度矩阵计算完成。")
print("矩阵形状:", student_project_similarity.shape)

# --- 为“队友推荐”构建模型 ---
# 队友推荐只基于学生之间的相似度，所以我们只用学生的画像数据
tfidf_matrix_students_only = tfidf_vectorizer.fit_transform(df_students['profile_text'])

# 计算学生与学生之间的余弦相似度
# 结果是一个 (学生数量 x 学生数量) 的对称矩阵
student_student_similarity = cosine_similarity(tfidf_matrix_students_only)
print("\n学生-学生 相似度矩阵计算完成。")
print("矩阵形状:", student_student_similarity.shape)


# --- 封装---

def recommend_projects(student_id, top_n=5):
    """根据学生ID，推荐Top N个最匹配的项目"""
    try:
        # 找到该学生在DataFrame中的索引位置
        student_idx = df_students[df_students['student_id'] == student_id].index[0]
        
        # 从相似度矩阵中，获取该学生与所有项目的相似度分数
        similarity_scores = student_project_similarity[student_idx]
        
        # 获取分数最高的前N个项目的索引
        # argsort()返回的是排序后的原始索引，[::-1]将其反转为降序
        top_project_indices = similarity_scores.argsort()[::-1][:top_n]
        
        # 返回推荐的项目信息
        recommended_projects = df_projects.iloc[top_project_indices]
        
        return recommended_projects
        
    except IndexError:
        return f"错误：未找到学生ID '{student_id}'"

def recommend_teammates(student_id, top_n=5):
    """根据学生ID，推荐Top N个最匹配的队友"""
    try:
        # 找到该学生在DataFrame中的索引位置
        student_idx = df_students[df_students['student_id'] == student_id].index[0]
        
        # 从学生相似度矩阵中，获取该学生与其他所有学生的相似度分数
        similarity_scores = student_student_similarity[student_idx]
        
        # 获取分数最高的前N+1个学生的索引（因为第一个总是他自己）
        # 我们要排除他自己，所以取[1:top_n+1]
        top_teammate_indices = similarity_scores.argsort()[::-1][1:top_n+1]
        
        # 返回推荐的队友信息
        recommended_teammates = df_students.iloc[top_teammate_indices]
        
        return recommended_teammates
        
    except IndexError:
        return f"错误：未找到学生ID '{student_id}'"

print("推荐函数封装完成。")


# --- 测试推荐引擎 ---

# 随机选择一个学生ID进行测试
test_student_id = df_students.sample(1)['student_id'].iloc[0]

print(f"--- 为学生 {test_student_id} 进行推荐测试 ---")

# 获取该学生的信息
student_info = df_students[df_students['student_id'] == test_student_id]
print("\n该学生的信息:")
print(student_info)

# 为他推荐项目
print(f"\n为 {test_student_id} 推荐的最匹配的 {5} 个项目是:")
recommended_p = recommend_projects(test_student_id)
print(recommended_p)

# 为他推荐队友
print(f"\n为 {test_student_id} 推荐的最适合的 {5} 个队友是:")
recommended_t = recommend_teammates(test_student_id)
print(recommended_t)
