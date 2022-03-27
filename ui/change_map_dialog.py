#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from aqt import qconnect

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from . ui_change_map import UiChangeMap

ANKI_FLASH_FIELDS = ["Word", "WordType", "Phonetic",
                     "Example", "Sound", "Image", "Content", "Copyright"]


class ChangeMapDialog(QtWidgets.QDialog):

    changeMapSignal = QtCore.pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.ui = UiChangeMap()
        self.ui.setupUi(self)

        qconnect(
            self.ui.buttonBox.button(
                QtWidgets.QDialogButtonBox.StandardButton.Ok).clicked,
            self.field_selected_handler,
        )

        qconnect(
            self.ui.fields.itemDoubleClicked,
            self.field_selected_handler,
        )

        self.show()

    def show_options(self):

        for field in ANKI_FLASH_FIELDS:
            item = QtWidgets.QListWidgetItem("Map to {}".format(field))
            self.ui.fields.addItem(item)
        self.ui.fields.addItem(
            QtWidgets.QListWidgetItem("<ignored>"))

    def field_selected_handler(self, event):

        index = self.ui.fields.currentRow()
        logging.info("Selected AnkiFlash field index {}".format(index))

        if index >= 0 and index < len(ANKI_FLASH_FIELDS):
            selected_field = ANKI_FLASH_FIELDS[index]
        else:
            selected_field = "<ignored>"
        self.changeMapSignal.emit(selected_field)
