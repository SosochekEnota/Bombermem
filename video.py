from moviepy.editor import *
from tiles import size

clip1 = VideoFileClip("data\\Milos.mp4", target_resolution=size)
clip2 = VideoFileClip("data\\flex.mp4", target_resolution=size)
clip3 = VideoFileClip("data\\keanu.mp4", target_resolution=size)
clip4 = VideoFileClip("data\\flex_1.mp4", target_resolution=size)
clip5 = VideoFileClip("data\\check.mp4", target_resolution=(500, 500))
clips = [clip1, clip2, clip3, clip4]

