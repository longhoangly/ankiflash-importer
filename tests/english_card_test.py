import os
import unittest
import shutil

from os.path import join

from .. service.worker import Worker
from .. service.constant import Constant
from .. service.enum.status import Status


class EnglishCardTests(unittest.TestCase):

    def test_create_english_english_card(self):

        translation = Constant.EN_EN
        generator = Worker.initialize_generator(translation)

        words = []
        words.append("long")
        words.append("loan")
        words.append("love")

        isOnline = False
        allWordTypes = True

        addonDir = "tests"
        mediaDir = "tests/media"
        os.makedirs(mediaDir, exist_ok=True)

        ankiCsvPath = join(addonDir, Constant.ANKI_DECK)

        worker = Worker(generator, words, translation, mediaDir,
                        isOnline, allWordTypes, ankiCsvPath)

        cards = worker.generate_cards_background()
        ankiCsv = join(addonDir, "anki_deck.csv")

        for card in cards:
            self.assertEqual(card.status, Status.SUCCESS)
            self.assertTrue(os.path.exists(ankiCsv))
            self.assertTrue(os.path.exists(mediaDir))

        os.remove(ankiCsv)
        shutil.rmtree(mediaDir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
