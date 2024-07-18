#!/usr/bin/python


class Constant:
    """Store all constant values for AnkiFlash"""

    # ANKI
    ANKI_DECK = "anki_deck.csv"
    MAPPING_CSV = "mapping.csv"

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
