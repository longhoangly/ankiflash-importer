#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from anki.models import ModelManager
from anki.importing.csvfile import TextImporter

from aqt import mw
from aqt.utils import showInfo

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGroupBox, QRadioButton

from .Ui.UiAnkiFlash import UiAnkiFlash
from .Service.Enum.Translation import Translation
from .Service.Card.ChineseGenerator import ChineseGenerator
from .Service.Card.VietnameseGenerator import VietnameseGenerator
from .Service.Card.SpanishGenerator import SpanishGenerator
from .Service.Card.JapaneseGenerator import JapaneseGenerator
from .Service.Card.FrenchGenerator import FrenchGenerator
from .Service.Card.EnglishGenerator import EnglishGenerator

from os.path import join
import csv
csv.field_size_limit(2**30)


class AnkiFlash(QDialog):
    """AnkiFlash Dialog class"""

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, version):
        super().__init__()
        self.version = version

        # Create an instance of the GUI
        self.ui = UiAnkiFlash()

        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self, version)

        # Set total input words count
        self.ui.inputTxt.textChanged.connect(self.inputTextChanged)

        # Set completed output cards count
        self.ui.outputTxt.textChanged.connect(self.outputTextChanged)

        # Set failures words count
        self.ui.failureTxt.textChanged.connect(self.failureTextChanged)

        # Handle Generate button clicked
        self.ui.generateBtn.clicked.connect(self.btnGenerateClicked)

        # Check if Import button should be enabled or disabled
        self.ui.deckNameTxt.textChanged.connect(self.enableImportBtn)
        self.ui.outputTxt.textChanged.connect(self.enableImportBtn)

        # Handle Import button clicked
        self.ui.importBtn.clicked.connect(self.btnImportClicked)

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

    def keyPressEvent(self, event):
        super(AnkiFlash, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def onKey(self, key):
        if key == QtCore.Qt.Key_Return and self.filePath:
            self.btnImportClicked()
        else:
            logging.info('key pressed: {}'.format(key))

    def enableImportBtn(self):
        if self.ui.deckNameTxt.text() and self.ui.outputTxt.toPlainText():
            self.ui.importBtn.setEnabled(True)
        else:
            self.ui.importBtn.setEnabled(False)

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
            self.ui, self.words, translation, self.isOnline, self.allWordTypes)

    def selectedRadio(self, groupBox: QGroupBox) -> str:

        # Get all radio buttons
        radioBtns = [radio for radio in groupBox.children(
        ) if isinstance(radio, QRadioButton)]

        # Find choosen radio and return text
        for radio in radioBtns:
            if radio.isChecked():
                return radio.text()

    def btnImportClicked(self):
        self.ui.importBar.setValue(10)

        # Base dir will be media folder
        # Download and save audios and images directly to media folder
        self.mediaDir = mw.col.media.dir()

        # AnkiFlash folder contains one time files such as template, csv cards...
        self.ankiFlashDir = join(self.mediaDir, r'AnkiFlash')
        self.ankiCsvFile = join(self.ankiFlashDir, r'AnkiDeck.csv')

        # Front template inside AnkiFlash folder
        frontFile = join(self.ankiFlashDir, r'front.html')
        with open(frontFile, 'r', encoding='utf-8') as file:
            self.front = file.read()

        # Back template inside AnkiFlash folder
        backFile = join(self.ankiFlashDir, r'back.html')
        with open(backFile, 'r', encoding='utf-8') as file:
            self.back = file.read()

        # Styling template inside AnkiFlash folder
        cssFile = join(self.ankiFlashDir, r'style.css')
        with open(cssFile, 'r', encoding='utf-8') as file:
            self.css = file.read()

        # Import note type and flashcards
        noteTypeName = u'AnkiFlashTemplate.{}'.format(self.version)
        allmodels = mw.col.models.allNames()

        # If note type already existed, skip creating note type
        if noteTypeName not in allmodels:
            self.createNoteType(
                noteTypeName, self.front, self.back, self.css)
            logging.info("Created note type: {}".format(noteTypeName))
        else:
            logging.info(
                "Note type existed already => {}".format(noteTypeName))
        self.ui.importBar.setValue(50)

        # Import csv text file into Anki
        self.importTextFile(self.ui.deckNameTxt.text(),
                            noteTypeName, self.ankiCsvFile)
        self.ui.importBar.setValue(100)
        logging.info("Imported csv file: {}".format(self.ankiCsvFile))

        showInfo("AnkiFlash cards imported successfully...")

    def createNoteType(self, noteTypeName, front, back, css):
        # Create empty note type
        mm = ModelManager(mw.col)
        nt = mm.new(noteTypeName)

        # Add fields into note type
        mm.add_field(nt, mm.new_field("Word"))
        mm.add_field(nt, mm.new_field("WordType"))
        mm.add_field(nt, mm.new_field("Phonetic"))
        mm.add_field(nt, mm.new_field("Example"))
        mm.add_field(nt, mm.new_field("Sound"))
        mm.add_field(nt, mm.new_field("Image"))
        mm.add_field(nt, mm.new_field("Content"))
        mm.add_field(nt, mm.new_field("Copyright"))

        # Add template into note type
        template = mm.new_template("AnkiFlash")
        template["qfmt"] = front
        template["afmt"] = back
        nt["css"] = css
        mm.add_template(nt, template)

        # Save model / note type
        mm.save(nt)

        # Update UI
        mw.reset()

    def importTextFile(self, deckName, noteTypeName, csvPath):
        # Select deck
        did = mw.col.decks.id(deckName)
        mw.col.decks.select(did)

        # Set note type for deck
        m = mw.col.models.byName(noteTypeName)
        deck = mw.col.decks.get(did)
        deck["mid"] = m["id"]
        mw.col.decks.save(deck)

        # Import into the collection
        ti = TextImporter(mw.col, csvPath)
        ti.model["did"] = did
        mw.col.models.save(ti.model, updateReqs=False)

        # ADD_MODE: import even if first field matches existing note
        ti.importMode = 2
        ti.delimiter = "\t"
        ti.allowHTML = True
        ti.open()
        ti.updateDelimiter()
        ti.run()

        # Update UI
        mw.reset()
