#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from aqt.utils import showInfo

from abc import ABC, abstractmethod
from typing import List

from ..Ui.UiAnkiFlash import UiAnkiFlash
from .BaseDictionary import BaseDictionary
from .Enum.Translation import Translation
from .Enum.Status import Status
from .Constant import Constant
from .Enum.Card import Card


class BaseGenerator(ABC):

    def __init__(self):
        self.delimiter: str = "==="

    @abstractmethod
    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        """Get all part of speech of a specific word"""
        raise NotImplementedError

    @abstractmethod
    def generateCard(self, ui: UiAnkiFlash, formattedWord: str, translation: Translation, ankiDir: str, isOnline: bool) -> Card:
        """Generate a flashcard from an input word"""
        raise NotImplementedError

    def generateCards(self, ui: UiAnkiFlash, words: List[str], translation: Translation, ankiDir: str, isOnline: bool, allWordTypes: bool) -> List[Card]:
        """Generate flashcards from input words"""

        cardCount: int = 0
        failureCount: int = 0

        if not allWordTypes and translation.source == "Enlgish":
            for value in words:
                formattedWord = "{}{}{}{}{}".format(
                    value, self.delimiter, value, self.delimiter, value)
                card = self.generateCard(
                    ui, formattedWord, ankiDir, translation, isOnline)
                logging.info("card = {}".format(card))

                if card.status == Status.SUCCESS:
                    cardCount += 1
                    ui.outputTxt.setPlainText(
                        ui.outputTxt.toPlainText() + "{}\n".format(card.meaning))
                else:
                    failureCount += 1
                    ui.failureTxt.setPlainText(ui.failureTxt.toPlainText() + "{} -> {}\n".format(
                        formattedWord, card.comment))
        else:
            for value in words:
                formattedWords = self.getFormattedWords(value, translation)
                if len(formattedWords) > 0:
                    for formattedWord in formattedWords:
                        card = self.generateCard(
                            ui, formattedWord, ankiDir, translation, isOnline)
                        logging.info("card = {}".format(card))
                        
                        if card.status == Status.SUCCESS:
                            cardCount += 1
                            ui.outputTxt.setPlainText(
                                ui.outputTxt.toPlainText() + "{}\n".format(card.meaning))
                        else:
                            failureCount += 1
                            ui.failureTxt.setPlainText(ui.failureTxt.toPlainText(
                            ) + "{} -> {}\n".format(formattedWord, card.comment))
                else:
                    ui.failureTxt.setPlainText(
                        ui.failureTxt.toPlainText() + "{} -> word not found\n".format(value))

        showInfo("""Completed 100%
        Input: {}
        Output: {}
        Failure: {}\n""".format(len(words), cardCount, failureCount))

    def initializeCard(self, formattedWord: str, translation: Translation):

        card = Card()
        wordParts: list[str] = formattedWord.split(Constant.SUB_DELIMITER)
        if Constant.SUB_DELIMITER in formattedWord and len(wordParts) == 3:
            card = Card(wordParts[0], wordParts[1], wordParts[2], translation)
        else:
            card.status = Status.WORD_NOT_FOUND
            card.comment = "Incorrect word format = {}".format(formattedWord)
        return card

    def singleDictionaryCard(self, formattedWord: str, translation: Translation, ankiDir: str, isOnline: bool, card: Card, dictionary: BaseDictionary) -> Card:

        if dictionary.search(formattedWord, translation):
            card.status = Status.CONNECTION_FAILED
            card.comment = Constant.CONNECTION_FAILED
            return card
        elif dictionary.isInvalidWord():
            card.status = Status.WORD_NOT_FOUND
            card.comment = Constant.WORD_NOT_FOUND
            return card

        card.wordType = dictionary.getWordType()
        card.phonetic = dictionary.getPhonetic()
        card.example = dictionary.getExample()

        card.sounds = dictionary.getSounds(ankiDir, isOnline)
        card.image = dictionary.getImage(ankiDir, isOnline)

        card.copyright = Constant.COPYRIGHT.format(
            dictionary.getDictionaryName())

        card.meaning = dictionary.getMeaning()
        card.tag = dictionary.getTag()

        return card

    def coupleDictionariesCard(self, formattedWord: str, translation: Translation, ankiDir: str, isOnline: bool, card: Card, mainDict: BaseDictionary, meaningDict: BaseDictionary) -> Card:

        if mainDict.search(formattedWord, translation) or meaningDict.search(formattedWord, translation):
            card.status = Status.CONNECTION_FAILED
            card.comment = Constant.CONNECTION_FAILED
            return card
        elif mainDict.isInvalidWord() or meaningDict.isInvalidWord():
            card.status = Status.WORD_NOT_FOUND
            card.comment = Constant.WORD_NOT_FOUND
            return card

        card.wordType = mainDict.getWordType()
        card.phonetic = mainDict.getPhonetic()
        card.example = mainDict.getExample()

        card.sounds = mainDict.getSounds(ankiDir, isOnline)
        card.image = mainDict.getImage(ankiDir, isOnline)

        card.copyright = Constant.COPYRIGHT.format("".join(
            mainDict.getDictionaryName(), ", and ", meaningDict.getDictionaryName()))

        # Meaning is get from meaning dictionary
        card.meaning = meaningDict.getMeaning()
        card.tag = mainDict.getTag()

        return card
