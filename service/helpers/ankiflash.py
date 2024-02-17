#!/usr/bin/python

import re
import string
import random
import hashlib
import unicodedata

from PyQt6 import QtGui
from PyQt6.QtWidgets import QMessageBox


class AnkiHelper:
    """All AnkiFlash related utilities methods"""

    @staticmethod
    def md5_utf8(string: str):
        return hashlib.md5(string.encode("utf-8")).hexdigest()

    @staticmethod
    def stringify(string: str):
        output = re.sub("\t+", " ", string)
        output = re.sub("\s+", " ", output)
        return output

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    @staticmethod
    def message_box(title, text, infoText, iconPath=None, width=None):
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
        msgBox.setStandardButtons(QMessageBox.StandardButton.Close)
        msgBox.setDefaultButton(QMessageBox.StandardButton.Close)

        if width is not None:
            msgBox.setStyleSheet("width: {}px;".format(width))

        msgBox.exec()

    @staticmethod
    def message_box_buttons(
        title, text, infoText, standardButtons, defaultButton, iconPath=None, width=None
    ):
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
            msgBox.setStyleSheet("width: {}px;".format(width))

        return msgBox.exec()

    @staticmethod
    def unique(_list):
        # insert the list to the set
        list_set = set(_list)
        # convert the set to the list
        unique_list = list(list_set)
        return unique_list

    @staticmethod
    def compare_ignore_encode(s1, s2):
        s1_normalized = unicodedata.normalize("NFD", s1)
        s2_normalized = unicodedata.normalize("NFD", s2)
        return s1_normalized == s2_normalized
