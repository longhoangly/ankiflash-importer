#!/usr/bin/python

import logging

from aqt import mw
from os.path import join
from typing import List

from PyQt6.QtWidgets import QDialog, QApplication

from .ui_generator import UiGenerator
from ..importer.importer_dialog import ImporterDialog
from ..mapper.fields_updater_dialog import FieldsUpdaterDialog
from ...service.helpers.ankiflash import AnkiHelper
from ...service.constant import Constant


class GeneratorDialog(QDialog):
    """Generator Dialog"""

    def __init__(self, version, iconPath, mediaDir):

        super().__init__()
        self.mediaDir = mediaDir
        self.iconPath = iconPath
        self.version = version

        self.ui = UiGenerator()
        self.ui.setupUi(self)

        self.fieldsUpdater = FieldsUpdaterDialog(self.iconPath, self.mediaDir)
        self.importer = ImporterDialog(self.version, self.iconPath, self.mediaDir)

        self.ui.inputTxt.textChanged.connect(self.input_text_changed)
        self.ui.copyBtn.clicked.connect(self.btn_copybtn_clicked)
        self.ui.importBtn.clicked.connect(self.btn_importer_clicked)
        self.ui.mappingBtn.clicked.connect(self.btn_mapping_clicked)
        self.ui.keywordCx.currentIndexChanged.connect(self.keyword_changed)

    def enable_mapping(self, isMappingEnable, keys: list):
        if isMappingEnable:
            self.ui.mappingBtn.setEnabled(True)
            self.ui.keywordCx.addItems(keys)
        else:
            self.ui.mappingBtn.setDisabled(True)
            self.ui.keywordCx.setVisible(False)
            self.ui.keywordLbl.setVisible(False)

    def set_input_words(self, words: List[str]):
        self.ui.inputTxt.setPlainText("\n".join(words))

    def close_event(self, event):
        logging.shutdown()

    def input_text_changed(self):
        words = self.ui.inputTxt.toPlainText().split("\n")
        # Filter words list, only get non-empty words
        self.words = list(filter(None, words))
        self.ui.totalLbl.setText("Total: {}".format(len(self.words)))

    def btn_copybtn_clicked(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Mode.Clipboard)
        cb.setText(self.ui.inputTxt.toPlainText(), mode=cb.Mode.Clipboard)
        AnkiHelper.message_box(
            "Info",
            "Inputs copied into clipboard.",
            "Let's paste input words to AnkiFlash Generator Chrome Extention to generate flashcards.",
            self.iconPath,
        )

    def btn_importer_clicked(self):
        self.importer.ui.importProgressBar.setValue(0)
        self.importer.show()

    def btn_mapping_clicked(self):
        self.fieldsUpdater.ui.importProgressBar.setValue(0)
        self.fieldsUpdater.show()

    def keyword_changed(self):
        input_words = []
        for noteId in mw.selectedNoteIds:
            note = mw.col.get_note(noteId)
            sorted_field = self.ui.keywordCx.currentText()
            keyword = note.__getitem__(sorted_field)
            input_words.append(keyword)
        mw.ankiFlash.generator.set_input_words(AnkiHelper.unique(input_words))
