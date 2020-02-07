from tiles import *
from generate_level import generate_level_
from main_menu import running
from video import *
from load_level import load_level
from create_level import create_level
import pygame
import random as r

FPS = 60
clock = pygame.time.Clock()
create_level()
player_1, player_2 = generate_level_(load_level("map.txt"))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bombermem")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            r.choice(clips).preview()
            screen = pygame.display.set_mode(size)
        if not player_1.check():
            running = False
    player_group.update()
    enemy_group.update()
    tiles_grass_group.draw(screen)
    tiles_box_group.draw(screen)
    tiles_iron_group.draw(screen)
    tiles_bomb_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
