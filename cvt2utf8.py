#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'x1ang.li'

import logging, os, argparse
import chardet

default_extlist = ['txt','java','jsp','py','php','js'] # The default file extensions
                                              # Only those files ending with extensions in this list will be converted.
                                              # Feel free to change this
remove_BOM = True

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


class Convert2Utf8:
    def __init__(self, extlist):
        self.extlist = extlist

    def walk_dir(self, dirname):
        for root, dirs, files in os.walk(dirname):
            for name in files:
                extension = os.path.splitext(name)[1][1:].strip().lower()
                # On linux there is a newline at the end which will cause the match to fail, so we just 'strip()' the '\n'
                # Also, add 'lower()' to ensure matching

                if (extension in self.extlist):
                    fullname = os.path.join(root, name)
                    try:
                        self.convert_file(fullname)
                    except IOError:
                        log.error("Unable to read or write the file: %s. Please check the file's permission.", fullname)
                    # else:
                    #     logging.error("Unable to process the file: %s. Please check.", fullname)
                    #     traceback.print_stack()



    def convert_file(self, filename):
        with open(filename, 'rb') as f: # read under the binary mode
            bytedata = f.read()

        if len(bytedata) == 0:
            log.info("Skipped empty file %s", filename)
            return

        encoding = chardet.detect(bytedata)['encoding']
        log.debug("Start scanning %s, which is %s - encoded", filename, encoding)

        if encoding == None:
            log.warning("Unable to detect the encoding of %s, so just leave it there.", filename)
            return

        if encoding.lower() == 'ascii':
            log.debug("Skipped %s - encoded %s", filename, encoding)
            return

        if remove_BOM:
            if encoding.lower() == 'utf-8':
                log.debug("Skipped %s - encoded %s", filename, encoding)
                return
        else:
            if encoding.lower().startswith('utf-8'):
                log.debug("Skipped %s - encoded %s", filename, encoding)
                return

        log.info("Start coverting %s, whose encoding is %s", filename, encoding)

        if encoding.lower() == 'gb2312':
            encoding = 'gb18030'

        try:
            strdata = bytedata.decode(encoding)
        except UnicodeDecodeError as e:
            log.error("Unicode error for file %s", filename)
            print(e)
            return

        log.debug("Overwriting file: %s in UTF-8", filename)
        with open(filename, 'wb') as f: # write under the binary mode
            f.write(strdata.encode('utf-8'))
        log.info("Finished converting the file: %s to UTF-8", filename)



    def run(self, root):
        if not os.path.exists(root):
            log.error("The file specified %s is neither a directory or a regular file", root)
            return

        log.info("Start working now!")

        if os.path.isdir(root):
            log.info("The root is: %s. ", root)
            log.info("Files with these extension names will be inspected: %s", self.extlist)
            self.walk_dir(root)
        else:
            log.info("Wow, only a single file will be processed: %s", root)
            self.convert_file(root)

        log.info("Finished all.")

        # If we hit here, it means the file specified is neither a directory or a regular file



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--exts', nargs='+', # '+'. Just like '*', all command-line args present are gathered into a list.
                        default=default_extlist,
                        help="the list of file extensions. Only those files ending with extensions in this list will be converted.")

    parser.add_argument('root',
                        help="the path pointing to the file or directory. \
                        If it's a directory, files contained in it with specified extensions will be converted to UTF-8. \
                        Otherwise, if it's a file, only that file will be converted to UTF-8")


    args = parser.parse_args()

    cvt2utf8 = Convert2Utf8(args.exts)
    cvt2utf8.run(args.root)
