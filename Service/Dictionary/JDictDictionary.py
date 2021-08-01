#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
from bs4.element import Tag

from ..Enum.Meaning import Meaning
from ..Enum.Translation import Translation

from ..Constant import Constant
from ..BaseDictionary import BaseDictionary
from ...Helpers.HtmlHelper import HtmlHelper
from ...Helpers.DictHelper import DictHelper


class JDictDictionary(BaseDictionary):

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

        urlParameters = "m=dictionary&fn=detail_word&id={}".format(self.wordId)
        self.doc = DictHelper.getJDictDoc(
            Constant.JDICT_URL_VN_JP_OR_JP_VN, urlParameters)

        return True if not self.doc else False

    def isInvalidWord(self) -> bool:
        """Check if the input word exists in dictionary?"""
        
        elements = self.doc.select("#txtKanji")
        if len(elements) == 0:
            return True

        elements = self.doc.select("#word-detail-info")
        return len(elements) > 0

    def getWordType(self) -> str:
        if not self.wordType:
            element: Tag = HtmlHelper.getDocElement(
                self.doc, "label[class*=word-type]", 0)
            self.wordType = "(" + element.get_text().strip() + ")" if element else ""
        return self.wordType

    def getExample(self) -> str:
        examples = []
        exampleElms = []
        for i in range(4):
            example: str = HtmlHelper.getDocElement(
                self.doc, "ul.ul-disc>li>u,ul.ul-disc>li>p", i)
            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example:
                break
            else:
                exampleElms.append(example)

        examples: list[str] = getJDictExamples(exampleElms)
        lowerWord = self.oriWord.lower()
        for i in range(len(examples)):
            example: str = examples[i].lower()
            if lowerWord in example:
                example = example.replace(
                    lowerWord, "{{c1::" + lowerWord + "}}")
            else:
                example = "{} {}".format(example, "{{c1::...}}")
            examples[i] = example

        return HtmlHelper.buildExample(examples, True)

    def getPhonetic(self) -> str:
        if not self.phonetic:
            self.phonetic = HtmlHelper.getText(self.doc, "span.romaji", 0)
        return self.phonetic

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        googleImage = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.oriWord)

        self.imageLink = HtmlHelper.getAttribute(
            self.doc, "a.fancybox.img", 0, "href")
        if not self.imageLink or "no-image" in self.imageLink:
            self.image = googleImage
            return self.image

        if "https" in self.imageLink:
            self.imageLink = "https://j-dict.com" + self.imageLink
        self.imageLink = self.imageLink.replace("\\?w=.*$", "", count=1)
        imageName = DictHelper.getFileName(self.imageLink)
        if isOnline:
            self.image = "<img src=\"" + self.imageLink + "\"/>"
        else:
            self.image = "<img src=\"" + imageName + "\"/>"
            DictHelper.downloadFiles(ankiDir, self.imageLink)
        return self.image

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = HtmlHelper.getAttribute(
            self.doc, "a.sound", 0, "data-fn")

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

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
        self.getPhonetic()

        meanings: List[Meaning] = []
        meaning = Meaning()

        meanGroup: Tag = HtmlHelper.getDocElement(
            self.doc, "#word-detail-info", 0)
        wordType: Tag = HtmlHelper.getChildElement(
            meanGroup, "label[class*=word-type]", 0)
        if wordType:
            meaning.wordType = wordType.get_text().strip()
        meanings.append(meaning)

        meanElms = meanGroup.select("ol.ol-decimal>li")
        for meanElm in meanElms:
            meaning = Meaning()
            mean: Tag = HtmlHelper.getChildElement(meanElm, ".nvmn-meaning", 0)
            if mean:
                meaning.meaning = mean.text

            exampleElms = meanElm.select(
                "ul.ul-disc>li>u,ul.ul-disc>li>p")
            innerExamples: list[str] = getJDictExamples(exampleElms)
            if not innerExamples:
                meaning.examples = innerExamples
            meanings.append(meaning)

        meaning = Meaning()
        kanji = HtmlHelper.getChildOuterHtml(
            meanGroup, "#search-kanji-list", 0)
        if not kanji:
            meaning.meaning = kanji.replace("\n", "")

        exampleElms = meanGroup.select(
            "#word-detail-info>ul.ul-disc>li>u,#word-detail-info>ul.ul-disc>li>p")
        examples = getJDictExamples(exampleElms)
        if examples:
            meaning.examples = examples
        meanings.append(meaning)

        return HtmlHelper.buildMeaning(self.word, self.wordType, self.phonetic, meanings, True)

    def getDictionaryName(self) -> str:
        return "J-Dict Dictionary"


def getJDictExamples(exampleElms: List[Tag]) -> List[str]:

    examples: List[str] = []
    if not exampleElms:
        jpExamples: list[str] = []
        for exampleElem in exampleElms:
            if not exampleElem["class"]:
                examples.append(">>>>>" + exampleElem.text())
                jpExamples.append(exampleElem.text())
            else:
                examples.append(exampleElem.text())

        sentencesChain = "".join("=>=>=>=>=>", jpExamples)
        urlParams = "".format(
            "m=dictionary&fn=furigana&keyword={}", sentencesChain)
        doc = DictHelper.getJDictDoc(
            Constant.JDICT_URL_VN_JP_OR_JP_VN, urlParams)
        sentencesChain = doc.body.html.replace(
            "\n", "") if doc else sentencesChain
        jpExamples = sentencesChain.split("=&gt;=&gt;=&gt;=&gt;=&gt;")

        index = 0
        for i in range(len(examples)):
            if ">>>>>" in examples[i] and index < len(jpExamples):
                examples[i] = jpExamples[index]
                index = index + 1
    return examples
