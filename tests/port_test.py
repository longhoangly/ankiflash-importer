#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import unittest
import requests
import logging

from service.helpers.common import wait_until
from service.helpers.simple_server import start_server, is_port_free
from tests.shared import CommonTest

PORT = 8081
HOST = "localhost"
BASE_URL = "http://{}:{}".format(HOST, PORT)
AGENT_STRING = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"


def getting_document_mock():

    logging.info("port is free at starting point")
    assert is_port_free(HOST, PORT)

    logging.info("starting server")
    start_server()
    wait_until(not is_port_free(HOST, PORT), 10)

    logging.info("validate that server is started")
    assert not is_port_free(HOST, PORT)

    logging.info("try to get content from server")
    for count in range(2):
        requests.get(
            "{}/api/v1/getrecord/word_content".format(BASE_URL),
            headers={
                "User-Agent": AGENT_STRING
            })

    logging.info("request to shutdown server")
    requests.get(
        "{}/api/v1/shutdown".format(BASE_URL),
        headers={
            "User-Agent": AGENT_STRING
        })
    wait_until(is_port_free(HOST, PORT), 10)

    logging.info("check if port released / server stopped")
    assert is_port_free(HOST, PORT)


class HelperTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.addonDir = "./tests"
        self.mediaDir = "./tests/media"
        self.commontest = CommonTest(self.addonDir, self.mediaDir)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def test_port_in_used(self):
        getting_document_mock()
        getting_document_mock()
        getting_document_mock()

    def test_port_is_free(self):
        assert is_port_free(HOST, PORT)


if __name__ == '__main__':
    unittest.main(verbosity=2)
