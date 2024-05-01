#!/usr/bin/python

from typing import List

from ..constant import Constant
from ..enum.card import Card
from ..enum.status import Status
from ..enum.translation import Translation
from ..helpers.dictionary import DictHelper
from ..dictionary.kantan import KantanDictionary
from ..dictionary.lacviet import LacVietDictionary
from ..dictionary.wiki import Wiktionary
from ..base_generator import BaseGenerator


class VietnameseGenerator(BaseGenerator):
    def get_formatted_words(
        self, word: str, translation: Translation, relatedWords: bool
    ) -> List[str]:
        word = word.lower().strip()
        foundWords = []
        if translation.equals(Constant.VN_JP):
            foundWords += DictHelper.get_kantan_words(word, relatedWords)
        elif translation.equals(Constant.VN_VN_WIKI):
            foundWords += DictHelper.get_wiki_words(word, relatedWords)
        else:
            foundWords.append(
                word + Constant.SUB_DELIMITER + word + Constant.SUB_DELIMITER + word
            )
        return foundWords

    def generate_card(
        self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool
    ) -> Card:

        card: Card = Card()

        # Vietnamese to English / French / Vietnamese
        if (
            translation.equals(Constant.VN_EN)
            or translation.equals(Constant.VN_FR)
            or translation.equals(Constant.VN_VN)
        ):

            lacVietDict = LacVietDictionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, lacVietDict
            )

        # Vietnamese to Vietnamese (Wiktionary)
        elif translation.equals(Constant.VN_VN_WIKI):

            wiktionary = Wiktionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, wiktionary
            )

        # Vietnamese to Japanese
        elif translation.equals(Constant.VN_JP):

            kantan = KantanDictionary()
            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, kantan
            )

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target
            )

        return card
