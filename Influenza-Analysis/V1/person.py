# person.py
#
# 这个文件定义了我们模拟世界中的核心对象：Person类。
# 每一个Person对象，都是一个独立的、拥有自己状态和行为的“智能体”。

import pygame
import random
import parameters as params

class Person:
    def __init__(self, x, y, status='HEALTHY'):
        """
        初始化一个Person对象。
        
        参数:
        x (int): 初始x坐标。
        y (int): 初始y坐标。
        status (str): 初始健康状态 ('HEALTHY', 'INFECTED', 'RECOVERED')。
        """
        self.x = x
        self.y = y
        
        # 赋予一个随机的移动方向和速度
        self.vx = random.uniform(-params.PERSON_VELOCITY, params.PERSON_VELOCITY)
        self.vy = random.uniform(-params.PERSON_VELOCITY, params.PERSON_VELOCITY)
        
        self.status = status
        self.infection_timer = 0 # 感染计时器

    def move(self):
        """更新这个人的位置，并处理边界碰撞。"""
        self.x += self.vx
        self.y += self.vy
        
        # 简单的边界反弹逻辑
        if self.x <= params.PERSON_RADIUS or self.x >= params.SCREEN_WIDTH - params.PERSON_RADIUS:
            self.vx *= -1
        if self.y <= params.PERSON_RADIUS or self.y >= params.SCREEN_HEIGHT - params.PERSON_RADIUS:
            self.vy *= -1

    def update_status(self):
        """根据计时器，更新这个人的健康状态。"""
        if self.status == 'INFECTED':
            self.infection_timer += 1
            if self.infection_timer >= params.RECOVERY_TIME:
                self.status = 'RECOVERED'

    def draw(self, screen):
        """根据状态，将这个人绘制到屏幕上。"""
        color = params.COLOR_HEALTHY
        if self.status == 'INFECTED':
            color = params.COLOR_INFECTED
        elif self.status == 'RECOVERED':
            color = params.COLOR_RECOVERED
            
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), params.PERSON_RADIUS)

    def try_to_infect(self, other_people):
        """
        如果这个人是感染者，尝试去感染范围内的其他人。
        """
        if self.status != 'INFECTED':
            return
            
        for other in other_people:
            # 只尝试感染健康的人，并且不是自己
            if other.status == 'HEALTHY' and self != other:
                # 计算两个人之间的距离
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                
                # 如果距离小于病毒传播半径
                if distance < params.INFECTION_RADIUS:
                    # 根据感染概率，进行一次随机判定
                    if random.random() < params.INFECTION_RATE:
                        other.status = 'INFECTED'
