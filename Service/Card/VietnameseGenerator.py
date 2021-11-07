#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
import logging

from ..Enum.Translation import Translation
from ..Enum.Card import Card
from ..Enum.Status import Status
from ..Constant import Constant
from ..BaseGenerator import BaseGenerator
from ...Helpers.DictHelper import DictHelper

from ..Dictionary.JDictDictionary import JDictDictionary
from ..Dictionary.LacVietDictionary import LacVietDictionary


class VietnameseGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        word = word.lower().strip()
        foundWords = []
        if translation.equals(Constant.VN_JP):
            foundWords += DictHelper.getJDictWords(word)
        else:
            foundWords.append(word + Constant.SUB_DELIMITER +
                              word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generateCard(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        card: Card = self.initializeCard(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        lacVietDict = LacVietDictionary()
        jDict = JDictDictionary()

        # Vietnamese to English/French
        if translation.equals(Constant.VN_EN) or translation.equals(Constant.VN_FR):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, lacVietDict)

        # Vietnamese to Japanese
        elif translation.equals(Constant.VN_JP):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, jDict)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target)

        return card
