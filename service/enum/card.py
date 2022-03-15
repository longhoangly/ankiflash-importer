#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from .. enum.translation import Translation


@dataclass
class Card:

    def __init__(self, translation=None):

        # word in html meaning
        self.word: str = ""
        # word id for getting html
        self.wordId: str = ""
        # original word from user's input
        self.oriWord: str = ""

        self.wordType: str = ""
        self.phonetic: str = ""
        self.example: str = ""

        self.image: str = ""
        self.sounds: str = ""
        self.status: str = ""

        self.meaning: str = ""
        self.copyright: str = ""
        self.comment: str = ""
        self.tag: str = ""

        self.translation: Translation = translation
