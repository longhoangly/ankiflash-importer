#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
import logging

from ..Enum.Translation import Translation
from ..Enum.Card import Card
from ..Enum.Status import Status
from ..BaseGenerator import BaseGenerator
from ..Constant import Constant
from ...Helpers.DictHelper import DictHelper

from ..Dictionary.JishoDictionary import JishoDictionary
from ..Dictionary.JDictDictionary import JDictDictionary


class JapaneseGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        word = word.lower().strip()
        foundWords: List[str] = []
        if translation.equals(Constant.JP_EN):
            foundWords += DictHelper.getJishoWords(word)
        elif translation.equals(Constant.JP_VN):
            foundWords += DictHelper.getJDictWords(word)
        else:
            foundWords.append(word + Constant.SUB_DELIMITER +
                              word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generateCard(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        card: Card = self.initializeCard(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        jDict = JDictDictionary()
        jishoDict = JishoDictionary()

        # Japanese to Vietnamese
        if translation.equals(Constant.JP_VN):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, jDict)

        # Japanese to English
        elif translation.equals(Constant.JP_EN):

            card = self.singleDictionaryCard(
                formattedWord, translation, ankiDir, isOnline, card, jishoDict)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target())

        return card
