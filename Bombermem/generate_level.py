import os

import pygame

size = WIDTH, HEIGHT = 950, 950
screen = pygame.display.set_mode(size)


#  Функция загрузки изображения
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


#  Функция загрузки карты из текстового файла
def load_level(filename):
    filename = "data/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    mapFile.close()
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


tile_images = {"wall": load_image("wood.png"), "empty": load_image("grass.png"),
               "iron": load_image("iron.png")}
player_image = load_image("mar.png", -1)
enemy_image = load_image("bomb.png")
bomb_image = load_image("bomb.png", -1)
tile_width = tile_height = 50
player = None
tiles_grass_group = pygame.sprite.Group()
tiles_iron_group = pygame.sprite.Group()
tiles_box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_explosion_group = pygame.sprite.Group()
tiles_bomb_group = pygame.sprite.Group()


class Tile_box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_box_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tile_grass(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_grass_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tile_iron(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_iron_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_id):
        super().__init__(tiles_bomb_group)
        self.image = bomb_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.timer = 120
        self.player = player_id
        self.up_free = True
        self.down_free = True
        self.left_free = True
        self.right_free = True

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.explode_bomb()

    def explode_bomb(self):
        self.player.bomb_placed -= 1
        tiles_bomb_group.remove(self)
        explosion_sound = pygame.mixer.Sound('explosion.wav')
        explosion_sound.play()
        for k in range(self.player.bomb_power + 1):
            for m in range(self.player.bomb_power + 1):
                if k == 0 and m > 0 and self.down_free is True:
                    if self.create_explosion(k, m):
                        self.down_free = False
                elif m == 0 and k > 0 and self.right_free is True:
                    if self.create_explosion(k, m):
                        self.right_free = False
        for k in range(0, self.player.bomb_power * -1 - 1, -1):
            for m in range(0, self.player.bomb_power * -1 - 1, -1):
                if k == 0 and m < 0 and self.up_free is True:
                    if self.create_explosion(k, m):
                        self.up_free = False
                elif m == 0 and k < 0 and self.left_free is True:
                    if self.create_explosion(k, m):
                        self.left_free = False

        self.create_explosion(0, 0)

    def create_explosion(self, k, m):
        print(k, m)
        explosion = Bomb_explosion(self.pos_x + k * tile_height,
                                   self.pos_y + m * tile_height)
        print(self.pos_x + k * tile_height, self.pos_y + m * tile_height, '\n')
        intersects = explosion.intersection()
        explosion.explode()
        if intersects:
            return True


class Bomb_explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_explosion_group)
        self.image = load_image('boom.png')
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.timer = 50

    def intersection(self):
        if pygame.sprite.spritecollide(self, tiles_box_group, False) or \
                pygame.sprite.spritecollide(self, tiles_iron_group, False):
            return True
        return False

    def explode(self):
        pygame.sprite.spritecollide(self, tiles_box_group, True)
        pygame.sprite.spritecollide(self, player_group, True)

    def remove_explosion(self):
        tiles_explosion_group.remove(self)

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.remove_explosion()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.bomb_power = 3
        self.max_bomb_placed = 1
        self.bomb_placed = 0
        self.char_width = 24
        self.char_height = 40
        self.speedx = 0
        self.speedy = 0
        self.bomb_intersect = True

    def place_bomb(self):
        if self.bomb_placed <= self.max_bomb_placed:
            bomb_x = (self.rect.x + self.char_width / 2) // tile_height * tile_height
            bomb_y = (self.rect.y + self.char_height / 2) // tile_height * tile_height
            Bomb(bomb_x, bomb_y, self)
            self.bomb_placed += 1
            self.bomb_intersect = True

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.space_pressed = False

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
        if pygame.sprite.spritecollideany(self, tiles_box_group) or \
                pygame.sprite.spritecollideany(self, tiles_iron_group):
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]

        if self.bomb_intersect is True:
            if not pygame.sprite.spritecollideany(self, tiles_bomb_group):
                self.bomb_intersect = False
        else:
            if pygame.sprite.spritecollideany(self, tiles_bomb_group):
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image = enemy_image
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
        if pygame.sprite.spritecollideany(self, tiles_box_group) or \
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


def generate_level_(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile_grass('empty', x, y)
            if level[y][x] == '#':
                Tile_box('wall', x, y)
            elif level[y][x] == '*':
                Tile_iron("iron", x, y)
            elif level[y][x] == '1':
                new_player = Player(x, y)
            elif level[y][x] == "2":
                Enemy(x, y)
    return new_player, x, y
