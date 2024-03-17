#!/usr/bin/python

import requests
import logging

from typing import List


from ..constant import Constant
from ..enum.meaning import Meaning
from ..enum.translation import Translation
from ..helpers.html import HtmlHelper
from ..helpers.dictionary import DictHelper
from ..base_dictionary import BaseDictionary
from ..helpers.ankiflash import AnkiHelper


class Wiktionary(BaseDictionary):
    def search(self, formattedWord: str, translation: Translation) -> bool:
        """Find input word from dictionary data"""

        if not translation.equals(Constant.VN_VN_WIKI):
            return True

        wordParts = formattedWord.split(Constant.SUB_DELIMITER)
        if Constant.SUB_DELIMITER in formattedWord and len(wordParts) == 3:
            self.word = wordParts[0]
            self.wordId = wordParts[1]
            self.oriWord = wordParts[2]
        else:
            raise RuntimeError("Incorrect word format: {}".format(formattedWord))

        payload = {
            "search": self.wordId.encode("utf-8"),
            "title": "Đặc_biệt:Tìm_kiếm".encode("utf-8"),
            "ns0": 1,
        }

        response = requests.get(
            Constant.WIKI_DETAILS_URL,
            params=payload,
            headers={"Content-Type": "text/plain;charset=UTF-8"},
        )

        self.doc = HtmlHelper.convert_html_to_soup(response.text)
        return True if not self.doc else False

    def is_invalid_word(self) -> bool:
        """Check if the input word exists in dictionary?"""

        words = self.doc.select("#firstHeading")
        if not words:
            return True
        self.word = words[0].get_text()

        warning = HtmlHelper.get_text(self.doc, "td.mbox-text", 0)
        return Constant.WIKI_SPELLING_WRONG in warning

    def get_word_type(self) -> str:
        if not self.wordType:
            elements = HtmlHelper.get_texts(self.doc, "span.mw-headline")
            elements = list(filter(lambda txt: "từ" in txt, elements))
            self.wordType = " | ".join(elements) if len(elements) > 0 else ""
            self.wordType = "(" + self.wordType + ")" if self.wordType else ""

        return self.wordType

    def get_example(self) -> str:
        examples = []
        for i in range(4):
            example: str = (
                HtmlHelper.get_element_outer_html(self.doc, "li>dl>dd", i)
                .replace("\n", "")
                .strip()
            )

            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example:
                break
            else:
                self.word = self.word.lower()
                example = example.lower()
                if self.word in example:
                    example = example.replace(self.word, "{{c1::" + self.word + "}}")
                else:
                    example = "{} {}".format(example, "{{c1::...}}")
                examples.append(example)

        return HtmlHelper.build_example(examples)

    def get_phonetic(self) -> str:
        if not self.phonetic:
            elements = HtmlHelper.get_texts(self.doc, "span.IPA", True)
            self.phonetic = (
                "[ " + " | ".join(elements) + " ]" if len(elements) > 0 else ""
            )
        return self.phonetic

    def get_image(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        googleImage = '<a href="https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}" style="font-size: 15px; color: blue">Search images by the word</a>'.format(
            self.oriWord
        )

        self.imageLink = HtmlHelper.get_attribute(
            self.doc, "img.mw-file-element", 0, "src"
        )
        if not self.imageLink or "logo" in self.imageLink:
            self.imageLink = HtmlHelper.get_attribute(
                self.doc, "img.mw-file-element", 1, "src"
            )

        if not self.imageLink:
            self.image = googleImage
            return self.image

        self.imageLink = Constant.WIKI_BASE_URL + self.imageLink

        imageName = DictHelper.get_last_url_segment(self.imageLink)
        if isOnline:
            self.image = '<img src="' + self.imageLink + '"/>'
        else:
            self.image = '<img src="' + imageName + '"/>'
            DictHelper.download_files(self.imageLink, False, ankiDir)
        return self.image

    def get_sounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = ""

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

    def get_meaning(self) -> str:
        self.get_word_type()
        self.get_phonetic()

        meanings: List[Meaning] = []
        meanGroup = HtmlHelper.get_doc_element(self.doc, "div.mw-body-content", 0)
        if meanGroup:
            meaning: Meaning
            meanElms = meanGroup.select("span.mw-headline,ol>li")

            wordTypes = []
            for meanElm in meanElms:
                # Word type
                if meanElm.name == "span" and "từ" in meanElm.get_text():
                    meaning = Meaning()
                    meaning.wordType = meanElm.get_text().replace("\n", "").capitalize()

                    if meaning.wordType not in wordTypes:
                        wordTypes.append(meaning.wordType)
                        meanings.append(meaning)

                # Meaning
                if meanElm.name == "li":
                    meaning = Meaning()
                    meaning.meaning = meanElm.get_text().replace("\n", "").strip()
                    meanings.append(meaning)

        return HtmlHelper.build_meaning(
            self.word, self.wordType, self.phonetic, meanings
        )

    def get_dictionary_name(self) -> str:
        return "Wiktionary"
