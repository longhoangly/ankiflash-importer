import os
import sys
import time
import shutil
import unittest
import logging

from tests.generator.common_test import CommonTest
from service.constant import Constant


class EnglishCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        self.addonDir = "./tests"
        self.mediaDir = "./tests/media"
        self.commontest = CommonTest(self.addonDir, self.mediaDir)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        self.words = []
        self.words.append("long")
        self.words.append("loan")
        self.words.append("love")

    def test_english_english_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.EN_EN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_english_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.EN_EN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_vietnamese_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.EN_VN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_vietnamese_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.EN_VN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_french_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.EN_FR
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_french_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.EN_FR
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_japanese_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.EN_JP
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_japanese_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.EN_JP
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_chinese_traditional_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.EN_CN_TD
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_chinese_traditional_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.EN_CN_TD
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_chinese_simplified_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.EN_CN_SP
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_english_chinese_simplified_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.EN_CN_SP
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    @classmethod
    def tearDownClass(self):
        os.remove(self.commontest.ankiCsvPath)
        os.remove(self.commontest.mappingCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
