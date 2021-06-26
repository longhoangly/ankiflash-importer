#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
AnkiFlash Importer
This plugin helps you import flashcards generated by AnkiFlash (https://ankiflash.com/)

Author: Long Ly
Website: https://www.facebook.com/ankiflashcom
Modified: Feb 21, 2021
"""

from anki.models import ModelManager
from anki.importing.csvfile import TextImporter

from aqt import mw
from aqt.utils import showInfo

from os.path import join, exists
from shutil import copyfile, Error
from PyQt5 import QtGui, QtCore, QtWidgets

import os
import sys
import csv
import re
import zipfile
csv.field_size_limit(2**30)


class AnkiFlashImporter(QtWidgets.QWidget):

    version = ""
    basedir = ""
    filePath = ""
    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, title, version):
        super(AnkiFlashImporter, self).__init__()

        self.version = version
        self.move(300, 300)
        self.setFixedSize(600, 82)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon('anki.png'))

        self.btnBrowse = QtWidgets.QPushButton('Browse', self)
        self.btnBrowse.setToolTip(
            'Click this button to browse generated cards package')
        self.btnBrowse.resize(self.btnBrowse.sizeHint())
        self.btnBrowse.move(5, 5)
        self.btnBrowse.clicked.connect(self.__btnBrowseClicked)

        self.txtPath = QtWidgets.QLineEdit(self)
        self.txtPath.setGeometry(90, 5, 467, 22)
        self.txtPath.setText("AnkiFlash zip file path")
        self.txtPath.textChanged.connect(self.__handleTextChanged)

        self.btnImport = QtWidgets.QPushButton('Import', self)
        self.btnImport.setToolTip(
            'Click this button to import generated cards package')
        self.btnImport.resize(self.btnImport.sizeHint())
        self.btnImport.move(5, 30)
        self.btnImport.setEnabled(False)
        self.btnImport.clicked.connect(self.__btnImportClicked)

        self.txtDeck = QtWidgets.QLineEdit(self)
        self.txtDeck.setGeometry(90, 30, 467, 22)
        self.txtDeck.setText("Input deck name")

        self.pBar = QtWidgets.QProgressBar(self)
        self.pBar.setGeometry(5, 56, 587, 22)
        self.pBar.setMinimum(0)
        self.pBar.setMaximum(100)
        self.show()

    def keyPressEvent(self, event):
        super(AnkiFlashImporter, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def onKey(self, key):
        if key == QtCore.Qt.Key_Return and self.filePath:
            self.__btnImportClicked()
        else:
            print('key pressed: %i' % key)

    def __btnBrowseClicked(self):
        file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose AnkiFlash zip file", "", "Zip-Files(*.zip)")
        self.filePath = ''.join(file[0])
        self.txtPath.setText(self.filePath)

        self.basedir = os.path.dirname(self.filePath)
        print('basedir=' + self.basedir)

        if self.filePath:
            zipFile = zipfile.ZipFile(self.filePath)
            for file in zipFile.namelist():
                zipFile.extract(file, self.basedir)
        else:
            self.txtPath.setText('AnkiFlash zip file path...')

    def __handleTextChanged(self):
        if self.filePath:
            self.btnImport.setEnabled(True)

    def __btnImportClicked(self):
        self.pBar.setValue(1)

        slash = ""
        srcdir = ""
        ankiCsvFile = ""

        if r'/' in self.basedir:
            slash = r'/'
        else:
            slash = r'\\'

        srcdir = self.basedir + slash + r'AnkiFlash'
        ankiCsvFile = srcdir + slash + r'AnkiDeck.csv'

        front = ""
        frontFile = srcdir + slash + r'front.html'
        with open(frontFile, 'r', encoding='utf-8') as file:
            front = file.read()

        back = ""
        backFile = srcdir + slash + r'back.html'
        with open(backFile, 'r', encoding='utf-8') as file:
            back = file.read()

        css = ""
        cssFile = srcdir + slash + r'style.css'
        with open(cssFile, 'r', encoding='utf-8') as file:
            css = file.read()

        desdir = mw.col.media.dir()
        self.__recursiveCopyToAnkiMedia(srcdir, desdir)
        print("Copied media files...")

        # Import note type and flashcards
        noteTypeName = u'AnkiFlashTemplate.' + self.version
        allmodels = mw.col.models.allNames()
        if noteTypeName not in allmodels:
            self.__createNoteType(noteTypeName, front, back, css)
        self.pBar.setValue(75)
        print("Created note type...")

        self.__importTextFile(self.txtDeck.text(), noteTypeName, ankiCsvFile)
        self.pBar.setValue(100)
        print("Imported csv file...")

        showInfo("AnkiFlash cards imported successfully...")
        # self.close()

    def __recursiveCopyToAnkiMedia(self, srcdir, desdir):
        count = 0
        for root, dirs, files in os.walk(''.join(srcdir)):
            for name in files:
                if count < 35:
                    count += 1
                    self.pBar.setValue(count)
                if name not in ['AnkiDeck.csv', 'Failures.csv']:
                    try:
                        copyfile(join(root, name), join(desdir, name))
                        print("Copy file {0} to {1}".format(
                            name, join(desdir, name)))
                    except Error:
                        print("File already existed...")
                    except IOError as e:
                        print(
                            "I/O error({0}): {1}".format(e.errno, e.strerror) + " [" + name + "]")
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise
            for name in dirs:
                self.__recursiveCopyToAnkiMedia(
                    join(root, name), ''.join(desdir))

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