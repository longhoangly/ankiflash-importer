import os
import sys
import time
import shutil
import unittest
import logging

from tests.generator.common_test import CommonTest
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
        self.words.append("lobe")
        self.words.append("aimer")

    def test_french_english_card_all_word_types(self):
        relatedWords = True
        translation = Constant.FR_EN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_french_english_card_first_word_type(self):
        relatedWords = False
        translation = Constant.FR_EN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_french_vietnamese_card_all_word_types(self):
        relatedWords = True
        translation = Constant.FR_VN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    def test_french_vietnamese_card_first_word_type(self):
        relatedWords = False
        translation = Constant.FR_VN
        self.commontest.create_flashcards(translation, self.words, relatedWords)
        time.sleep(1)

    @classmethod
    def tearDownClass(self):
        os.remove(self.commontest.ankiCsvPath)
        os.remove(self.commontest.mappingCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
