#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt.utils import showInfo

from typing import List

from ...Ui.UiAnkiFlash import UiAnkiFlash
from ...Service.Enum.Translation import Translation
from ...Service.Enum.Card import Card
from ...Service.BaseGenerator import BaseGenerator


class FrenchGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        showInfo("This is getFormattedWords from FrenchGenerator")
        return [""]

    def generateCard(self, ui: UiAnkiFlash, formattedWord: str, translation: Translation, isOnline: bool) -> Card:
        showInfo("This is generateCard from FrenchGenerator")
        return Card()
