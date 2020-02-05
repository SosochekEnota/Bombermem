import os
import pygame


size = WIDTH, HEIGHT = 550, 550
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


tile_images = {"wall": load_image("box.png"), "empty": load_image("grass.png")}
player_image = load_image("mar.png", -1)
tile_width = tile_height = 50
player = None
tiles_grass_group = pygame.sprite.Group()
tiles_box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
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


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_bomb_group)
        self.image = load_image("bomb.png")
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
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
        if pygame.sprite.spritecollideany(self, tiles_box_group):
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


def generate_level_(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile_grass('empty', x, y)
            elif level[y][x] == '#':
                Tile_box('wall', x, y)
            elif level[y][x] == '@':
                Tile_grass('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y
