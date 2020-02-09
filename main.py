from tiles import *
from generate_level import generate_level_
from main_menu import running
from video import *
from load_level import load_level
from create_level import create_level
from win import win
from music import play_music, stop_music, music_list
import pygame
import random as r


FPS = 60
running_win = False
clock = pygame.time.Clock()
create_level()
player_1, player_2, enemy = generate_level_(load_level("map.txt"))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bombermem")
list_of_keys = []  # Список нажатий на клавиатуру для проверки Konami-code

# Главный игровой цикл
while running:
    play_music(music_list)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                r.choice(clips).preview()
                screen = pygame.display.set_mode(size)
            if event.key == pygame.K_KP8:
                list_of_keys.append("8")
            if event.key == pygame.K_KP2:
                list_of_keys.append("2")
            if event.key == pygame.K_KP4:
                list_of_keys.append("4")
            if event.key == pygame.K_KP6:
                list_of_keys.append("6")
            if event.key == pygame.K_b:
                list_of_keys.append("B")
            if event.key == pygame.K_a:
                list_of_keys.append("A")
            if event.key == pygame.K_SLASH:
                player_2.place_bomb()
            if event.key == pygame.K_SPACE:
                player_1.place_bomb()

    if "88224646BA" in "".join(list_of_keys):
        clip7.preview()
        list_of_keys.clear()
    player_1_group.update()
    player_2_group.update()
    enemy_group.update()
    for e in enemy:  # Проверка пересечения врагов с игроками
        if e.intersect == "player_1":
            running = False
            win("second.png")
        if e.intersect == "player_2":
            running = False
            win("first.png")
    if not player_1.alive:
        running = False
        win("first.png")
    if not player_2.alive:
        running = False
        win("second.png")
    tiles_bomb_group.update()
    tiles_explosion_group.update()
    tiles_grass_group.draw(screen)
    tiles_box_group.draw(screen)
    tiles_bomb_group.draw(screen)
    tiles_explosion_group.draw(screen)
    power_ups_group.draw(screen)
    tiles_iron_group.draw(screen)
    player_1_group.draw(screen)
    player_2_group.draw(screen)
    enemy_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
