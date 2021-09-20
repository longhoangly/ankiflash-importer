#!/usr/bin/python
# -*- coding: utf-8 -*-


from typing import List
import logging

from ..Enum.Translation import Translation
from ..Enum.Status import Status
from ..Enum.Card import Card

from ..Constant import Constant
from ..BaseGenerator import BaseGenerator

from ..Dictionary.CollinsDictionary import CollinsDictionary
from ..Dictionary.LacVietDictionary import LacVietDictionary


class FrenchGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        foundWords = []
        foundWords.append(word + Constant.SUB_DELIMITER +
                          word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generateCard(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        card: Card = self.initializeCard(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        lacVietDict = LacVietDictionary()
        collinsDict = CollinsDictionary()

        # French to Vietnamese
        if translation.equals(Constant.FR_VN):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, lacVietDict)

        # French to English
        elif translation.equals(Constant.FR_EN):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, collinsDict)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target)

        return card
