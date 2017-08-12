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
    'overwrite' : False,
    'add_BOM'   : False,
    'convert_UTF'   : False,
    'confi_thres' : 0.8,
}

# We have to set a minimum threshold. Only those target_encoding results returned by chartdet that are above that threshold level would be accepted.
# See https://github.com/x1angli/convert2utf/issues/4 for further details



logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


class Convert2Utf8:
    def __init__(self, args):
        self.args = args


    def walk_dir(self, dirname):
        for root, dirs, files in os.walk(dirname):
            for name in files:
                extension = os.path.splitext(name)[1][1:].strip().lower()
                # On linux there is a newline at the end which will cause the match to fail, so we just 'strip()' the '\n'
                # Also, add 'lower()' to ensure matching

                if (extension in self.args.exts):
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

        chr_res = chardet.detect(bytedata)
        if chr_res['encoding'] == None or chr_res['confidence'] < DEFAULT_CONF['confi_thres']:
            log.warning("Ignoring %s, since its encoding is unable to detect.", filename)
            return

        src_enc = chr_res['encoding'].lower()
        log.debug("Scanned %s, whose encoding is %s ", filename, src_enc)

        if (src_enc == 'ascii'):
            log.info("Skipped %s, whose encoding is %s", filename, src_enc)
            return

        if (not self.args.convert_utf) and src_enc.startswith('utf'):
            log.info("Skipped %s, whose encoding is %s", filename, src_enc)
            return

        # Since chardet only recognized all GB-based target_encoding as 'gb2312', the decoding will fail when the text file
        # contains certain special charaters. To make it more special-character-tolerant, we should
        # upgrade the target_encoding to 'gb18030', which is a character set larger than gb2312.
        if src_enc.lower() == 'gb2312':
            src_enc = 'gb18030'

        try:
            strdata = bytedata.decode(src_enc)
        except UnicodeDecodeError as e:
            log.error("Unicode error for file %s", filename)
            print(e)
            return

        # preserving file time information (modification time and access time)
        src_stat = os.stat(filename)

        # if the 'overwrite' flag is 'False', we would make a backup of the original text file.
        if not self.args.overwrite:
            backup_name = filename + '.' + str(int(round(time.time() * 1000))) + '.bak'
            log.info("Renaming %s to %s", filename, backup_name)
            os.rename(filename, backup_name)

        tgt_enc = self.args.target_encoding
        log.debug("Writing the file: %s in %s", filename, tgt_enc)
        with open(filename, 'wb') as f: # write under the binary mode
            f.write(strdata.encode(tgt_enc))
        log.info("Converted the file: %s from %s to %s", filename, src_enc, tgt_enc)

        # setting the new file's time to the old file
        os.utime(filename, times = (src_stat.st_atime, src_stat.st_ctime))
    # end of def convert_file(self, filename)



    def run(self):
        root = self.args.root
        if not os.path.exists(root):
            log.error("The file specified %s is neither a directory nor a regular file", root)
            return

        log.info("Start working now!")

        if os.path.isdir(root):
            log.info("The root is: %s. ", root)
            log.info("Files with these extension names will be inspected: %s", self.args.exts)
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
            if extension == 'bak':
                fullname = os.path.join(root, name)
                ctime = os.path.getctime(fullname)
                if ctime > last40min:
                    os.remove(fullname)
                    log.info("Removed the file: %s", fullname)


def cli():
    parser = argparse.ArgumentParser(
        prog='cvt2utf8',
        description="A tool that converts non-UTF-encoded text files UTF-8 encoded files.",
        epilog="You can use this tool to remove BOM from .php source code files, or convert other target_encoding into UTF-8")

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
        '-u',
        '--cvtutf',
        action  = 'store_true',
        dest    = 'convert_utf',
        default = DEFAULT_CONF['convert_UTF'],
        help    = "By default, we will skip files whose encodings are UTF (including UTF-8 and UTF-16), and BOM headers in these files will remain unchanged. "
                  "But, if you want to change BOM headers for these files, you could utilize this option to change their signatures.",
        )

    parser.add_argument(
        '-b',
        '--addbom',
        action  = 'store_true',
        dest    = 'add_bom',
        default = DEFAULT_CONF['add_BOM'],
        help    = "If this command line argument is missing, we convert files to UTF-8 without BOM (i.e. the target encoding would be just 'utf-8'). "
                  "But with this flag, we would add BOM in encoded text files (i.e. the target encoding would be 'utf-8-sig').",
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
        args.target_encoding = 'utf-8-sig' if args.add_bom else 'utf-8'

        cvt2utf8 = Convert2Utf8(args)
        cvt2utf8.run()

if __name__ == '__main__':
    cli()
