import os
import shutil
import unittest

from service.worker import Worker
from service.constant import Constant
from service.enum.status import Status


class CommonTest(unittest.TestCase):

    def create_flashcards(self, translation, words):

        generator = Worker.initialize_generator(translation)

        isOnline = False
        allWordTypes = True
        os.makedirs(self.mediaDir, exist_ok=True)

        worker = Worker(generator, words, translation, self.mediaDir,
                        isOnline, allWordTypes, self.ankiCsvPath)

        cards = worker.generate_cards_background()

        for card in cards:
            self.assertEqual(card.status, Status.SUCCESS)
            self.assertTrue(os.path.exists(self.ankiCsvPath))
            self.assertTrue(os.path.exists(self.mediaDir))
