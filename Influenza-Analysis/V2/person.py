import pygame
import random
import parameters as params

class Person:
    def __init__(self, x, y, status='HEALTHY'):
        """
        Initializes a Person agent.
        """
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1) 
        self.vy = random.uniform(-1, 1)
        self.status = status
        self.infection_timer = 0

    def move(self, velocity):
        """Updates the person's position and handles boundary collisions."""
        self.x += self.vx * velocity
        self.y += self.vy * velocity
        
        if self.x <= params.PERSON_RADIUS or self.x >= params.SCREEN_WIDTH - params.PERSON_RADIUS:
            self.vx *= -1
        if self.y <= params.PERSON_RADIUS or self.y >= params.SCREEN_HEIGHT - params.PERSON_RADIUS:
            self.vy *= -1

    def update_status(self, recovery_time_frames):
        """Updates the health status based on the infection timer."""
        if self.status == 'INFECTED':
            self.infection_timer += 1
            if self.infection_timer >= recovery_time_frames:
                self.status = 'RECOVERED'

    def draw(self, screen):
        """Draws the person on the screen according to their status."""
		#定义展示状态
        color_map = {
            'HEALTHY': params.COLOR_HEALTHY,
            'INFECTED': params.COLOR_INFECTED,
            'RECOVERED': params.COLOR_RECOVERED # Corrected spelling
        }
        color = color_map[self.status]
            
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), params.PERSON_RADIUS)

    def get_infected(self):
        """Sets the person's status to INFECTED."""
        if self.status == 'HEALTHY':
            self.status = 'INFECTED'
            self.infection_timer = 0
