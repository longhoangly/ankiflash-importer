#!/usr/bin/python
# -*- coding: utf-8 -*-

from anki.models import ModelManager
from anki.importing.csvfile import TextImporter
from aqt import mw
from aqt.utils import showInfo

from os.path import join
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

from .Ui_ankiflash import Ui_Dialog
from .Generator import Generator

import csv
csv.field_size_limit(2**30)


class AnkiFlashDlg(QDialog):
    """AnkiFlash Dialog class"""
    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, version):
        super().__init__()
        self.version = version

        # Create an instance of the GUI
        self.ui = Ui_Dialog()

        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self, version)

        # Handle Generate button clicked
        self.ui.generateBtn.clicked.connect(self.__btnGenerateClicked)

        # Enable Import button only if deck name entered
        self.ui.deckNameTxt.textChanged.connect(self.__deckNameTextChanged)
        self.ui.outputTxt.textChanged.connect(self.__deckNameTextChanged)

        # Handle Import button clicked
        self.ui.importBtn.clicked.connect(self.__btnImportClicked)

        # Create an instance of the generator
        self.generator = Generator()

    def keyPressEvent(self, event):
        super(AnkiFlashDlg, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def onKey(self, key):
        if key == QtCore.Qt.Key_Return and self.filePath:
            self.__btnImportClicked()
        else:
            print('key pressed: %i' % key)

    def __deckNameTextChanged(self):
        if self.ui.deckNameTxt.text() and self.ui.outputTxt.toPlainText():
            self.ui.importBtn.setEnabled(True)
        else:
            self.ui.importBtn.setEnabled(False)

    def __btnGenerateClicked(self):
        # Get word list, validate if empty?
        inputText = self.ui.inputTxt.toPlainText()

        if not inputText:
            showInfo("Empty input. No word found. Please check your input.")
            return
        else:
            self.words = inputText.split("\n")
        
        self.ui.outputTxt.setPlainText("")
        self.ui.failureTxt.setPlainText("")

        # Send word list to generator
        self.generator.flashcards(self.words)

    def __btnImportClicked(self):
        self.ui.importBar.setValue(10)

        self.baseDir = mw.col.media.dir()
        self.ankiFlashDir = join(self.baseDir, r'AnkiFlash')

        self.ankiCsvFile = join(self.ankiFlashDir, r'AnkiDeck.csv')

        frontFile = join(self.ankiFlashDir, r'front.html')
        with open(frontFile, 'r', encoding='utf-8') as file:
            self.front = file.read()

        backFile = join(self.ankiFlashDir, r'back.html')
        with open(backFile, 'r', encoding='utf-8') as file:
            self.back = file.read()

        cssFile = join(self.ankiFlashDir, r'style.css')
        with open(cssFile, 'r', encoding='utf-8') as file:
            self.css = file.read()

        # Import note type and flashcards
        noteTypeName = u'AnkiFlashTemplate.' + self.version
        allmodels = mw.col.models.allNames()

        if noteTypeName not in allmodels:
            self.__createNoteType(
                noteTypeName, self.front, self.back, self.css)
            print("Created note type: " + noteTypeName)
        else:
            print("Note type existed already => " + noteTypeName)
        self.ui.importBar.setValue(50)

        self.__importTextFile(self.ui.deckNameTxt.text(),
                              noteTypeName, self.ankiCsvFile)
        self.ui.importBar.setValue(100)
        print("Imported csv file: " + self.ankiCsvFile)

        showInfo("AnkiFlash cards imported successfully...")

    def __createNoteType(self, noteTypeName, front, back, css):
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

    def __importTextFile(self, deckName, noteTypeName, csvPath):
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
