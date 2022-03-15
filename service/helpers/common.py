#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import socket
import time


def wait_until(condition, timeout, period=0.5, expected_value=True):
    mustend = time.time() + timeout
    while time.time() < mustend:
        logging.info("Checking time={}, condition={}".format(
            time.time(), condition))
        if condition == expected_value:
            return True
        time.sleep(period)
    return False


def is_port_free(host, port) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        indicator = s.connect_ex((host, port))
        s.close()

        if indicator == 0:
            logging.info("Port {} is open (in-used port) !!!".format(port))
            return False
        else:
            logging.info("Port {} is closed (free port) !!!".format(port))
            return True

    except socket.gaierror:
        logging.info("Hostname Could Not Be Resolved !!!")
    except socket.error:
        logging.info("Host not responding !!!")
