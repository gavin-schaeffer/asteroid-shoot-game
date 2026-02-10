import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED,LINE_WIDTH, SHOT_RADIUS, PLAYER_SHOOT_SPEEED,PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_LIVES
import circleshape
from shot import Shot
import sys

class Player(circleshape.CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = PLAYER_LIVES
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.shot_cooldown -= dt

    def move(self,dt):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    def draw(self, screen):    
        pygame.draw.polygon(screen, "red", self.triangle(), width=LINE_WIDTH)
        
    def shoot(self):
        if self.shot_cooldown > 0:
            pass
        else:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
            bullet = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            bullet.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEEED
    
    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            return 1
        else:
            print("Game over!")
            return 0