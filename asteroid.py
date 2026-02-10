import circleshape
import pygame
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_KINDS,ASTEROID_MAX_RADIUS
from logger import log_state, log_event
import random

class Asteroid(circleshape.CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=LINE_WIDTH)
       
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            dir = random.uniform(20,50)
            first_new_asteroid_vel = self.velocity.rotate(dir)
            second_new_asteroid_vel = self.velocity.rotate(-dir)
            new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS
            first_asteroid = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            second_asteroid = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            first_asteroid.velocity = first_new_asteroid_vel * 1.2
            second_asteroid.velocity = second_new_asteroid_vel * 1.2
    
    def record_score(self):
        if self.radius == ASTEROID_MAX_RADIUS:
            return 1
        elif self.radius == ASTEROID_MIN_RADIUS:
            return 3
        else:
            return 2