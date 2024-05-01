#!/usr/bin/python

from typing import List

from ..enum.card import Card
from ..enum.translation import Translation
from ..base_generator import BaseGenerator


class ChineseGenerator(BaseGenerator):
    def get_formatted_words(
        self, word: str, translation: Translation, relatedWords: bool
    ) -> List[str]:
        raise NotImplementedError

    def generate_card(
        self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool
    ) -> Card:
        raise NotImplementedError
