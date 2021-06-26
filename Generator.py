#!/usr/bin/python
# -*- coding: utf-8 -*-

from aqt.utils import showInfo

from PyQt5 import QtWidgets

import os
import csv
csv.field_size_limit(2**30)


class Generator:

    def flashcards(self, words):

        showInfo("To Be Continue...\n" + "\n".join(map(str, words)))
