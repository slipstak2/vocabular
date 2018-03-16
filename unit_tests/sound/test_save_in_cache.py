# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestSoundBaseClass
import os
from classes.sound.sound_files_manager import SoundEng


class TestSoundOnlinePathGetter(TestSoundBaseClass):
    def setUp(self):
        self.soundsEng = SoundEng

    def tearDown(self):
        pass

    def testCachePath(self):
        self.assertEqual(
            os.path.normpath(os.path.join(self.soundsEng.cacheSound3Root, 'Eng/dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3')),
            self.soundsEng.cachePath(u'http://dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3')
        )

    def testCheckOnlineExist(self):
        self.assertTrue(self.soundsEng.checkOnlineExist('http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp3'))
        self.assertFalse(self.soundsEng.checkOnlineExist('http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp9'))

    def testSaveUrlInCache(self):
        url = 'http://s3.amazonaws.com/audio.vocabulary.com/1.0/us/A/1WLMHFJWU12UX.mp3'
        self.assertTrue(self.soundsEng.checkOnlineExist(url))
        self.assertTrue(self.soundsEng.saveInLocalCache(url))
        self.assertTrue(self.soundsEng.checkCacheExist(url))
