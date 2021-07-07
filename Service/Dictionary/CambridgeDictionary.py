#!/usr/bin/python
# -*- coding: utf-8 -*-

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

        self.word = HtmlHelper.getText(self.doc, "span.headword>span,.hw", 0)
        return not self.word

    def getWordType(self) -> str:
        if not self.wordType:
            self.wordType = HtmlHelper.getText(self.doc, "span.pos", 0)
            self.wordType = "(" + self.wordType + ")" if self.wordType else ""
        return self.wordType

    def getExample(self) -> str:
        raise NotImplementedError

    def getPhonetic(self) -> str:
        if not self.phonetic:
            phoneticBrE = HtmlHelper.getText(self.doc, "span.phon", 0)
            phoneticNAmE = HtmlHelper.getText(self.doc, "span.phon", 1)
            self.phonetic = "{} {}".format(
                phoneticBrE, phoneticNAmE).replace("//", " / ")
        return self.phonetic

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        raise NotImplementedError

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        raise NotImplementedError

    def getMeaning(self) -> str:
        self.getWordType()
        self.getPhonetic()

        meanings: List[Meaning] = []
        headerGroups = self.doc.select("div[class*=entry-body__el]")
        for headerGroup in headerGroups:
            # Word Type Header
            meaning = Meaning()
            wordTypeHeader = headerGroup.select(
                ".pos-header,div[class*=di-head]", limit=1)
            if wordTypeHeader:
                headerTexts = []
                elements = wordTypeHeader.select(".pos,.pron")
                for element in elements:
                    headerTexts.append(element.text)

                meaning.wordType = " ".join(headerTexts)
                meanings.append(meaning)

            examples = []
            meanGroups = headerGroup.select("div.sense-block")
            for meanGroup in meanGroups:
                # Header
                meaning = Meaning()
                header = meanGroup.select("h3", limit=1)
                if header:
                    meaning.wordType = header.text
                    meanings.append(meaning)

                # Meaning
                meaningElms = meanGroup.select("div[class*=def-block]")
                for meaningElm in meaningElms:
                    meaning = Meaning()
                    definition =meaningElm.select("b.def", limit=1)
                    if definition:
                        meaning.meaning =definition.text

                    examples = []
                    for element in meaningElm.select(".eg,.trans"):
                        examples.append(Tag(element).text)
                    meaning.examples = examples
                    meanings.append(meaning)

                # Extra Examples
                meaning = Meaning()
                examples = []
                extraExample =meanGroup.select(".extraexamps>p", limit=1)
                if extraExample:
                    meaning.wordType =extraExample.text
                    for element in meanGroup.select(".extraexamps>ul>li.eg"):
                        examples.append(Tag(element).text)
                    meaning.examples = examples
                    meanings.append(meaning)

        return HtmlHelper.buildMeaning(self.word, self.wordType, self.phonetic, meanings)

    def getDictionaryName(self) -> str:
        return "Cambridge Dictionary"
