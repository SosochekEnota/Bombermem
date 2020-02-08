import pygame
sc = pygame.display.set_mode((100, 100))
pygame.mixer.init()


#  Работа с музыкой
def play_music(song):
    if type(song) == list:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(music_list[0])
            pygame.mixer.music.play()
            music_list.append(music_list.pop(0))
    else:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=-1)


def stop_music(song):
    if type(song) == list:
        pass
    else:
        pygame.mixer.music.load(song)
        pygame.mixer.music.stop()


music_list = ["data\\game_10.mp3", "data\\game_2.mp3", "data\\game_1.mp3", "data\\game_3.mp3",
              "data\\game_4.mp3", "data\\game_5.mp3", "data\\game_6.mp3", "data\\game_7.mp3",
              "data\\game_8.mp3", "data\\game_9.mp3", "data\\game_11.mp3"]
main_menu_music = "data\\main_menu.mp3"
win_music = "data\\win.mp3"
