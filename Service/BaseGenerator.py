#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod
from typing import List

from .BaseDictionary import BaseDictionary
from .Enum.Translation import Translation
from .Enum.Status import Status
from .Constant import Constant
from .Enum.Card import Card

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import os
import csv
csv.field_size_limit(2**30)


class BaseGenerator(ABC):

    @abstractmethod
    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        """Get all part of speech of a specific word"""
        raise NotImplementedError

    @abstractmethod
    def generateCard(self, formattedWord: str, translation: Translation, mediaDir: str, isOnline: bool) -> Card:
        """Generate a flashcard from an input word"""
        raise NotImplementedError

    def initializeCard(self, formattedWord: str, translation: Translation):

        card = Card()
        wordParts: list[str] = formattedWord.split(Constant.SUB_DELIMITER)
        if Constant.SUB_DELIMITER in formattedWord and len(wordParts) == 3:
            card = Card(wordParts[0], wordParts[1], wordParts[2], translation)
        else:
            card.status = Status.WORD_NOT_FOUND
            card.comment = "Incorrect word format = {}".format(formattedWord)

        logging.info("word = {}".format(card.word))
        logging.info("wordId = {}".format(card.wordId))
        logging.info("oriWord = {}".format(card.oriWord))

        logging.info("source = {}".format(translation.source))
        logging.info("target = {}".format(translation.target))

        return card

    def singleDictionaryCard(self, formattedWord: str, translation: Translation, mediaDir: str, isOnline: bool, card: Card, dictionary: BaseDictionary) -> Card:

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

        card.sounds = dictionary.getSounds(mediaDir, isOnline)
        card.image = dictionary.getImage(mediaDir, isOnline)

        card.copyright = Constant.COPYRIGHT.format(
            dictionary.getDictionaryName())

        card.meaning = dictionary.getMeaning()
        card.tag = dictionary.getTag()

        return card

    def multipleDictionariesCard(self, formattedWord: str, translation: Translation, mediaDir: str, isOnline: bool, card: Card, mainDict: BaseDictionary, meaningDict: BaseDictionary) -> Card:

        if mainDict.search(formattedWord, translation) or meaningDict.search(formattedWord, translation):
            card.status = Status.CONNECTION_FAILED
            card.comment = Constant.CONNECTION_FAILED
            return card
        elif mainDict.isInvalidWord() or meaningDict.isInvalidWord():
            card.status = Status.WORD_NOT_FOUND
            card.comment = Constant.WORD_NOT_FOUND
            return card

        if translation.equals(Constant.EN_VN) or translation.equals(Constant.EN_FR):
            card.wordType = meaningDict.getWordType()
        else:
            card.wordType = mainDict.getWordType()

        card.phonetic = mainDict.getPhonetic()
        card.example = mainDict.getExample()

        card.sounds = mainDict.getSounds(mediaDir, isOnline)
        card.image = mainDict.getImage(mediaDir, isOnline)

        card.copyright = Constant.COPYRIGHT.format("{}{}{}".format(
            mainDict.getDictionaryName(), ", and ", meaningDict.getDictionaryName()))

        # Meaning is get from meaningDict
        card.meaning = meaningDict.getMeaning()
        card.tag = mainDict.getTag()

        return card


class Worker(QObject):

    # Create a worker class to run in background using QThread
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    cardStr = pyqtSignal(str)
    failureStr = pyqtSignal(str)

    def __init__(self, generator, words, translation, mediaDir, isOnline, allWordTypes, ankiCsvPath):
        super().__init__()

        self.delimiter: str = "==="
        self.formattedWords: List[str] = []
        self.cards: List[Card] = []

        self.generator: BaseGenerator = generator
        self.words: List[str] = words
        self.translation: Translation = translation
        self.mediaDir: str = mediaDir
        self.isOnline: bool = isOnline
        self.allWordTypes: bool = allWordTypes
        self.csvFilePath: str = ankiCsvPath

    def generateCardsBackground(self) -> List[Card]:
        """Generate flashcards from input words"""

        total: int = 0
        proceeded: int = 0
        cardCount: int = 0
        failureCount: int = 0

        total = len(self.words)
        if not self.allWordTypes and self.translation.source == "English":
            for value in self.words:
                formattedWord = "{}{}{}{}{}".format(
                    value, self.delimiter, value, self.delimiter, value)
                card = self.generator.generateCard(
                    formattedWord, self.mediaDir, self.translation, self.isOnline)
                proceeded += 1
                percent = (proceeded / total) * 100
                self.progress.emit(percent)

                if card.status == Status.SUCCESS:
                    cardCount += 1
                    self.cards.append(card)
                    self.cardStr.emit(card.meaning)
                else:
                    failureCount += 1
                    self.failureStr.emit(
                        "{} -> {}".format(value, card.comment))
        else:
            for value in self.words:
                self.formattedWords = self.generator.getFormattedWords(
                    value, self.translation)
                total += len(self.formattedWords) - 1
                if len(self.formattedWords) > 0:
                    for formattedWord in self.formattedWords:
                        card = self.generator.generateCard(
                            formattedWord, self.mediaDir, self.translation, self.isOnline)
                        proceeded = proceeded + 1
                        percent = (proceeded / total) * 100
                        self.progress.emit(percent)

                        if card.status == Status.SUCCESS:
                            cardCount += 1
                            self.cards.append(card)
                            self.cardStr.emit(card.meaning)
                        else:
                            failureCount += 1
                            self.failureStr.emit(
                                "{} -> {}".format(formattedWord.split(self.delimiter)[0], card.comment))
                else:
                    failureCount += 1
                    self.failureStr.emit(Constant.WORD_NOT_FOUND.format(value))

        cardLines: list[str] = []
        for card in self.cards:
            cardContent = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(
                card.word if self.translation.equals(
                    Constant.VN_JP) else card.oriWord,
                Constant.TAB,
                card.wordType,
                Constant.TAB,
                card.phonetic,
                Constant.TAB,
                card.example,
                Constant.TAB,
                card.sounds,
                Constant.TAB,
                card.image,
                Constant.TAB,
                card.meaning,
                Constant.TAB,
                card.copyright,
                Constant.TAB,
                card.tag + "\n")
            cardLines.append(cardContent)

        try:
            os.remove(self.csvFilePath)
        except OSError:
            logging.info("{} does not exist!".format(self.csvFilePath))
            pass
        with open(self.csvFilePath, 'w', encoding='utf-8') as file:
            file.writelines(cardLines)

        # Finished
        self.progress.emit(100)
        self.finished.emit()
