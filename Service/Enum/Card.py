#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from ...Service.Enum.Translation import Translation


class Card:

    word: str
    wordId: str
    oriWord: str

    wordType: str
    phonetic: str
    example: str

    image: str
    imageLink: str
    sound: str
    soundLinks: List[str]
    status: str

    meaning: str
    tag: str
    copyright: str
    comment: str

    translation: Translation

    def __init__(self, word=None, wordId=None, oriWord=None, translation=None) -> None:
        self.word = word
        self.wordId = wordId
        self.oriWord = oriWord
        self.translation = translation
