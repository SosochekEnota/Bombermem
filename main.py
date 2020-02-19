from tiles import *
from generate_level import generate_level_
from main_menu import running, players
from video import *
from load_level import load_level
from create_level import create_level
from win import win
from music import play_music, stop_music, music_list
import pygame
import random as r

if players == "two":
    FPS = 60
    running_win = False
    clock = pygame.time.Clock()
    create_level(players)
    player_1, player_2, enemy, nothing = generate_level_(load_level("map.txt"), "two")
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bombermem")

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
                if event.key == pygame.K_SLASH:
                    player_2.place_bomb()
                if event.key == pygame.K_SPACE:
                    player_1.place_bomb()

        player_1_group.update()
        player_2_group.update()
        enemy_group.update()
        for e in enemy:  # Проверка пересечения врагов с игроками
            if e.intersect == "player_1":
                running_two = False
                win("second.png")
            if e.intersect == "player_2":
                running_two = False
                win("first.png")
        if not player_1.alive:
            running_two = False
            win("first.png")
        if not player_2.alive:
            running_two = False
            win("second.png")
        if not player_1_group:
            running_two = False
            win("second.png")
        if not player_2_group:
            running_two = False
            win("first.png")

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

if players == "one":
    FPS = 60
    running_win = False
    level = 1
    clock = pygame.time.Clock()
    create_level(players)
    player_1, player_2, enemy, ghost = generate_level_(load_level("map.txt"), "one", level)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bombermem")

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
                if event.key == pygame.K_SPACE:
                    player_1.place_bomb()

        player_1_group.update()
        door_group.update()
        if ghost is not None:
            ghost.speed(level)
        enemy_group.update()
        for e in enemy:  # Проверка пересечения врагов с игроками
            if e.intersect == "player_1":
                running_two = False
                win("one_lose.png")

        if not player_1.alive:
            running_two = False
            win("one_lose.png")

        if not player_1_group:
            running_two = False
            win("one_lose.png")

        if player_1.open and player_1.trapdoor:
            level += 1
            if level > 69:
                running = False
                win("one.png")
            create_level("one")
            tiles_grass_group.empty()
            tiles_iron_group.empty()
            tiles_box_group.empty()
            player_1_group.empty()
            player_2_group.empty()
            door_group.empty()
            enemy_group.empty()
            tiles_explosion_group.empty()
            tiles_bomb_group.empty()
            power_ups_group.empty()
            key_group.empty()

            player_1, player_2, enemy, ghost = generate_level_(load_level("map.txt"), "one", level)

        tiles_bomb_group.update()
        tiles_explosion_group.update()
        tiles_grass_group.draw(screen)
        key_group.draw(screen)
        tiles_box_group.draw(screen)
        tiles_bomb_group.draw(screen)
        tiles_explosion_group.draw(screen)
        power_ups_group.draw(screen)
        tiles_iron_group.draw(screen)
        player_1_group.draw(screen)
        player_2_group.draw(screen)
        door_group.draw(screen)
        enemy_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
