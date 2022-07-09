import logging
import string
from service.helpers.ankiflash import AnkiHelper


class Note:

    data = {
        "keyMap": "",
        "field1": "field1Value" + AnkiHelper.id_generator(6, string.digits),
        "field2": "field2Value" + AnkiHelper.id_generator(6, string.digits),
        "field3": "field3Value" + AnkiHelper.id_generator(6, string.digits),
    }

    def __init__(self, word) -> None:
        super().__init__()
        self.data["keyMap"] = word

    def __getitem__(self, key):
        data = self.data[key]
        return data

    def __setitem__(self, key, updatedContent):
        self.data[key] = updatedContent
        logging.info("updated data {}".format(str(self.data)[0:50]))

    def flush(self):
        pass
