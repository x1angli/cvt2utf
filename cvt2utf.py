#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'x1angli'
__version__ = '2.0.0'

import logging, os, argparse, textwrap, time
import traceback

import chardet

DEFAULT_CONF = {
    # Only those files ending with extensions in this list will be scanned or converted.
    'scan_exts': {'txt', 'md'},

    # if the file is larger than this size limit, we could skip it.
    'size_limit': 100 * 1024 ** 2,  # default: 100MB

    'codec_chain': ['chardet'],

    # We have to set a minimum threshold. Only those target_encoding results returned by chartdet that are above
    # that threshold level would be accepted.
    'confi_thres': 0.73,

    # (Used in the clean_bak subcommand only) It sets the earliest time for those backup file to be cleaned.
    # If a file is created earlier than the cutoff_time, it will be skipped by the "clean_backup" command.
    'cutoff_time': 40 * 60  # unit: seconds
}

CHARDET_NAME_TO_PYNATIVE_NAME = {
    # We need to treat ascii as UTF-8 encoded so as skip converting it to the same utf-8
    "ascii": "utf_8",

    "GB18030": "gb18030",

    # For GB2312/GBK related discussions, See https://github.com/chardet/chardet/pull/264/files and
    # https://github.com/chardet/chardet/issues/94
    "GBK": "gb18030",
    "GB2312": "gb18030",

    "utf-8": "utf_8",
    "UTF-8-SIG": "utf_8_sig",
    "UTF-16": "utf_16",
    "ISO-8859-1": "iso-8859-1",
}


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


def map_chardet_name_to_native(chardet_name: str) -> str:
    if not chardet_name:
        raise ValueError(f"the chardet_name should be a meaningful string: {chardet_name}")
        return None
    if chardet_name in CHARDET_NAME_TO_PYNATIVE_NAME:
        return CHARDET_NAME_TO_PYNATIVE_NAME[chardet_name]
    else:
        return chardet_name


def detect_single_file(filename: str):
    with open(filename, 'rb') as f:  # read under the binary mode
        file_bytes = f.read()
        chr_res = chardet.detect(file_bytes)
        log.debug(f"The codec of {filename} returned by chardet is {chr_res}.")
        if not chr_res['encoding'] or chr_res['confidence'] < DEFAULT_CONF['confi_thres']:
            raise Exception(f"Unable to detect the encoding of {filename}, {chr_res}")

        return chr_res['encoding']


def detect_show_single_file(filename: str, *args):
    with open(filename, 'rb') as f:  # read under the binary mode
        file_bytes = f.read()
        chr_res = chardet.detect(file_bytes)
        log.info(f"Chardet has parsed {filename} as {chr_res}.")
        return None


def convert_single_file(file_name, args):
    size = os.path.getsize(file_name)
    if size == 0 or size > DEFAULT_CONF['size_limit']:
        log.debug(f"Skipped {file_name} because it either is empty or exceeds our limit {DEFAULT_CONF['size_limit']} ")
        return

    src_codec = detect_single_file(file_name)

    src_codec = map_chardet_name_to_native(src_codec)

    if args.skip_utf and src_codec.startswith('utf'):
        log.debug(f"Skipped an UTF file {file_name}")
        return

    if src_codec == args.tgt_codec:
        log.debug(f"Skipped a {src_codec} file {file_name}.")
        return

    with open(file_name, 'rb') as f:  # read under the binary mode
        file_bytes = f.read()

    try:
        log.debug(f"Opening file {file_name} with assuming its encoding as {src_codec}")
        file_str = file_bytes.decode(src_codec)
    except UnicodeDecodeError as e:
        raise Exception(f"Unable to open {file_name} with codec {src_codec}")

    # # preserving file time information (modification time and access time)
    # src_stat = os.stat(filename)

    # if the 'nobak' flag hasn't been set, we would create a backup file.
    if args.create_bak:
        backup_name = file_name + '.' + str(int(time.time())) + '.bak'
        log.info("Renaming %s to %s", file_name, backup_name)
        os.rename(file_name, backup_name)

    log.debug(f"Writing the file: {file_name} in {args.tgt_codec}")
    with open(file_name, 'wb') as f:  # write under the binary mode
        f.write(file_str.encode(args.tgt_codec))
    log.info(f"Converted the file: {file_name} from {src_codec} to {args.tgt_codec}")
    # # setting the new file's time to the old file
    # os.utime(filename, times=(src_stat.st_atime, src_stat.st_ctime))


def walk_dir(base, scan_exts, walk_func, walk_func_args=None):
    for root, dirs, files in os.walk(base):
        for name in files:

            extension = os.path.splitext(name)[1][1:].strip().lower()
            # On linux there is a newline at the end which will cause the match to fail,
            # so we just 'strip()' the '\n'
            # Also, add 'lower()' for case-insensitive matching

            if extension in scan_exts:
                file_fullname = os.path.join(root, name)
                try:
                    walk_func(file_fullname, walk_func_args)
                except IOError:
                    log.error(f"Unable to read or write the file: {file_fullname}. Please check the file's permission.", )
                except KeyboardInterrupt:
                    log.warning("Interrupted by keyboard (e.g. Ctrl+C)")
                    exit()
                except Exception as ex:
                    log.error("Unable to process the file: %s. Please check.", file_fullname)
                    traceback.print_exec()


def convert_main(args):
    base = args.base
    if not os.path.exists(base):
        log.error(f"The {base} does not exist")
        return

    log.info("Start converting ... ready, set, go... ")

    if os.path.isdir(base):
        log.info(f"The root folder is: {base}. ")
        log.info(f"Files with these extension names will be processed: {args.scan_exts}")

        walk_dir(base, args.scan_exts, convert_single_file, args)
    else:
        log.info(f"A single file will be processed: {base}")
        convert_single_file(base, args)

    log.info("All finished. ")


def detect_show_main(args):
    base = args.base
    if not os.path.exists(base):
        raise ValueError(f"The base {base} does not exist")

    if os.path.isdir(base):
        log.info(f"The root folder is: {base}. ")
        log.info(f"Files with these extension names will be processed: {args.scan_exts}")

        walk_dir(base, args.scan_exts, detect_show_single_file)
    else:
        log.info(f"A single file will be processed: {base}")
        detect_show_single_file(base)


def clean_bak_main(args):
    base = args.base
    if not os.path.exists(base):
        log.error(f"The {base} does not exist")
        return

    if not os.path.isdir(base):
        log.error(f"The {base} is not a directory")
        return

    cutoff_time = time.time() - DEFAULT_CONF['cutoff_time']

    log.info(f"Removing all newly-created .bak files under {base}")

    for root, dirs, files in os.walk(base):
        for name in files:
            extension = os.path.splitext(name)[1][1:]
            if extension == 'bak':
                fullname = os.path.join(root, name)
                ctime = os.path.getctime(fullname)
                if ctime > cutoff_time:
                    os.remove(fullname)
                    log.info("Removed the file: %s", fullname)
# end of clean_bak_main(args)


def cli():
    parser = argparse.ArgumentParser(
        description="A tool that converts non-UTF-encoded text files UTF-8 encoded files.",
        epilog=textwrap.dedent('''
            You can use this tool to remove BOM all code files from your source code repo, 
            make c++ files UTF8-compatible so that the project can be compiled on any system locale.            
            '''),
    )

    parser.add_argument('-v', '--version', action='version', version=__version__)

    subparsers = parser.add_subparsers(dest='cmd')

    convert_parser = subparsers.add_parser('convert', aliases=['cvt'], help=textwrap.dedent(f'''
            The main command that converts {DEFAULT_CONF['scan_exts']} files into UTF8-encoded ones.
            '''))

    convert_parser.set_defaults(func=convert_main)

    convert_parser.add_argument(
        'base',
        metavar="/path/to/the/dir/to/convert",
        help=textwrap.dedent('''
            the path pointing to the file or directory.
            If it's a directory, files contained in it with specified extensions will be converted to UTF-8.
            Otherwise, if it's a file, only that file will be converted to UTF-8.
            ''')
    )

    convert_parser.add_argument(
        '-ext',
        '--scan_exts',
        nargs='+',  # '+'. Just like '*', all command-line args present are gathered into a list.
        dest='scan_exts',
        default=DEFAULT_CONF['scan_exts'],
        type=set,
        help="The list of file extensions to be converted.",
    )

    convert_parser.add_argument(
        '--nobak',
        dest='create_bak',
        action='store_false',
        default=True,
        help=textwrap.dedent('''
            By default, we will create a .bak file for each file that we have converted.
            But, with this flag, it would directly overwrite existing file without creating any backup files.
            '''),
    )

    convert_parser.add_argument(
        '--skiputf',
        dest='skip_utf',
        action='store_true',
        default=False,
        help=textwrap.dedent('''
                "By default, we will only skip those files whose codec are exactly the same as the target. e.g. 
                If the original file is `utf_8_sig`-encoded, while the target is `utf_8`, then the BOM file will be removed.
                But, with this flag, the file will be skipped so that it's still `utf_8_sig`-encoded. 
                '''),
    )

    tgt_group = convert_parser.add_mutually_exclusive_group()  # This group will be used to specify the target encoding

    tgt_group.add_argument(
        '-tgt',
        '--target',
        dest='tgt_codec',
        default='utf_8',
        help=textwrap.dedent('''
            If this command line argument is missing, we convert files to UTF-8 without BOM 
            (i.e. the target encoding would be just `utf_8`, rather than `utf_8_sig`). 
            But, with this flag, we would add BOM in encoded text files (i.e. the target encoding would be 'utf-8-sig').
            '''),
    )
    tgt_group.add_argument(
        '-bom',
        '--u8bom',
        dest='tgt_codec',
        action='store_const',
        const='utf_8_sig',
        help=textwrap.dedent('''
            If this command line argument is missing, we convert files to UTF-8 without BOM 
            (i.e. the target encoding would be just `utf_8`, rather than `utf_8_sig`). 
            But, with this flag, we would add BOM in encoded text files (i.e. the target encoding would be 'utf-8-sig').
            '''),
    )

    detect_parser = subparsers.add_parser('detect', aliases=['det'], help=textwrap.dedent(f'''
            Scans files and show their codec.
            '''))

    detect_parser.set_defaults(func=detect_show_main)

    detect_parser.add_argument(
        'base',
        metavar="/base/path/",
        help=textwrap.dedent('''
            the path pointing to the file or directory.
            If it's a directory, the dir will be traversed, and files with specified extensions under this dir will be 
                converted to UTF-8.
            Alternatively, it can also be the path to a single file. 
            ''')
    )

    detect_parser.add_argument(
        '-ext',
        '--scan_exts',
        nargs='+',  # '+'. Just like '*', all command-line args present are gathered into a list.
        dest='scan_exts',
        default=DEFAULT_CONF['scan_exts'],
        type=set,
        help="The list of file extensions whose encodings to be detected.",
    )

    cleanbak_parser = subparsers.add_parser('cleanbak', aliases=['clean'], help=textwrap.dedent(f'''
            This command cleans all .bak files generated within last {DEFAULT_CONF['cutoff_time']} seconds.
            '''))

    cleanbak_parser.set_defaults(func=clean_bak_main)

    cleanbak_parser.add_argument(
        'base',
        metavar="/base/path/",
        help=textwrap.dedent('''
            the path pointing to the  directory. 
            ".bak" files created underneath it within a certain period of time will be removed.
            ''')
    )

    args = parser.parse_args()

    if args.cmd is None:
        import sys
        args = parser.parse_args(['convert'] + sys.argv[1:])

    args.func(args)


if __name__ == '__main__':
    cli()
