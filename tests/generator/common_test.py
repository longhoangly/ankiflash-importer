#!/usr/bin/python

import os
import unittest
import logging

from typing import List
from os.path import join

from service.constant import Constant
from service.enum.card import Card
from service.gen_worker import GenWorker
from service.enum.status import Status
from logging.handlers import RotatingFileHandler


class CommonTest(unittest.TestCase):
    def __init__(self, addonDir, mediaDir):
        super().__init__()

        # disable old log process
        logging.shutdown()

        self.mediaDir = mediaDir
        self.ankiCsvPath = join(addonDir, Constant.ANKI_DECK)
        self.mappingCsvPath = join(addonDir, Constant.MAPPING_CSV)

        # Config Logging (Rotate Every 10MB)
        os.makedirs(join(addonDir, r"logs"), exist_ok=True)
        self.ankiFlashLog = join(addonDir, r"logs/ankiflash.log")

        rfh = RotatingFileHandler(
            filename=self.ankiFlashLog,
            maxBytes=50000000,
            backupCount=5,
            encoding="utf-8",
        )
        should_roll_over = os.path.isfile(self.ankiFlashLog)
        if should_roll_over:
            rfh.doRollover()
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(threadName)s [%(thread)d] - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            handlers=[rfh],
        )

    def create_flashcards(
        self, translation, words, relatedWords, failedCount=0
    ) -> List[Card]:
        isOnline = False
        os.makedirs(self.mediaDir, exist_ok=True)

        worker = GenWorker(
            words, translation, self.mediaDir, isOnline, relatedWords, self.ankiCsvPath
        )

        result = worker.generate_cards_background()

        self.assertGreater(len(result["cards"]), 0)
        for card in result["cards"]:
            self.assertEqual(card.status, Status.SUCCESS)

        self.assertEqual(len(result["failedCards"]), failedCount)
        for card in result["failedCards"]:
            self.assertEqual(card.status, Status.WORD_NOT_FOUND)

        self.assertTrue(os.path.exists(self.ankiCsvPath))
        self.assertTrue(os.path.exists(self.mappingCsvPath))
        self.assertTrue(os.path.exists(self.mediaDir))
