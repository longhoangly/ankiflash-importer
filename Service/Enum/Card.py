#!/usr/bin/python
# -*- coding: utf-8 -*-

from ...Service.Enum.Translation import Translation


class Card:

    word: str
    wordId: str
    oriWord: str

    wordType: str
    phonetic: str
    example: str

    image: str
    sound: str
    status: str

    meaning: str
    tag: str
    copyright: str
    comment: str

    translation: Translation

    def __init__(self, word, wordId, oriWord, translation) -> None:
        self.word = word
        self.wordId = wordId
        self.oriWord = oriWord
        self.translation = translation
