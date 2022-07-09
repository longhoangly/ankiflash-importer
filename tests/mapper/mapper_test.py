import os
import sys
import time
import shutil
import unittest
import logging

from soupsieve import select

from service.mapper import Mapper
from service.constant import Constant
from tests.generator.common_test import CommonTest
from tests.mapper.note import Note


class MapperTests(unittest.TestCase):
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

        self.mapper = Mapper()

    def test_mapping_english_english_cards(self):
        allWordTypes = True
        translation = Constant.EN_EN
        self.commontest.create_flashcards(translation, self.words, allWordTypes)
        time.sleep(1)

        keywordIdx = "keyMap"
        selectedNotes = [Note("long"), Note("loan")]
        mapping = {"field1": "WordType", "field2": "Example", "field3": "Phonetic"}
        cardFields = ["keyMap", "field1", "field2", "field3"]

        updated_count = self.mapper.update_flashcards(
            self.addonDir,
            keywordIdx,
            selectedNotes,
            mapping,
            cardFields,
        )
        logging.info("Updated {} flashcards!".format(updated_count))

        self.assertEqual(updated_count, 2)
        for note in selectedNotes:
            self.assertTrue("field1Value" not in note.data["field1"])
            self.assertTrue("field2Value" not in note.data["field2"])
            self.assertTrue("field3Value" not in note.data["field3"])

    @classmethod
    def tearDownClass(self):
        os.remove(self.commontest.ankiCsvPath)
        os.remove(self.commontest.mappingCsvPath)
        shutil.rmtree(self.mediaDir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
