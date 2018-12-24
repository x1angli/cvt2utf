#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'x1ang.li'

import logging, os, argparse, textwrap, time
import codecs
import chardet

from cvt2utf.meta_inf import __version__

DEFAULT_CONF = {
    'inc_exts': {'txt'},  # File extensions to be converted.
    # Only those files ending with extensions in this list will be scanned or converted.

    'exc_exts': {'bak'},  # File ends with such extensions will NOT be converted.

    'size_limit': 10 * 1024 ** 2,  # if the file is larger than this size limit, we could skip it. default 10MB

    'codec_chain': ['ascii', 'utf_8_sig', 'latin_1', 'chardet'],
    # We will try elements in this list sequentially.
    # If the element is `chardet` we will obtain the result from chardet.
    # If the element is a valid codec name, we will attempt to open the file with the `strict` mode
    # Note: If it contains `ascii`, it must be place as the first one.
    # Note: `utf_8_sig` should have a priority higher than `latin_1`

    'confi_thres': 0.8,
    # We have to set a minimum threshold. Only those target_encoding results returned by chartdet that are above
    # that threshold level would be accepted.
    # See https://github.com/x1angli/convert2utf/issues/4 for further details

    'cut_time': 40  # The cut-off time used when executing, unit: minutes
}

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


def normalize_codec_name(chardet_name):
    """
    Normalizes chardet codec names to Python codec names.
    :param chardet_name: chardet codec names
    :return: Python codec names. See: https://docs.python.org/3.7/library/codecs.html#standard-encodings
    """

    python_name = chardet_name.lower().replace('iso-', 'iso').replace('-', '_')
    python_name = codecs.lookup(python_name).name

    # Since chardet only recognized all GB-based target_encoding as 'gb2312', the decoding will fail when the text file
    # contains certain special charaters. To make it more special-character-tolerant, we should
    # upgrade the target_encoding to 'gb18030', which is a character set larger than gb2312.
    if python_name == 'gb2312':
        return 'gb18030'

    return python_name


def detect_codec(bytedata, filename):

    for codec in DEFAULT_CONF['codec_chain']:
        if codec == 'chardet':
            chr_res = chardet.detect(bytedata)
            if not chr_res['encoding'] or chr_res['confidence'] < DEFAULT_CONF['confi_thres']:
                log.debug(f"The codec of {filename} is unable to detect, the result is {chr_res}.")
            else:
                return normalize_codec_name(chr_res['encoding'])
        else:
            try:
                bytedata.decode(codec, 'strict')
                return codec
            except UnicodeDecodeError:
                log.debug(f"{filename} is not {codec}-encoded.")
                continue
    # end of for-loop

    return None
# end of detect_codec(bytedata, filename):


def walk_dir(base, args):
    for root, dirs, files in os.walk(base):
        for name in files:

            extension = os.path.splitext(name)[1][1:].strip().lower()
            # On linux there is a newline at the end which will cause the match to fail,
            # so we just 'strip()' the '\n'
            # Also, add 'lower()' to ensure matching

            if extension in args.inc_exts and extension not in args.exc_exts:
                fullname = os.path.join(root, name)
                try:
                    convert_file(fullname, args)
                except IOError:
                    log.error("Unable to read or write the file: %s. Please check the file's permission.", fullname)
                except KeyboardInterrupt:
                    log.warning("Interrupted by keyboard (e.g. Ctrl+C)")
                    exit()
                # else:
                #     log.error("Unable to process the file: %s. Please check.", fullname)
                #     traceback.print_stack()


def convert_file(filename, args):

    size = os.path.getsize(filename)

    if size == 0 or size > DEFAULT_CONF['size_limit']:
        log.debug(f"Skipped {filename} because it either is empty or exceeds our limit {DEFAULT_CONF['size_limit']} ")
        return

    with open(filename, 'rb') as f:  # read under the binary mode
        file_bytes = f.read()

    src_codec = detect_codec(file_bytes, filename)
    if src_codec is None:
        log.warning(f"Unable to recognize the codec for {filename}.")
        return
    log.debug(f"Scanned {filename}, whose encoding is {src_codec} ")

    if src_codec == 'ascii':
        src_codec = 'utf_8'

    if args.skip_utf and src_codec.startswith('utf'):
        log.debug(f"Skipped an UTF file {filename}")
        return

    if src_codec == args.tgt_codec:
        log.debug(f"Skipped a {src_codec} file {filename}.")
        return

    try:
        file_str = file_bytes.decode(src_codec)
    except UnicodeDecodeError as e:
        log.error(f"Unable to open {filename} with codec {src_codec}")
        # print(e)
        return

    # # preserving file time information (modification time and access time)
    # src_stat = os.stat(filename)

    # if the 'nobak' flag is 'False', we would make a backup of the original text file.
    if args.create_bak:
        backup_name = filename + '.' + str(int(time.time())) + '.bak'
        log.info("Renaming %s to %s", filename, backup_name)
        os.rename(filename, backup_name)

    # log.debug(f"Writing the file: {filename} in {args.tgt_codec}")
    with open(filename, 'wb') as f:  # write under the binary mode
        f.write(file_str.encode(args.tgt_codec))
    log.info(f"Converted the file: {filename} from {src_codec} to {args.tgt_codec}")

    # # setting the new file's time to the old file
    # os.utime(filename, times=(src_stat.st_atime, src_stat.st_ctime))

# end of def convert_file(self, filename)


def cvt_codec_main(args):
    base = args.base
    if not os.path.exists(base):
        log.error(f"The {base} does not exist")
        return

    # merging the hard-coded config with the command-line arguments
    args.inc_exts = DEFAULT_CONF['inc_exts'] if args.inc_exts is None else set(args.inc_exts) | DEFAULT_CONF['inc_exts']
    args.exc_exts = DEFAULT_CONF['exc_exts'] if args.exc_exts is None else set(args.exc_exts) | DEFAULT_CONF['exc_exts']

    log.info("Start working now!")

    if os.path.isdir(base):
        log.info(f"The root folder is: {base}. ")
        log.info(f"Files with these extension names will be processed: {args.inc_exts}")
        log.info(f"Files with these extension names will be ignored: {args.exc_exts}")

        walk_dir(base, args)
    else:
        log.info(f"A single file will be processed: {base}")
        convert_file(base, args)

    log.info("Finished all.")

# end of def cvt_codec_main(args):


def clean_bak_main(args):
    base = args.base
    if not os.path.exists(base):
        log.error(f"The {base} does not exist")
        return

    if not os.path.isdir(base):
        log.error(f"The {base} is not a directory")
        return

    cutoff_time = time.time() - DEFAULT_CONF['cut_time'] * 60

    log.info("Removing all newly-created .bak files under %s", base)

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

    cvt_parser = subparsers.add_parser('convert', aliases=['cvt'], help=textwrap.dedent(f'''
            The main command that converts {DEFAULT_CONF['inc_exts']} files into UTF8-encoded ones.
            Files with these extension names will be ignored: {DEFAULT_CONF['exc_exts']}
            '''))

    cvt_parser.set_defaults(func=cvt_codec_main)

    cvt_parser.add_argument(
        'base',
        metavar="/base/path/",
        help=textwrap.dedent('''
            the path pointing to the file or directory.
            If it's a directory, files contained in it with specified extensions will be converted to UTF-8.
            Otherwise, if it's a file, only that file will be converted to UTF-8.
            ''')
    )

    cvt_parser.add_argument(
        '-i',
        '--inc',
        nargs='+',  # '+'. Just like '*', all command-line args present are gathered into a list.
        dest='inc_exts',
        # default=DEFAULT_CONF['inc_exts'],
        help="The list of file extensions to be converted.",
    )

    cvt_parser.add_argument(
        '-x',
        '--exc',
        nargs='+',
        dest='exc_exts',
        # default=DEFAULT_CONF['exc_exts'],
        help="The list of file extensions that will be excluded (skipped).",
    )

    cvt_parser.add_argument(
        '--nobak',
        dest='create_bak',
        action='store_false',
        default=True,
        help=textwrap.dedent('''
            By default, we will create a .bak file for each file that we have converted.
            But, with this flag, it would directly overwrite existing file without creating any backup files.
            '''),
    )

    cvt_parser.add_argument(
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

    tgt_group = cvt_parser.add_mutually_exclusive_group()  # This group will be used to specify the target encoding

    tgt_group.add_argument(
        '-t',
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
        '-b',
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

    cb_parser = subparsers.add_parser('cleanbak', aliases=['cb'], help=textwrap.dedent(f'''
            This command cleans all .bak files generated within last {DEFAULT_CONF['cut_time']} minutes.
            It does NOT convert anything. Use this flag with extra caution! 
            '''))
    cb_parser.set_defaults(func=clean_bak_main)

    cb_parser.add_argument(
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
