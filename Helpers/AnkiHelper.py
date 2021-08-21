#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import random


class AnkiHelper:
    """All Dictionary related utilities methods"""

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
