#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QGroupBox, QMessageBox, QRadioButton
from PyQt5.QtCore import QThread
from PyQt5 import QtGui

from .Ui.UiGenerator import UiGenerator
from .ImporterDialog import ImporterDialog
from .Service.Enum.Translation import Translation
from .Service.BaseGenerator import Worker

from .Service.Card.ChineseGenerator import ChineseGenerator
from .Service.Card.VietnameseGenerator import VietnameseGenerator
from .Service.Card.SpanishGenerator import SpanishGenerator
from .Service.Card.JapaneseGenerator import JapaneseGenerator
from .Service.Card.FrenchGenerator import FrenchGenerator
from .Service.Card.EnglishGenerator import EnglishGenerator
from .Service.Constant import Constant
from .Helpers.AnkiHelper import AnkiHelper

from os.path import join
import logging
import csv
csv.field_size_limit(2**30)


class GeneratorDialog(QDialog):
    """Generator Dialog"""

    def __init__(self, version, iconPath, addonDir, mediaDir):

        super().__init__()
        self.mediaDir = mediaDir
        self.iconPath = iconPath

        # Paths
        self.ankiCsvPath = join(addonDir, r'AnkiDeck.csv')

        # Create Generator GUI
        self.ui = UiGenerator()
        self.ui.setupUi(self, version, iconPath)
        self.ui.cancelBtn.setDisabled(True)

        # Create Importer Instance
        self.importer = ImporterDialog(version, iconPath, addonDir)
        self.importer.keyPressed.connect(self.importer.onKey)

        # Set Total Input Word count
        self.ui.inputTxt.textChanged.connect(self.inputTextChanged)

        # Set Completed Output Card count
        self.ui.outputTxt.textChanged.connect(self.outputTextChanged)

        # Set Failures Word count
        self.ui.failureTxt.textChanged.connect(self.failureTextChanged)

        # Handle clicks on Generate button
        self.ui.generateBtn.clicked.connect(self.btnGenerateClicked)

        # Handle clicks on Progress bar
        self.ui.importBtn.clicked.connect(self.btnImporterClicked)

        self.getSupportedLanguages()
        # Handle user clicks on translation
        self.ui.source1.clicked.connect(self.getSupportedLanguages)
        self.ui.source2.clicked.connect(self.getSupportedLanguages)
        self.ui.source3.clicked.connect(self.getSupportedLanguages)
        self.ui.source4.clicked.connect(self.getSupportedLanguages)

    def closeEvent(self, event):
        logging.shutdown()

    def inputTextChanged(self):
        words = self.ui.inputTxt.toPlainText().split("\n")
        # Filter words list, only get non-empty words
        self.words = list(filter(None, words))
        self.ui.totalLbl.setText("Total: {}".format(len(self.words)))

    def outputTextChanged(self):
        cards = self.ui.outputTxt.toPlainText().split("\n")
        # Filter cards list, only get non-empty cards
        self.cards = list(filter(None, cards))
        self.cardCount = len(self.cards)
        self.ui.completedLbl.setText("Completed: {}".format(len(self.cards)))

    def failureTextChanged(self):
        failures = self.ui.failureTxt.toPlainText().split("\n")
        # Filter failures list, only get non-empty failures
        self.failures = list(filter(None, failures))
        self.failureCount = len(self.failures)
        self.ui.failureLbl.setText("Failure: {}".format(len(self.failures)))

    def initializeGenerator(self, translation: Translation):
        if translation.source == Constant.ENGLISH:
            self.generator = EnglishGenerator()
        elif translation.source == Constant.JAPANESE:
            self.generator = JapaneseGenerator()
        elif translation.source == Constant.VIETNAMESE:
            self.generator = VietnameseGenerator()
        elif translation.source == Constant.FRENCH:
            self.generator = FrenchGenerator()
        elif translation.source == Constant.SPANISH:
            self.generator = SpanishGenerator()
        elif Constant.CHINESE in translation.source:
            self.generator = ChineseGenerator()

    def btnGenerateClicked(self):
        # Validate if input text empty?
        inputText = self.ui.inputTxt.toPlainText()

        if not inputText:
            AnkiHelper.messageBox("Info",
                                  "No input words available for generating.",
                                  "Please check your input words!",
                                  self.iconPath)
            return

        # Increase to 2% as a processing signal to user
        self.ui.generateProgressBar.setValue(2)
        self.ui.generateBtn.setDisabled(True)

        # Clean up output before generating cards
        self.ui.outputTxt.setPlainText("")
        self.ui.failureTxt.setPlainText("")

        # Get translation options
        source = self.selectedRadio(self.ui.sourceBox)
        target = self.selectedRadio(self.ui.translatedToBox)
        self.translation = Translation(source, target)

        # Get generating options
        self.allWordTypes = self.ui.allWordTypes.isChecked()
        self.isOnline = self.ui.isOnline.isChecked()

        # Initialize Generator based on translation
        self.initializeGenerator(self.translation)

        # Step 2: Create a QThread object
        self.bgThread = QThread(self)
        self.bgThread.setTerminationEnabled(True)

        # Step 3: Create a worker object
        self.worker = Worker(self.generator, self.words, self.translation, self.mediaDir,
                             self.isOnline, self.allWordTypes, self.ankiCsvPath)

        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.bgThread)

        # Step 5: Connect signals and slots
        self.bgThread.started.connect(self.worker.generateCardsBackground)

        self.worker.finished.connect(self.bgThread.quit)
        self.bgThread.finished.connect(self.bgThread.deleteLater)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.reportProgress)

        self.worker.cardStr.connect(self.reportCard)
        self.worker.failureStr.connect(self.reportFailure)

        # Step 6: Start the thread
        self.bgThread.start()
        self.ui.cancelBtn.setEnabled(True)
        self.ui.generateBtn.setDisabled(True)

        # Handle cancel background task
        self.ui.cancelBtn.clicked.connect(self.cancelBackgroundTask)

        # Final resets
        self.bgThread.finished.connect(self.finishedGenerationProgress)

    def cancelBackgroundTask(self):
        logging.info("Canceling background task...")
        self.bgThread.requestInterruption()
        self.bgThread.quit()
        self.ui.outputTxt.setPlainText("")
        self.isCancelled = True

    def finishedGenerationProgress(self):

        self.ui.cancelBtn.setDisabled(True)
        self.ui.generateBtn.setEnabled(True)

        # Return if thread is interrupted
        if self.isCancelled:
            AnkiHelper.messageBox("Info",
                                  "Flashcard generation process stopped!",
                                  "Restart by clicking Generate button.",
                                  self.iconPath)
            return

        if self.ui.outputTxt.toPlainText():
            btnSelected = AnkiHelper.messageBoxButtons("Info",
                                                       "Finished generating flashcards.\nThanks for using AnkiFlash!",
                                                       "Do you want to import generated flashcards now?\n\nProgress completed 100%\n- Input: {}\n- Output: {}\n- Failure: {}".format(
                                                           len(self.words), self.cardCount, self.failureCount),
                                                       QMessageBox.No | QMessageBox.Yes,
                                                       QMessageBox.Yes,
                                                       self.iconPath)
            if btnSelected == QMessageBox.Yes:
                self.btnImporterClicked()
        else:
            AnkiHelper.messageBoxButtons("Info",
                                         "Finished generating flashcards.\nThanks for using AnkiFlash!",
                                         "No output flashcards available for importing.\n\nProgress completed 100%\n- Input: {}\n- Output: {}\n- Failure: {}".format(
                                             len(self.words), self.cardCount, self.failureCount),
                                         QMessageBox.Close,
                                         QMessageBox.Close,
                                         self.iconPath)

    def reportProgress(self, percent):

        # Return if thread is interrupted
        if self.bgThread.isInterruptionRequested():
            return

        self.ui.generateProgressBar.setValue(percent)

    def reportCard(self, cardStr):

        # Return if thread is interrupted
        if self.bgThread.isInterruptionRequested():
            return

        currentText = self.ui.outputTxt.toPlainText()
        if currentText:
            currentText += "\n"
        self.ui.outputTxt.setPlainText("{}{}".format(currentText, cardStr))

    def reportFailure(self, failureStr):

        # Return if thread is interrupted
        if self.bgThread.isInterruptionRequested():
            return

        currentText = self.ui.failureTxt.toPlainText()
        if currentText:
            currentText += "\n"
        self.ui.failureTxt.setPlainText(
            "{}{}".format(currentText, failureStr))

    def btnImporterClicked(self):
        if self.ui.outputTxt.toPlainText():
            self.importer.ui.importProgressBar.setValue(0)
            self.importer.show()
        else:
            AnkiHelper.messageBox(
                "Info",
                "No output flashcards available for importing.",
                "Please check your input words!",
                self.iconPath)

    def getSupportedLanguages(self):
        source = self.selectedRadio(self.ui.sourceBox)
        supportTranslations = {Constant.ENGLISH: [Constant.ENGLISH, Constant.VIETNAMESE, Constant.CHINESE_TD, Constant.CHINESE_SP, Constant.FRENCH, Constant.JAPANESE],
                               Constant.VIETNAMESE: [Constant.ENGLISH, Constant.FRENCH, Constant.JAPANESE],
                               Constant.FRENCH: [Constant.ENGLISH, Constant.VIETNAMESE],
                               Constant.JAPANESE: [Constant.ENGLISH, Constant.VIETNAMESE]}

        targetLanguages = supportTranslations.get(source)
        logging.info("targetLanguages {}".format(targetLanguages))

        radioBtns = [radio for radio in self.ui.translatedToBox.children(
        ) if isinstance(radio, QRadioButton)]

        for radio in radioBtns:
            if radio.text() == Constant.ENGLISH:
                radio.click()

            if radio.text() in targetLanguages:
                radio.setEnabled(True)
                self.changeRadioColor(radio, True)
            else:
                radio.setEnabled(False)
                self.changeRadioColor(radio, False)

    def changeRadioColor(self, radio: QRadioButton, isEnabled: bool):
        if isEnabled:
            radio.setStyleSheet(self.ui.source1.styleSheet())
        else:
            radio.setStyleSheet("color:gray")

    def selectedRadio(self, groupBox: QGroupBox) -> str:
        # Get all radio buttons
        radioBtns = [radio for radio in groupBox.children(
        ) if isinstance(radio, QRadioButton)]
        # Find choosen radio and return text
        for radio in radioBtns:
            if radio.isChecked():
                return radio.text()
