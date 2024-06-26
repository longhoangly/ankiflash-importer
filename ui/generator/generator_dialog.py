#!/usr/bin/python

import logging

from aqt import mw
from os.path import join
from typing import List

from PyQt6.QtWidgets import QDialog, QGroupBox, QMessageBox, QRadioButton
from PyQt6.QtCore import QThread

from .ui_generator import UiGenerator
from ..importer.importer_dialog import ImporterDialog
from ..mapper.fields_updater_dialog import FieldsUpdaterDialog
from ...service.enum.translation import Translation
from ...service.gen_worker import GenWorker
from ...service.constant import Constant
from ...service.helpers.ankiflash import AnkiHelper


class GeneratorDialog(QDialog):
    """Generator Dialog"""

    def __init__(self, version, iconPath, addonDir, mediaDir):

        super().__init__()
        self.mediaDir = mediaDir
        self.addonDir = addonDir
        self.iconPath = iconPath
        self.version = version

        self.ankiCsvPath = join(addonDir, Constant.ANKI_DECK)

        self.ui = UiGenerator()
        self.ui.setupUi(self)
        self.ui.cancelBtn.setDisabled(True)

        if len(mw.selectedNotes) > 0:
            self.ui.relatedWords.setDisabled(True)
            self.ui.relatedWords.setChecked(False)
            self.ui.relatedWords.setStyleSheet("color:gray")

        self.fieldsUpdater = FieldsUpdaterDialog(
            self.iconPath, self.addonDir, self.mediaDir
        )

        self.importer = ImporterDialog(
            self.version, self.iconPath, self.addonDir, self.mediaDir
        )

        self.ui.inputTxt.textChanged.connect(self.input_text_changed)
        self.ui.outputTxt.textChanged.connect(self.output_text_changed)
        self.ui.failureTxt.textChanged.connect(self.failure_text_changed)

        self.ui.generateBtn.clicked.connect(self.btn_generate_clicked)
        self.ui.importBtn.clicked.connect(self.btn_importer_clicked)
        self.ui.mappingBtn.clicked.connect(self.btn_mapping_clicked)

        self.get_supported_languages()
        self.ui.source.currentIndexChanged.connect(self.get_supported_languages)
        self.ui.keywordCx.currentIndexChanged.connect(self.keyword_changed)

    def enable_mapping(self, isMappingEnable, keys: list):

        if isMappingEnable:
            self.ui.mappingBtn.setEnabled(True)
            self.ui.importBtn.setDisabled(True)
            self.ui.keywordCx.addItems(keys)
        else:
            self.ui.mappingBtn.setDisabled(True)
            self.ui.importBtn.setEnabled(True)
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

    def output_text_changed(self):

        cards = self.ui.outputTxt.toPlainText().split("\n")
        # Filter cards list, only get non-empty cards
        self.cards = list(filter(None, cards))
        self.cardCount = len(self.cards)
        self.ui.completedLbl.setText("Completed: {}".format(len(self.cards)))

    def failure_text_changed(self):

        failures = self.ui.failureTxt.toPlainText().split("\n")
        # Filter failures list, only get non-empty failures
        self.failures = list(filter(None, failures))
        self.failureCount = len(self.failures)
        self.ui.failureLbl.setText("Failure: {}".format(len(self.failures)))

    def btn_generate_clicked(self):

        # Validate if input text empty?
        inputText = self.ui.inputTxt.toPlainText()

        if not inputText:
            AnkiHelper.message_box(
                "Info",
                "No input words available for generating.",
                "Please check your input words!",
                self.iconPath,
            )
            return

        # Increase to 2% as a processing signal to user
        self.ui.generateProgressBar.setValue(2)
        self.ui.generateBtn.setDisabled(True)

        # Clean up output before generating cards
        self.ui.outputTxt.setPlainText("")
        self.ui.failureTxt.setPlainText("")

        # Get translation options
        source = self.ui.source.currentText()
        target = self.ui.target.currentText()
        self.translation = Translation(source, target)

        # Get generating options
        self.relatedWords = self.ui.relatedWords.isChecked()
        self.isOnline = self.ui.isOnline.isChecked()

        # Step 2: Create a QThread object
        self.bgThread = QThread(self)
        self.bgThread.setTerminationEnabled(True)

        # Step 3: Create a worker object
        self.worker = GenWorker(
            self.words,
            self.translation,
            self.mediaDir,
            self.isOnline,
            self.relatedWords,
            self.ankiCsvPath,
        )

        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.bgThread)

        # Step 5: Connect signals and slots
        self.bgThread.started.connect(self.worker.generate_cards_background)

        self.worker.finished.connect(self.bgThread.quit)
        self.bgThread.finished.connect(self.bgThread.deleteLater)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.progress.connect(self.report_progress)

        self.worker.cardStr.connect(self.report_card)
        self.worker.failureStr.connect(self.report_failure)

        # Step 6: Start the thread
        self.bgThread.start()
        self.ui.cancelBtn.setEnabled(True)
        self.ui.generateBtn.setDisabled(True)

        # Handle cancel background task
        self.isCancelled = False

        receiversCount = self.ui.cancelBtn.receivers(self.ui.cancelBtn.clicked)
        if receiversCount > 0:
            logging.info("Already connected before...{}".format(receiversCount))
            self.ui.cancelBtn.clicked.disconnect()

        self.ui.cancelBtn.clicked.connect(self.cancel_background_task)

        # Final resets
        self.bgThread.finished.connect(self.finished_generation_progress)

    def cancel_background_task(self):

        logging.info("Canceling background task...")
        self.bgThread.requestInterruption()
        self.bgThread.quit()

        self.ui.outputTxt.setPlainText("")
        self.isCancelled = True

        AnkiHelper.message_box(
            "Info",
            "Flashcards generation process stopped!",
            "Restart by clicking Generate button.",
            self.iconPath,
        )

    def finished_generation_progress(self):

        self.ui.cancelBtn.setDisabled(True)
        self.ui.generateBtn.setEnabled(True)

        # Return if thread is cancelled
        if self.isCancelled:
            self.ui.outputTxt.setPlainText("")
            return

        if self.ui.outputTxt.toPlainText():

            mode = "map" if len(mw.selectedNotes) > 0 else "import"
            btnSelected = AnkiHelper.message_box_buttons(
                "Info",
                "Finished generating flashcards.\nThanks for using AnkiFlash!",
                "Do you want to {} generated flashcards now?\n\nProgress completed 100%\n- Input: {}\n- Output: {}\n- Failure: {}".format(
                    mode, len(self.words), self.cardCount, self.failureCount
                ),
                QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.Yes,
                self.iconPath,
            )
            if btnSelected == QMessageBox.StandardButton.Yes:
                if len(mw.selectedNotes) > 0:
                    self.btn_mapping_clicked()
                else:
                    self.btn_importer_clicked()
        else:
            AnkiHelper.message_box_buttons(
                "Info",
                "Finished generating flashcards.\nThanks for using AnkiFlash!",
                "No output flashcards available for importing or mapping.\n\nProgress completed 100%\n- Input: {}\n- Output: {}\n- Failure: {}".format(
                    len(self.words), self.cardCount, self.failureCount
                ),
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close,
                self.iconPath,
            )

    def report_progress(self, percent):

        # Return if thread is interrupted
        if self.bgThread.isInterruptionRequested():
            return

        self.ui.generateProgressBar.setValue(percent)

    def report_card(self, cardStr):

        # Return if thread is interrupted
        if self.bgThread.isInterruptionRequested():
            return

        currentText = self.ui.outputTxt.toPlainText()
        if currentText:
            currentText += "\n"
        self.ui.outputTxt.setPlainText("{}{}".format(currentText, cardStr))

    def report_failure(self, failureStr):

        # Return if thread is interrupted
        if self.bgThread.isInterruptionRequested():
            return

        currentText = self.ui.failureTxt.toPlainText()
        if currentText:
            currentText += "\n"
        self.ui.failureTxt.setPlainText("{}{}".format(currentText, failureStr))

    def btn_importer_clicked(self):

        if self.ui.outputTxt.toPlainText():
            self.importer.ui.importProgressBar.setValue(0)
            self.importer.show()
        else:
            AnkiHelper.message_box(
                "Info",
                "No output flashcards available for importing notes.",
                "Please check your input words!",
                self.iconPath,
            )

    def btn_mapping_clicked(self):

        if self.ui.outputTxt.toPlainText():
            self.fieldsUpdater.ui.importProgressBar.setValue(0)
            self.fieldsUpdater.show()
        else:
            AnkiHelper.message_box(
                "Info",
                "No output flashcards available for updating notes.",
                "Please check your input words!",
                self.iconPath,
            )

    def get_supported_languages(self):
        source = self.ui.source.currentText()
        targetLanguages = Constant.SUPPORTED_TRANSLATIONS.get(source)
        logging.info("targetLanguages {}".format(targetLanguages))

        self.ui.target.clear()
        self.ui.target.addItems(targetLanguages)

    def change_radio_color(self, radio: QRadioButton, isEnabled: bool):
        if isEnabled:
            radio.setStyleSheet(self.ui.source.styleSheet())
        else:
            radio.setStyleSheet("color:gray")

    def selected_radio(self, groupBox: QGroupBox) -> str:
        # Get all radio buttons
        radioBtns = [
            radio for radio in groupBox.children() if isinstance(radio, QRadioButton)
        ]
        # Find choosen radio and return text
        for radio in radioBtns:
            if radio.isChecked():
                return radio.text()

    def keyword_changed(self):

        input_words = []
        for noteId in mw.selectedNoteIds:
            note = mw.col.get_note(noteId)
            sorted_field = self.ui.keywordCx.currentText()
            keyword = note.__getitem__(sorted_field)

            input_words.append(keyword)
        mw.ankiFlash.generator.set_input_words(AnkiHelper.unique(input_words))
