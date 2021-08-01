#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt.utils import showInfo

from PyQt5.QtWidgets import QDialog, QGroupBox, QMessageBox, QRadioButton
from PyQt5.QtCore import QThread

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

from os.path import join
import logging
import csv
csv.field_size_limit(2**30)


class GeneratorDialog(QDialog):
    """Generator Dialog"""

    def __init__(self, version, iconPath, addonDir, mediaDir):
        super().__init__()
        self.mediaDir = mediaDir

        # Paths
        self.ankiCsvPath = join(addonDir, r'AnkiDeck.csv')

        # Create Generator GUI
        self.ui = UiGenerator()
        self.ui.setupUi(self, version, iconPath)

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

    def btnGenerateClicked(self):
        # Validate if input text empty?
        inputText = self.ui.inputTxt.toPlainText()

        if not inputText:
            showInfo("Empty input. No word found. Please check your input.")
            return

        # Increase to 2% as a processing signal to user
        self.ui.generateProgressBar.setValue(2)
        self.ui.generateBtn.setDisabled(True)

        # Clean up output before generating cards
        self.ui.outputTxt.setPlainText("")
        self.ui.failureTxt.setPlainText("")

        source = self.selectedRadio(self.ui.sourceBox)
        target = self.selectedRadio(self.ui.translatedToBox)
        self.translation = Translation(source, target)

        self.allWordTypes = self.ui.allWordTypes.isChecked()
        self.isOnline = self.ui.isOnline.isChecked()

        # Initialize Generator based on translation
        self.initializeGenerator(self.translation)

        # Step 2: Create a QThread object
        thread = QThread(self)

        # Step 3: Create a worker object
        self.worker = Worker(self.generator, self.words, self.translation, self.mediaDir,
                             self.isOnline, self.allWordTypes, self.ankiCsvPath)

        # Step 4: Move worker to the thread
        self.worker.moveToThread(thread)

        # Step 5: Connect signals and slots
        thread.started.connect(self.worker.generateCardsBackground)

        self.worker.finished.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.reportProgress)

        self.worker.cardStr.connect(self.reportCard)
        self.worker.failureStr.connect(self.reportFailure)

        # Step 6: Start the thread
        thread.start()

        # Final resets
        self.ui.generateBtn.setEnabled(False)
        thread.finished.connect(self.finishedGenerationProgress)

    def finishedGenerationProgress(self):
        self.ui.generateBtn.setEnabled(True)
        btnSelected = QMessageBox.question(None, "Info", "Do you want to import generated cards now?\n\nProgress completed 100%\n- Input: {}\n- Output: {}\n- Failure: {}".format(len(self.words), self.cardCount, self.failureCount),
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if btnSelected == QMessageBox.Yes:
            # Show Importer Dialog
            self.importer.ui.importProgressBar.setValue(0)
            self.importer.show()

    def selectedRadio(self, groupBox: QGroupBox) -> str:
        # Get all radio buttons
        radioBtns = [radio for radio in groupBox.children(
        ) if isinstance(radio, QRadioButton)]
        # Find choosen radio and return text
        for radio in radioBtns:
            if radio.isChecked():
                return radio.text()

    def reportProgress(self, percent):
        logging.info("progress: {}".format(percent))
        self.ui.generateProgressBar.setValue(percent)

    def reportCard(self, cardStr):
        logging.info("cardStr: {}".format(cardStr).encode("utf-8"))
        currentText = self.ui.outputTxt.toPlainText()
        if currentText:
            currentText += "\n"
        self.ui.outputTxt.setPlainText("{}{}".format(currentText, cardStr))

    def reportFailure(self, failureStr):
        logging.info("failureStr: {}".format(failureStr))
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
            showInfo("Please check your output cards, nothing to import!")
