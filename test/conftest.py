""" Test Fixtures for use by any tests. """

import pytest
import subprocess
import requests
import pickledb
import os, random, time, string
from test.lib import lib, config_parser


_headers = {'Content-Type':'application/json'}


@pytest.fixture(scope='session', autouse=True)
def set_env():
    os.putenv('PORT', config_parser.port())


@pytest.fixture(scope='module', autouse=True)
def start_server():
    proc = subprocess.Popen(config_parser.server())
    time.sleep(4)
    yield proc.pid
    proc.kill()
   

@pytest.fixture(scope='function')
def start_server_manual():
    proc = subprocess.Popen(config_parser.server())
    time.sleep(4)
    yield proc.pid
    proc.kill()


@pytest.fixture(scope='session')
def db():
    db = pickledb.load('requests.db', False)
    db.set('key', 0)
    return db


@pytest.fixture(scope='module')
def calls(db):
    def call():
        count = db.get('key')
        db.set('key', count + 1)
    return call


@pytest.fixture(scope='module')
def get_calls(db):
    def call():
        return db.get('key')
    return call


@pytest.fixture(scope='session')
def baseurl():
    return 'http://localhost:' + config_parser.port()


@pytest.fixture()
def get(baseurl):
    def _join(path):
        return requests.get(baseurl + path, headers=_headers)
    return _join


@pytest.fixture()
def get_no_header(baseurl):
    def _join(path):
       return requests.get(baseurl + path)
    return _join


@pytest.fixture()
def get_with_data(baseurl):
    def _join(path):
        return requests.get(baseurl + path, data = '{"foo":"bar"}')
    return _join


@pytest.fixture()
def post(baseurl):
    def _join(path, password):
        return requests.post(baseurl + path, headers=_headers, \
                data = '{"password":"' + password + '"}')
    return _join


@pytest.fixture()
def post_timeout(baseurl):
    def _join(path, password):
        return requests.post(baseurl + path, headers=_headers, timeout=10.0, \
                data = '{"password":"' + password + '"}')
    return _join


@pytest.fixture(scope='session')
def random_passwords():
    _passwords = []
    for i in range(17):
        _passwords.append(
            ''.join(random.choice(string.ascii_letters + string.digits) \
                    for _ in range(i)))
    return _passwords


@pytest.fixture(scope='session')
def big_password():
    _passwords = []
    for i in range(1):
        _passwords.append(
            ''.join(random.choice(string.ascii_letters + string.digits) \
                    for _ in range(128)))
    return _passwords


@pytest.fixture(scope='session')
def random_passwords_punc():
    _passwords = []
    for i in range(17):
        _passwords.append(
            ''.join(random.choice(string.punctuation) for _ in range(i)))
    return _passwords


@pytest.fixture(scope='session')
def generate_sha512():
    def _join(password):
        return lib.sha512(password.encode()).decode()
    return(_join)
