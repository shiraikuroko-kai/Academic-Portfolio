# main.py
#
# 这是我们模拟器的主程序。
# 它负责初始化Pygame，创建所有Person对象，并运行主模拟循环。

import pygame
import random
import parameters as params
from person import Person

# --- 1. 初始化 ---
pygame.init()

# 创建窗口和时钟
screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT))
pygame.display.set_caption("交互式疫情传播模拟器 (MVP)")
clock = pygame.time.Clock()

# 创建字体，用于在屏幕上显示信息
font = pygame.font.SysFont('SimHei', 24) # 使用SimHei来支持中文

# --- 2. 创建人口 ---
population = []
for _ in range(params.POPULATION_SIZE):
    x = random.randint(params.PERSON_RADIUS, params.SCREEN_WIDTH - params.PERSON_RADIUS)
    y = random.randint(params.PERSON_RADIUS, params.SCREEN_HEIGHT - params.PERSON_RADIUS)
    population.append(Person(x, y))

# 随机选择初始感染者
for i in range(params.INITIAL_INFECTED):
    random.choice(population).status = 'INFECTED'
    
print("模拟环境初始化完成。")

# --- 3. 主模拟循环 ---
running = True
while running:
    # --- 3.1 事件处理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 3.2 更新逻辑 ---
    for person in population:
        person.move()          # 移动每个人
        person.update_status() # 更新每个人的状态
        person.try_to_infect(population) # 感染者尝试去感染他人

    # --- 3.3 渲染画面 ---
    screen.fill(params.COLOR_BACKGROUND) # 填充背景色

    for person in population:
        person.draw(screen) # 绘制每个人

    # --- 3.4 显示统计信息 ---
    healthy_count = sum(1 for p in population if p.status == 'HEALTHY')
    infected_count = sum(1 for p in population if p.status == 'INFECTED')
    recovered_count = sum(1 for p in population if p.status == 'RECOVERED')

    # 创建要显示的文本
    stats_text_lines = [
        f"总人数: {params.POPULATION_SIZE}",
        f"健康 (绿色): {healthy_count}",
        f"感染 (红色): {infected_count}",
        f"康复 (蓝色): {recovered_count}",
    ]
    
    # 将文本逐行渲染到屏幕左上角
    for i, line in enumerate(stats_text_lines):
        text_surface = font.render(line, True, params.COLOR_TEXT)
        screen.blit(text_surface, (10, 10 + i * 30))

    # 更新整个屏幕
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(params.FPS)

# --- 4. 退出程序 ---
pygame.quit()
print("模拟结束。")
