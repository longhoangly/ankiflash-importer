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


class LacVietDictionary(BaseDictionary):

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
        if translation.equals(Constant.VN_EN):
            url = HtmlHelper.lookupUrl(Constant.LACVIET_URL_VN_EN, self.wordId)
        elif (translation.equals(Constant.VN_FR)):
            url = HtmlHelper.lookupUrl(Constant.LACVIET_URL_VN_FR, self.wordId)
        elif (translation.equals(Constant.EN_VN)):
            url = HtmlHelper.lookupUrl(Constant.LACVIET_URL_EN_VN, self.wordId)
        elif (translation.equals(Constant.FR_VN)):
            url = HtmlHelper.lookupUrl(Constant.LACVIET_URL_FR_VN, self.wordId)

        self.doc = HtmlHelper.getDocument(url)

        return True if not self.doc else False

    def isInvalidWord(self) -> bool:
        """Check if the input word exists in dictionary?"""
        
        words = self.doc.select("div.w.fl")
        if not words:
            return True

        warning = HtmlHelper.getText(self.doc, "div.i.p10", 0)
        return Constant.LACVIET_SPELLING_WRONG in warning

    def getWordType(self) -> str:
        if not self.wordType:
            element = HtmlHelper.getElement(self.doc, "div.m5t.p10lr", 0)
            self.wordType = element.text.replace("|Tất cả", "").replace(
                "|Từ liên quan", "") if element else ""

            if not self.wordType:
                elements = HtmlHelper.getTexts(self.doc, "div.m5t.p10lr")
                self.wordType = "".join(" | ", elements) if len(
                    elements) > 0 else ""

            self.wordType = "(" + self.wordType + ")" if self.wordType else ""
        return self.wordType

    def getExample(self) -> str:
        examples = []
        for i in range(4):
            example: str = HtmlHelper.getText(self.doc, "div.e", i)
            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example:
                break
            else:
                self.word = self.word.lower()
                example = example.lower()
                if self.word in example:
                    example = example.replace(
                        self.word, "{{c1::" + self.word + "}}")
                else:
                    example = "{} {}".format(example, "{{c1::...}}")
                examples.append(example)

        return HtmlHelper.buildExample(examples)

    def getPhonetic(self) -> str:
        if not self.phonetic:
            self.phonetic = HtmlHelper.getText(self.doc, "div.p5l.fl.cB", 0)
        return self.phonetic

    def getImage(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        self.imageLink = ""
        self.image = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.word)
        return self.image

    def getSounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = HtmlHelper.getAttribute(
            self.doc, "embed", 0, "flashvars")

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

        self.soundLinks = self.soundLinks.replace(
            "file=", "").replace("&autostart=false", "")

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
        meanGroups = self.doc.select("div[id*=partofspeech]")

        for meanGroup in meanGroups:
            meanElms = meanGroup.select("div")
            meanCount = len(meanGroup.select(".m"))
            if str(Tag(meanGroup).get("id")).lower() == "partofspeech_100":
                meanElms.addAll(meanGroup.getElementsByTag("a"))

            meaning = Meaning()
            examples = []
            firstMeaning = True

            for meanElm in meanElms:
                if "ub" in meanElm["class"]:
                    if meanCount > 0:
                        # has meaning = > get text
                        meaning.setWordType(meanElm.text())
                    else:
                        # only type = > get inner html
                        meaning.setWordType(
                            meanElm.html().replaceAll("\n", ""))
                elif "m" in meanElm["class"]:
                    # from the second meaning tag
                    if not firstMeaning:
                        meaning.setExamples(examples)
                        meanings.add(meaning)
                        # reset value
                        meaning = Meaning()
                        examples = []

                    meaning.meaning = meanElm.text
                    firstMeaning = False
                elif "e" in meanElm["class"] or "em" in meanElm["class"] or "im" in meanElm["class"] or "id" in meanElm["class"] or "href" in meanElm["class"]:
                    examples.add(meanElm.text())

        self.meaning.examples = examples
        meanings.add(meaning)

        return HtmlHelper.buildMeaning(self.word, self.wordType, self.phonetic, meanings)

    def getDictionaryName(self) -> str:
        return "Lac Viet Dictionary"
