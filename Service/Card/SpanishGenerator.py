#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from ...Service.Enum.Translation import Translation
from ...Service.Enum.Card import Card
from ...Service.BaseGenerator import BaseGenerator


class SpanishGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        raise NotImplementedError

    def generateCard(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:
        raise NotImplementedError
