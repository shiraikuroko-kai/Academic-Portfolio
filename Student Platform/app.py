# app.py
# Web应用后端
# 使用Flask框架

from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Flask---
app = Flask(__name__)


# 定义一个全局变量来存储预计算好的数据和模型
recommendation_data = {}

def build_recommendation_engine():
    print("开始构建推荐引擎...")
    try:
        df_students = pd.read_csv('./data/students.csv')
        df_projects = pd.read_csv('./data/projects.csv')
        print(f"成功加载 {len(df_students)} 名学生, {len(df_projects)} 个项目。")
    except FileNotFoundError:
        print("数据文件被偷走里")
        return None

    # 数据预处理
    df_students['skills'] = df_students['skills'].fillna('')
    df_students['interests'] = df_students['interests'].fillna('')
    df_projects['required_skills'] = df_projects['required_skills'].fillna('')
    df_students['profile_text'] = (df_students['skills'] + ',' + df_students['interests']).str.replace(',', ' ')
    df_projects['required_skills_text'] = df_projects['required_skills'].str.replace(',', ' ')
    
    # 构建TF-IDF模型与计算相似度矩阵
    tfidf_vectorizer = TfidfVectorizer()
    
    # 学生-项目
    corpus_projects = pd.concat([df_students['profile_text'], df_projects['required_skills_text']], ignore_index=True)
    tfidf_matrix_projects = tfidf_vectorizer.fit_transform(corpus_projects)
    student_vectors = tfidf_matrix_projects[:len(df_students)]
    project_vectors = tfidf_matrix_projects[len(df_students):]
    student_project_similarity = cosine_similarity(student_vectors, project_vectors)
    
    # 学生-学生
    tfidf_matrix_students_only = tfidf_vectorizer.fit_transform(df_students['profile_text'])
    student_student_similarity = cosine_similarity(tfidf_matrix_students_only)
    
    # 将所有需要的数据和模型存入全局变量
    recommendation_data['df_students'] = df_students
    recommendation_data['df_projects'] = df_projects
    recommendation_data['student_project_similarity'] = student_project_similarity
    recommendation_data['student_student_similarity'] = student_student_similarity
    
    print("推荐引擎构建完成！")

# --- 定义Web路由与视图函数 ---

@app.route('/', methods=['GET', 'POST'])
def index():
    df_students = recommendation_data.get('df_students')
    
    # --- 修改之处：传递完整的学生信息列表，而不仅仅是ID ---
    all_students = df_students.to_dict(orient='records')
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        
        student_info = df_students[df_students['student_id'] == student_id]
        
        student_idx = student_info.index[0]
        similarity_scores_p = recommendation_data['student_project_similarity'][student_idx]
        top_project_indices = similarity_scores_p.argsort()[::-1][:5]
        recommended_projects = recommendation_data['df_projects'].iloc[top_project_indices]
        
        similarity_scores_t = recommendation_data['student_student_similarity'][student_idx]
        top_teammate_indices = similarity_scores_t.argsort()[::-1][1:6]
        recommended_teammates = df_students.iloc[top_teammate_indices]
        
        return render_template('index.html', 
                               students=all_students, # 传递完整的学生列表
                               selected_student_id=student_id,
                               student_info=student_info.to_dict(orient='records')[0],
                               recommended_projects=recommended_projects.to_dict(orient='records'),
                               recommended_teammates=recommended_teammates.to_dict(orient='records'))

    # 首次加载页面
    return render_template('index.html', students=all_students)

# --- 启动 ---
if __name__ == '__main__':
    build_recommendation_engine() # 在启动前，先构建好推荐引擎
    app.run(debug=True) # debug=True模式，方便我们调试
