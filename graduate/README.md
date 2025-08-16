# 黄鹤楼 vs. 龟峰 - 游客评价对比分析(scroll down to check english version)

说实话，这算是我第一个真正意义上、从头到尾独立完成的数据科学项目。整个过程充满了学习、试错，当然，也少不了熬夜和长黑眼圈。能最终完成，真的要特别感谢我的两位导师——崔德鑫老师和我的班主任杨静老师。

## 1.项目思路

我的论文题目，是想对比一下黄鹤楼和龟峰这两个著名景点，看看游客们对它们的真实需求和看法到底有什么不同。我当时的想法是，如果能通过分析大量的网络评论，挖掘出游客们在谈论不同景点时最关心的“主题”，以及他们情感上的“变化趋势”，那应该能为景区的运营和营销提供一些有价值的参考。

这个仓库里，主要包含了两个阶段的代码：

刚开始，是我在写论文时，最原始、最真实的代码“草稿”。里面是我当时探索用的各种零散脚本，比如用`jieba`做分词，用`snownlp`做情感分析等等。说实话，现在看这些代码多少写得有点潦草。
于是在毕业后，我花了一段时间重新整理和重构的版本。我把之前所有零散的思路，都整合到了这一个Jupyter Notebook里，并且用了一些更高级、更规范的方法，比如LDA主题模型。

## 2. 项目执行

#### 数据来源
数据是我当时用Python写的爬虫，从携程网上获取的黄鹤楼和龟峰的几千条公开评论。这个过程本身就是一次宝贵的学习经历。

#### 核心分析思路
1. 情感演化分析:我想知道，疫情前后，大家对这两个景点的评价有什么变化。所以我用`snownlp`计算了每条评论的情感分数，然后按月汇总，画出了两个景点口碑变化的折线图。
2. 主题建模 (Topic Modeling):这是最有趣的部分。光看好评差评还不够，我想知道大家具体都在聊些什么。这里我必须感谢崔德鑫老师，在他的指导下，我学习并使用了LDA模型。这个模型能自动地从一大堆评论里，把大家最关心的几个核心“主题”给聚类出来。比如，黄鹤楼的游客更关心“历史”、“长江大桥”，而龟峰的游客则更关心“自然风光”、“栈道”。

## 3. 收获

这个项目对我来说，最大的收获不是技术，而是思维方式的转变。

一开始，我满脑子都是“我要用什么酷炫的算法。但在杨静老师的反复引导下，我慢慢明白，数据分析的起点，永远应该是“我们想解决一个什么实际问题。是她教会我，要时刻思考数据背后的商业逻辑和用户情境。比如，她提醒我关注“可解释性模型”的重要性，这个建议让我受益匪浅。
我有很多“天马行空”的想法，但崔德鑫老师则一次次地把我拉回地面。我还记得我在课堂上选择过“生物机器人”的主题进行演讲，这是我印象最深的一次，他教会我做研究必须严谨，每一步都需要有扎实的数据和清晰的逻辑作为支撑。是他带着我，一步步地把一个模糊的想法，变成了一个结构清晰、可执行的研究方案。

没有这两位老师的指导和帮助，我绝对不可能独立完成这份毕业论文。

## 4. 如何运行

1.  克隆这个仓库。
2.  确保已安装所有必要的库 (`pandas`, `jieba`, `snownlp`, `gensim`, `matplotlib`)。
3.  数据都在`/data`文件夹里。
4.  推荐直接打开并运行`Thesis_Analysis_Refactored.ipynb`，这里面包含了最完整、最清晰的分析流程和可视化结果。

感谢您花时间阅读。这个项目对我来说，意义非凡。它不仅是我本科四年的学术总结，更是一段关于成长、反思和感恩的旅程。


# Yellow Crane Tower vs. Gui Peak - A Comparative Analysis of Tourist Reviews

To be honest, this was my first real data science project that I completed independently from start to finish. The process was filled with learning, trial and error, and of course, more than a few long nights. I genuinely couldn't have finished it without the guidance of my two mentors—Professor Cui Dexin, and my academic advisor, Professor Yang Jing.

## 1. The Idea

My goal for this thesis was to compare two famous attractions, Yellow Crane Tower and Gui Peak, to understand the real demands and perceptions of tourists. My thinking was that if I could analyze a large volume of online reviews to uncover the core "topics" people focused on and the "trends" in their sentiment, it could offer valuable insights for the attractions' operations and marketing.

This repository contains two main phases of my work:

At first, there were the raw, original code 'drafts' from when I was writing the thesis. It includes various scattered scripts I used for exploration, like using `jieba` for word segmentation and `snownlp` for sentiment analysis. Honestly, looking back now, the code is a bit messy.

That's why, after graduation, I spent some time refactoring and restructuring it. I consolidated all the scattered ideas into this single Jupyter Notebook and applied more advanced and standardized methods, like LDA for topic modeling.

## 2. The Execution

#### Data Source
The data was collected using a Python scraper I wrote to get several thousand public reviews for Yellow Crane Tower and Gui Peak from Ctrip (a popular travel site). This process itself was an invaluable learning experience.

#### Core Analysis
1.  **Sentiment Evolution Analysis:** I wanted to see how public opinion about these two attractions changed before and after the pandemic. So, I used `snownlp` to calculate the sentiment score for each review, then aggregated them by month to plot a line chart showing the trend of their public perception over time.
2.  **Topic Modeling:** This was the most interesting part. Looking at just "good" or "bad" reviews wasn't enough; I wanted to know what people were *actually* talking about. I must thank Professor Cui Dexin here. Under his guidance, I learned and used the LDA (Latent Dirichlet Allocation) model. This model can automatically cluster the core "topics" from a large corpus of reviews. For instance, tourists at Yellow Crane Tower were more concerned with "history" and the "Yangtze River Bridge," while visitors to Gui Peak focused more on "natural scenery" and "plank roads."

## 3. The Takeaways

For me, the biggest takeaway from this project wasn't the technology, but the shift in my way of thinking.

At the beginning, my mind was filled with "what cool algorithm can I use?" But with Professor Yang Jing's repeated guidance, I slowly came to understand that the starting point for data analysis should always be "what real problem are we trying to solve?" She taught me to constantly think about the business logic and user context behind the data. For instance, she reminded me of the importance of "interpretable models," and that advice was incredibly valuable.

I had many "wild ideas," but it was Professor Cui Dexin who brought me back down to earth time and again. I still remember a presentation I gave in his class on the topic of "bio-robotics"—it's my most vivid memory. He taught me that research must be rigorous, and every step needs to be supported by solid data and clear logic. He was the one who guided me, step by step, to turn a vague idea into a clearly structured and executable research plan.

Without the guidance and help of these two professors, I absolutely could not have completed this thesis independently.

## 4. How to Run

1.  Clone this repository.
2.  Make sure you have all the necessary libraries installed (`pandas`, `jieba`, `snownlp`, `gensim`, `matplotlib`).
3.  The data is located in the `/data` folder.
4.  I recommend running `Thesis_Analysis_Refactored.ipynb` directly, as it contains the most complete and clear analysis workflow and visualization results.

Thank you for taking the time to read this. This project means a great deal to me. It's not just the academic culmination of my four years in university, but also a journey of growth, reflection, and gratitude.