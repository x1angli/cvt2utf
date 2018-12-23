"""A setuptools based setup module.
"""

import os, textwrap
from setuptools import setup, find_packages


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

meta_info = {}

here = os.path.abspath(os.path.dirname(__file__))
meta_f = os.path.join(here, 'cvt2utf', 'meta_inf.py')
with open(meta_f) as fp:
    exec(fp.read(), meta_info)


setup(
    name="convert2utf",

    version=meta_info['__version__'],

    packages=find_packages(exclude=['docs', 'examples', 'tests', 'venv']),

    description=textwrap.dedent('''
        A lightweight tool that converts non-UTF-encoded (such as GB2312, BIG5 encoded) files to UTF-8 encoded files. 
        It can also add or remove Byte-order-mark (BOM) in UTF-encoded files.
        '''),

    author='x1ang.li',

    author_email='cvt2utf@x1ang.li',

    url='https://github.com/x1angli/convert2utf',

    license='MIT',

    keywords='target_encoding UTF-8 UTF UTF8 GBK GB2312 Byte-Order-Mark BOM',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Text Editors',
        'Topic :: Text Processing :: General',
    ],

    install_requires=['chardet'],

    python_requires='>=3',

    entry_points={
        'console_scripts': [
            'cvt2utf = cvt2utf.main:cli',
        ],
    }
)
