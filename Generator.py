#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt.utils import showInfo

from PyQt5 import QtWidgets

from .Ui_ankiflash import Ui_Dialog

import os
import csv
csv.field_size_limit(2**30)


class Generator:

    def flashcards(self, ui: Ui_Dialog, words: list):

        showInfo("To Be Continue...\n" + "\n".join(map(str, words)))
        showInfo("To Be Continue...\n" + ui.inputTxt.toPlainText())
