#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod
from typing import List

from . enum.translation import Translation
from . enum.status import Status
from . enum.card import Card

from . base_dictionary import BaseDictionary
from . constant import Constant


class BaseGenerator(ABC):

    @abstractmethod
    def get_formatted_words(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        """
        Get all part of speech of a specific word
        """
        raise NotImplementedError

    @abstractmethod
    def generate_card(self, formattedWord: str, translation: Translation, mediaDir: str, isOnline: bool) -> Card:
        """
        Generate a flashcard from an input word
        """
        raise NotImplementedError

    def initialize_card(self, formattedWord: str, translation: Translation):

        card = Card(translation)
        wordParts: list[str] = formattedWord.split(Constant.SUB_DELIMITER)

        if Constant.SUB_DELIMITER in formattedWord and len(wordParts) == 3:
            card.status = Status.SUCCESS
            card.comment = Constant.SUCCESS
        else:
            raise RuntimeError(
                "Incorrect formattedWord: {}".format(formattedWord))

        logging.info("source = {}".format(translation.source))
        logging.info("target = {}".format(translation.target))

        return card

    def single_dictionary_card(self, formattedWord: str, translation: Translation, mediaDir: str, isOnline: bool, dictionary: BaseDictionary) -> Card:

        card = self.initialize_card(formattedWord, translation)

        if dictionary.search(formattedWord, translation):
            card.status = Status.CONNECTION_FAILED
            card.comment = Constant.CONNECTION_FAILED
            return card
        elif dictionary.is_invalid_word():
            dictionary.word
            card.status = Status.WORD_NOT_FOUND
            card.comment = Constant.WORD_NOT_FOUND
            return card

        card.wordType = dictionary.get_word_type()
        card.phonetic = dictionary.get_phonetic()
        card.example = dictionary.get_example()

        card.sounds = dictionary.get_sounds(mediaDir, isOnline)
        card.image = dictionary.get_image(mediaDir, isOnline)

        card.copyright = Constant.COPYRIGHT.format(dictionary.get_dictionary_name())
        card.meaning = dictionary.get_meaning()

        card = dictionary.set_card_word(card)
        card.tag = dictionary.get_tag()

        return card

    def multiple_dictionaries_card(self, formattedWord: str, translation: Translation, mediaDir: str, isOnline: bool, mainDict: BaseDictionary, meaningDict: BaseDictionary) -> Card:

        card = self.initialize_card(formattedWord, translation)

        if mainDict.search(formattedWord, translation) or meaningDict.search(formattedWord, translation):
            card.status = Status.CONNECTION_FAILED
            card.comment = Constant.CONNECTION_FAILED
            return card
        elif mainDict.is_invalid_word() or meaningDict.is_invalid_word():
            card.status = Status.WORD_NOT_FOUND
            card.comment = Constant.WORD_NOT_FOUND
            return card

        if translation.equals(Constant.EN_VN) or translation.equals(Constant.EN_FR):
            card.wordType = meaningDict.get_word_type()
        else:
            card.wordType = mainDict.get_word_type()

        card.phonetic = mainDict.get_phonetic()
        card.example = mainDict.get_example()

        card.sounds = mainDict.get_sounds(mediaDir, isOnline)
        card.image = mainDict.get_image(mediaDir, isOnline)

        card.copyright = Constant.COPYRIGHT.format("{}, and {}".format(
            mainDict.get_dictionary_name(), meaningDict.get_dictionary_name()))
        # Meaning is get from meaningDict
        card.meaning = meaningDict.get_meaning()

        card = mainDict.set_card_word(card)
        card.tag = mainDict.get_tag()

        return card
