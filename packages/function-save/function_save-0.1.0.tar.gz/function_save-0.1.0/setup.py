from setuptools import setup, find_packages
VERSION = '0.1.0'
DESCRIPTION = 'This function automatically saves your function calls and result and prints it in a systematic format for better debugging and analysis.'
LONG_DESCRIPTION = ''

setup(
    name = 'function_save',
    version = VERSION,
    author = 'Dev',
    author_email = 'amazingdev.dev@gmail.com',
    description = DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    keywords = ['python','function']
)