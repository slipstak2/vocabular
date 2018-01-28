#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://api.lingvolive.com/sounds?uri=LingvoUniversal%20(En-Ru)/brief.wav

def func1():
    import pygame

    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

    pygame.init()

    pygame.mixer.init()

    pygame.mixer.music.load('E:/YandexDisk/Vocabular/sounds/eng/exciting.mp3')

    pygame.mixer.music.play(-1)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def func2():
    import pygame
    from Tkinter import *

    root = Tk()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('E:/YandexDisk/Vocabular/sounds/eng/exciting.mp3')

    pygame.mixer.music.play(-1)
    pygame.mixer.music.load('E:/YandexDisk/Vocabular/sounds/rus/захватывающий.mp3')
    pygame.mixer.music.play()
    root.mainloop()

func2()


'''age
import vlc
p = vlc.MediaPlayer('E:/YandexDisk/Vocabular/sounds/eng/exciting.mp3')
p.play()
'''














#open kmplayer
'''
import webbrowser
webbrowser.open('E:/YandexDisk/Vocabular/sounds/eng/exciting.mp3')
webbrowser.open(u'E:/YandexDisk/Vocabular/sounds/rus/захватывающий.mp3')
'''
