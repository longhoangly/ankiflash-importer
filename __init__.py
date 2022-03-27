#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
AnkiFlash Importer

This is the next generation of AnkiFlash Importer, it's now not only include importer but also embeded the generator inside.
* Generator helps you to generate flashcards for learning vocabularies
* Importer helps to import those flashcards into Anki

Author: Long Ly
Website: https://www.facebook.com/ankiflashcom
Modified: Jun 24, 2021
"""

import os
import logging
from os.path import join
from logging.handlers import RotatingFileHandler

import aqt
from aqt import mw, gui_hooks
from PyQt5.QtWidgets import QAction, QMenu

from . service.constant import Constant
from . service.helpers.anki_helper import AnkiHelper
from . ui.generator_dialog import GeneratorDialog

version = '1.1.0'
# Update field content for existing cards
mw.selectedNoteIds = []
mw.selectedNotes = []


class AnkiFlash():
    """AnkiFlash"""

    def __init__(self, version):

        # disable old log process
        logging.shutdown()

        # Directories
        self.addonDir = join(mw.pm.addonFolder(), "1129289384")
        self.mediaDir = mw.col.media.dir()
        os.makedirs(self.mediaDir, exist_ok=True)

        # Paths
        self.iconPath = join(self.addonDir, r'resources/anki.png')
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)

        # Config Logging (Rotate Every 10MB)
        os.makedirs(join(self.addonDir, r'logs'), exist_ok=True)
        self.ankiFlashLog = join(self.addonDir, r'logs/ankiflash.log')

        rfh = RotatingFileHandler(
            filename=self.ankiFlashLog, maxBytes=50000000, backupCount=3, encoding='utf-8')
        should_roll_over = os.path.isfile(self.ankiFlashLog)
        if should_roll_over:
            rfh.doRollover()
        logging.basicConfig(level=logging.INFO,
                            format=u"%(asctime)s - %(threadName)s [%(thread)d] - %(message)s",
                            datefmt="%d-%b-%y %H:%M:%S",
                            handlers=[rfh])

    def show_generator(self):
        self.generator.show()


def init_anki_flash():

    mw.ankiFlash = AnkiFlash(version)
    mw.ankiFlash.generator = GeneratorDialog(
        version, mw.ankiFlash.iconPath, mw.ankiFlash.addonDir, mw.ankiFlash.mediaDir)
    mw.ankiFlash.generator.enable_mapping(False)

    input_words = []
    if len(mw.selectedNoteIds) > 0:
        mw.ankiFlash.generator.enable_mapping(True)

        for noteId in mw.selectedNoteIds:
            note = mw.col.get_note(noteId)
            mw.selectedNotes.append(note)
            first_note_field = note.__getitem__(note.keys()[0])
            input_words.append(first_note_field)
        mw.ankiFlash.generator.set_input_words(AnkiHelper.unique(input_words))

    mw.ankiFlash.show_generator()


# Create
ankiFlashAct = QAction("AnkiFlash {}".format(version), mw)
ankiFlashAct.triggered.connect(init_anki_flash)
mw.form.menuTools.addAction(ankiFlashAct)


def add_context_menu_item(browser: aqt.browser.Browser, menu: QMenu) -> None:

    browserAct = QAction("Update notes with AnkiFlash", mw)
    browserAct.triggered.connect(init_anki_flash)
    menu.addAction(browserAct)
    # Getting selected notes
    mw.selectedNoteIds = browser.selected_notes()


gui_hooks.browser_will_show_context_menu.append(add_context_menu_item)
