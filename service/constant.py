#!/usr/bin/python

from .enum.translation import Translation


class Constant:
    """Store all constant values for AnkiFlash"""

    # ANKI
    ANKI_DECK = "anki_deck.csv"
    MAPPING_CSV = "mapping.csv"

    # OXFORD
    OXFORD_SPELLING_WRONG = "Did you spell it correctly?"
    OXFORD_WORD_NOT_FOUND = "Oxford Learner's Dictionaries | Find the meanings"
    OXFORD_DETAILS_URL = (
        "https://www.oxfordlearnersdictionaries.com/definition/english/{}"
    )
    OXFORD_SEARCH_URL_EN_EN = (
        "https://www.oxfordlearnersdictionaries.com/search/english/direct/?q={}"
    )

    # LACVIET
    LACVIET_SPELLING_WRONG = "Dữ liệu đang được cập nhật"
    LACVIET_BASE_URL = "https://tratu.coviet.vn"
    LACVIET_SEARCH_URL = "https://tratu.coviet.vn/ajax/TraTu.Util.AjaxFunction,App_Code.ashx?_method=GetComplete&_session=no"

    # CAMBRIDGE
    CAMBRIDGE_SPELLING_WRONG = "Did you spell it correctly?"
    CAMBRIDGE_URL_EN_CN_TD = "https://dictionary.cambridge.org/search/english-chinese-traditional/direct/?q={}"
    CAMBRIDGE_URL_EN_CN_SP = "https://dictionary.cambridge.org/search/english-chinese-simplified/direct/?q={}"
    CAMBRIDGE_URL_EN_FR = (
        "https://dictionary.cambridge.org/search/english-french/direct/?q={}"
    )
    CAMBRIDGE_URL_EN_JP = (
        "https://dictionary.cambridge.org/search/english-japanese/direct/?q={}"
    )

    # COLLINS
    COLLINS_SPELLING_WRONG = "Sorry, no results for"
    COLLINS_URL_FR_EN = (
        "https://www.collinsdictionary.com/search/?dictCode=french-english&q={}"
    )

    # KANTAN
    KANTAN_URL_VN_JP_OR_JP_VN = "https://kantan.vn/postrequest.ashx"

    # WIKI
    WIKI_BASE_URL = "https:"
    WIKI_SEARCH_WORD_URL = (
        "https://vi.wiktionary.org/w/rest.php/v1/search/title?q={}&limit=5"
    )
    WIKI_DETAILS_URL = "https://vi.wiktionary.org/w/index.php"
    WIKI_SPELLING_WRONG = "Chưa có trang nào có tên"

    # JISHO
    JISHO_WORD_NOT_FOUND = "Sorry, couldn't find anything matching"
    JISHO_WORD_URL_JP_EN = "https://jisho.org/word/{}"
    JISHO_SEARCH_URL_JP_EN = "https://jisho.org/search/{}"

    # CONSTANTS
    TAB = "\t"
    MAIN_DELIMITER = "\\*\\*\\*"
    SUB_DELIMITER = "==="
    NO_EXAMPLE = "No example {{c1::...}}"
    SUCCESS = "Success"
    COPYRIGHT = "This card's content is collected from the following dictionaries: {}"
    WORD_NOT_FOUND = "Word not found. Could you please check spelling by using the dictionary or feedback to us!"
    CONNECTION_FAILED = "Cannot connect to dictionaries, please try again later!"
    NOT_SUPPORTED_TRANSLATION = "The translation from {} to {} is not supported!"

    # LANGUAGES
    ENGLISH = "English"
    FRENCH = "French"
    VIETNAMESE = "Vietnamese"
    VIETNAMESE_WIKI = "Vietnamese (Wiktionary)"
    CHINESE = "Chinese"
    CHINESE_TD = "Chinese (Traditional)"
    CHINESE_SP = "Chinese (Simplified)"
    JAPANESE = "Japanese"
    SPANISH = "Spanish"

    # TRANSLATION
    EN_EN = Translation(ENGLISH, ENGLISH)
    EN_VN = Translation(ENGLISH, VIETNAMESE)
    EN_CN_TD = Translation(ENGLISH, CHINESE_TD)
    EN_CN_SP = Translation(ENGLISH, CHINESE_SP)
    EN_FR = Translation(ENGLISH, FRENCH)
    EN_JP = Translation(ENGLISH, JAPANESE)

    VN_EN = Translation(VIETNAMESE, ENGLISH)
    VN_FR = Translation(VIETNAMESE, FRENCH)
    VN_JP = Translation(VIETNAMESE, JAPANESE)
    VN_VN = Translation(VIETNAMESE, VIETNAMESE)
    VN_VN_WIKI = Translation(VIETNAMESE, VIETNAMESE_WIKI)

    FR_VN = Translation(FRENCH, VIETNAMESE)
    FR_EN = Translation(FRENCH, ENGLISH)

    JP_EN = Translation(JAPANESE, ENGLISH)
    JP_VN = Translation(JAPANESE, VIETNAMESE)

    # AnkiFlash fields for mapping content
    ANKI_FLASH_FIELDS = [
        "Word",
        "WordType",
        "Phonetic",
        "Example",
        "Sound",
        "Image",
        "Meaning",
        "Copyright",
    ]

    # All supported languages
    SUPPORTED_TRANSLATIONS = {
        ENGLISH: [ENGLISH, VIETNAMESE, CHINESE_TD, CHINESE_SP, FRENCH, JAPANESE],
        VIETNAMESE: [VIETNAMESE_WIKI, ENGLISH, FRENCH, JAPANESE, VIETNAMESE],
        FRENCH: [ENGLISH, VIETNAMESE],
        JAPANESE: [ENGLISH, VIETNAMESE],
    }
