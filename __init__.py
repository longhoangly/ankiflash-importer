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

from aqt import mw
from PyQt5.QtWidgets import QAction
from .Ankiflash import AnkiFlash


version = '1.0.0'


def ankiFlash():
    mw.myWidget = window = AnkiFlash(version)
    window.keyPressed.connect(window.onKey)
    window.show()


ankiFlashAct = QAction("AnkiFlash {}".format(version), mw)
ankiFlashAct.triggered.connect(ankiFlash)
mw.form.menuTools.addAction(ankiFlashAct)
