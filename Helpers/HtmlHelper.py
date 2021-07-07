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
        return str(element.string) if element else ""

    @staticmethod
    def getTexts(doc: BeautifulSoup, selector: str) -> List[str]:
        elements = doc.select(selector)
        texts = []
        for element in elements:
            texts.append(str(element.string))
        return texts

    @staticmethod
    def getInnerHtml(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.getDocElement(doc, selector, index)
        return element.text if element else ""

    @staticmethod
    def getInnerHtml(element: Tag, selector: str, index: int) -> str:
        element = HtmlHelper.getChildElement(element, selector, index)
        return element.text if element else ""

    @staticmethod
    def getDocOuterHtml(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.getDocElement(doc, selector, index)
        return element.parent.text if element else ""

    @staticmethod
    def getChildOuterHtml(element: Tag, selector: str, index: str) -> str:
        element = HtmlHelper.getChildElement(element, selector, index)
        return element.parent.text if element else ""

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
        for example in examples:
            str_list.append(
                "<li class=\"content-example\">%s</li>".format(example))
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

        str_list.append("<h2 class=\"h\">%s</h2>".format(word))
        if wordType:
            str_list.append(
                "<span class=\"content-type\">%s</span>".format(wordType))

        if phonetic:
            str_list.append(
                "<span class=\"content-phonetic\">%s</span>".format(phonetic))

        str_list.append("<ol class=\"content-order\">")
        for meaning in meanings:
            if meaning.wordType:
                str_list.append(
                    "<h4 class=\"content-type\" style='margin-left: -20px;'>%s</h4>".format(meaning.wordType))

            if meaning.meaning:
                str_list.append(
                    "<li class=\"content-meaning\">%s</li>".format(meaning.meaning))

            if meaning.examples:
                str_list.append("<ul class=\"content-circle\">")
                for example in meaning.examples:
                    str_list.append(
                        "<li class=\"content-example\">%s</li>".format(example))
                str_list.append("</ul>")

        str_list.append("</ol>")
        str_list.append("</div>")

        return "".join(str_list)