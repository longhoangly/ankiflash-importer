#!/usr/bin/python
# -*- coding: utf-8 -*-


from typing import List
import logging

from ..Enum.Translation import Translation
from ..Enum.Status import Status
from ..Enum.Card import Card

from ..Constant import Constant
from ..BaseGenerator import BaseGenerator
from ...Helpers.DictHelper import DictHelper

from ..Dictionary.LacVietDictionary import LacVietDictionary
from ..Dictionary.CambridgeDictionary import CambridgeDictionary
from ..Dictionary.OxfordDictionary import OxfordDictionary


class EnglishGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        word = word.lower().strip()
        foundWords = []
        if translation.equals(Constant.EN_EN) and allWordTypes:
            foundWords += DictHelper.getOxfordWords(word)
        else:
            foundWords.append(word + Constant.SUB_DELIMITER +
                              word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generateCard(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        formattedWord = formattedWord.lower()
        card: Card = self.initializeCard(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        oxfordDict = OxfordDictionary()
        cambridgeDict = CambridgeDictionary()
        lacVietDict = LacVietDictionary()

        # English to English
        if (translation.equals(Constant.EN_EN)):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, oxfordDict)

        # English to Chinese/French/Japanese
        elif translation.equals(Constant.EN_CN_TD) or translation.equals(Constant.EN_CN_SP) or translation.equals(Constant.EN_JP) or translation.equals(Constant.EN_FR):

            card = self.multipleDictionariesCard(
                formattedWord, translation, ankiDir, isOnline, card, oxfordDict, cambridgeDict)

        # English to Vietnamese
        elif translation.equals(Constant.EN_VN):

            card = self.multipleDictionariesCard(
                formattedWord, translation, ankiDir, isOnline, card, oxfordDict, lacVietDict)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target)

        return card
