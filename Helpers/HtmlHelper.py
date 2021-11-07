#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List
import requests
import logging

from urllib.parse import unquote
from bs4 import BeautifulSoup
from bs4.element import Tag
from ..Service.Enum.Meaning import Meaning


class HtmlHelper:
    """All HTML related utilities methods"""

    @staticmethod
    def lookupUrl(dictUrl: str, word: str):
        word = word.replace(" ", "%20")
        return dictUrl.format(word)

    @staticmethod
    def urlDecode(url: str):
        try:
            return unquote(url)
        except:
            logging.info(
                "Exception occurred, cannot decode url: {}".format(url))
        return ""

    @staticmethod
    def getDocument(url: str) -> BeautifulSoup:
        logging.info("url {}".format(url))
        html_text = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0"}).text
        return BeautifulSoup(html_text, 'html.parser')

    @staticmethod
    def getDocElement(doc: BeautifulSoup, selector: str, index: int) -> Tag:
        elements = doc.select(selector)
        return elements[index] if len(elements) - index > 0 else None

    @staticmethod
    def getChildElement(element: Tag, selector: str, index: int) -> Tag:
        elements = element.select(selector)
        return elements[index] if len(elements) - index > 0 else None

    @staticmethod
    def getText(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.getDocElement(doc, selector, index)
        return element.get_text().strip() if element else ""

    @staticmethod
    def getTexts(doc: BeautifulSoup, selector: str, isUnique: bool = False) -> List[str]:
        elements = doc.select(selector)
        texts = []
        for element in elements:
            if not isUnique:
                texts.append(element.get_text().strip())
            elif element.get_text() not in texts:
                texts.append(element.get_text().strip())
        return texts

    @staticmethod
    def getElementInnerHtml(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.getDocElement(doc, selector, index)
        return element.decode_contents() if element else ""

    @staticmethod
    def getChildInnerHtml(element: Tag, selector: str, index: int) -> str:
        element = HtmlHelper.getChildElement(element, selector, index)
        return element.decode_contents() if element else ""

    @staticmethod
    def getElementOuterHtml(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.getDocElement(doc, selector, index)
        return str(element) if element else ""

    @staticmethod
    def getChildOuterHtml(element: Tag, selector: str, index: str) -> str:
        element = HtmlHelper.getChildElement(element, selector, index)
        return str(element) if element else ""

    @staticmethod
    def getAttribute(doc: BeautifulSoup, selector: str, index: int, attr: str) -> str:
        element = HtmlHelper.getDocElement(doc, selector, index)
        return element.get(attr) if element else ""

    @staticmethod
    def buildExample(examples: List[str], isJapanese: bool = False) -> str:
        str_list = []

        if (isJapanese):
            str_list.append("<div class=\"content-container japan-font\">")
        else:
            str_list.append("<div class=\"content-container\">")

        str_list.append("<ul class=\"content-circle\">")

        if (isJapanese):
            index = 0
            for example in examples:
                if index % 2 == 0:
                    str_list.append(
                        "<li class=\"content-example\">{}</li>".format(example.strip()))
                else:
                    str_list.append(
                        "<li class=\"content-sub-example\">{}</li>".format(example.strip()))
                index += 1
        else:
            for example in examples:
                str_list.append(
                    "<li class=\"content-example\">{}</li>".format(example.strip()))

        str_list.append("</ul>")
        str_list.append("</div>")

        return "".join(str_list)

    @staticmethod
    def buildMeaning(word: str, wordType: str, phonetic: str, meanings: List[Meaning], isJapanese: bool = False) -> str:

        str_list = []

        if (isJapanese):
            str_list.append("<div class=\"content-container japan-font\">")
        else:
            str_list.append("<div class=\"content-container\">")

        str_list.append("<h2 class=\"h\">{}</h2>".format(word.strip()))
        if wordType:
            str_list.append(
                "<span class=\"content-type\">{}</span>".format(wordType.strip()))

        if phonetic:
            str_list.append(
                "<span class=\"content-phonetic\">{}</span>".format(phonetic.strip()))

        str_list.append("<ul class=\"content-order\">")
        for mean in meanings:

            if mean.wordType:
                str_list.append(
                    "<h4 class=\"content-meaning-type\"'>{}</h4>".format(mean.wordType.strip()))
                str_list.append("</ul>")
                str_list.append("<ul class=\"content-order\">")

            if mean.meaning:
                str_list.append(
                    "<li class=\"content-meaning\">{}</li>".format(mean.meaning.strip()))

            if mean.subMeaning:
                str_list.append(
                    "<div class=\"content-sub-meaning\">{}</div>".format(mean.subMeaning.strip()))

            if "list" in str(type(mean.examples)) and len(mean.examples) > 0:
                str_list.append("<ul class=\"content-circle\">")

                if (isJapanese):
                    index = 0
                    for example in mean.examples:
                        if index % 2 == 0:
                            str_list.append(
                                "<li class=\"content-example\">{}</li>".format(example.strip()))
                        else:
                            str_list.append(
                                "<li class=\"content-sub-example\">{}</li>".format(example.strip()))
                        index += 1
                else:
                    for example in mean.examples:
                        str_list.append(
                            "<li class=\"content-example\">{}</li>".format(example.strip()))

                str_list.append("</ul>")

        str_list.append("</ul>")
        str_list.append("</div>")

        return "".join(str_list)
