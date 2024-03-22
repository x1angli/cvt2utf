"""
pytests for the file cvt2utf.py
"""

import pytest

from . import cvt2utf


@pytest.mark.parametrize("chardet_name, expected", [
    ('ascii', 'utf_8'),
    ('BOCU-1', 'BOCU-1'),
    ('EUC-JP', 'EUC-JP'),
    ('GB18030', 'gb18030'),
    ('GB2312', 'gb18030'),
    ('GBK', 'gb18030'),
    ('HZ-GB-2312', 'HZ-GB-2312'),
    ('ISO-2022-CN', 'ISO-2022-CN'),
    ('ISO-2022-JP', 'ISO-2022-JP'),
    ('ISO-2022-KR', 'ISO-2022-KR'),
    ('ISO-8859-1', 'iso-8859-1'),
    ('SCSU', 'SCSU'),
    ('UTF-1', 'UTF-1'),
    ('UTF-16', 'utf_16'),
    ('UTF-16BE', 'UTF-16BE'),
    ('UTF-16LE', 'UTF-16LE'),
    ('UTF-32', 'UTF-32'),
    ('UTF-32BE', 'UTF-32BE'),
    ('UTF-32LE', 'UTF-32LE'),
    ('UTF-7', 'UTF-7'),
    ('UTF-8-SIG', 'utf_8_sig'),
    ('utf-8', 'utf_8'),
    ('UTF-EBCDIC', 'UTF-EBCDIC'),
])
def test_map_chardet_name_to_native(chardet_name, expected):
    """
    pytest for the function map_chardet_name_to_native
    """
    assert cvt2utf.map_chardet_name_to_native(chardet_name) == expected


@pytest.mark.parametrize("filename, expected", [
    ("sample_data/ascii.crlf.txt", "ascii"),
    ("sample_data/gb2312.crlf.txt", "GB2312"),
    ("sample_data/gbk.crlf.txt", "GBK"),
    ("sample_data/latin1.crlf.txt", "ISO-8859-1"),
    ("sample_data/utf-16be.txt", "UTF-16BE"),
    ("sample_data/utf-16le.txt", "UTF-16LE"),
    ("sample_data/utf-8-bom.txt", "UTF-8-SIG"),
    ("sample_data/utf-8.crlf.txt", "UTF-8"),
])
def test_detect_single_file(filename, expected):
    """
    pytest for the function detect_single_file
    """
    assert cvt2utf.detect_single_file(filename) == expected
