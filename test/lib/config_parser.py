""" Get server executable location and PORT """

import os, ConfigParser


_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../config.ini')
_config = ConfigParser.ConfigParser()

def server():
    _config.read(_config_file)
    return _config.get('SERVER', 'server')

def port():
    _config.read(_config_file)
    return _config.get('PORT', 'port')
