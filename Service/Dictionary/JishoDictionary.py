#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
from bs4 import BeautifulSoup

from bs4.element import Tag

from ...Service.BaseDictionary import BaseDictionary
from ...Service.Constant import Constant
from ...Helpers.HtmlHelper import HtmlHelper
from ...Helpers.DictHelper import DictHelper
from ...Service.Enum.Meaning import Meaning
from ...Service.Enum.Translation import Translation


class JishoDictionary(BaseDictionary):

    def search(self, formattedWord: str, translation: Translation) -> bool:
        """Find input word from dictionary data"""
        wordParts = formattedWord.split(self.delimiter)

        if (formattedWord.contains(self.delimiter) and len(wordParts) == 3):
            self.word = wordParts[0]
            self.wordId = wordParts[1]
            self.oriWord = wordParts[2]
        else:
            raise RuntimeError(
                "Incorrect word format: {}".format(formattedWord))

        url = HtmlHelper.lookupUrl(Constant.JISHO_WORD_URL_JP_EN, self.wordId)
        self.doc = HtmlHelper.getDocument(url)

        return True if self.doc else False

    def isInvalidWord(self) -> bool:
        """Check if the input word exists in dictionary?"""
        if Constant.JISHO_WORD_NOT_FOUND in self.doc.parent.text:
            return True

        word = HtmlHelper.getText(self.doc, ".concept_light-representation", 0)
        return not word

    def getWordType(self) -> str:
        if not self.wordType:
            elements = self.doc.select(
                "div.concept_light.clearfix div.meaning-tags")
            wordTypes = []

            for element in elements:
                if element.string and "Wikipedia definition" != element.string and "Other forms" != element.string:
                    wordTypes.add("[" + element.string + "]")

            self.wordType = "(" + "".join(" / ", wordTypes) + \
                ")" if len(wordTypes) > 0 else ""
        return self.wordType

    def getExample(self) -> str:
        examples: list[str] = []
        for i in range(4):
            example = HtmlHelper.getInnerHtml(self.doc, ".sentence", i)
            if example and i == 0:
                return Constant.NO_EXAMPLE
            elif example:
                break
            else:
                lowerWord = self.oriWord.lower()
                example = Tag(example).string.lower()

                if lowerWord in example:
                    example = example.replace(
                        lowerWord, "{{c1::" + lowerWord + "}}")
                else:
                    example = "".format("{} {}", example, "{{c1::...}}")
                examples.append(example.replace("\n", ""))

        return HtmlHelper.buildExample(examples, True)

    def getPhonetic(self) -> str:
        raise NotImplementedError

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        self.imageLink = ""
        self.image = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.word)
        return self.image

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = HtmlHelper.getAttribute(
            self.doc, "audio>source[type=audio/mpeg]", 0, "src")

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
            for meanElm in meanElms:
                if "meaning-tags" in meanElm["class"]:
                    meaning = Meaning()
                    meaning.setWordType(meanElm.text())
                    meanings.add(meaning)

                if "meaning-wrapper" in meanElm["class"]:
                    meaning = Meaning()
                    mean = HtmlHelper.getChildElement(
                        meanElm, ".meaning-meaning", 0)
                    if mean:
                        meaning.meaning = mean.string

                    examples = []
                    exampleElms = meanElm.select(".sentence")
                    for exampleElm in exampleElms:
                        if exampleElm:
                            examples.append(
                                exampleElm.html().replaceAll("\n", ""))

                    meaning.examples = examples
                    meanings.append(meaning)

            meaning = Meaning()
            extraExamples = getJishoJapaneseSentences(self.word)
            if extraExamples:
                meaning.wordType = "Extra Examples"
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
        sentences.append(sentenceElm.html.replace("\n", ""))

        if maxCount >= 10:
            break
        maxCount = maxCount + 1

    return sentences
