#!/usr/bin/python

from typing import List

from ..constant import Constant
from ..enum.translation import Translation
from ..enum.card import Card
from ..enum.status import Status
from ..helpers.dictionary import DictHelper
from ..dictionary.jisho import JishoDictionary
from ..dictionary.kantan import KantanDictionary
from ..base_generator import BaseGenerator


class JapaneseGenerator(BaseGenerator):
    def get_formatted_words(
        self, word: str, translation: Translation, allWordTypes: bool
    ) -> List[str]:
        word = word.lower().strip()

        foundWords: List[str] = []
        if translation.equals(Constant.JP_EN) and allWordTypes:
            foundWords += DictHelper.get_jisho_words(word)

        elif translation.equals(Constant.JP_VN):
            foundWords += DictHelper.get_kantan_words(word, allWordTypes)
        else:
            foundWords.append(
                word + Constant.SUB_DELIMITER + word + Constant.SUB_DELIMITER + word
            )
        return foundWords

    def generate_card(
        self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool
    ) -> Card:

        card: Card = Card()

        # Japanese to Vietnamese
        if translation.equals(Constant.JP_VN):

            kantan = KantanDictionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, kantan
            )

        # Japanese to English
        elif translation.equals(Constant.JP_EN):

            jishoDict = JishoDictionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, jishoDict
            )

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target()
            )

        return card
