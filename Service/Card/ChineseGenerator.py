#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from ..Enum.Translation import Translation
from ..Enum.Card import Card
from ..BaseGenerator import BaseGenerator


class ChineseGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        raise NotImplementedError

    def generateCard(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:
        raise NotImplementedError
