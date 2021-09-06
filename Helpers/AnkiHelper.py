#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import random
from os.path import join

from aqt import mw

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox


class AnkiHelper:
    """All Dictionary related utilities methods"""

    @staticmethod
    def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def messageBox(title, text, infoText, iconPath=None, width=None):

        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)

        msgBox = QMessageBox()
        msgBox.setFont(font)

        if iconPath is not None:
            icon = QtGui.QIcon(iconPath)
            msgBox.setWindowIcon(icon)

        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setInformativeText(infoText)
        msgBox.setStandardButtons(QMessageBox.Close)
        msgBox.setDefaultButton(QMessageBox.Close)

        if width is not None:
            msgBox.setStyleSheet('width: {}px;'.format(width))

        msgBox.exec_()

    @staticmethod
    def messageBoxButtons(title, text, infoText, standardButtons, defaultButton, iconPath=None, width=None):

        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)

        msgBox = QMessageBox()
        msgBox.setFont(font)

        if iconPath is not None:
            icon = QtGui.QIcon(iconPath)
            msgBox.setWindowIcon(icon)

        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setInformativeText(infoText)
        msgBox.setStandardButtons(standardButtons)
        msgBox.setDefaultButton(defaultButton)

        if width is not None:
            msgBox.setStyleSheet('width: {}px;'.format(width))

        return msgBox.exec_()
