#!/usr/bin/python

import logging

from os.path import join
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal
from .constant import Constant


class Mapper(QObject):
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def update_flashcards(
        self, addonDir, mappingKey, selectedNotes, mappingConfig, cardFields
    ) -> str:
        """Mapping flashcards to AnkiFlash fields"""

        mappingCsvPath = join(addonDir, Constant.MAPPING_CSV)
        mappingCsvLines: List[str] = []

        with open(mappingCsvPath, "r", encoding="utf-8") as file:
            mappingCsvLines = file.readlines()

        def convertCardLinesToMap(mappingCsvLines):
            cardMap = {}

            for cardLine in mappingCsvLines:
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

                cardMap[card["Word"]] = card

            return cardMap

        csvCardMap = convertCardLinesToMap(mappingCsvLines)
        self.progress.emit(10)
        logging.info(csvCardMap)
        # {'long': {'Word': 'long', 'WordType': '(tính từ | phó từ | nội động từ)', 'Phonetic': '/lɒŋ/ /lɔːŋ/', 'Example': '<div class=...

        percentage = 10
        updated_count = 0
        for idx, note in enumerate(selectedNotes):

            isUpdated = False
            if ((idx + 1) / len(selectedNotes)) * 100 > 5:
                percentage = ((idx + 1) / len(selectedNotes)) * 100

            keyword = note.__getitem__(mappingKey)
            if keyword in csvCardMap:

                generatedCard = csvCardMap[keyword]
                logging.info("keyword {}".format(keyword))
                logging.info("mappingConfig {}".format(mappingConfig))
                logging.info("generatedCard {}...".format(str(generatedCard)[0:50]))

                for cardField in cardFields:
                    logging.info("cardField {}".format(cardField))

                    if (
                        cardField in mappingConfig
                        and mappingConfig[cardField] in generatedCard
                        and mappingConfig[cardField] != "<ignored>"
                    ):
                        updatedContent = generatedCard[mappingConfig[cardField]]
                        note.__setitem__(cardField, updatedContent)
                        isUpdated = True
                        logging.info(
                            "Updated field '{}' with value '{}'...".format(
                                cardField, updatedContent[0:50]
                            )
                        )

                        note.flush()

            if isUpdated:
                updated_count += 1
            self.progress.emit(int(percentage))

        return updated_count
