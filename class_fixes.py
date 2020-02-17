class SmartEnemy(Enemy):
    def update(self):
        self.vertical_speed = 0
        self.horizontal_speed = 0

        self.rect_0 = (self.rect.x, self.rect.y)

        if not self.generated_time or self.collide():
            self.re_generate()

        self.speed()
        self.move()

        if self.collide():
            self.rect.x = self.rect_0[0]
            self.rect.y = self.rect_0[1]

        super().checker()
        self.generated_time -= 1

    def re_generate(self):
        self.delta_directions = self.directions.copy()
        self.delta_directions.pop(self.direction)
        self.generated_time = randint(45, 75)
        self.direction = self.directions.index(''.join(sample(self.delta_directions, 1)))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(enemy_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
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
        if self.directions[self.direction % 4] == 'up':
            self.vertical_speed = -3
        elif self.directions[self.direction % 4] == 'right':
            self.horizontal_speed = 3
        elif self.directions[self.direction % 4] == 'down':
            self.vertical_speed = 3
        elif self.directions[self.direction % 4] == 'left':
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


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(door_group)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)

    def update(self):
        pass