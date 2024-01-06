import os
import sys
import time
import shutil
import unittest
import logging

from tests.generator.common_test import CommonTest
from service.constant import Constant


class JapaneseCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        self.addonDir = "./tests"
        self.mediaDir = "./tests/media"
        self.commontest = CommonTest(self.addonDir, self.mediaDir)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        self.words = []
        self.words.append("夕日")
        # self.words.append("減る")
        # self.words.append("ゆかげん")
        self.words.append("長く")

    def test_japanese_english_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.JP_EN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_japanese_english_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.JP_EN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_japanese_vietnamese_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.JP_VN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    def test_japanese_vietnamese_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.JP_VN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

    @classmethod
    def tearDownClass(self):
        os.remove(self.commontest.ankiCsvPath)
        os.remove(self.commontest.mappingCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
