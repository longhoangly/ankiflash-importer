#!/usr/bin/python

import logging

from typing import Optional
from PyQt6 import QtCore
from PyQt6 import QtWidgets

from aqt import mw, qconnect

from .ui_fields_updater import UiFieldsUpdater
from .change_map_dialog import ChangeMapDialog
from ...service.mapper import Mapper
from ...service.helpers.ankiflash import AnkiHelper


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

        self.mapper = Mapper()
        self.mapper.progress.connect(self.updateMappingProgress)

    def key_press_event(self, event):
        super().key_press_event(event)
        self.keyPressed.emit(event.key())

    def on_key(self, key):
        if key == QtCore.Qt.Key.Key_Return:
            self.btn_update_clicked()
        else:
            logging.info("key pressed: {}".format(key))

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

        self.signalMapper = QtCore.QSignalMapper(self)
        self.cardFields = get_flashcards_fields()
        for num in range(len(self.cardFields)):

            text = 'Your "{}" field is'.format(self.cardFields[num])
            self.grid.addWidget(QtWidgets.QLabel(text), num, 0)

            text = "<ignored>"
            self.grid.addWidget(QtWidgets.QLabel(text), num, 1)

            button = QtWidgets.QPushButton("Change")
            self.signalMapper.setMapping(button, num)

            self.grid.addWidget(button, num, 2)
            button.clicked.connect(self.signalMapper.map)

        self.signalMapper.mappedInt["int"].connect(self.trigger_change_map_dialog)

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

        text = (
            selectField
            if selectField == "<ignored>"
            else 'mapped to "{}"'.format(selectField)
        )
        set_dest_field_text(self.userFieldIndex * 3 + 1, text)

        self.mapping[self.userField] = selectField

    def updateMappingProgress(self, progress):
        self.ui.importProgressBar.setValue(progress)

    def btn_update_clicked(self):
        self.ui.importProgressBar.setValue(5)
        logging.info(self.mapping)
        # {'Example': 'Copyright', 'cardField': 'ankiFlashField'...}

        keywordIdx = mw.ankiFlash.generator.ui.keywordCx.currentText()
        updated_count = self.mapper.update_flashcards(
            self.addonDir,
            keywordIdx,
            mw.selectedNotes,
            self.mapping,
            self.cardFields,
        )

        AnkiHelper.message_box(
            "Info",
            "Finished updating flashcards.",
            "Let's enjoy learning curve.\nUpdated {} flashcards!".format(updated_count),
            self.iconPath,
        )
        self.close()
        mw.reset()
