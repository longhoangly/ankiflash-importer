#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
from bs4.element import Tag
from bs4 import BeautifulSoup

from ..Enum.Meaning import Meaning
from ..Enum.Translation import Translation

from ..Constant import Constant
from ..BaseDictionary import BaseDictionary
from ...Helpers.HtmlHelper import HtmlHelper
from ...Helpers.DictHelper import DictHelper


class JishoDictionary(BaseDictionary):

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

        url = HtmlHelper.lookupUrl(Constant.JISHO_WORD_URL_JP_EN, self.wordId)
        self.doc = HtmlHelper.getDocument(url)

        return True if not self.doc else False

    def isInvalidWord(self) -> bool:
        """Check if the input word exists in dictionary?"""

        if Constant.JISHO_WORD_NOT_FOUND in self.doc.get_text():
            return True

        word = HtmlHelper.getText(self.doc, ".concept_light-representation", 0)
        return not word

    def getWordType(self) -> str:
        if not self.wordType:
            elements = self.doc.select(
                "div.concept_light.clearfix div.meaning-tags")

            wordTypes = []
            for element in elements:
                wType = element.get_text().strip()

                if wType and "Wikipedia definition" != wType and "Other forms" != wType:
                    if wType not in wordTypes:
                        wordTypes.append(wType)

            self.wordType = "(" + " / ".join(wordTypes) + \
                ")" if len(wordTypes) > 0 else ""
        return self.wordType

    def getExample(self) -> str:
        examples: list[str] = []
        for i in range(4):
            example = HtmlHelper.getChildInnerHtml(
                self.doc, ".sentence", i)
            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example and i != 0:
                break
            else:
                lowerWord = self.oriWord.lower()
                exampleStr = example.strip().lower()

                if lowerWord in exampleStr:
                    exampleStr = exampleStr.replace(
                        lowerWord, "{{c1::" + lowerWord + "}}")
                else:
                    exampleStr = "{} {}".format(exampleStr, "{{c1::...}}")
                examples.append(exampleStr.replace("\n", ""))

        return HtmlHelper.buildExample(examples, True)

    def getPhonetic(self) -> str:
        return ""

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        self.imageLink = ""
        self.image = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.oriWord)
        return self.image

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = HtmlHelper.getAttribute(
            self.doc, "audio>source", 0, "src")

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

        self.soundLinks = "https:" + self.soundLinks
        links = self.soundLinks.split(";")
        for soundLink in links:
            soundName = DictHelper.getFileName(soundLink)
            if isOnline:
                self.sounds = "<audio src=\"{}\" type=\"audio/wav\" preload=\"auto\" autobuffer controls>[sound:{}]</audio> {}".format(
                    soundLink, soundLink, self.sounds if len(self.sounds) > 0 else "")
            else:
                self.sounds = "<audio src=\"{}\" type=\"audio/wav\" preload=\"auto\" autobuffer controls>[sound:{}]</audio> {}".format(
                    soundName, soundName, self.sounds if len(self.sounds) > 0 else "")

        if not isOnline:
            DictHelper.downloadFiles(ankiDir, self.soundLinks)
        return self.sounds

    def getMeaning(self) -> str:
        self.getWordType()

        meanings: List[Meaning] = []
        meanGroup = HtmlHelper.getDocElement(self.doc, ".meanings-wrapper", 0)
        if meanGroup:
            meaning: Meaning
            meanElms = meanGroup.select(".meaning-tags,.meaning-wrapper")

            wordTypes = []
            for meanElm in meanElms:
                # Word type
                if "meaning-tags" in meanElm["class"]:
                    meaning = Meaning()
                    meaning.wordType = meanElm.get_text().capitalize()
                    if meaning.wordType not in wordTypes:
                        wordTypes.append(meaning.wordType)
                        meanings.append(meaning)

                # Meaning
                if "meaning-wrapper" in meanElm["class"]:
                    meaning = Meaning()
                    mean = HtmlHelper.getChildElement(
                        meanElm, ".meaning-meaning", 0)
                    if mean:
                        meaning.meaning = mean.get_text().strip()

                    examples = []
                    exampleElms = meanElm.select(".sentence")
                    for exampleElm in exampleElms:
                        if exampleElm:
                            examples.append(
                                exampleElm.get_text().replace("\n", ""))

                    meaning.examples = examples
                    meanings.append(meaning)

            # Extra examples
            meaning = Meaning()
            extraExamples = getJishoJapaneseSentences(self.word)
            if extraExamples:
                meaning.wordType = "Extra examples"
                meaning.examples = extraExamples
                meanings.append(meaning)

        return HtmlHelper.buildMeaning(self.word, self.wordType, self.phonetic, meanings, True)

    def getDictionaryName(self) -> str:
        return "Jisho Dictionary"


def getJishoJapaneseSentences(word: str) -> List[str]:

    url = HtmlHelper.lookupUrl(
        Constant.JISHO_SEARCH_URL_JP_EN, word + "%20%23sentences")
    document: BeautifulSoup = HtmlHelper.getDocument(url)

    sentences: list[str] = []
    sentenceElms = []
    if document:
        sentenceElms = document.select(".sentence_content")

    maxCount = 1
    for sentenceElm in sentenceElms:
        sentences.append(sentenceElm.decode_contents().replace("\n", ""))

        if maxCount >= 10:
            break
        maxCount = maxCount + 1

    return sentences
