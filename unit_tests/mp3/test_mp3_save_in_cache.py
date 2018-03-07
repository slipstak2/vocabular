# -*- coding: utf-8 -*-

import os
from app_settings import AppSettings
from unit_tests.base.test_base import TestMp3BaseClass


class TestMp3OnlinePathGetter(TestMp3BaseClass):
    def setUp(self):
        self.mp3Eng = AppSettings().mp3Eng

    def tearDown(self):
        pass

    def testCachePath(self):
        self.assertEqual(
            os.path.normpath(os.path.join(self.mp3Eng.cacheMp3Root, 'Eng/dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3')),
            self.mp3Eng.cachePath(u'http://dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3')
        )

    def testCheckExist(self):
        self.assertTrue(self.mp3Eng.checkExist('http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp3'))
        self.assertFalse(self.mp3Eng.checkExist('http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp9'))

    def testSaveUrlInCache(self):
        url = 'http://www.yourdictionary.com/audio/t/to/town.mp3'
        self.assertTrue(self.mp3Eng.saveInLocalCache(url))
        self.assertTrue(os.path.exists(self.mp3Eng.cachePath(url)))
