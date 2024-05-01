import os
import sys
import time
import shutil
import unittest
import logging

from tests.generator.common_test import CommonTest
from service.constant import Constant


class VietnameseCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.addonDir = "./tests"
        self.mediaDir = "./tests/media"
        self.commontest = CommonTest(self.addonDir, self.mediaDir)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        self.words = []
        self.words.append("hay")
        self.words.append("mỗi khi")
        self.words.append("tôi")
        self.words.append("chúng ta")
        self.words.append("yêu")
        self.words.append("dài")

    def test_vietnamese_english_card_all_word_types(self):
        relatedWords = True
        translation = Constant.VN_EN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_vietnamese_english_first_word_type(self):
        relatedWords = False
        translation = Constant.VN_EN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_vietnamese_vietnamese_card_all_word_types(self):
        relatedWords = True
        translation = Constant.VN_VN
        self.commontest.create_flashcards(translation, self.words, relatedWords, 1)
        time.sleep(1)

    def test_vietnamese_vietnamese_first_word_type(self):
        relatedWords = False
        translation = Constant.VN_VN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_vietnamese_french_card_all_word_types(self):
        relatedWords = True
        translation = Constant.VN_FR
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_vietnamese_french_card_first_word_type(self):
        relatedWords = False
        translation = Constant.VN_FR
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_vietnamese_japanese_card_all_word_types(self):
        relatedWords = True
        translation = Constant.VN_JP
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_vietnamese_japanese_card_first_word_type(self):
        relatedWords = False
        translation = Constant.VN_JP
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    @classmethod
    def tearDownClass(self):
        os.remove(self.commontest.ankiCsvPath)
        os.remove(self.commontest.mappingCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
