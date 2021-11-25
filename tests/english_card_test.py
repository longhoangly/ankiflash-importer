import os
import shutil
import unittest

from os.path import join
from shared import CommonTest
from service.constant import Constant


class EnglishCardTests(unittest.TestCase):

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

    def test_english_english_card(self):
        translation = Constant.EN_EN
        self.commontest.create_flashcards(translation, self.words)

    def test_english_vietnamese_card(self):
        translation = Constant.EN_VN
        self.commontest.create_flashcards(translation, self.words)

    def test_english_french_card(self):
        translation = Constant.EN_FR
        self.commontest.create_flashcards(translation, self.words)

    def test_english_japanese_card(self):
        translation = Constant.EN_JP
        self.commontest.create_flashcards(translation, self.words)

    def test_english_chinese_traditional_card(self):
        translation = Constant.EN_CN_TD
        self.commontest.create_flashcards(translation, self.words)

    def test_english_chinese_simplified_card(self):
        translation = Constant.EN_CN_SP
        self.commontest.create_flashcards(translation, self.words)

    @classmethod
    def tearDownClass(self):
        os.remove(self.ankiCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
