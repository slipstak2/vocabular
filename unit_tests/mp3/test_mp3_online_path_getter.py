# -*- coding: utf-8 -*-

from app_settings import AppSettings
from unit_tests.base.test_base import TestSoundBaseClass


class TestSoundOnlinePathGetter(TestSoundBaseClass):
    def setUp(self):
        self.soundsEng = AppSettings().soundsEng

    def tearDown(self):
        pass

    def testTown(self):
        expectedPaths = self.soundsEng.onlineSoundPaths('town')
        self.assertEqual(10, len(expectedPaths))
        targetPaths = [
            u'http://dictionary.cambridge.org/us/media/english/uk_pron/u/ukt/uktou/uktouch030.mp3',
            u'http://dictionary.cambridge.org/us/media/english/us_pron/t/tow/town_/town.mp3',
            u'http://img2.tfd.com/pron/mp3/en/UK/d3/d3sfsksosjht.mp3',
            u'http://img2.tfd.com/pron/mp3/en/US/d3/d3sfsksosjht.mp3',
            u'http://s3.amazonaws.com/audio.vocabulary.com/1.0/us/T/194ON040Z9VX2.mp3',
            u'http://static.sfdict.com/staticrep/dictaudio/T04/T0408500.mp3',
            u'http://www.onelook.com/pronounce/macmillan/UK/town-British-English-pronunciation.mp3',
            u'http://www.onelook.com/pronounce/macmillan/US/town-American-English-pronunciation.mp3',
            u'http://www.oxforddictionaries.com/media/english/uk_pron/t/tow/town_/town__gb_1.mp3',
            u'http://www.yourdictionary.com/audio/t/to/town.mp3',
        ]
        for targetPath, expectedPath in zip(targetPaths, expectedPaths):
            self.assertEqual(targetPath, expectedPath)

    def testHrundik(self):
        expectedPaths = self.soundsEng.onlineSoundPaths('hrundik')
        self.assertEqual(0, len(expectedPaths))

    def testUPPER_CASE(self):
        expectedPaths = self.soundsEng.onlineSoundPaths('AQUEDUCT')
        self.assertEqual(10, len(expectedPaths))
        targetPaths = [
            u'http://dictionary.cambridge.org/us/media/english/uk_pron/u/uka/ukaqu/ukaquat003.mp3',
            u'http://dictionary.cambridge.org/us/media/english/us_pron/a/aqu/aqued/aqueduct.mp3',
            u'http://img2.tfd.com/pron/mp3/en/UK/sg/sgdjshsydtdtsrdos5gk.mp3',
            u'http://img2.tfd.com/pron/mp3/en/US/sg/sgdjshsydtdtsrdos5gk.mp3',
            u'http://s3.amazonaws.com/audio.vocabulary.com/1.0/us/A/1TNHT9FM3KBC1.mp3',
            u'http://static.sfdict.com/staticrep/dictaudio/A06/A0627700.mp3',
            u'http://www.onelook.com/pronounce/macmillan/UK/aqueduct-British-English-pronunciation.mp3',
            u'http://www.onelook.com/pronounce/macmillan/US/aqueduct-American-English-pronunciation.mp3',
            u'http://www.oxforddictionaries.com/media/english/uk_pron/a/aqu/aqued/aqueduct__gb_1.mp3',
            u'http://www.yourdictionary.com/audio/a/aq/aqueduct.mp3',
        ]
        for targetPath, expectedPath in zip(targetPaths, expectedPaths):
            self.assertEqual(targetPath, expectedPath)
