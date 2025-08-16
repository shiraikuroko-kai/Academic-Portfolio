这是我为2020年第九届“泰迪杯”数据挖掘挑战赛C题（游客目的地印象分析）比赛结束后复盘的项目。这是我早期独立完成的数据分析项目之一。

## 1.项目目标

主办方给了我们两份文本数据，分别是真实的景区和酒店的网络评论，让我们用数据挖掘的方法，去分析游客对这些地方的。具体来说，需要完成四个任务：
1.  提取每个目的地的“印象”关键词。
2.  建立一个模型，对每个目的地进行综合评分。
3.  分析哪些网络评论是“有效”的，哪些是“水军”或低质量的。
4.  挖掘高、中、低不同评分层次的目的地，各自独特的“特色”是什么。

## 2.我的工作流程与方法

整个分析过程刚开始在一个Jupyter Notebook里完成，代码和思路尽可能地做了注释，但后来觉得Geany使用起来更为方便，便更换了工具进行操作。
#### 问题一：词云或印象分析
一开始，我最直接的想法就是简单地用`jieba`分词，然后统计词频。但很快我就发现了一个问题：排名靠前的全是“不错”、“方便”、“可以”这些没什么信息量的词。
这时我才意识到也许需要一种更能体现“重要性”而不仅仅是“频率”的算法。因此，我最终采用了TF-IDF算法。为了让结果更精确，必须手动调教整理一份停用词表，用来过滤掉那些通用但无意义的词语。
#### 问题二：景区酒店综合评价
这个问题要求我们对服务、位置、设施等五个维度进行评分。简单地将专家给出的分数做平均，似乎太草率了。我想知道，对游客来说，这五个维度是不是同等重要？
为了找到一个更客观的权重，我研究并使用了熵权法。这个方法能根据数据本身的波动性来给每个维度賦予权重。比如，如果所有酒店的“卫生”得分都差不多，那这个指标的区分度就不大，权重就低。我觉得这个思路比主观地设定权重更科学。
#### 问题三：文本有效性分析
“有效性”是个很模糊的概念。我把它定义为了一个由三个核心指标构成的“评论质量分”：
1.  文本长度：评论越长，信息量可能越大。
2.  情感强度：我用了`snownlp`库来计算每条评论的情感分数。我认为，无论是“极好”还是“极差”，情感越强烈的评论，通常越真实。
3.  信息密度：我用`jieba`的词性标注功能，计算了每条评论中名词和动词的占比。我认为“实词”越多的评论，内容越具体，质量越高。
最后，我将这三个指标归一化后加权，得到了一个最终的“有效性得分”。
#### 问题四：特色分析
这一步其实是前几步成果的综合应用。我利用问题二的排名，筛选出高、中、低三个档次的目的地。然后，我再次利用TF-IDF算法，但这次的语料库是所有目的地，这样计算出的TF-IDF分数，就能更好地反映一个词在特定目的地评论中的“独特性”。

## 3.主要的学习与挑战

说实话，这个项目做得磕磕绊绊，但也让我学到了很多书本上没有的东西。

首先数据清理这部分是最花时间的，我一开始花了很长时间调试一个`KeyError`，最后才发现，景区和酒店两个Excel文件里，表示评论内容的列名居然不一样！（一个是`评论详情`，另一个是`评论内容`）。这让我明白，数据清洗和预处理是所有分析的第一步，也是最重要的一步。
路径问题也同样很重要，我最早的代码里，文件路径都是写死的（比如`C:\\Users\\...`）。后来我才意识到，这样的代码除了在我自己的电脑上，在任何地方都无法运行。我把所有路径都重构为了相对路径（比如`./data/`），这让我的项目变得“可移植”了。再加上用`.apply()`函数给几万条评论计算情感分数和做词性标注，真的很慢。程序经常“假死”很久，我一度以为是代码写错了。后来我学会了使用`tqdm`库，给这个漫长的过程加了一个进度条，虽然没有让它变快，但至少让我心里有底了。

## 4.技术栈

语言: Python
核心库: Pandas, Jieba, SnowNLP, NumPy

## 5.运行方法

1.  克隆这个仓库。
2.  确保已安装所有必要的库 (`pip install pandas openpyxl jieba snownlp tqdm`)。
3.  将原始数据文件 (`景区评论.xlsx`, `酒店评论.xlsx`) 放入`/data`文件夹。
4.  将`hit_stopwords.txt`文件放入`/stopwords`文件夹。
5.  按顺序运行`Problem_1_...ipynb`, `Problem_2_...ipynb`等文件即可。所有结果文件都会保存在`/output`文件夹中。```

# English version

This is my post-competition review of my project for the 9th "Tadib Cup" Data Mining Challenge (Problem C: Analysis of Tourist Destination Impressions) from 2020. This was one of my earliest independent data analysis projects.

## 1. Project Goal

The organizers provided us with two text datasets, which were real online reviews for tourist attractions and hotels, and asked us to use data mining methods to analyze tourists' impressions of these places. Specifically, we needed to complete four tasks:
1.  Extract "impression" keywords for each destination.
2.  Build a model to give each destination a comprehensive score.
3.  Analyze which online reviews were "effective" and which were "spam" or low-quality.
4.  Identify the unique "features" of destinations at high, medium, and low rating levels.

## 2. My Workflow & Methodology

At the beginning, I did the entire analysis in a Jupyter Notebook, trying to comment on the code and my thought process as much as possible. But later on, I found Geany more convenient to use, so I switched tools.

#### Problem 1: Word Cloud / Impression Analysis
Initially, my most direct idea was to simply use `jieba` for word segmentation and then count the frequencies. But I quickly discovered a problem: the top-ranked words were all uninformative ones like "not bad," "convenient," and "okay."
That's when I realized I probably needed an algorithm that could reflect "importance" rather than just "frequency." Therefore, I ended up using the TF-IDF algorithm. To make the results more accurate, it was essential to manually tune and organize a stopword list to filter out those generic but meaningless words.

#### Problem 2: Comprehensive Evaluation of Attractions & Hotels
This problem required us to score five dimensions, including service, location, and facilities. Simply averaging the expert scores seemed too crude. I wanted to know, are these five dimensions equally important to tourists?
To find a more objective weighting, I researched and used the Entropy Weight Method. This method can assign weights to each dimension based on the volatility of the data itself. For example, if all hotels have similar "cleanliness" scores, that metric doesn't differentiate them much, so its weight would be low. I felt this approach was more scientific than subjectively setting the weights.

#### Problem 3: Text Effectiveness Analysis
"Effectiveness" is a very vague concept. I defined it as a "review quality score" composed of three core metrics:
1.  Text Length: The longer the review, the more information it likely contains.
2.  Sentiment Strength: I used the `snownlp` library to calculate the sentiment score for each review. I believe that the stronger the emotion—whether extremely positive or extremely negative—the more authentic the review usually is.
3.  Information Density: I used `jieba`'s part-of-speech tagging function to calculate the proportion of nouns and verbs in each review. I think that reviews with more "content words" are more specific and of higher quality.
Finally, I normalized and weighted these three metrics to get a final "effectiveness score."

#### Problem 4: Feature Analysis
This step was really an integration of the previous results. I used the rankings from Problem 2 to select destinations from high, medium, and low tiers. Then, I used the TF-IDF algorithm again, but this time the corpus included all destinations. This way, the calculated TF-IDF scores could better reflect a word's "uniqueness" in the reviews for a specific destination.

## 3. Key Learnings & Challenges

To be honest, this project was a bumpy ride, but it also taught me a lot of things you can't learn from a textbook.

First, data cleaning took the most time. I spent a long time debugging a `KeyError` at the beginning, only to finally realize that the column names for the review content in the two Excel files—for attractions and hotels—were actually different! (One was `评论详情`, the other was `评论内容`). This taught me that data cleaning and preprocessing are the first and most important steps in any analysis.

Path issues were also a big deal. In my earliest code, the file paths were all hard-coded (like `C:\\Users\\...`). I later realized that such code wouldn't run anywhere except on my own computer. I refactored all the paths to be relative (like `./data/`), which made my project "portable." On top of that, using the `.apply()` function to calculate sentiment scores and do part-of-speech tagging for tens of thousands of reviews was really slow. The program would often "freeze" for a long time, and I initially thought I had a bug in my code. Later, I learned to use the `tqdm` library to add a progress bar to this long process. It didn't make it faster, but at least it let me know what was going on.

## 4. Technical Stack

Language: Python
Core Libraries: Pandas, Jieba, SnowNLP, NumPy

## 5. How to Run

1.  Clone this repository.
2.  Make sure you have all the necessary libraries installed (`pip install pandas openpyxl jieba snownlp tqdm`).
3.  Place the original data files (`景区评论.xlsx`, `酒店评论.xlsx`) into the `/data` folder.
4.  Place the `hit_stopwords.txt` file into the `/stopwords` folder.
5.  Run the files like `Problem_1_...ipynb`, `Problem_2_...ipynb` in order. All result files will be saved in the `/output` folder.