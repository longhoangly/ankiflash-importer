#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from ..Enum.Meaning import Meaning
from ..Enum.Translation import Translation

from ..Constant import Constant
from ..BaseDictionary import BaseDictionary
from ...Helpers.HtmlHelper import HtmlHelper
from ...Helpers.AnkiHelper import AnkiHelper


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
            wordTypes = HtmlHelper.getTexts(self.doc, "span.pos.dpos", True)
            self.wordType = " | ".join(wordTypes) if len(wordTypes) > 0 else ""
            self.wordType = "({})".format(self.wordType)
        return self.wordType

    def getExample(self) -> str:
        raise NotImplementedError

    def getPhonetic(self) -> str:
        if not self.phonetic:
            self.phonetic = HtmlHelper.getText(self.doc, "span.pron.dpron", 0)
        return self.phonetic

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        raise NotImplementedError

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        raise NotImplementedError

    def getMeaning(self) -> str:
        self.getWordType()
        self.getPhonetic()

        allMeaningTexts: List[str] = []
        meanings: List[Meaning] = []
        headerGroups = self.doc.select(
            "div[class*=kdic],div[class*=entry-body__el]")
        for headerGroup in headerGroups:
            # Word Type
            typeMeaning = Meaning()
            elements = headerGroup.select(".pos.dpos,.pron.dpron,.guideword")
            headerTexts = []
            for element in elements:
                headerTexts.append(
                    element.get_text().replace("\n", " ").capitalize())
            typeMeaning.wordType = AnkiHelper.stringify(
                " ".join(headerTexts)).replace(") (", " | ")

            indexMeaning = 0
            meaningElms = headerGroup.select("div[class*=def-block]")
            for meaningElm in meaningElms:
                # Meaning
                meaning = Meaning()
                header = meaningElm.select_one(".def.ddef_d,.phrase.dphrase")
                if header:
                    meaning.meaning = header.get_text().replace("\n", " ")
                    meaning.meaning = AnkiHelper.stringify(meaning.meaning)

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

                # Only add wordtype if there is a meaning
                if meaning.meaning not in allMeaningTexts:
                    # Only add after the first meaning
                    if(indexMeaning == 0):
                        meanings.append(typeMeaning)
                    meanings.append(meaning)
                    indexMeaning += 1
                    # Don't add duplicated meaning!
                    allMeaningTexts.append(meaning.meaning)

        return HtmlHelper.buildMeaning(self.word, self.wordType, self.phonetic, meanings, True)

    def getDictionaryName(self) -> str:
        return "Cambridge Dictionary"
