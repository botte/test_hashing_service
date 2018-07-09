""" Functions for both conftest.py and the test files. """

import re
import hashlib
import base64
import os


def is_base64(password):
    if len(password) % 4 == 0 and re.search('^[A-Za-z0-9+\/=]+\Z', password):
        return(True)
    else:
        return(False)


def sha512(password):
    sha = hashlib.sha512(password)
    shadig = sha.digest()
    b64 = base64.b64encode(shadig)
    return(b64)
