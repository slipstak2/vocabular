# -*- coding: utf-8 -*-

from classes.sound.sound_files_manager import SoundEng
from unit_tests.base.test_base import TestSoundBaseClass


class TestFtp(TestSoundBaseClass):
    def setUp(self):
        self.soundsEng = SoundEng

    def tearDown(self):
        pass

    def testUploadToFtp(self):
        url = 'http://www.yourdictionary.com/audio/t/to/town.mp3'
        #self.assertTrue(self.soundsEng.uploadToFtp(url))
        #self.assertTrue(self.soundsEng.checkCacheExist(url))
