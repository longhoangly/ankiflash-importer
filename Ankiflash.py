#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt import mw

from os.path import join
from logging.handlers import RotatingFileHandler
from .GeneratorDialog import GeneratorDialog

import os
import logging


class AnkiFlash():
    """AnkiFlash"""

    def __init__(self, version):

        # disable old log process
        logging.shutdown()

        # Directories
        self.addonDir = join(mw.pm.addonFolder(), "1129289384")
        self.mediaDir = mw.col.media.dir()

        # Paths
        self.iconPath = join(self.addonDir, r'Resources/anki.png')
        self.ankiCsvPath = join(self.addonDir, r'AnkiDeck.csv')

        # Config Logging (Rotate Every 10MB)
        os.makedirs(join(self.addonDir, r'Logs'), exist_ok=True)
        self.ankiFlashLog = join(self.addonDir, r'Logs/ankiflash.log')

        rfh = RotatingFileHandler(
            filename=self.ankiFlashLog, maxBytes=50000000, backupCount=3, encoding='utf-8')
        should_roll_over = os.path.isfile(self.ankiFlashLog)
        if should_roll_over:
            rfh.doRollover()
        logging.basicConfig(level=logging.INFO,
                            format=u"%(asctime)s - %(threadName)s [%(thread)d] - %(message)s",
                            datefmt="%d-%b-%y %H:%M:%S",
                            handlers=[rfh])

        # Create Generator Dialog
        self.generator = GeneratorDialog(
            version, self.iconPath, self.addonDir, self.mediaDir)
        self.generator.show()
