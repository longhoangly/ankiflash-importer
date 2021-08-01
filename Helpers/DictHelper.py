#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import logging
import os

from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag

from ..Service.Constant import Constant
from .HtmlHelper import HtmlHelper


class DictHelper:
    """All Dictionary related utilities methods"""

    @staticmethod
    def getFileName(link: str) -> str:
        link_els = link.split("/")
        return link_els[len(link_els) - 1]

    @staticmethod
    def downloadFiles(mediaDir: str, urls: str):
        downloadLinks = urls.split(";")
        for link in downloadLinks:
            fileName = DictHelper.getFileName(link)
            filePath = "{}/{}".format(mediaDir, fileName)
            logging.info("sound path: {}".format(filePath))
            if os.path.isdir(mediaDir) and link:
                r = requests.get(url=link, headers={
                                 "User-Agent": "Mozilla/5.0"}, allow_redirects=True)
                open(filePath, 'wb').write(r.content)
            else:
                logging.info("mediaDir={}, dir.exists={}, link={}".format(
                    mediaDir, os.path.isdir(mediaDir), link))

    @staticmethod
    def getJDictDoc(url: str, body: str):
        logging.info("url={}, body={}".format(url, body).encode("utf-8"))
        html = requests.post(url=url, data=body, headers={
                             "User-Agent": "Mozilla/5.0"})
        return BeautifulSoup(html.text, 'html.parser')

    @staticmethod
    def getJDictWords(word: str) -> List[str]:
        urlParameters = "m=dictionary&fn=search_word&keyword={}&allowSentenceAnalyze=true".format(
            word)
        document = DictHelper.getJDictDoc(
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

    @staticmethod
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

            if foundWordElm and word.lower() in foundWordElm.get_text().strip().lower() and detailLink and not detailLink.text:
                detailLinkEls: list[str] = detailLink.attr("href").split("/")
                jDictWords.append(foundWordElm.get_text().strip()
                                  + Constant.SUB_DELIMITER
                                  + HtmlHelper.urlDecode(detailLinkEls[detailLinkEls.length - 1])
                                  + Constant.SUB_DELIMITER
                                  + word)

        logging.info("jDictWords = {}".format("".join("---", jDictWords)))

        return jDictWords

    @staticmethod
    def getOxfordWords(word: str):
        foundWords: list[str] = []
        url = HtmlHelper.lookupUrl(Constant.OXFORD_SEARCH_URL_EN_EN, word)
        doc: BeautifulSoup = HtmlHelper.getDocument(url)

        if doc:
            firstLink: str = HtmlHelper.getAttribute(doc, "link", 0, "href")
            if "definition/english" in firstLink:
                matchedWord = HtmlHelper.getText(doc, ".headword", 0)
                if matchedWord:
                    foundWords.append(
                        matchedWord
                        + Constant.SUB_DELIMITER
                        + DictHelper.getFileName(firstLink)
                        + Constant.SUB_DELIMITER
                        + word)

            allMatchesBlocks = doc.select("dl.accordion.ui-grad")
            for allMatches in allMatchesBlocks:
                lis = allMatches.select("li")
                for li in lis:
                    poss = li.find_all("pos")
                    for pos in poss:
                        pos.decompose()
                    for span in li.select("span"):
                        if span.get_text().strip().lower() == word.lower():
                            wordId = DictHelper.getFileName(
                                li.select_one("a").get("href"))
                            foundWords.append(
                                wordId + Constant.SUB_DELIMITER + wordId + Constant.SUB_DELIMITER + word)
        else:
            logging.info("Words not found: {}".format(word))

        logging.info("foundWords: {}".format(foundWords))
        return foundWords
