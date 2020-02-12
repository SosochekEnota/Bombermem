import pygame
from load_image import load_image
from random import sample, randint

size = WIDTH, HEIGHT = 950, 950
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Bombermem")
images = {"wall": load_image("wood.png"), "grass": load_image("grass.png"),
          "iron": load_image("iron.png"), "player_1": load_image("steve.png"),
          "player_2": load_image("alex.png"), "enemy": load_image("enemy.png"),
          "moving_enemy": load_image("moving_enemy.png"), "smart_enemy": load_image("smart_enemy.png"),
          "ghost_enemy": load_image("ghost_enemy.png"), "bomb": load_image("bomb.png", -1)}

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


#  Класс Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, group, preset, preset_key):
        super().__init__(group)
        self.group = group
        self.sprites = preset
        self.keys = preset_key
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

        self.image = self.sprites[0]
        keystate = pygame.key.get_pressed()
        if keystate[self.keys[0]]:
            self.speedx = -self.velocity
            self.image = self.sprites[2]
        if keystate[self.keys[1]]:
            self.speedx = self.velocity
            self.image = self.sprites[1]
        if keystate[self.keys[2]]:
            self.speedy = self.velocity
            self.image = self.sprites[0]
        if keystate[self.keys[3]]:
            self.speedy = -self.velocity
            self.image = self.sprites[3]

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

        if pygame.sprite.spritecollideany(self, enemy_group):
            self.alive = False


#  Класс Игрока 1
class PlayerOne(Player):
    def __init__(self, tile_type, pos_x, pos_y):
        preset = [load_image("steve.png"), load_image("steve_1.png"),
                  load_image("steve_2.png"), load_image("steve_3.png")]
        preset_key = [pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_w]
        super().__init__(tile_type, pos_x, pos_y, player_1_group, preset, preset_key)


#  Класс Игрока 2
class PlayerTwo(Player):
    def __init__(self, tile_type, pos_x, pos_y):
        preset = [load_image("alex.png"), load_image("alex_1.png"),
                  load_image("alex_2.png"), load_image("alex_3.png")]
        preset_key = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
        super().__init__(tile_type, pos_x, pos_y, player_2_group, preset, preset_key)


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.generated_time = randint(120, 300)
        self.directions = ['up', 'right', 'down', 'left']
        self.direction = 0  # direction represented as index of element from self.directions
        self.intersect = False

    def collide(self):
        if pygame.sprite.spritecollideany(self, tiles_box_group) or \
                pygame.sprite.spritecollideany(self, tiles_iron_group) or \
                pygame.sprite.spritecollideany(self, tiles_bomb_group):
            return True

    def speed(self):
        if self.directions[self.direction] == 'up':
            self.vertical_speed = -3
        elif self.directions[self.direction] == 'right':
            self.horizontal_speed = 3
        elif self.directions[self.direction] == 'down':
            self.vertical_speed = 3
        elif self.directions[self.direction] == 'left':
            self.horizontal_speed = -3

    def move(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.x += self.horizontal_speed
        self.rect.y += self.vertical_speed

    def checker(self):
        if pygame.sprite.spritecollideany(self, player_1_group):
            self.intersect = "player_1"
        if pygame.sprite.spritecollideany(self, player_2_group):
            self.intersect = "player_2"


#  Класс лоубота
class StandingEnemy(Enemy):
    def update(self):
        super().checker()


#  Класс средбота
class MovingEnemy(Enemy):
    def update(self):
        self.horizontal_speed = 0
        self.vertical_speed = 0

        self.speed()

        self.rect_0 = (self.rect.x, self.rect.y)

        self.move()

        if self.collide():
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]
            self.direction += 1

        super().checker()


class SmartEnemy(Enemy):
    def update(self):
        self.vertical_speed = 0
        self.horizontal_speed = 0

        self.rect_0 = (self.rect.x, self.rect.y)

        if not self.generated_time or self.collide():
            if not self.generated_time:
                self.re_generate()
            if self.collide():
                self.re_generate()
                self.rect.x = self.rect_0[0]
                self.rect.y = self.rect_0[1]
        else:
            self.speed()
            self.move()

        super().checker()

    def re_generate(self):
        self.generated_time = randint(120, 300)
        self.direction = randint(1, 4)


class GhostEnemy(Enemy):
    def __init__(self, tile_type, pos_x, pos_y, player):
        super().__init__(tile_type, pos_x, pos_y)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.player = player

    def update(self):
        if self.rect.x < self.player.rect.x:
            self.horizontal_speed = -0.5
        elif self.rect.x > self.player.rect.x:
            self.horizontal_speed = 0.5
        if self.rect.y > self.player.rect.y:
            self.vertical_speed = 0.5
        elif self.rect.y < self.player.rect.y:
            self.vertical_speed = -0.5

        self.move()
        super().checker()