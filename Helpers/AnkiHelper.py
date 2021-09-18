#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import string
import random
import hashlib

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox


class AnkiHelper:
    """All Dictionary related utilities methods"""

    @staticmethod
    def md5Utf8(string: str):
        return hashlib.md5(string.encode("utf-8")).hexdigest()

    @staticmethod
    def stringify(string: str):
        output = re.sub('\t+', ' ', string)
        output = re.sub('\s+', ' ', output)
        return output

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
