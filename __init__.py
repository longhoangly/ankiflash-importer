#!/usr/bin/python

"""
AnkiFlash Importer

This is the next generation of AnkiFlash Importer, it's now not only include importer but also embeded the generator inside.
* Generator helps you to generate flashcards for learning vocabularies
* Importer helps to import those flashcards into Anki

Author: Long Ly
Website: https://www.facebook.com/ankiflashcom
Modified: May 24, 2022
"""

import os
import logging
from os.path import join
from logging.handlers import RotatingFileHandler
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

import aqt
from aqt import mw, gui_hooks

from .service.constant import Constant
from .service.helpers.ankiflash import AnkiHelper
from .ui.generator.generator_dialog import GeneratorDialog

version = "1.3.0"


class AnkiFlash:
    """AnkiFlash"""

    def __init__(self, version):

        # disable old log process
        logging.shutdown()

        # Directories
        self.addonDir = join(mw.pm.addonFolder(), "1129289384")
        self.mediaDir = mw.col.media.dir()
        os.makedirs(self.mediaDir, exist_ok=True)

        # Paths
        self.iconPath = join(self.addonDir, r"resources/anki.png")
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)

        # Config Logging (Rotate Every 10MB)
        os.makedirs(join(self.addonDir, r"logs"), exist_ok=True)
        self.ankiFlashLog = join(self.addonDir, r"logs/ankiflash.log")

        rfh = RotatingFileHandler(
            filename=self.ankiFlashLog,
            maxBytes=50000000,
            backupCount=3,
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

    def show_generator(self):
        self.generator.show()


def init_anki_flash(browser: aqt.browser.Browser):

    sorted_field = ""
    input_words = []

    mw.selectedNotes = []
    mw.mapping_keys = []

    if browser is not None:
        mw.selectedNoteIds = browser.selected_notes()

        if len(mw.selectedNoteIds) > 0:
            for noteId in mw.selectedNoteIds:
                note = mw.col.get_note(noteId)
                mw.selectedNotes.append(note)

                sorted_idx = mw.col.models.sort_idx(note.note_type())
                sorted_field = note.keys()[sorted_idx]

                keyword = note.__getitem__(sorted_field)
                input_words.append(keyword)

                if len(mw.mapping_keys) == 0:
                    mw.mapping_keys = note.keys()
                else:
                    mw.mapping_keys = list(set(mw.mapping_keys) & set(note.keys()))

        tmp_set = set(mw.mapping_keys)
        tmp_set.remove(sorted_field)
        mw.mapping_keys = [sorted_field] + list(tmp_set)

    mw.ankiFlash = AnkiFlash(version)
    mw.ankiFlash.generator = GeneratorDialog(
        version, mw.ankiFlash.iconPath, mw.ankiFlash.addonDir, mw.ankiFlash.mediaDir
    )

    if browser is not None:
        mw.ankiFlash.generator.enable_mapping(True, mw.mapping_keys)
        mw.ankiFlash.generator.set_input_words(AnkiHelper.unique(input_words))
    else:
        mw.ankiFlash.generator.enable_mapping(False, [])

    mw.ankiFlash.show_generator()


# Create
ankiFlashAct = QAction("AnkiFlash {}".format(version), mw)
ankiFlashAct.triggered.connect(lambda: init_anki_flash(None))
mw.form.menuTools.addAction(ankiFlashAct)


def add_context_menu_item(browser: aqt.browser.Browser, menu: QMenu) -> None:

    browserAct = QAction("Update notes with AnkiFlash", mw)
    browserAct.triggered.connect(lambda: init_anki_flash(browser))
    menu.addAction(browserAct)


gui_hooks.browser_will_show_context_menu.append(add_context_menu_item)
