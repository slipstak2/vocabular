from unit_tests.base.testBase import TestDBBaseClass


class TestDict(TestDBBaseClass):
    def setUp(self):
        print 'setUp'

    def tearDown(self):
        print 'tearDown'

    def testTestProject(self):
        self.assertEqual(4, 2 + 2)

    def testSinglePlatforms(self):
        self.assertEqual(4, 2 * 2)
