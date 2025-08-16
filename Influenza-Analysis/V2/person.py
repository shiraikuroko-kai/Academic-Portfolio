# Version 2.0
import pygame
import random
import parameters as params

class Person:
    def __init__(self, x, y, status='HEALTHY'):
        self.x = x
        self.y = y
        self.vx = random.uniform(-params.PERSON_VELOCITY, params.PERSON_VELOCITY)
        self.vy = random.uniform(-params.PERSON_VELOCITY, params.PERSON_VELOCITY)
        self.status = status
        self.infection_timer = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x <= params.PERSON_RADIUS or self.x >= params.SCREEN_WIDTH - params.PERSON_RADIUS:
            self.vx *= -1
        if self.y <= params.PERSON_RADIUS or self.y >= params.SCREEN_HEIGHT - params.PERSON_RADIUS:
            self.vy *= -1

    def update_status(self, recovery_time_frames):
        if self.status == 'INFECTED':
            self.infection_timer += 1
            if self.infection_timer >= recovery_time_frames:
                self.status = 'RECOVERED'

    def draw(self, screen):
        color_map = {
            'HEALTHY': params.COLOR_HEALTHY,
            'INFECTED': params.COLOR_INFECTED,
            'RECOVEROVED': params.COLOR_RECOVERED
        }
        pygame.draw.circle(screen, color_map.get(self.status, params.COLOR_HEALTHY), (int(self.x), int(self.y)), params.PERSON_RADIUS)

    def get_infected(self):
        self.status = 'INFECTED'
        self.infection_timer = 0
