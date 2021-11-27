import os
import shutil
import unittest

from os.path import join
from shared import CommonTest
from service.constant import Constant


class VietnameseCardTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.addonDir = "./tests"
        self.mediaDir = "./tests/media"
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)

        self.words = []
        self.words.append("mỗi khi")
        self.words.append("tôi")
        self.words.append("chúng ta")
        self.words.append("yêu")
        self.words.append("dài")

        self.commontest = CommonTest(
            self.addonDir, self.mediaDir, self.ankiCsvPath)

    def test_vietnamese_english_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.VN_EN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_english_first_word_type(self):
        allWordTypes = False
        translation = Constant.VN_EN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_vietnamese_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.VN_VN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_vietnamese_first_word_type(self):
        allWordTypes = False
        translation = Constant.VN_VN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_french_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.VN_FR
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_french_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.VN_FR
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_japanese_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.VN_JP
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    def test_vietnamese_japanese_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.VN_JP
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)

    @classmethod
    def tearDownClass(self):
        os.remove(self.ankiCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
