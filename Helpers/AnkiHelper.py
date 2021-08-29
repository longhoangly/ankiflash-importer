#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import random

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox


class AnkiHelper:
    """All Dictionary related utilities methods"""

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def messageBox(title, text, infoText):
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)

        msgBox = QMessageBox()
        msgBox.setFont(font)

        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setInformativeText(infoText)
        msgBox.setStandardButtons(QMessageBox.Close)
        msgBox.setDefaultButton(QMessageBox.Close)
        msgBox.exec_()
