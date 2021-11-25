import os
import shutil
import unittest

from os.path import join
from shared import CommonTest
from service.constant import Constant


class FrenchCardTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.addonDir = "."
        self.mediaDir = "./media"
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)

        self.words = []
        self.words.append("long")
        self.words.append("loan")
        self.words.append("love")

        self.commontest = CommonTest()
        self.commontest.mediaDir = self.mediaDir
        self.commontest.ankiCsvPath = self.ankiCsvPath

    def test_french_english_card(self):
        translation = Constant.FR_EN
        self.commontest.create_flashcards(translation, self.words)

    def test_french_vietnamese_card(self):
        translation = Constant.FR_VN
        self.commontest.create_flashcards(translation, self.words)

    @classmethod
    def tearDownClass(self):
        os.remove(self.ankiCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
