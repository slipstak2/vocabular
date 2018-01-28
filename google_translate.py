#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gtts import gTTS
import os

def run(text, filename, lang):
    tts = gTTS(text, lang)
    tts.save("{}.mp3".format(filename))


#run('stored', lang='en')
run(u'поисковая система', 'poiskovay_system', lang='ru')
