#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup
from .Enum.Translation import Translation


class BaseDictionary(ABC):

    delimiter: str = "==="
    doc: BeautifulSoup

    word: str
    wordId: str
    oriWord: str

    ankiDir: str
    image: str
    sounds: str

    wordType: str
    phonetic: str

    def __init__(self):
        pass

    @abstractmethod
    def search(self, formattedWord, translation: Translation) -> bool:
        """Find input word from dictionary data"""
        raise NotImplementedError

    @abstractmethod
    def isInvalidWord(self) -> bool:
        """Check if the input word exists in dictionary?"""
        raise NotImplementedError

    @abstractmethod
    def getWordType(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getExample(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getPhonetic(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        raise NotImplementedError

    @abstractmethod
    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def getMeaning(self) -> str:
        raise NotImplementedError

    def getTag(self) -> str:
        return self.word[0]

    @abstractmethod
    def getDictionaryName(self) -> str:
        raise NotImplementedError
