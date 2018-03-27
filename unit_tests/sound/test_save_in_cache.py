# -*- coding: utf-8 -*-

from unit_tests.base.test_base import TestSoundBaseClass
import os
from classes.file.sound_web_file import SoundEngWebFile


class TestSaveInCache(TestSoundBaseClass):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCachePath(self):
        url = u'http://dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3'
        soundWebFile = SoundEngWebFile(url)
        self.assertEqual(
            os.path.normpath(os.path.join(soundWebFile.cacheRoot, 'Eng/dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3')),
            soundWebFile.cachePath
        )

    def testCheckOnlineExist(self):
        soundOKFile = SoundEngWebFile('http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp3')
        self.assertTrue(soundOKFile.checkOnlineExist())
        soundFailFile = SoundEngWebFile('http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp9')
        self.assertFalse(soundFailFile.checkOnlineExist())

    def testSaveUrlInCache(self):
        url = 'http://s3.amazonaws.com/audio.vocabulary.com/1.0/us/A/1WLMHFJWU12UX.mp3'
        soundWebFile = SoundEngWebFile(url)
        self.assertTrue(soundWebFile.checkOnlineExist())
        self.assertTrue(soundWebFile.saveInLocalCache())
        self.assertTrue(soundWebFile.checkCacheExist())
