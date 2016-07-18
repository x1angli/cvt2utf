from setuptools import setup
import textwrap


setup(
    name="convert2utf",
    version="0.8",
    license='https://opensource.org/licenses/MIT',
    summary="A lightweight tool that converts non-UTF-encoded (such as GB2312, GBK, BIG5 encoded) files to UTF-8 encoded files. At the same time, it can also remove Byte-order-mark (BOM) in those files.",
    description=textwrap.dedent("""
        convert2utf
        ===========

        |PyPI version| |Build Status| |Coverage Status|

        A lightweight tool that converts non-UTF-encoded (such as GB2312, GBK, BIG5 encoded) files to UTF-8 encoded files. It can also remove Byte-order-mark (BOM) in those files.

        convert2utf can either be executed from command line (CLI), or imported into other Python code.

        There are two modes: batch mode and single file mode. Batch mode: Pass in a directory as the input, and all text files that meets the criteria underneath it will be converted to UTF8-encoding. Single file mode_: If the input argument is just an individual file, it would be straightforwardly converted to UTF-8."""),
    author='x1ang.li',
    author_email='convert2utf@x1ang.li',
    url='https://github.com/x1angli/convert2utf',
    install_requires=['chardet'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Text Editors',
        'Topic :: Text Processing :: General',
    ],
)
