import pygame
from load_image import load_image
from video import clip5, clip7
from music import main_menu_music, play_music, stop_music


main_screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Bombermem")
play = pygame.sprite.Group()
hint = pygame.sprite.Group()
title = pygame.sprite.Group()
mouse = pygame.sprite.Group()
running = False
list_of_keys = []  # Список нажатий на клавиатуру для проверки Konami-code
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


start_button_1 = Button(play, load_image("start_1.png"), 0, 200)
start_button_2 = Button(play, load_image("start_2.png"), 250, 200)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP8:
                list_of_keys.append("8")
            if event.key == pygame.K_KP2:
                list_of_keys.append("2")
            if event.key == pygame.K_KP4:
                list_of_keys.append("4")
            if event.key == pygame.K_KP6:
                list_of_keys.append("6")
            if event.key == pygame.K_b:
                list_of_keys.append("B")
            if event.key == pygame.K_a:
                list_of_keys.append("A")

    if "88224646BA" in "".join(list_of_keys):
        clip7.preview()
        list_of_keys.clear()
        main_screen = pygame.display.set_mode((500, 500))

    main_screen.fill(pygame.Color("white"))
    play.draw(main_screen)
    hint.draw(main_screen)
    title.draw(main_screen)
    mouse.draw(main_screen)
    #  Проверить нажатие на кнопку старт
    if check:
        two_players = start_button_2.update()
        one_player = start_button_1.update()
        if two_players:
            running = True
            players = "two"
            running_main = False
            stop_music()
        if one_player:
            running = True
            players = "one"
            running_main = False
            stop_music()
        check = False
    pygame.display.flip()
