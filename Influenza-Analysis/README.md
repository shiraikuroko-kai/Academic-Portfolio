这是一个使用Python和Pygame构建的、可交互的、实时的疫情传播模拟器。它允许用户动态地调整关键参数，并观察这些参数如何影响一个封闭人群中的传播动态。（scroll down check the english version）
# 1. 项目动机与背景

这个项目的灵感，来源于北京师范大学系统科学学院狄增如教授的一堂课。在课上，他演示了一个复杂系统模型，我当时完全被“简单的、局部的规则，如何能涌现出复杂的、全局的行为”这一概念所吸引。这个项目，就是我通过构建一个可上手的、交互式的“数字实验室”，来亲身探索这一概念的尝试。

# 2. 技术架构与方法论

这个模拟器是建立在“智能体基模型”之上的，这是数据科学领域中，用于为复杂系统建模的一个强大范式。
核心组件:
person.py (智能体): 定义了我们系统中的基本单位——Person类。每一个智能体都拥有自己的状态（健康、感染、康复）和一套简单的行为规则（例如，如何移动、如何更新自己的状态）。
parameters.py (环境): 集中管理了模拟器的所有全局参数，例如人口数量、病毒特性和UI设置。
main.py (模拟器引擎): 主程序。它负责初始化环境、运行主模拟循环、通过GUI处理用户交互，并实时地将系统的状态渲染出来。
模拟循环 (一个数据科学的视角):
模拟的每一帧，都可以被看作是一个数据生成过程中的离散时间步：
状态更新: 每个智能体的状态，都根据其内部逻辑进行更新（例如，一个感染者的计时器在推进）。
交互与传播: 智能体之间基于物理上的邻近性进行交互。一个由“传染率”参数控制的随机过程，决定了这些交互的结果，并导致状态的改变（发生感染）。
数据聚合与可视化: 系统的全局状态（健康、感染、康复的人数）被实时地聚合与可视化，为当前参数所带来的影响，提供了即时的反馈。

# 3. 项目意义

尽管这个项目呈现为一个简单的可视化应用，但它对于数据科学和信息技术领域，具有重要的意义：
从“分析”到“合成”： 它代表了超越简单分析已存在数据的关键一步。这是一次通过模拟来合成数据的练习，它允许我们去探索那些真实世界数据可能不存在的场景。这正是预测建模和风险分析的基石。
理解“涌现”现象： 这个模拟生动地展示了，复杂的、宏观的模式（经典的SIR - 易感者、感染者、康复者 - 疫情曲线）是如何从简单的、微观的智能体交互中出来的。这是复杂系统科学中的一个核心概念，其应用范围极其广泛，从金融市场建模到城市规划，无所不包。
交互式数据探索： 带有可调节滑块的GUI，将这个程序从一个静态的脚本，转变为一个交互式的数据探索工具。它允许用户进行快速的假设检验（如传染率翻倍的变化等等），并培养起对模型在不同参数下的敏感性的直观理解。对于信息技术领域来说，这体现了决策支持系统 (DSS)的理想形态。

# 4. 技术栈

语言: Python 3
核心库: Pygame (用于渲染和主循环), Pygame-Widgets (用于GUI控件)

# 5. 如何运行
1.克隆这个仓库。
2.确保已安装所有必要的库: pip install pygame pygame-widgets。
3.在您的终端中，运行主脚本: python main.py。
4.用屏幕底部的滑块，来实时地调整模拟参数。
5.点击“重置”按钮，来用当前的参数设置，开始一轮新的模拟。

This project is an interactive, real-time simulation of epidemic spread, built with Python and Pygame. It allows users to dynamically adjust key parameters and observe their impact on the transmission dynamics within a closed population.

# 1. Project Motivation & Background

The inspiration for this project came from a lecture by Professor Di Zengru of the School of Systems Science at Beijing Normal University. During the class, he demonstrated a complex systems model, and I was fascinated by how simple, localized rules could lead to complex, emergent global behavior. This project is my attempt to explore that concept by building a hands-on, interactive "digital laboratory" for studying epidemic dynamics.

My goal was to move beyond static data analysis of past events and create a tool that could answer "what-if" questions. This required a shift from a purely "Data Analytics" mindset to a "Systems Modeling & Simulation" approach, which is a critical component of modern Information Technology and decision science.

# 2. Technical Architecture & Methodology

The simulator is built upon an Agent-Based Model, a powerful paradigm in data science for modeling complex systems.

# Core Components:
person.py: Defines the `Person` class, the fundamental "agent" in our system. Each agent possesses its own state (HEALTHY, INFECTED, RECOVERED) and a set of simple behavioral rules (e.g., how to move, how to update its status).
parameters.py :Centralizes all global parameters of the simulation, such as population size, virus characteristics, and UI settings.
main.py:The main program that initializes the environment, runs the main simulation loop, handles user interactions through a GUI, and renders the state of the system in real-time.

# The Simulation Loop (A Data Science Perspective):
Each frame of the simulation can be seen as a discrete time step in a data generation process:
1.State Update:The state of each agent is updated based on its internal logic (e.g., an infected person's timer progresses).
2.Interaction & Transmission: Agents interact with each other based on proximity. A stochastic process (controlled by the `Infection Rate` parameter) determines the outcome of these interactions, leading to state changes (infection).
3.Data Aggregation & Visualization: The global state of the system (counts of healthy, infected, recovered) is aggregated and visualized in real-time, providing immediate feedback on the impact of the current parameters.

# 3. Significance

While presented as a simple visual application, this project holds significant meaning for data science and information technology:

From Analysis to Synthesis: It represents a crucial step beyond simply *analyzing* existing data. It is an exercise in *synthesizing* data through simulation, allowing for the exploration of scenarios where real-world data may not exist. This is the foundation of predictive modeling and risk analysis.
Understanding Emergent Phenomena: The simulation vividly demonstrates how complex, macro-level patterns (the classic SIR - Susceptible, Infected, Recovered - epidemic curve) can emerge from simple, micro-level agent interactions. This is a core concept in complex systems science and has applications in everything from financial market modeling to urban planning.
Interactive Data Exploration:The GUI with adjustable sliders transforms the program from a static script into an interactive data exploration tool. It allows for rapid hypothesis testing ("What happens if I double the infection rate?") and fosters an intuitive understanding of the model's sensitivity to different parameters. For Information Technology, this embodies the ideal of a Decision Support System.

# 4. Technical Stack

Language:Python 3
Core Libraries:Pygame (for rendering and the main loop), Pygame-Widgets (for GUI controls)

# 5. How to Run

1.  Clone this repository.
2.  Ensure you have the necessary libraries installed: `pip install pygame pygame-widgets`.
3.  Run the main script from your terminal: `python main.py`.
4.  Use the sliders at the bottom of the screen to adjust the simulation parameters in real-time.
5.  Click the "Reset" button to start a new simulation with the current parameter settings.