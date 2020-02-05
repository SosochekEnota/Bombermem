from generate_level import *
from video import *
import pygame
import random as r

FPS = 60
clock = pygame.time.Clock()
player, level_x, level_y = generate_level_(load_level('map_1.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            r.choice(clips).preview()
            screen = pygame.display.set_mode(size)
    player_group.update()
    tiles_grass_group.draw(screen)
    tiles_box_group.draw(screen)
    tiles_bomb_group.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()