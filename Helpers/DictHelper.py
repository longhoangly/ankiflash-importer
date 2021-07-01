#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import os

from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag

from ..Service.Constant import Constant
from .HtmlHelper import HtmlHelper


class DictHelper:
    """All Dictionary related utilities methods"""

    def getFileName(link: str) -> str:
        link_els = link.split("/")
        return link_els[len(link_els) - 1]

    def downloadFiles(ankiDir: str, urls: str):
        downloadLinks = urls.split(";")
        for link in downloadLinks:
            fileName = DictHelper.getFileName(link)
            filePath = "{}/{}".format(ankiDir, fileName)
            if os.path.isdir(ankiDir) and not link:
                r = requests.get(link, allow_redirects=True)
                open(filePath, 'wb').write(r.content)
            else:
                logging.warn("ankiDir={}, dir.exists={}, link={}".format(
                    ankiDir, os.path.isdir(ankiDir), link))

    def getJDictDoc(self, url: str, body: str):
        logging.info("url={}, body={}", url, body)
        html = requests.post(url, body)
        return BeautifulSoup(html.text, 'html.parser')

    def getJDictWords(self, word: str) -> List[str]:
        urlParameters = "m=dictionary&fn=search_word&keyword={}&allowSentenceAnalyze=true".format(
            word)
        document = self.getJDictDoc(
            Constant.JDICT_URL_VN_JP_OR_JP_VN, urlParameters)
        wordElms: List[Tag] = []
        if document:
            wordElms = document.select("ul>li")

        jDictWords = []
        for wordElm in wordElms:
            dataId = wordElm.find(attrs={"data-id": True})
            if word.lower() in str(wordElm.get("title")).lower() and not dataId:
                jDictWords.append(wordElm.get("title") + Constant.SUB_DELIMITER +
                                  dataId + Constant.SUB_DELIMITER + word)

        return jDictWords

    def getJishoWords(word: str) -> List[str]:

        url = HtmlHelper.lookupUrl(Constant.JISHO_SEARCH_URL_JP_EN, word)
        document: BeautifulSoup = HtmlHelper.getDocument(url)
        wordElms: List[Tag] = []
        if document:
            wordElms = document.select(".concept_light.clearfix")

        jDictWords: List[str] = []
        for wordElem in wordElms:
            foundWordElm: Tag = HtmlHelper.getChildElement(
                wordElem, ".concept_light-representation", 0)
            detailLink: Tag = HtmlHelper.getChildElement(
                wordElem, ".light-details_link", 0)

            if foundWordElm and word.lower() in foundWordElm.string.lower() and detailLink and not detailLink.text:
                detailLinkEls: list[str] = detailLink.attr("href").split("/")
                logging.debug("word = {}", word)
                logging.debug("foundWordElm.text() = {}", foundWordElm.text())
                logging.debug("detailLinkEls = {}",
                              "".join("---", detailLinkEls))
                jDictWords.append(foundWordElm.string
                                  + Constant.SUB_DELIMITER
                                  + HtmlHelper.urlDecode(detailLinkEls[detailLinkEls.length - 1])
                                  + Constant.SUB_DELIMITER
                                  + word)

        return jDictWords

    def getOxfordWords(self, word: str):
        foundWords: list[str] = []
        url = HtmlHelper.lookupUrl(Constant.OXFORD_SEARCH_URL_EN_EN, word)
        doc: BeautifulSoup = HtmlHelper.getDocument(url)

        if doc:
            firstLink: str = HtmlHelper.getAttribute(doc, "link", 0, "href")
            if "definition/english" in firstLink:
                matchedWord = HtmlHelper.getText(doc, ".headword", 0)
                if not matchedWord:
                    foundWords.append(
                        matchedWord
                        + Constant.SUB_DELIMITER
                        + DictHelper.getFileName(firstLink)
                        + Constant.SUB_DELIMITER
                        + word)

            allMatchesBlocks = doc.select("dl.accordion.ui-grad")
            for allMatches in allMatchesBlocks:
                lis = Tag(allMatches).select("li")
                for li in lis:
                    poss = Tag(li).find_all("pos")
                    for pos in poss:
                        Tag(pos).decompose()
                    for span in Tag(li).select("span"):
                        matchedWord = span.string
                        if matchedWord.lower() == word.lower():
                            wordId = DictHelper.getFileName(
                                Tag(li).select("a").attr("href"))
                            foundWords.append(
                                wordId + Constant.SUB_DELIMITER + wordId + Constant.SUB_DELIMITER + word)
        else:
            logging.info("Words not found: {}", self.word)

        return foundWords
