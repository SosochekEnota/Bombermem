import pygame
from load_image import load_image
from video import clip5

main_screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Bombermem")
buttons = pygame.sprite.Group()
mouse = pygame.sprite.Group()
running = False


class Button(pygame.sprite.Sprite):
    image = load_image("1.png")

    def __init__(self, buttons):
        super().__init__(buttons)
        self.image = Button.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self):
        if pygame.sprite.spritecollideany(self, mouse):
            return True
        return False


class Mouse(pygame.sprite.Sprite):
    image = load_image("mouse.png")

    def __init__(self, mouse):
        super().__init__(mouse)
        self.image = Mouse.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]


a = Button(buttons)
Mouse(mouse)
running_main = True
check = False
clip5.preview()
while running_main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_main = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            check = True
        if event.type == pygame.MOUSEMOTION:
            mouse.update(event.pos)
    main_screen.fill(pygame.Color("blue"))
    buttons.draw(main_screen)
    mouse.draw(main_screen)
    if check:
        running = a.update()
        if running:
            running_main = False
        check = False
    pygame.display.flip()
