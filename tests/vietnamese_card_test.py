import os
import shutil
import unittest

from os.path import join
from shared import CommonTest
from service.constant import Constant


class VietnameseCardTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.addonDir = "."
        self.mediaDir = "./media"
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)

        self.words = []
        self.words.append("mỗi khi")
        self.words.append("tôi")
        self.words.append("chúng ta")
        self.words.append("yêu")
        self.words.append("dài")

        self.commontest = CommonTest()
        self.commontest.mediaDir = self.mediaDir
        self.commontest.ankiCsvPath = self.ankiCsvPath

    def test_vietnamese_english_card(self):
        translation = Constant.VN_EN
        self.commontest.create_flashcards(translation, self.words)

    def test_vietnamese_vietnamese_card(self):
        translation = Constant.VN_VN
        self.commontest.create_flashcards(translation, self.words)

    def test_vietnamese_french_card(self):
        translation = Constant.VN_FR
        self.commontest.create_flashcards(translation, self.words)

    def test_vietnamese_japanese_card(self):
        translation = Constant.VN_JP
        self.commontest.create_flashcards(translation, self.words)

    @classmethod
    def tearDownClass(self):
        os.remove(self.ankiCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
