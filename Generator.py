#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt.utils import showInfo

from .Service.Enum.Translation import Translation
from .Service.Card.ChineseGenerator import ChineseGenerator
from .Service.Card.VietnameseGenerator import VietnameseGenerator
from .Service.Card.SpanishGenerator import SpanishGenerator
from .Service.Card.JapaneseGenerator import JapaneseGenerator
from .Service.Card.FrenchGenerator import FrenchGenerator
from .Service.Card.EnglishGenerator import EnglishGenerator
from .Ui.UiGenerator import UiGenerator
from .Importer import Importer

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGroupBox, QRadioButton
from os.path import join

import logging


class Generator(QDialog):
    """Generator Dialog"""

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, version, iconPath, addonDir, mediaDir):
        super().__init__()
        self.mediaDir = mediaDir

        #Paths
        self.ankiCsvPath = join(addonDir, r'AnkiDeck.csv')

        # Create Generator GUI
        self.ui = UiGenerator()
        self.ui.setupUi(self, version, iconPath)

        # Create Importer Instance
        self.importer = Importer(version, iconPath, addonDir)

        # Set Total Input Word count
        self.ui.inputTxt.textChanged.connect(self.inputTextChanged)

        # Set Completed Output Card count
        self.ui.outputTxt.textChanged.connect(self.outputTextChanged)

        # Set Failures Word count
        self.ui.failureTxt.textChanged.connect(self.failureTextChanged)

        # Handle Generate button clicks
        self.ui.generateBtn.clicked.connect(self.btnGenerateClicked)

    def keyPressEvent(self, event):
        super(Generator, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def onKey(self, key):
        if key == QtCore.Qt.Key_Return and self.filePath:
            self.btnImportClicked()
        else:
            logging.info('key pressed: {}'.format(key))

    def inputTextChanged(self):
        words = self.ui.inputTxt.toPlainText().split("\n")
        # Filter words list, only get non-empty words
        self.words = list(filter(None, words))
        self.ui.totalLbl.setText("Total: {}".format(len(self.words)))

    def outputTextChanged(self):
        cards = self.ui.outputTxt.toPlainText().split("\n")
        # Filter cards list, only get non-empty cards
        self.cards = list(filter(None, cards))
        self.ui.completedLbl.setText("Completed: {}".format(len(self.cards)))

    def failureTextChanged(self):
        failures = self.ui.failureTxt.toPlainText().split("\n")
        # Filter failures list, only get non-empty failures
        self.failures = list(filter(None, failures))
        self.ui.failureLbl.setText("Failure: {}".format(len(self.failures)))

    def btnGenerateClicked(self):
        # Validate if input text empty?
        inputText = self.ui.inputTxt.toPlainText()

        if not inputText:
            showInfo("Empty input. No word found. Please check your input.")
            return

        # Clean up output before generating cards
        self.ui.outputTxt.setPlainText("")
        self.ui.failureTxt.setPlainText("")

        source = self.selectedRadio(self.ui.sourceBox)
        target = self.selectedRadio(self.ui.translatedToBox)
        translation = Translation(source, target)

        # Initialize Generator based on translation
        self.initializeGenerator(translation)

        self.allWordTypes = self.ui.allWordTypes.isChecked()
        self.isOnline = self.ui.isOnline.isChecked()

        # Send word list to generator
        self.generator.generateCards(
            self.words, translation, self.mediaDir, self.isOnline, self.allWordTypes, self.ankiCsvPath, self.ui, self.importer)

    def initializeGenerator(self, translation: Translation):
        if translation.source == "English":
            self.generator = EnglishGenerator()
        elif translation.source == "Japanese":
            self.generator = JapaneseGenerator()
        elif translation.source == "Vietnamese":
            self.generator = VietnameseGenerator()
        elif translation.source == "French":
            self.generator = FrenchGenerator()
        elif translation.source == "Spanish":
            self.generator = SpanishGenerator()
        elif translation.source == "Chinese":
            self.generator = ChineseGenerator()

    def selectedRadio(self, groupBox: QGroupBox) -> str:

        # Get all radio buttons
        radioBtns = [radio for radio in groupBox.children(
        ) if isinstance(radio, QRadioButton)]

        # Find choosen radio and return text
        for radio in radioBtns:
            if radio.isChecked():
                return radio.text()
