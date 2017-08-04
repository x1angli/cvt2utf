#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'x1ang.li'

import logging, os, argparse, textwrap
import time
import chardet

# Default configuration will take effect when corresponding input args are missing.
# Feel free to change this for your convenience.
DEFAULT_CONF = {
    # Only those files ending with extensions in this list will be scanned or converted.
    'exts'      : ['txt'],
    'keep_BOM'  : False,
    'overwrite' : False,
}

# We have to set a minimum threshold. Only those encoding results returned by chartdet that are above that threshold level would be accepted.
# See https://github.com/x1angli/convert2utf/issues/4 for further details
CONFIDENCE_THRESHOLD = 0.8


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


class Convert2Utf8:
    def __init__(self, exts, keep_BOM, overwrite):
        self.exts = exts
        self.skip_encoding = ['ascii', 'utf-8']
        if keep_BOM:
            self.skip_encoding.append('utf-8-sig')
        self.overwrite = overwrite

    def walk_dir(self, dirname):
        for root, dirs, files in os.walk(dirname):
            for name in files:
                extension = os.path.splitext(name)[1][1:].strip().lower()
                # On linux there is a newline at the end which will cause the match to fail, so we just 'strip()' the '\n'
                # Also, add 'lower()' to ensure matching

                if (extension in self.exts):
                    fullname = os.path.join(root, name)
                    try:
                        self.convert_file(fullname)
                    except IOError:
                        log.error("Unable to read or write the file: %s. Please check the file's permission.", fullname)
                    except KeyboardInterrupt:
                        log.warning("Interrupted by keyboard (e.g. Ctrl+C)")
                        exit()
                    # else:
                    #     log.error("Unable to process the file: %s. Please check.", fullname)
                    #     traceback.print_stack()



    def convert_file(self, filename):
        with open(filename, 'rb') as f: # read under the binary mode
            bytedata = f.read()

        if len(bytedata) == 0:
            log.info("Skipped empty file %s", filename)
            return

        chardet_result = chardet.detect(bytedata)
        if chardet_result['encoding'] == None or chardet_result['confidence'] < CONFIDENCE_THRESHOLD:
            log.warning("Unable to detect the encoding of %s, and it will be ignored.", filename)
            return

        encoding = chardet_result['encoding'].lower()
        log.debug("Scanned %s, which is %s - encoded", filename, encoding)

        if (encoding in self.skip_encoding):
            log.debug("Skipped %s - encoded %s", filename, encoding)
            return

        # Since chardet only recognized all GB-based encoding as 'gb2312', we may encounter errors when the text file
        # contains certain charaters, breaking the program. To make it more special-character-tolerant, we should
        # upgrade the encoding to 'gb18030', which contains more characters than gb2312.
        if encoding.lower() == 'gb2312':
            encoding = 'gb18030'

        # preserving file time information (modification time and access time)
        old_stat = os.stat(filename)

        log.debug("Start coverting %s, whose encoding is %s", filename, encoding)
        try:
            strdata = bytedata.decode(encoding)
        except UnicodeDecodeError as e:
            log.error("Unicode error for file %s", filename)
            print(e)
            return

        # if the 'overwrite' flag is 'False', we would make a backup of the original text file.
        if not self.overwrite:
            backup_name = filename + '.bak'
            i = 0
            while os.path.exists(backup_name):
                backup_name = filename + '.bak' + str(i)
                i = i+1
            log.debug("Renaming old file %s to new file %s", filename, backup_name)
            os.rename(filename, backup_name)

        log.debug("Writing the file: %s in UTF-8", filename)
        with open(filename, 'wb') as f: # write under the binary mode
            f.write(strdata.encode('utf-8'))

        # setting the new file's time to the old file
        os.utime(filename, times = (old_stat.st_atime, old_stat.st_ctime))
        log.info("Converted the file: %s to UTF-8 from %s", filename, encoding)
    # end of def convert_file(self, filename)



    def run(self, root):
        if not os.path.exists(root):
            log.error("The file specified %s is neither a directory nor a regular file", root)
            return

        log.info("Start working now!")

        if os.path.isdir(root):
            log.info("The root is: %s. ", root)
            log.info("Files with these extension names will be inspected: %s", self.exts)
            self.walk_dir(root)
        else:
            log.info("Wow, only a single file will be processed: %s", root)
            self.convert_file(root)

        log.info("Finished all.")
    # end of def run(self, root):

def clean_backups(dirname):
    if not os.path.isdir(dirname):
        log.error("The file specified %s is not a directory ", dirname)
        return

    now = time.time()
    last40min = now - 60 * 40

    log.info("Removing all newly-created .bak files under %s", dirname)

    for root, dirs, files in os.walk(dirname):
        for name in files:
            extension = os.path.splitext(name)[1][1:]
            if extension.startswith('bak'):
                fullname = os.path.join(root, name)
                ctime = os.path.getctime(fullname)
                if ctime > last40min:
                    os.remove(fullname)
                    log.info("Removed the file: %s", fullname)


def cli():
    parser = argparse.ArgumentParser(
        prog='cvt2utf8',
        description="A tool that converts non-UTF-encoded text files UTF-8 encoded files.",
        epilog="You can use this tool to remove BOM from .php source code files, or convert other encoding into UTF-8")

    parser.add_argument(
        'root',
        metavar = "filename",
        help    = textwrap.dedent('''\
            the path pointing to the file or directory.
            If it's a directory, files contained in it with specified extensions will be converted to UTF-8.
            Otherwise, if it's a file, only that file will be converted to UTF-8.''')
        )

    parser.add_argument(
        '-e',
        '--exts',
        nargs   = '+', # '+'. Just like '*', all command-line args present are gathered into a list.
        default = DEFAULT_CONF['exts'],
        help    = "the list of file extensions. Only those files ending with extensions in this list will be converted.",
        )

    parser.add_argument(
        '-o',
        '--overwrite',
        action  = 'store_true',
        default = DEFAULT_CONF['overwrite'],
        help    = "Danger! If you turn this switch on, it would directly overwrite existing file without creating any backups.",
        )

    parser.add_argument(
        '-k',
        '--keepbom',
        action  = 'store_true',
        dest    = 'keep_BOM',
        default = DEFAULT_CONF['keep_BOM'],
        help    = "If the text file begins with UTF-8's Byte-Order-Mask, we would keep it rather than remove it.",
        )

    parser.add_argument(
        '-c',
        '--cleanbak',
        action  = 'store_true',
        dest    = 'clean_bak',
        default = False,
        help    = textwrap.dedent('''Clean all .bak files generated within last 40 minutes.
                        When enabled, no files will be converted to UTF-8. Use this flag with extra caution! '''),
        )


    args = parser.parse_args()

    if args.clean_bak:
        clean_backups(args.root)

    else:
        cvt2utf8 = Convert2Utf8(args.exts, args.keep_BOM, args.overwrite)
        cvt2utf8.run(args.root)

if __name__ == '__main__':
    cli()
