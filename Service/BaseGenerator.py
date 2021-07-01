#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt.utils import showInfo

from abc import ABC, abstractmethod
from typing import List

from ..Ui.UiAnkiFlash import UiAnkiFlash
from ..Service.Enum.Translation import Translation
from ..Service.Enum.Card import Card


class BaseGenerator(ABC):

    delimiter: str = "==="

    @abstractmethod
    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        """Get all part of speech of a specific word"""
        raise NotImplementedError

    @abstractmethod
    def generateCard(self, ui: UiAnkiFlash, formattedWord: str, translation: Translation, isOnline: bool) -> Card:
        """Generate a flashcard from an input word"""
        raise NotImplementedError

    def generateCards(self, ui: UiAnkiFlash, words: List[str], translation: Translation, isOnline: bool, allWordTypes: bool) -> List[Card]:
        """Generate flashcards from input words"""

        cardCount: int = 0
        failureCount: int = 0

        if not allWordTypes and translation.source == "Enlgish":
            for value in words:
                formattedWord = "{}{}{}{}{}".format(
                    value, self.delimiter, value, self.delimiter, value)
                card = self.generateCard(
                    ui, formattedWord, translation, isOnline)

                if card.status == "Success":
                    cardCount += 1
                    ui.outputTxt += "{}\n".format(card.meaning)
                else:
                    failureCount += 1
                    ui.failureTxt += "{} -> {}\n".format(
                        formattedWord, card.comment)
        else:
            for value in words:
                formattedWords = self.getFormattedWords(value, translation)
                if len(formattedWords) > 0:
                    for formattedWord in formattedWords:
                        card = self.generateCard(
                            ui, formattedWord, translation, isOnline)

                        if card.status == "Success":
                            cardCount += 1
                            ui.outputTxt += "{}\n".format(card.meaning)
                        else:
                            failureCount += 1
                            ui.failureTxt += "{} -> {}\n".format(
                                formattedWord, card.comment)
                else:
                    ui.failureTxt += "{} -> word not found\n".format(value)

        showInfo("""Completed 100%
        Input: {}
        Output: {}
        Failure: {}\n""".format(len(words), cardCount, failureCount))
