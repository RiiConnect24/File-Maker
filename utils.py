import logging
import os
import requests
import struct

from datadog import statsd
from raven import Client
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

from Channels.Forecast_Channel.config import production # We only need to read the production variable at this time.

"""Unification of utilities used by all scripts."""

requests.packages.urllib3.disable_warnings()  # This is so we don't get some warning about SSL.

errors = 0

if production:
    client = Client(sentry_url)
    handler = SentryHandler(client)
    setup_logging(handler)
    logger = logging.getLogger(__name__)


def log(msg, level):  # TODO: Use number levels, strings are annoying
    global errors

    if level is not "VERBOSE" and level is not "INFO":
        errors += 1

    print msg

    if production:
        if level is "VERBOSE":
            logger.debug(msg)
        elif level is "INFO":
            logger.info(msg)
        elif level is "WARNING":
            logger.warning(msg)
        elif level is "CRITICAL":
            logger.error(msg)

# http://stackoverflow.com/a/600612/3874884
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
    else:
        return


"""Pack integers to specific type."""


# Unsigned integers


def u8(data):
    if data < 0 or data > 255:
        log("u8 out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack(">B", data)


def u16(data):
    if data < 0 or data > 65535:
        log("u16 out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack(">H", data)


def u32(data):
    if data < 0 or data > 4294967295:
        log("u32 out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack(">I", data)


def u32_littleendian(data):
    if data < 0 or data > 4294967295:
        log("u32 little endian out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack("<I", data)


# Signed integers


def s8(data):
    if data < -128 or data > 128:
        log("s8 out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack(">b", data)


def s16(data):
    if data < -32768 or data > 32768:
        log("s16 out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack(">h", data)


def s32(data):
    if data < -2147483648 or data > 2147483648:
        log("s32 out of range: %s" % data, "CRITICAL")
        data = 0
    return struct.pack(">i", data)

