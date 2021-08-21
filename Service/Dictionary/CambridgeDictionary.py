#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from typing import List
from bs4.element import Tag

from ..Enum.Meaning import Meaning
from ..Enum.Translation import Translation

from ..Constant import Constant
from ..BaseDictionary import BaseDictionary
from ...Helpers.HtmlHelper import HtmlHelper


class CambridgeDictionary(BaseDictionary):

    def search(self, formattedWord: str, translation: Translation) -> bool:
        """Find input word from dictionary data"""

        wordParts = formattedWord.split(self.delimiter)
        if self.delimiter in formattedWord and len(wordParts) == 3:
            self.word = wordParts[0]
            self.wordId = wordParts[1]
            self.oriWord = wordParts[2]
        else:
            raise RuntimeError(
                "Incorrect word format: {}".format(formattedWord))

        url = ""
        if translation.equals(Constant.EN_CN_TD):
            url = HtmlHelper.lookupUrl(
                Constant.CAMBRIDGE_URL_EN_CN_TD, self.wordId)
        elif (translation.equals(Constant.EN_CN_SP)):
            url = HtmlHelper.lookupUrl(
                Constant.CAMBRIDGE_URL_EN_CN_SP, self.wordId)
        elif (translation.equals(Constant.EN_FR)):
            url = HtmlHelper.lookupUrl(
                Constant.CAMBRIDGE_URL_EN_FR, self.wordId)
        elif (translation.equals(Constant.EN_JP)):
            url = HtmlHelper.lookupUrl(
                Constant.CAMBRIDGE_URL_EN_JP, self.wordId)

        self.doc = HtmlHelper.getDocument(url)

        return True if not self.doc else False

    def isInvalidWord(self) -> bool:
        """Check if the input word exists in dictionary?"""

        title = HtmlHelper.getText(self.doc, "title", 0)
        if Constant.CAMBRIDGE_SPELLING_WRONG in title:
            return True

        self.word = HtmlHelper.getText(self.doc, ".dhw", 0)
        return not self.word

    def getWordType(self) -> str:
        if not self.wordType:
            wordTypes = HtmlHelper.getTexts(self.doc, "span.pos")
            self.wordType = " | ".join(wordTypes) if len(wordTypes) > 0 else ""
            self.wordType = "({})".format(self.wordType)
        return self.wordType

    def getExample(self) -> str:
        raise NotImplementedError

    def getPhonetic(self) -> str:
        if not self.phonetic:
            self.phonetic = HtmlHelper.getText(self.doc, "span.pron", 0)
        return self.phonetic

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        raise NotImplementedError

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        raise NotImplementedError

    def getMeaning(self) -> str:
        self.getWordType()
        self.getPhonetic()

        meanings: List[Meaning] = []
        headerGroups = self.doc.select("div[class*=kdic]")
        for headerGroup in headerGroups:
            # Word Type
            meaning = Meaning()
            elements = headerGroup.select(".pos,.pron")
            headerTexts = []
            for element in elements:
                headerTexts.append(element.get_text())
            meaning.wordType = " ".join(headerTexts)
            meanings.append(meaning)

            meaningElms = headerGroup.select("div[class*=def-block]")
            for meaningElm in meaningElms:
                # Meaning
                meaning = Meaning()
                header = meaningElm.select_one(".def.ddef_d,.phrase.dphrase")
                if header:
                    meaning.meaning = header.get_text()

                # Sub Meaning
                definitions = meaningElm.select(".ddef_b>span.trans")
                definitionTexts = []
                for definition in definitions:
                    definitionTexts.append(definition.get_text())
                meaning.subMeaning = " ".join(definitionTexts) if len(
                    definitionTexts) > 0 else ""

                # Examples
                examples = []
                for element in meaningElm.select(".eg,.trans.hdb"):
                    examples.append(element.get_text())
                meaning.examples = examples
                meanings.append(meaning)

        return HtmlHelper.buildMeaning(self.word, self.wordType, self.phonetic, meanings)

    def getDictionaryName(self) -> str:
        return "Cambridge Dictionary"
