""" pip install test suite with console script. """
from setuptools import setup, find_packages

setup(
    name = 'run_tests',
    version = '0.1.0',
    license = 'na',
    description = 'Password Hashing REST API testing.',

    author = 'Brian Otte',
    author_email = 'otte.brian@gmail.com',

    install_requires=['pytest', 'requests', 'psutil', 'pickledb', 'pytest-html'],

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
