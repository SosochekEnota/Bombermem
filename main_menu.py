import pygame
from load_image import load_image
from video import clip5
from music import main_menu_music, play_music, stop_music

main_screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Bombermem")
play = pygame.sprite.Group()
hint = pygame.sprite.Group()
title = pygame.sprite.Group()
mouse = pygame.sprite.Group()
running = False
check = False


# Класс для кнопок
class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.spritecollideany(self, mouse):
            return True
        return False


#  Класс для курсора
class Mouse(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self, coords):
        self.rect.x = coords[0]
        self.rect.y = coords[1]


start_button = Button(play, load_image("start.png"), 0, 200)
Button(hint, load_image("hint.png"), 0, 250)
Button(title, load_image("title.png"), 0, 0)
Mouse(mouse, load_image("mouse.png"))

running_main = True
clip5.preview()
play_music(main_menu_music)
while running_main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_main = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            check = True
        if event.type == pygame.MOUSEMOTION:
            mouse.update(event.pos)

    main_screen.fill(pygame.Color("white"))
    play.draw(main_screen)
    hint.draw(main_screen)
    title.draw(main_screen)
    mouse.draw(main_screen)
    #  Проверить нажатие на кнопку старт
    if check:
        running = start_button.update()
        if running:
            running_main = False
            stop_music(main_menu_music)
        check = False
    pygame.display.flip()
