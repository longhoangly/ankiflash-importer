#!/usr/bin/python


from typing import List

from ..constant import Constant
from ..enum.translation import Translation
from ..enum.card import Card
from ..enum.status import Status
from ..dictionary.collins import CollinsDictionary
from ..dictionary.lacviet import LacVietDictionary
from ..base_generator import BaseGenerator


class FrenchGenerator(BaseGenerator):
    def get_formatted_words(
        self, word: str, translation: Translation, allWordTypes: bool
    ) -> List[str]:
        word = word.lower().strip()

        foundWords = []
        foundWords.append(
            word + Constant.SUB_DELIMITER + word + Constant.SUB_DELIMITER + word
        )
        return foundWords

    def generate_card(
        self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool
    ) -> Card:

        card: Card = Card()

        # French to Vietnamese
        if translation.equals(Constant.FR_VN):

            lacVietDict = LacVietDictionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, lacVietDict
            )

        # French to English
        elif translation.equals(Constant.FR_EN):

            collinsDict = CollinsDictionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, collinsDict
            )

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target
            )

        return card
