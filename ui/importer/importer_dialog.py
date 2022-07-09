#!/usr/bin/python

import os
import logging

from os.path import join
from shutil import copyfile
from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog

from aqt import mw
from anki.models import ModelManager
from anki.importing.csvfile import TextImporter

from .ui_importer import UiImporter
from ...service.constant import Constant
from ...service.helpers.ankiflash import AnkiHelper
from ...service.importer import Importer

import csv

csv.field_size_limit(2**30)


class ImporterDialog(QDialog):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, version, iconPath, addonDir, mediaDir):

        super().__init__()
        self.version = version
        self.addonDir = addonDir
        self.mediaDir = mediaDir
        self.iconPath = iconPath

        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)
        self.frontFile = join(self.addonDir, r"resources/front.html")
        self.backFile = join(self.addonDir, r"resources/back.html")
        self.cssFile = join(self.addonDir, r"resources/style.css")

        self.keyPressed.connect(self.on_key)

        self.ui = UiImporter()
        self.ui.setupUi(self)

        self.ui.deckNameTxt.textChanged.connect(self.enable_import_btn)
        self.ui.importBtn.clicked.connect(lambda: self.btn_import_clicked(version))

    def key_press_event(self, event):
        super().key_press_event(event)
        self.keyPressed.emit(event.key())

    def on_key(self, key):
        if key == QtCore.Qt.Key_Return and self.ui.deckNameTxt.text():
            self.btn_import_clicked(self.version)
        else:
            logging.info("key pressed: {}".format(key))

    def enable_import_btn(self):
        if self.ui.deckNameTxt.text():
            self.ui.importBtn.setEnabled(True)
        else:
            self.ui.importBtn.setEnabled(False)

    def btn_import_clicked(self, version):
        self.ui.importProgressBar.setValue(20)

        with open(self.frontFile, "r", encoding="utf-8") as file:
            self.front = file.read()

        with open(self.backFile, "r", encoding="utf-8") as file:
            self.back = file.read()

        with open(self.cssFile, "r", encoding="utf-8") as file:
            self.css = file.read()

        updateExistingNote = self.ui.checkBox.isChecked()
        # Create note type if needs
        noteTypeName = "AnkiFlashTemplate.{}".format(version)

        is_nt_diff = Importer.is_note_type_diff(
            noteTypeName, self.front, self.back, self.css, mw
        )

        mm = ModelManager(mw.col)

        # Create new note type if not exist or existent but won't update existing!
        if (is_nt_diff == None) or (is_nt_diff != None and not updateExistingNote):
            # If note type already existed, and we don't want to udpate existing! We need a new name!
            if is_nt_diff != None:
                noteTypeName = "AnkiFlashTemplate.{}.{}".format(
                    version, AnkiHelper.id_generator()
                )
                noteTypeId = mw.col.models.id_for_name(noteTypeName)
                while noteTypeId != None:
                    noteTypeName = "AnkiFlashTemplate.{}.{}".format(
                        version, AnkiHelper.id_generator()
                    )
                    noteTypeId = mw.col.models.id_for_name(noteTypeName)

            Importer.create_note_type(
                noteTypeName, self.front, self.back, self.css, mw, mm
            )
            logging.info("{} Note type created.".format(noteTypeName))

        elif is_nt_diff and updateExistingNote:
            Importer.update_note_type(
                noteTypeName, self.front, self.back, self.css, mw, mm
            )
            logging.info("{} Note type is existent, override it.".format(noteTypeName))
        else:
            logging.info(
                "{} Note type is existent, the same with AnkiFlash, use it.".format(
                    noteTypeName
                )
            )
        self.ui.importProgressBar.setValue(50)

        # Import csv text file into Anki
        mode = self.ui.importModeBox.currentText()
        ti = TextImporter(mw.col, self.ankiCsvPath)
        Importer.import_text_file(
            self.ui.deckNameTxt.text(), mode, noteTypeName, mw, ti
        )
        self.ui.importProgressBar.setValue(100)
        logging.info("Imported csv file: {}".format(self.ankiCsvPath))

        AnkiHelper.message_box(
            "Info",
            "Finished importing flashcards.",
            "Let's enjoy learning curve.",
            self.iconPath,
        )

        os.makedirs(join(self.mediaDir, r"resources"), exist_ok=True)
        copyfile(
            join(self.addonDir, r"resources/Raleway-Regular.ttf"),
            join(self.mediaDir, r"resources/Raleway-Regular.ttf"),
        )
        copyfile(
            join(self.addonDir, r"resources/OpenSans-Regular.ttf"),
            join(self.mediaDir, r"resources/OpenSans-Regular.ttf"),
        )

        self.close()
