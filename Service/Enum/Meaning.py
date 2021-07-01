#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List


class Meaning:

    wordType: str
    meaning: str
    examples: List[str]

    def __init__(self, meaning=None, examples=None) -> None:
        self.meaning = meaning
        self.examples = examples
