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

    def update(self):
        pass


class StandingEnemy(Enemy):
    def update(self):
        pygame.sprite.spritecollide(self, player_1_group, True)
        pygame.sprite.spritecollide(self, player_2_group, True)


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

        pygame.sprite.spritecollide(self, player_1_group, True)
        pygame.sprite.spritecollide(self, player_2_group, True)


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