"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path


# Get the long description from the README file
# try:
#     import pypandoc
#     long_description = pypandoc.convert('README.md', 'rst')
# except(IOError, ImportError):
#     long_description = open('README.md').read()


# here = path.abspath(path.dirname(__file__))
#
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()


setup(
    name="convert2utf",

    version="1.0.2",

    packages=find_packages(),

    description="A lightweight tool that converts non-UTF-encoded (such as GB2312, GBK, BIG5 encoded) files to UTF-8 encoded files. It can also add or remove Byte-order-mark (BOM) in UTF-encoded files.",

    author='x1ang.li',

    author_email='xl@x1ang.li',

    url='https://github.com/x1angli/convert2utf',

    license='MIT',

    keywords='target_encoding UTF-8 UTF UTF8 GBK GB2312 Byte-Order-Mark BOM',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Text Editors',
        'Topic :: Text Processing :: General',
    ],

    install_requires=['chardet'],
)
