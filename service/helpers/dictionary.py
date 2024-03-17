#!/usr/bin/python

import os
import logging
import requests
import urllib.parse

from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag

from ..constant import Constant
from .ankiflash import AnkiHelper
from .html import HtmlHelper


class DictHelper:
    """All Dictionary related utilities methods"""

    @staticmethod
    def get_last_url_segment(link: str) -> str:
        link_els = link.split("/")
        return link_els[len(link_els) - 1]

    @staticmethod
    def download_files(urls: str, isOnline: bool, mediaDir: str) -> List[str]:
        validUrls = []
        for link in urls.split(";"):
            response = requests.get(
                url=link, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True
            )
            statusCode = response.status_code
            if statusCode == 200:
                validUrls.append(link)
                if not isOnline:
                    fileName = DictHelper.get_last_url_segment(link)
                    filePath = "{}/{}".format(mediaDir, fileName)
                    logging.info("file path: {}".format(filePath))
                    if os.path.isdir(mediaDir) and link:
                        tw = open(filePath, "wb")
                        tw.write(response.content)
                        tw.close()
                    else:
                        logging.info(
                            "mediaDir={}, dir.exists={}, link={}".format(
                                mediaDir, os.path.isdir(mediaDir), link
                            )
                        )
        return validUrls

    @staticmethod
    def get_kantan_doc(url: str, body: str):

        logging.info("url={}, body={}".format(url, body.encode("utf-8")))
        response = requests.post(
            url=url,
            data=body.encode("utf-8"),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
        )

        resp = response.json()
        content = resp["Content"].replace("\n", " ").replace("\r", " ")
        logging.info("JP document {}".format(content))

        return BeautifulSoup(content, "html.parser")

    @staticmethod
    def get_kantan_words(word: str, allWordTypes: bool) -> List[str]:

        search_word = urllib.parse.quote(word)
        urlParameters = (
            "m=dictionary&fn=search_word&keyword={}&allowSentenceAnalyze=true".format(
                search_word
            )
        )
        document = DictHelper.get_kantan_doc(
            Constant.KANTAN_URL_VN_JP_OR_JP_VN, urlParameters
        )
        wordElms: List[Tag] = []
        if document:
            wordElms = document.select("ul>li")

        kantanWords = []
        for wordElm in wordElms:
            dataId = wordElm.get("data-id")

            if word.lower() in wordElm.get("title").lower() and dataId:
                kantanWords.append(
                    wordElm.get("title")
                    + Constant.SUB_DELIMITER
                    + dataId
                    + Constant.SUB_DELIMITER
                    + word
                )

        logging.info("JP kantanWords {}".format(kantanWords))
        return kantanWords if allWordTypes else [kantanWords[0]]

    @staticmethod
    def get_jisho_words(word: str) -> List[str]:

        url = HtmlHelper.lookup_url(Constant.JISHO_SEARCH_URL_JP_EN, word)
        document: BeautifulSoup = HtmlHelper.get_document(url)
        wordElms: List[Tag] = []
        if document:
            wordElms = document.select(".concept_light.clearfix")

        jishoWords: List[str] = []
        for wordElem in wordElms:
            foundWordElm: Tag = HtmlHelper.get_child_element(
                wordElem, ".concept_light-representation", 0
            )
            detailLink: Tag = HtmlHelper.get_child_element(
                wordElem, ".light-details_link", 0
            )

            if (
                foundWordElm
                and word.lower() in foundWordElm.get_text().strip().lower()
                and detailLink
                and detailLink.get_text()
            ):
                detailLinkEls: list[str] = detailLink.get("href").split("/")
                jishoWords.append(
                    AnkiHelper.stringify(
                        foundWordElm.get_text().replace("\n", " ").strip()
                    )
                    + Constant.SUB_DELIMITER
                    + HtmlHelper.url_decode(
                        detailLinkEls[len(detailLinkEls) - 1]
                    ).strip()
                    + Constant.SUB_DELIMITER
                    + word
                )

        logging.info("jishoWords = {}".format("---".join(jishoWords)))
        return jishoWords

    @staticmethod
    def get_oxford_words(word: str):

        foundWords: list[str] = []
        url = HtmlHelper.lookup_url(Constant.OXFORD_SEARCH_URL_EN_EN, word)
        doc: BeautifulSoup = HtmlHelper.get_document(url)

        if doc:
            firstLink: str = HtmlHelper.get_attribute(doc, "link", 0, "href")
            if "definition/english" in firstLink:
                matchedWord = HtmlHelper.get_text(doc, ".headword", 0)
                if matchedWord:
                    foundWords.append(
                        matchedWord
                        + Constant.SUB_DELIMITER
                        + DictHelper.get_last_url_segment(firstLink)
                        + Constant.SUB_DELIMITER
                        + word
                    )

            allMatchesBlocks = doc.select("dl.accordion.ui-grad")
            for allMatches in allMatchesBlocks:
                lis = allMatches.select("li")
                for li in lis:
                    poss = li.find_all("pos")
                    for pos in poss:
                        # remove the whole pos tag
                        pos.decompose()
                    for span in li.select("span"):
                        if span.get_text().strip().lower() == word.lower():
                            wordId = DictHelper.get_last_url_segment(
                                li.select_one("a").get("href")
                            )
                            foundWords.append(
                                wordId
                                + Constant.SUB_DELIMITER
                                + wordId
                                + Constant.SUB_DELIMITER
                                + word
                            )
        else:
            logging.info("Words not found: {}".format(word))

        logging.info("foundWords: {}".format(foundWords))
        return foundWords

    @staticmethod
    def get_wiki_words(word: str, allWordTypes: bool):

        foundWords: list[str] = []
        url = HtmlHelper.lookup_url(Constant.WIKI_SEARCH_WORD_URL, word)

        response = requests.get(
            url=url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json; charset=UTF-8",
            },
        )

        resp = response.json()
        if resp["pages"]:
            for wordDict in resp["pages"]:
                foundWords.append(
                    wordDict["key"]
                    + Constant.SUB_DELIMITER
                    + wordDict["key"]
                    + Constant.SUB_DELIMITER
                    + word
                )
        else:
            logging.info("Word not found: {}".format(word))

        logging.info("foundWords: {}".format(foundWords))
        return foundWords if allWordTypes else [foundWords[0]]
