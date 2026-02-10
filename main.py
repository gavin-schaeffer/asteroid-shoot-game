import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot
import sys
from constants import PLAYER_LIVES

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score_font = pygame.font.SysFont("OCR-A", 32)
    lives_font = pygame.font.SysFont("OCR-A", 24)
    game_over_font = pygame.font.SysFont("Impact", 96)
    score = 0
    lives = PLAYER_LIVES + 1
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots,updatable, drawable)
    asteroid_field_object = AsteroidField()
    main_player = Player(SCREEN_WIDTH/2 , SCREEN_HEIGHT/2)
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        #score print to screen
        text_surface = score_font.render(f"Score: {score}", True, "yellow")
        screen.blit(text_surface, (10, 10))
        #lives print to screen
        text_surface = lives_font.render(f"lives: {'+ '* lives}", True, "yellow")
        screen.blit(text_surface, (1180, 10))
        for object in drawable:
            object.draw(screen)
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(main_player) == True:
                if main_player.lose_life() == 1:
                    log_event("player_hit")
                    lives -= 1
                    asteroid.kill()
                else:
                    print(f"FINAL SCORE: {score}")
                    screen.fill("black")
                    line1 = game_over_font.render("GAME OVER!", True, "white")
                    line2 = score_font.render(f"Final Score: {score}", True, "white")
                    rect1 = line1.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20))
                    rect2 = line2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
                    screen.blit(line1, rect1)
                    screen.blit(line2, rect2)
                    pygame.display.flip()
                    pygame.time.wait(4000)
                    sys.exit()
        for asteroid in asteroids: 
            for shot in shots:
                if asteroid.collides_with(shot) == True:
                    log_event("asteroid_shot")
                    score += asteroid.record_score()
                    asteroid.split()
                    shot.kill()
        pygame.display.flip()
        dt = clock.tick(60)/1000

if __name__ == "__main__":
    main()
