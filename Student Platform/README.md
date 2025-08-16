# 学生科研组队平台

这是我在2021年立项并负责的一个校级创新创业项目。项目的初衷，源于我自己在参与科研竞赛时遇到的一个非常普遍的痛点：想做项目的时候找不到好队友，有好想法的时候又找不到合适的项目。当时，我希望设计一个平台，来解决这个问题。当初是冲着国家级项目的目标进行立项的，但是因为前期的调研不充分，相较于合格的国家级项目的可操作数据包存在非常巨大的差距，因此后期经审核，确定为校级立项。

说实话，这个项目最终因为种种原因，并没有完全按照最初宏大的设想完成。但毕业之后，我利用一段完整的时间，重新梳理了当时的思路，并决定用一个MVP（最小可行性产品）的形式，将这个项目的核心想法——一个基于内容推荐的智能匹配引擎——真正地实现出来。

这个仓库，就是这次重构和复盘的最终成果。

## 1. 项目的核心功能

这个MVP的核心，不是一个华丽的界面，而是一个能解决实际问题的推荐算法。它主要实现两个功能：

1.  项目推荐: 输入一个学生的ID，系统会根据他的技能和兴趣画像，从项目库中推荐出最匹配的5个项目。
2.  队友推荐: 输入一个学生的ID，系统会从学生库中，为他推荐最适合一起组队的5位潜在队友。

## 2. 我的技术实现思路

#### 数据层

*   `students.csv`: 每个学生都有随机分配的专业、技能标签（如 `Python`, `数据分析`, `UI设计`）和兴趣标签。
*   `projects.csv`: 每个项目都有一个随机生成的项目名称、描述以及最重要的——所需技能标签。

#### 算法
我需要一种方法，来量化“学生”和“项目”，以及“学生”和“学生”之间的匹配度。我最终选择了在文本推荐领域非常经典的一种组合：TF-IDF + 余弦相似度，结果还是比较令人满意的。

1. 我把每个学生的“技能+兴趣”标签，以及每个项目的“所需技能”标签，都看作是一篇独立的“文档”。然后，我使用`scikit-learn`库的`TfidfVectorizer`，将这些文本标签转化成了可以进行数学计算的TF-IDF向量。
2. 有了向量之后，我就可以用余弦相似度来计算任意两个向量之间的“夹角”。夹角越小，相似度就越高。
    *   学生A和项目B的相似度，决定了项目B是否值得被推荐给学生A。
    *   学生A和学生B的相似度，决定了他们是否适合成为队友。

#### 展示层
为了能直观地看到推荐效果，我用Flask框架搭建了一个极其简单的Web应用 (`app.py` 和 `templates/index.html`)。它只有一个页面，你可以从下拉菜单里选择一个学生ID，然后后端就会调用我的推荐引擎，把结果用卡片的形式展示在页面上。

## 3. 主要的学习与反思

这个项目对我来说，最大的收获不是最终的代码，而是整个过程中的反思。

*   从“想法”到“产品”的距离：我深刻地体会到，一个“天马行空”的想法，和一个能被实现的、有清晰边界的产品原型之间，有多么巨大的鸿沟。最初的申报书里，我们设想了社区、聊天、积分等各种复杂的功能。但这次重构，我只专注于一件事：把推荐这个核心功能做出来。这种对功能核心的聚焦，是我最大的成长。
*   管理与技术的平衡：作为项目负责人，我意识到自己的角色不仅仅是一个“写代码的”。在项目早期，我犯过典型的错误：在需求没有完全想清楚之前，就急于开始技术选型。这次重构的过程，也是我对整个项目流程进行复盘和优化的过程。
*   “脏活累活”的重要性：生成模拟数据、预处理文本、构建TF-IDF词汇表……这些工作虽然没有算法那么“性感”，但我发现，它们占据了整个项目80%的时间，并且直接决定了最终推荐结果的质量。

## 4. 技术栈

*   语言:Python 3
*   核心库: Pandas, scikit-learn, Faker, Flask

## 5. 运行方法

1.  克隆这个仓库。
2.  确保已安装所有必要的库 (`pip install pandas Faker scikit-learn Flask`)。
3.  首先，运行数据生成脚本：`python data_generator.py`。
4.  然后，启动Web应用：`python app.py`。
5.  在浏览器中打开 `http://127.0.0.1:5000/` 即可看到效果。

---
首先感谢杨静老师和姜赢老师的陪伴与支持，虽然未能顺利结项，但这个项目对我来说，仍然是一次宝贵的学习和成长经历。

# Student Research Collaboration Platform

This was a university-level innovation project that I initiated and led in 2021. The original idea came from a very common pain point I experienced myself when participating in research competitions: it was hard to find good teammates when you had a project idea, and hard to find a suitable project when you were looking for a team. At the time, I wanted to design a platform to solve this problem. Initially, we were aiming for this to be a national-level project, but due to insufficient preliminary research, there was a huge gap in the viability of our data package compared to what was required. As a result, after review, it was approved as a university-level project.

To be honest, for various reasons, the project was never fully realized according to its initial grand vision. But after graduation, I took a dedicated period of time to revisit the original ideas and decided to build an MVP (Minimum Viable Product). The goal was to bring the core concept—an intelligent matching engine based on content recommendation—to life.

This repository is the final result of that refactoring and reflection process.

## 1. Core Features of the Project

The core of this MVP is not a fancy interface, but a recommendation algorithm that solves a real problem. It mainly implements two functions:

1.  Project Recommendation: Input a student's ID, and the system will recommend the top 5 most suitable projects from the project pool based on their skills and interests profile.
2.  Teammate Recommendation: Input a student's ID, and the system will recommend the top 5 best-suited potential teammates from the student pool.

## 2. My Technical Approach

#### The Data Layer

`students.csv`: Each student has a randomly assigned major, skill tags (e.g., `Python`, `Data Analysis`, `UI Design`), and interest tags.
`projects.csv`: Each project has a randomly generated name, a description, and, most importantly, a set of required skill tags.

#### The Algorithm
I needed a way to quantify the match between a "student" and a "project," as well as between "student" and "student." I eventually chose a classic combination in the field of text recommendation: TF-IDF + Cosine Similarity, and the results were quite satisfying.

1. I treated each student's "skills + interests" tags and each project's "required skills" tags as separate "documents." Then, I used `scikit-learn`'s `TfidfVectorizer` to transform these text tags into mathematical TF-IDF vectors that could be computed.
2. Once I had the vectors, I could use Cosine Similarity to calculate the "angle" between any two vectors. The smaller the angle, the higher the similarity.
    The similarity between Student A and Project B determines whether Project B is worth recommending to Student A.
    The similarity between Student A and Student B determines if they would be good teammates.

#### The Presentation Layer
To visualize the recommendation results intuitively, I built an extremely simple web application using the Flask framework (`app.py` and `templates/index.html`). It has a single page where you can select a student ID from a dropdown menu. The backend will then call my recommendation engine and display the results in a card-based format on the page.

## 3. Key Learnings & Reflections

For me, the biggest takeaway from this project wasn't the final code, but the shift in my way of thinking.

The distance from "idea" to "product": I gained a deep appreciation for the huge gap between a "wild idea" and a feasible product prototype with clear boundaries. In the original proposal, we envisioned all sorts of complex features like a community forum, chat functions, and a points system. But in this refactoring, I focused on just one thing: making the core recommendation feature work. This focus on the MVP was my biggest area of growth.
Balancing management and technology: As the project leader, I realized my role wasn't just about "writing code." In the early stages, I made a classic mistake: rushing to choose the technology before the requirements were fully understood. This refactoring process was also a chance for me to review and optimize my entire project workflow.
The importance of the "grunt work": Generating mock data, preprocessing text, building the TF-IDF vocabulary... although these tasks aren't as "sexy" as the algorithm itself, I found that they took up about 80% of the project's time and directly determined the quality of the final recommendations.

## 4. Technical Stack

Language: Python 3
Core Libraries: Pandas, scikit-learn, Faker, Flask

## 5. How to Run

1.  Clone this repository.
2.  Make sure you have all the necessary libraries installed (`pip install pandas Faker scikit-learn Flask`).
3.  First, run the data generation script: `python data_generator.py`.
4.  Then, start the web application: `python app.py`.
5.  Open `http://1227.0.0.1:5000/` in your browser to see the results.

---
First and foremost, I want to thank Professor Yang Jing and Professor Jiang Ying for their guidance and support. Although the project was not successfully concluded in its original form, it remains an invaluable learning and growth experience for me.