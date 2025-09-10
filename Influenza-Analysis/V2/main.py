import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
import random
import parameters as params
from person import Person
import matplotlib.pyplot as plt
import pandas as pd 

pygame.init()

SIMULATION_HEIGHT = params.SCREEN_HEIGHT - 200
CONTROL_PANEL_Y = SIMULATION_HEIGHT

screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT))
pygame.display.set_caption("疫情模拟器")
clock = pygame.time.Clock()
font_stats = pygame.font.SysFont('SimHei', 24)
font_slider = pygame.font.SysFont('SimHei', 18)
font_slider_value = pygame.font.SysFont('Arial', 20, bold=True)

# 创建GUI
panel_rect = pygame.Rect(0, CONTROL_PANEL_Y, params.SCREEN_WIDTH, 200)
slider_width = 200
slider_start_x = 50
slider_y = CONTROL_PANEL_Y + 60
slider_gap = 290

slider_population = Slider(screen, slider_start_x, slider_y, slider_width, 15, min=10, max=500, step=10, initial=params.POPULATION_SIZE, colour=(200, 200, 200), handleColour=(0, 122, 255))
slider_velocity = Slider(screen, slider_start_x + slider_gap, slider_y, slider_width, 15, min=0.5, max=10, step=0.5, initial=params.PERSON_VELOCITY, colour=(200, 200, 200), handleColour=(0, 122, 255))
slider_infection_rate = Slider(screen, slider_start_x + slider_gap * 2, slider_y, slider_width, 15, min=0.01, max=1.0, step=0.01, initial=params.INFECTION_RATE, colour=(200, 200, 200), handleColour=(0, 122, 255))
slider_recovery_time = Slider(screen, slider_start_x + slider_gap * 3, slider_y, slider_width, 15, min=1, max=30, step=1, initial=15, colour=(200, 200, 200), handleColour=(0, 122, 255))

button_reset = Button(screen, params.SCREEN_WIDTH - 200, CONTROL_PANEL_Y + 120, 150, 50, text='resetsim',
                      inactiveColour=(0, 122, 255), hoverColour=(0, 100, 220), pressedColour=(0, 80, 180),
                      textColour=(255, 255, 255), onClick=lambda: reset_simulation())

population = []
history_data = []

# 核心
def reset_simulation():
    global population, history_data, simulation_ended
    population = []
    history_data = []
    simulation_ended = False # Reset the flag
    pop_size = slider_population.getValue()
    for _ in range(pop_size):
        x = random.randint(params.PERSON_RADIUS, params.SCREEN_WIDTH - params.PERSON_RADIUS)
        y = random.randint(params.PERSON_RADIUS, SIMULATION_HEIGHT - params.PERSON_RADIUS)
        population.append(Person(x, y))
    
    if population:
        for _ in range(params.INITIAL_INFECTED):
            if population:
                random.choice(population).get_infected()
    print("模拟已重置。")

def plot_history_and_save(history):
    if not history:
        print("没有历史数据可供绘制或内存读取出错")
        return
        
    print("模拟结束，正在生成SIR曲线图...")
    df_history = pd.DataFrame(history, columns=['Healthy', 'Infected', 'Recovered'])
    
    plt.figure(figsize=(12, 7))
    plt.plot(df_history['Healthy'], label='Healthy ', color='green')
    plt.plot(df_history['Infected'], label='Infected ', color='red')
    plt.plot(df_history['Recovered'], label='Recovered ', color='blue')
    
    plt.title('SIR Epidemic Curve from Simulation', fontsize=16)
    plt.xlabel('Time (Frames)', fontsize=12)
    plt.ylabel('Number of People', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig('SIR_curve.png')
    print("成功！SIR曲线图已保存为 'SIR_curve.png'")

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

reset_simulation()

running = True
simulation_ended = False

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # 更新
    current_velocity = slider_velocity.getValue()
    current_infection_rate = slider_infection_rate.getValue()
    recovery_time_frames = slider_recovery_time.getValue() * params.FPS

    # 模拟交互
    infected_people = [p for p in population if p.status == 'INFECTED']
    for healthy in population:
        if healthy.status == 'HEALTHY':
            for infected in infected_people:
                distance = ((infected.x - healthy.x) ** 2 + (infected.y - healthy.y) ** 2) ** 0.5
                if distance < params.INFECTION_RADIUS:
                    if random.random() < current_infection_rate:
                        healthy.get_infected()
                        break 

    for person in population:
        person.move(current_velocity) 
        person.update_status(recovery_time_frames)

    #  渲染画面 
    screen.fill(params.COLOR_BACKGROUND)
    for person in population:
        person.draw(screen)

    pygame.draw.rect(screen, (235, 235, 235), panel_rect) 
    pygame.draw.line(screen, (200, 200, 200), (0, CONTROL_PANEL_Y), (params.SCREEN_WIDTH, CONTROL_PANEL_Y), 2)
    pygame_widgets.update(events)
    
    # 渲染GUI
    draw_text("人口密度:", font_slider, params.COLOR_TEXT, screen, slider_start_x, slider_y - 25)
    draw_text("流动性:", font_slider, params.COLOR_TEXT, screen, slider_start_x + slider_gap, slider_y - 25)
    draw_text("传染率:", font_slider, params.COLOR_TEXT, screen, slider_start_x + slider_gap*2, slider_y - 25)
    draw_text("康复时间 (秒):", font_slider, params.COLOR_TEXT, screen, slider_start_x + slider_gap*3, slider_y - 25)
    
    draw_text(str(slider_population.getValue()), font_slider_value, (0, 0, 0), screen, slider_start_x + slider_width + 15, slider_y - 5)
    draw_text(f"{slider_velocity.getValue():.1f}", font_slider_value, (0, 0, 0), screen, slider_start_x + slider_gap + slider_width + 15, slider_y - 5)
    draw_text(f"{slider_infection_rate.getValue():.2f}", font_slider_value, (0, 0, 0), screen, slider_start_x + slider_gap*2 + slider_width + 15, slider_y - 5)
    draw_text(f"{slider_recovery_time.getValue()}s", font_slider_value, (0, 0, 0), screen, slider_start_x + slider_gap*3 + slider_width + 15, slider_y - 5)
    
    # 实时统计
    healthy_count = sum(1 for p in population if p.status == 'HEALTHY')
    infected_count = sum(1 for p in population if p.status == 'INFECTED')
    recovered_count = len(population) - healthy_count - infected_count
    
    history_data.append((healthy_count, infected_count, recovered_count))
    
    if infected_count == 0 and not simulation_ended and len(history_data) > 1:
        plot_history_and_save(history_data)
        simulation_ended = True
    
    stats_labels = [f"健康 (Healthy): {healthy_count}", f"感染 (Infected): {infected_count}", f"康复 (Recovered): {recovered_count}"]
    for i, label in enumerate(stats_labels):
         draw_text(label, font_stats, params.COLOR_TEXT, screen, 20, CONTROL_PANEL_Y + 110 + i * 25)

    pygame.display.flip()
    clock.tick(params.FPS)

pygame.quit()
