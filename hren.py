import pygame
import os

size = WIDTH, HEIGHT = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

char_width = 24
char_height = 40


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png', -1)
bomb_image = load_image('bomb.png', -1)

tile_width = tile_height = 50


class Bomb_explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(explosion_group)
        self.image = load_image('boom.png')
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.timer = 50
        pygame.sprite.spritecollide(self, tiles_box_group, True)
        pygame.sprite.spritecollide(self, player_group, True)

    def update(self):
        self.timer -= 1
        self.remove_explosion()

    def remove_explosion(self):
        if self.timer == 0:
            explosion_group.remove(self)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player_id):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.timer = player_id.bomb_timer
        self.power = player.bomb_power

        super().__init__(bombs_group)

        self.image = bomb_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.timer -= 1
        self.remove_bomb()

    def remove_bomb(self):
        if self.timer == 0:
            bombs_group.remove(self)
            for k in range(0, self.power + 1):
                for m in range(0, self.power + 1):
                    if not k * m:
                        Bomb_explosion(self.pos_x + k * tile_height,
                                       self.pos_y + m * tile_height)
                        Bomb_explosion(-1 * k * tile_height + self.pos_x,
                                       -1 * m * tile_height + self.pos_y)


class Tile_box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

        super().__init__(tiles_box_group)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Tile_grass(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_grass_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.bomb_power = 3
        self.bomb_placed = 0
        self.bomb_timer = 120
        self.bomb_counter = 1

        self.speed_x = 0
        self.speed_y = 0

        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def place_bomb(self):
        if self.bomb_placed < self.bomb_counter:
            bomb_x = (self.rect.x + char_width / 2) // tile_height * tile_height
            bomb_y = (self.rect.y + char_height / 2) // tile_height * tile_height
            Bomb(bomb_x, bomb_y, self)
            self.bomb_placed += 1

    def update(self):
        self.speed_x = 0
        self.speed_y = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -4
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 4
        if keystate[pygame.K_DOWN]:
            self.speed_y = 4
        if keystate[pygame.K_UP]:
            self.speed_y = -4
        if keystate[pygame.K_SPACE]:
            self.place_bomb()
        self.rect_0 = (self.rect.x, self.rect.y)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

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

        if self.bomb_placed:
            self.bomb_timer -= 1
            if self.bomb_timer == 0:
                self.bomb_placed -= 1
                self.bomb_timer = 120


player = None

explosion_group = pygame.sprite.Group()
bombs_group = pygame.sprite.Group()
tiles_grass_group = pygame.sprite.Group()
tiles_box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
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


player, level_x, level_y = generate_level(load_level('map.txt'))
FPS = 60
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LALT] and keys[pygame.K_F4]:
                running = False

    bombs_group.update()
    player_group.update()
    explosion_group.update()
    tiles_grass_group.draw(screen)
    tiles_box_group.draw(screen)
    explosion_group.draw(screen)
    bombs_group.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
