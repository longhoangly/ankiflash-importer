#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

import logging
import requests

from urllib.parse import unquote
from bs4 import BeautifulSoup
from bs4.element import Tag
from ..Service.Enum.Meaning import Meaning


class HtmlHelper:
    """All HTML related utilities methods"""

    def lookupUrl(self, dictUrl: str, word: str):
        word = word.replace(" ", "%20")
        return dictUrl.format(word)

    def urlDecode(self, url: str):
        try:
            return unquote(url)
        except:
            logging.info(
                "Exception occurred, cannot decode url: {}".format(url))
        return ""

    def getDocument(self, url: str) -> BeautifulSoup:
        html_text = requests.get(url).text
        return BeautifulSoup(html_text, 'html.parser')

    def getDocElement(self, doc: BeautifulSoup, selector: str, index: int) -> Tag:
        elements = doc.select(selector)
        return elements[index] if len(elements) - index > 0 else None

    def getChildElement(self, element: Tag, selector: str, index: int) -> Tag:
        elements = element.select(selector)
        return elements[index] if len(elements) - index > 0 else None

    def getText(self, doc: BeautifulSoup, selector: str, index: int) -> str:
        element = self.getDocElement(doc, selector, index)
        return str(element.string) if element else ""

    def getTexts(self, doc: BeautifulSoup, selector: str) -> List[str]:
        elements = doc.select(selector)
        texts = []
        for element in elements:
            texts.append(str(Tag(element).string))
        return texts

    def getInnerHtml(self, doc: BeautifulSoup, selector: str, index: int) -> str:
        element = self.getDocElement(doc, selector, index)
        return element.text if element else ""

    def getInnerHtml(self, element: Tag, selector: str, index: int) -> str:
        element = self.getChildElement(element, selector, index)
        return element.text if element else ""

    def getDocOuterHtml(self, doc: BeautifulSoup, selector: str, index: int) -> str:
        element = self.getDocElement(doc, selector, index)
        return Tag(element.parent).text if element else ""

    def getChildOuterHtml(self, element: Tag, selector: str, index: str) -> str:
        element = self.getChildElement(element, selector, index)
        return Tag(element.parent).text if element else ""

    def getAttribute(self, doc: BeautifulSoup, selector: str, index: int, attr: str) -> str:
        element = self.getDocElement(doc, selector, index)
        return Tag(element).find({attr: True}) if element else ""

    def buildExample(self, examples: list[str], isJapanese: bool = False) -> str:
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

    def buildMeaning(self, word: str, wordType: str, phonetic: str, meanings: list[Meaning], isJapanese: bool = False) -> str:
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
