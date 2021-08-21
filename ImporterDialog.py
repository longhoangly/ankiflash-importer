#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt import mw
from aqt.utils import showInfo
from anki.models import ModelManager
from anki.importing.csvfile import TextImporter

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore

from .Ui.UiImporter import UiImporter
from .Helpers.AnkiHelper import AnkiHelper

from os.path import join
import logging
import csv
csv.field_size_limit(2**30)


class ImporterDialog(QDialog):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, version, iconPath, addonDir):
        super().__init__()
        self.version = version
        self.addonDir = addonDir

        # Paths
        self.ankiCsvPath = join(self.addonDir, r'AnkiDeck.csv')
        self.frontFile = join(self.addonDir, r'Resources/front.html')
        self.backFile = join(self.addonDir, r'Resources/back.html')
        self.cssFile = join(self.addonDir, r'Resources/style.css')
        self.iconPath = join(self.addonDir, r'Resources/anki.png')

        # Importer GUI
        self.ui = UiImporter()
        self.ui.setupUi(self, version, iconPath)

        # Check if Import button should be enabled or disabled
        self.ui.deckNameTxt.textChanged.connect(self.enableImportBtn)

        # Handle Import button clicked
        self.ui.importBtn.clicked.connect(
            lambda: self.btnImportClicked(version))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def onKey(self, key):
        if key == QtCore.Qt.Key_Return and self.ui.deckNameTxt.text():
            self.btnImportClicked(self.version)
        else:
            logging.info('key pressed: {}'.format(key))

    def enableImportBtn(self):
        if self.ui.deckNameTxt.text():
            self.ui.importBtn.setEnabled(True)
        else:
            self.ui.importBtn.setEnabled(False)

    def btnImportClicked(self, version):
        self.ui.importProgressBar.setValue(10)

        with open(self.frontFile, 'r', encoding='utf-8') as file:
            self.front = file.read()

        with open(self.backFile, 'r', encoding='utf-8') as file:
            self.back = file.read()

        with open(self.cssFile, 'r', encoding='utf-8') as file:
            self.css = file.read()

        forceCreateNewNote = True
        # Import note type and flashcards
        noteTypeName = u'AnkiFlashTemplate.{}'.format(version)
        noteTypeId = mw.col.models.id_for_name(noteTypeName)

        if forceCreateNewNote and noteTypeId != None:
            while (noteTypeId != None):
                noteTypeName = u'AnkiFlashTemplate.{}.{}'.format(version, AnkiHelper.id_generator())
                noteTypeId = mw.col.models.id_for_name(noteTypeName)

        # If note type already existed, skip creating note type
        if noteTypeId == None:
            self.createNoteType(
                noteTypeName, self.front, self.back, self.css)
            logging.info("Created note type! {}".format(noteTypeName))
        else:
            logging.info(
                "Note type existed already, skip it! {}".format(noteTypeName))
        self.ui.importProgressBar.setValue(50)

        # Import csv text file into Anki
        self.importTextFile(self.ui.deckNameTxt.text(),
                            noteTypeName, self.ankiCsvPath)
        self.ui.importProgressBar.setValue(100)
        logging.info("Imported csv file: {}".format(self.ankiCsvPath))

        showInfo("AnkiFlash cards imported successfully...")
        self.close()

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
