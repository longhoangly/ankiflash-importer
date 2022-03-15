import os
import sys
import time
import shutil
import unittest
import logging

from shared import CommonTest
from service.constant import Constant


class FrenchCardTests(unittest.TestCase):

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

    def test_french_english_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.FR_EN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)
        time.sleep(1)

    def test_french_english_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.FR_EN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)
        time.sleep(1)

    def test_french_vietnamese_card_all_word_types(self):
        allWordTypes = True
        translation = Constant.FR_VN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)
        time.sleep(1)

    def test_french_vietnamese_card_first_word_type(self):
        allWordTypes = False
        translation = Constant.FR_VN
        self.commontest.create_flashcards(
            translation, self.words, allWordTypes)
        time.sleep(1)

    @classmethod
    def tearDownClass(self):
        os.remove(self.commontest.ankiCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
