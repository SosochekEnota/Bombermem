import pygame
from load_image import load_image
size = WIDTH, HEIGHT = 950, 950
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bombermem")
images = {"wall": load_image("wood.png"), "grass": load_image("grass.png"),
          "iron": load_image("iron.png"), "player_1": load_image("steve.png"),
          "player_2": load_image("alex.png"), "enemy": load_image("enemy.png")}

tiles_grass_group = pygame.sprite.Group()
tiles_iron_group = pygame.sprite.Group()
tiles_box_group = pygame.sprite.Group()
player_1_group = pygame.sprite.Group()
player_2_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_bomb_group = pygame.sprite.Group()
tile_width = tile_height = 50


#  Класс тайла дерева
class Wood(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_box_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


#  Класс тайла земли
class Grass(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_grass_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


#  Класс тайла железа
class Iron(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_iron_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


#  Класс Игрока 1
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(player_1_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -4
        if keystate[pygame.K_d]:
            self.speedx = 4
        if keystate[pygame.K_s]:
            self.speedy = 4
        if keystate[pygame.K_w]:
            self.speedy = -4

        self.rect_0 = (self.rect.x, self.rect.y)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, tiles_box_group) or\
                pygame.sprite.spritecollideany(self, tiles_iron_group):
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def check(self):
        alive = True
        if pygame.sprite.spritecollideany(self, enemy_group):
            alive = False
        return alive


#  Класс Игрока 2
class PlayerTwo(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(player_2_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4
        if keystate[pygame.K_UP]:
            self.speedy = -4

        self.rect_0 = (self.rect.x, self.rect.y)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, tiles_box_group) or\
                pygame.sprite.spritecollideany(self, tiles_iron_group):
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def check(self):
        alive = True
        if pygame.sprite.spritecollideany(self, enemy_group):
            alive = False
        return alive


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.speedx = 0
        self.speedy = 0
        self.move = [-1, -1, 1, 1]
        self.i = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        if self.i % 4 in [0, 2]:
            self.speedx = 3 * self.move[self.i % 4]
        else:
            self.speedy = 3 * self.move[self.i % 4]

        self.rect_0 = (self.rect.x, self.rect.y)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, tiles_box_group) or\
                pygame.sprite.spritecollideany(self, tiles_iron_group):
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]
            self.i += 1

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
