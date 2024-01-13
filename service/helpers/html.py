#!/usr/bin/python

import time
import requests
import logging
import webbrowser

from typing import List
from bs4.element import Tag
from bs4 import BeautifulSoup
from urllib.parse import unquote

from ..enum.meaning import Meaning
from .server import start_server

PORT = 8081
HOST = "localhost"
BASE_URL = "http://{}:{}".format(HOST, PORT)
AGENT_STRING = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"


class HtmlHelper:
    """All HTML related utilities methods"""

    @staticmethod
    def lookup_url(dictUrl: str, word: str):
        word = word.replace(" ", "%20")
        return dictUrl.format(word)

    @staticmethod
    def url_decode(url: str):
        try:
            return unquote(url)
        except:
            logging.info("Exception occurred, cannot decode url: {}".format(url))
        return ""

    @staticmethod
    def convert_html_to_soup(docStr: str) -> BeautifulSoup:
        return BeautifulSoup(docStr, "html.parser")

    @staticmethod
    def get_document(url: str) -> BeautifulSoup:
        logging.info("url {}".format(url))
        html_text = requests.get(url, headers={"User-Agent": AGENT_STRING}).text

        return BeautifulSoup(html_text, "html.parser")

    @staticmethod
    def get_collins_document(url: str) -> BeautifulSoup:
        logging.info("url={}".format(url))

        start_server()

        logging.info("Open web browser to get word content")
        webbrowser.open(url)

        html_text = None
        for count in range(20):
            logging.info("count={}".format(count))

            html_text = requests.get(
                "{}/api/v1/getrecord/word_content".format(BASE_URL),
                headers={"User-Agent": AGENT_STRING},
            ).text

            if html_text:
                logging.info("html_text={}".format(html_text[0:100]))
                html_text = unquote(html_text)
                break

            count += 1
            time.sleep(1)

        logging.info("html_text={}".format(html_text[0:100]))
        html_text = unquote(html_text)

        requests.get(
            "{}/api/v1/shutdown".format(BASE_URL), headers={"User-Agent": AGENT_STRING}
        )

        return BeautifulSoup(html_text, "html.parser")

    @staticmethod
    def get_doc_element(doc: BeautifulSoup, selector: str, index: int) -> Tag:
        elements = doc.select(selector)
        return elements[index] if len(elements) - index > 0 else None

    @staticmethod
    def get_child_element(element: Tag, selector: str, index: int) -> Tag:
        elements = element.select(selector)
        return elements[index] if len(elements) - index > 0 else None

    @staticmethod
    def get_text(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.get_doc_element(doc, selector, index)
        return element.get_text().strip() if element else ""

    @staticmethod
    def get_texts(
        doc: BeautifulSoup, selector: str, isUnique: bool = False
    ) -> List[str]:
        elements = doc.select(selector)
        texts = []
        for element in elements:
            if not isUnique:
                texts.append(element.get_text().strip())
            elif element.get_text() not in texts:
                texts.append(element.get_text().strip())
        return texts

    @staticmethod
    def get_element_inner_html(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.get_doc_element(doc, selector, index)
        return element.decode_contents() if element else ""

    @staticmethod
    def get_child_inner_html(element: Tag, selector: str, index: int) -> str:
        element = HtmlHelper.get_child_element(element, selector, index)
        return element.decode_contents() if element else ""

    @staticmethod
    def get_element_outer_html(doc: BeautifulSoup, selector: str, index: int) -> str:
        element = HtmlHelper.get_doc_element(doc, selector, index)
        return str(element) if element else ""

    @staticmethod
    def get_child_outer_html(element: Tag, selector: str, index: str) -> str:
        element = HtmlHelper.get_child_element(element, selector, index)
        return str(element) if element else ""

    @staticmethod
    def get_attribute(doc: BeautifulSoup, selector: str, index: int, attr: str) -> str:
        element = HtmlHelper.get_doc_element(doc, selector, index)
        return element.get(attr) if element else ""

    @staticmethod
    def build_example(examples: List[str], isJapanese: bool = False) -> str:
        str_list = []

        if isJapanese:
            str_list.append('<div class="content-container japan-font">')
        else:
            str_list.append('<div class="content-container">')

        str_list.append('<ul class="content-circle">')

        if isJapanese:
            index = 0
            for example in examples:
                if index % 2 == 0:
                    str_list.append(
                        '<li class="content-example">{}</li>'.format(example.strip())
                    )
                else:
                    str_list.append(
                        '<li class="content-sub-example">{}</li>'.format(
                            example.strip()
                        )
                    )
                index += 1
        else:
            for example in examples:
                str_list.append(
                    '<li class="content-example">{}</li>'.format(example.strip())
                )

        str_list.append("</ul>")
        str_list.append("</div>")

        return "".join(str_list)

    @staticmethod
    def build_meaning(
        word: str,
        wordType: str,
        phonetic: str,
        meanings: List[Meaning],
        isJapanese: bool = False,
    ) -> str:
        str_list = []

        if isJapanese:
            str_list.append('<div class="content-container japan-font">')
        else:
            str_list.append('<div class="content-container">')

        str_list.append('<h2 class="h">{}</h2>'.format(word.strip()))
        if wordType:
            str_list.append(
                '<span class="content-type">{}</span>'.format(wordType.strip())
            )

        if phonetic:
            str_list.append(
                '<span class="content-phonetic">{}</span>'.format(phonetic.strip())
            )

        str_list.append('<ul class="content-order">')
        for mean in meanings:
            if mean.wordType:
                str_list.append(
                    '<h4 class="content-meaning-type"\'>{}</h4>'.format(
                        mean.wordType.strip()
                    )
                )
                str_list.append("</ul>")
                str_list.append('<ul class="content-order">')

            if mean.meaning:
                str_list.append(
                    '<li class="content-meaning">{}</li>'.format(mean.meaning.strip())
                )

            if mean.subMeaning:
                str_list.append(
                    '<div class="content-sub-meaning">{}</div>'.format(
                        mean.subMeaning.strip()
                    )
                )

            if "list" in str(type(mean.examples)) and len(mean.examples) > 0:
                str_list.append('<ul class="content-circle">')

                if isJapanese:
                    index = 0
                    for example in mean.examples:
                        if index % 2 == 0:
                            str_list.append(
                                '<li class="content-example">{}</li>'.format(
                                    example.strip()
                                )
                            )
                        else:
                            str_list.append(
                                '<li class="content-sub-example">{}</li>'.format(
                                    example.strip()
                                )
                            )
                        index += 1
                else:
                    for example in mean.examples:
                        str_list.append(
                            '<li class="content-example">{}</li>'.format(
                                example.strip()
                            )
                        )

                str_list.append("</ul>")

        str_list.append("</ul>")
        str_list.append("</div>")

        return "".join(str_list)
