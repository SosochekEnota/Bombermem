import os

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


explosion_image = load_image('boom.png')
bomb_image = load_image('bomb.png', -1)

tile_height = tile_width = 50

tiles_grass_group = pygame.sprite.Group()
tiles_iron_group = pygame.sprite.Group()
tiles_box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_bomb_group = pygame.sprite.Group()
tiles_explosion_group = pygame.sprite.Group()


