#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from aqt import mw, qconnect

from PyQt6 import QtCore
from PyQt6 import QtWidgets

from . ui_fields_updater import UiFieldsUpdater
from . change_map_dialog import ChangeMapDialog

from ... service.constant import Constant
from ... service.helpers.anki_helper import AnkiHelper

import logging
from os.path import join


class FieldsUpdaterDialog(QtWidgets.QDialog):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, iconPath, addonDir, mediaDir):

        super().__init__()
        self.addonDir = addonDir
        self.mediaDir = mediaDir
        self.iconPath = iconPath

        self.ui = UiFieldsUpdater()
        self.ui.setupUi(self)

        self.keyPressed.connect(self.on_key)
        self.ui.updateBtn.clicked.connect(self.btn_update_clicked)

        # Default mapping first field to Word in AnkiFlash
        self.setup_mapping_frame()
        self.show_mapping()

        self.mapping = {}

    def key_press_event(self, event):
        super().key_press_event(event)
        self.keyPressed.emit(event.key())

    def on_key(self, key):
        if key == QtCore.Qt.Key_Return:
            self.btn_update_clicked()
        else:
            logging.info('key pressed: {}'.format(key))

    def setup_mapping_frame(self) -> None:

        # qt seems to have a bug with adding/removing from a grid, so we add
        # to a separate object and add/remove that instead

        self.frame = QtWidgets.QFrame(self.ui.mappingArea)
        self.ui.mappingArea.setWidget(self.frame)

        self.mapbox = QtWidgets.QVBoxLayout(self.frame)
        self.mapbox.setContentsMargins(0, 0, 0, 0)
        self.mapwidget: Optional[QtWidgets.QWidget] = None

        self.mapwidget = QtWidgets.QWidget()
        self.mapbox.addWidget(self.mapwidget)

        self.grid = QtWidgets.QGridLayout(self.mapwidget)
        self.mapwidget.setLayout(self.grid)

        self.grid.setContentsMargins(3, 3, 3, 3)
        self.grid.setSpacing(6)

    def show_mapping(self):

        def get_flashcards_fields():
            fields = []
            for note in mw.selectedNotes:
                noteType = note.note_type()
                fields += mw.col.models.field_names(noteType)
            fields = AnkiHelper.unique(fields)
            fields.sort()

            return fields

        self.mapper = QtCore.QSignalMapper(self)
        self.cardFields = get_flashcards_fields()
        for num in range(len(self.cardFields)):

            text = "Your \"{}\" field is".format(self.cardFields[num])
            self.grid.addWidget(QtWidgets.QLabel(text), num, 0)

            text = "<ignored>"
            self.grid.addWidget(QtWidgets.QLabel(text), num, 1)

            button = QtWidgets.QPushButton("Change")
            self.mapper.setMapping(button, num)

            self.grid.addWidget(button, num, 2)
            button.clicked.connect(self.mapper.map)

        self.mapper.mappedInt['int'].connect(self.trigger_change_map_dialog)

    def trigger_change_map_dialog(self, indentifier):

        self.changeMap = ChangeMapDialog()
        self.changeMap.show_options()
        qconnect(self.changeMap.changeMapSignal, self.update_map)

        self.userFieldIndex = indentifier
        self.userField = self.cardFields[indentifier]

    def update_map(self, selectField):

        def set_dest_field_text(index, text):
            item = self.grid.itemAt(index)
            item.widget().setText(text)

        text = selectField if selectField == "<ignored>" else "mapped to \"{}\"".format(
            selectField)
        set_dest_field_text(self.userFieldIndex * 3 + 1, text)

        self.mapping[self.userField] = selectField

    def btn_update_clicked(self):

        self.ui.importProgressBar.setValue(5)
        logging.info(self.mapping)

        self.csvMappingPath = join(self.addonDir, Constant.MAPPING_CSV)
        with open(self.csvMappingPath, 'r', encoding='utf-8') as file:
            self.ankiCsvLines = file.readlines()

        def convertLinesToCardsMap(ankiCsvLines):
            cards = {}

            for cardLine in ankiCsvLines:
                cardValues = cardLine.split("\t")

                card = {}
                card["Word"] = cardValues[0]
                card["WordType"] = cardValues[1]
                card["Phonetic"] = cardValues[2]
                card["Example"] = cardValues[3]
                card["Sound"] = cardValues[4]
                card["Image"] = cardValues[5]
                card["Meaning"] = cardValues[6]
                card["Copyright"] = cardValues[7]
                cards[card["Word"]] = card

            return cards

        self.csvCardsMap = convertLinesToCardsMap(self.ankiCsvLines)
        self.ui.importProgressBar.setValue(5)

        logging.info(self.csvCardsMap)

        percentage = 5
        for idx, note in enumerate(mw.selectedNotes):
            first_note_field = note.__getitem__(note.keys()[0])
            logging.info("first_note_field {}".format(first_note_field))

            if ((idx + 1) / len(mw.selectedNotes)) * 100 > 5:
                percentage = ((idx + 1) / len(mw.selectedNotes)) * 100

            if first_note_field in self.csvCardsMap:
                generatedCard = self.csvCardsMap[first_note_field]

                for cardField in self.cardFields:
                    if cardField in self.mapping and cardField in generatedCard and self.mapping[cardField] != "<ignored>":

                        updatedContent = generatedCard[self.mapping[cardField]]
                        note.__setitem__(cardField, updatedContent)
                        logging.info("Update field '{}' with value '{}'".format(
                            cardField, updatedContent))
                        note.flush()

            self.ui.importProgressBar.setValue(int(percentage))

        AnkiHelper.message_box("Info",
                               "Finished updating flashcards.",
                               "Let's enjoy learning curve.",
                               self.iconPath)
        self.close()
        mw.reset()
