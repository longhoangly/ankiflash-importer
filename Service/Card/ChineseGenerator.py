#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from ...Ui.UiAnkiFlash import UiAnkiFlash
from ..Enum.Translation import Translation
from ..Enum.Card import Card
from ..BaseGenerator import BaseGenerator


class ChineseGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        raise NotImplementedError

    def generateCard(self, ui: UiAnkiFlash, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:
        raise NotImplementedError
