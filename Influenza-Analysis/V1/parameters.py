# parameters.py

# --- 屏幕设置 ---
SCREEN_WIDTH = 1200  # 窗口宽度
SCREEN_HEIGHT = 800 # 窗口高度
FPS = 60           # 游戏帧率

# --- 人口设置 ---
POPULATION_SIZE = 200 # 模拟的总人数
PERSON_RADIUS = 5     # 屏幕上每个人的半径大小

# --- 模拟行为参数 ---
# 这些参数未来可以被滑块控制
INITIAL_INFECTED = 1       # 初始感染者数量
PERSON_VELOCITY = 2        # 人的移动速度
INFECTION_RADIUS = 15      # 病毒的有效“接触”半径 (大于人的半径)
INFECTION_RATE = 0.05      # 接触后的感染概率 (5%)
RECOVERY_TIME = 15 * FPS   # 康复所需时间 (15秒 * 帧率 = 总帧数)

# --- 颜色定义 (使用RGB值) ---
COLOR_HEALTHY = (0, 200, 0)       # 绿色
COLOR_INFECTED = (200, 0, 0)      # 红色
COLOR_RECOVERED = (0, 0, 200)     # 蓝色
COLOR_BACKGROUND = (240, 240, 240) # 浅灰色
COLOR_TEXT = (20, 20, 20)           # 深灰色
