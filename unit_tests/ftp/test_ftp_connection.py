from unit_tests.base.test_base import TestFtpBaseClass
from classes.ftp.ftp_manager import FtpManager


class TestFtpConnection(TestFtpBaseClass):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnection(self):
        with FtpManager() as ftpManager:
            self.assertTrue(ftpManager.isConnect)
