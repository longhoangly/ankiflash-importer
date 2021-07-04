#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..Enum.Translation import Translation


class Card:

    word: str
    wordId: str
    oriWord: str

    wordType: str
    phonetic: str
    example: str

    image: str
    sounds: str
    status: str

    meaning: str
    copyright: str
    comment: str
    tag: str

    translation: Translation

    def __init__(self, word=None, wordId=None, oriWord=None, translation=None) -> None:
        self.word = word
        self.wordId = wordId
        self.oriWord = oriWord
        self.translation = translation
