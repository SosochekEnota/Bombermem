from moviepy.editor import *
from generate_level import size
import pygame

pygame.display.set_caption("Bombermem")
clip1 = VideoFileClip("data\\Milos.mp4", target_resolution=size)
clip2 = VideoFileClip("data\\flex.mp4", target_resolution=size)
clip3 = VideoFileClip("data\\keanu.mp4", target_resolution=size)

clips = [clip1, clip2, clip3]

