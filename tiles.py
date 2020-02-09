import pygame
from load_image import load_image
from random import sample

size = WIDTH, HEIGHT = 950, 950
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bombermem")
images = {"wall": load_image("wood.png"), "grass": load_image("grass.png"),
          "iron": load_image("iron.png"), "player_1": load_image("steve.png"),
          "player_2": load_image("alex.png"), "enemy": load_image("enemy.png"),
          "bomb": load_image("bomb.png", -1)}

tiles_grass_group = pygame.sprite.Group()
tiles_iron_group = pygame.sprite.Group()
tiles_box_group = pygame.sprite.Group()
player_1_group = pygame.sprite.Group()
player_2_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_explosion_group = pygame.sprite.Group()
tiles_bomb_group = pygame.sprite.Group()
power_ups_group = pygame.sprite.Group()
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


# Бомба
class Bomb(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, player_id):
        super().__init__(tiles_bomb_group)
        self.image = images[tile_type]
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
        explosion_sound = pygame.mixer.Sound("data\\explosion.wav")
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
        explosion = BombExplosion(self.pos_x + k * tile_height,
                                  self.pos_y + m * tile_height)
        intersects = explosion.intersection()
        explosion.explode()
        if intersects:
            return True


#  Взрыв бомбы
class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_explosion_group)
        self.image = load_image("boom.png")
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.timer = 20

    def intersection(self):
        if pygame.sprite.spritecollide(self, tiles_box_group, False) or \
                pygame.sprite.spritecollide(self, tiles_iron_group, False):
            return True
        return False

    def explode(self):
        for elem in pygame.sprite.spritecollide(self, tiles_box_group, True):
            PowerUp(elem.rect.x, elem.rect.y)
        pygame.sprite.spritecollide(self, player_1_group, True)
        pygame.sprite.spritecollide(self, player_2_group, True)
        pygame.sprite.spritecollide(self, enemy_group, True)

    def remove_explosion(self):
        tiles_explosion_group.remove(self)

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.remove_explosion()


#  Класс улучшений
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(power_ups_group)
        self.type = \
            sample(["bomb_power", "bomb_amount", "character_speed", "", "", "", "", "", "", ""], k=1)[0]
        if self.type != "":
            self.image = load_image(f"{self.type}.png", -1)
            self.rect = self.image.get_rect().move(pos_x, pos_y)
        else:
            power_ups_group.remove(self)

    def power_up_lifted(self, player_id):
        if self.type == "bomb_power":
            player_id.bomb_power += 1
        elif self.type == "bomb_amount":
            player_id.max_bomb_placed += 1
        else:
            player_id.velocity += 0.25


#  Класс Игрока 1
class PlayerOne(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(player_1_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.speedx = 0
        self.speedy = 0
        self.velocity = 4
        self.bomb_power = 1
        self.max_bomb_placed = 1
        self.bomb_placed = 0
        self.char_width = 30
        self.alive = True
        self.char_height = 30
        self.bomb_intersect = True

    def place_bomb(self):
        if self.bomb_placed < self.max_bomb_placed:
            bomb_x = (self.rect.x + self.char_width / 2) // tile_height * tile_height
            bomb_y = (self.rect.y + self.char_height / 2) // tile_height * tile_height
            Bomb("bomb", bomb_x, bomb_y, self)
            self.bomb_placed += 1
            self.bomb_intersect = True

    def update(self):
        self.speedx = 0
        self.speedy = 0

        self.image = load_image("steve.png")
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -self.velocity
            self.image = load_image("steve_2.png")
        if keystate[pygame.K_d]:
            self.speedx = self.velocity
            self.image = load_image("steve_1.png")
        if keystate[pygame.K_s]:
            self.speedy = self.velocity
            self.image = load_image("steve.png")
        if keystate[pygame.K_w]:
            self.speedy = -self.velocity
            self.image = load_image("steve_3.png")

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

        if pygame.sprite.spritecollide(self, power_ups_group, False):
            for elem in pygame.sprite.spritecollide(self, power_ups_group, False):
                elem.power_up_lifted(self)
                power_ups_group.remove(elem)

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if pygame.sprite.spritecollideany(self, enemy_group) or not player_1_group:
            self.alive = False


#  Класс Игрока 2
class PlayerTwo(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(player_2_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.speedx = 0
        self.speedy = 0
        self.velocity = 4
        self.bomb_power = 1
        self.max_bomb_placed = 1
        self.bomb_placed = 0
        self.char_width = 30
        self.alive = True
        self.char_height = 30
        self.bomb_intersect = True

    def place_bomb(self):
        if self.bomb_placed < self.max_bomb_placed:
            bomb_x = (self.rect.x + self.char_width / 2) // tile_height * tile_height
            bomb_y = (self.rect.y + self.char_height / 2) // tile_height * tile_height
            Bomb("bomb", bomb_x, bomb_y, self)
            self.bomb_placed += 1
            self.bomb_intersect = True

    def update(self):
        self.speedx = 0
        self.speedy = 0

        self.image = load_image("alex.png")
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.velocity
            self.image = load_image("alex_2.png")
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.velocity
            self.image = load_image("alex_1.png")
        if keystate[pygame.K_DOWN]:
            self.speedy = self.velocity
            self.image = load_image("alex.png")
        if keystate[pygame.K_UP]:
            self.speedy = -self.velocity
            self.image = load_image("alex_3.png")

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

        if pygame.sprite.spritecollide(self, power_ups_group, False):
            for elem in pygame.sprite.spritecollide(self, power_ups_group, False):
                elem.power_up_lifted(self)
                power_ups_group.remove(elem)

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if pygame.sprite.spritecollideany(self, enemy_group) or not player_1_group:
            self.alive = False


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.speedx = 0
        self.speedy = 0
        self.move = [-1, -1, 1, 1]
        self.direction = 0
        self.intersect = None

    def update(self):
        self.speedx = 0
        self.speedy = 0

        if self.direction % 4 in [0, 2]:
            self.speedx = 3 * self.move[self.direction % 4]
        else:
            self.speedy = 3 * self.move[self.direction % 4]

        self.rect_0 = (self.rect.x, self.rect.y)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, tiles_box_group) or \
                pygame.sprite.spritecollideany(self, tiles_iron_group) or \
                pygame.sprite.spritecollideany(self, tiles_bomb_group):
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]
            self.direction += 1

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if pygame.sprite.spritecollideany(self, player_1_group):
            self.intersect = "player_1"
        if pygame.sprite.spritecollideany(self, player_2_group):
            self.intersect = "player_2"
