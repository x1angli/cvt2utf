Converts text files or source code files into UTF-8 encoding
============================================================

This lightweight tool converts non-UTF-encoded (such as GB2312, GBK,
BIG5 encoded) files to UTF-8 encoded files. It can either be executed
from command line (CLI), or imported into other Python code.

Installation
------------

Automatic Installation (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Make sure Python 3, along with pip, is properly installed.
2. In your CLI, execute ``pip install convert2utf``

Manual Installation (for developers only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Make sure Python 3 is properly installed.
2. Clone this project, or just download the .zip file from github.com
   and unarchive it
3. Start CLI (command line interface), enter the local folder
4. Setup Python virtual environment with ``virtualenv ...`` or
   ``python -m venv ...``
5. Run: ``pip install -r requirements.txt``

Usage
-----

There is only one mandatory argument: filename, where you can specify
the directory or file name. \* ***Batch mode***: Pass in a directory as
the input, and all text files that meets the criteria underneath it will
be converted to UTF8-encoding. \* ***Single file mode***: If the input
argument is just an individual file, it would be straightforwardly
converted to UTF-8.

***Examples:***

-  Change all .txt files to UTF-8 encoding.

   ``python cvt2utf.py "/path/to/your/repo"``

-  Change all .txt files to UTF-8 encoding. Plus remove byte-order marks
   (a.k.a. “BOM”s or “signature”s) from existing UTF-8 files.

   ``python cvt2utf.py "/path/to/your/repo" -u``

-  Change all .csv files to UTF-8 encoding.

   Since BOM are used by some applications (such as Microsoft Excel), we
   want to add BOM

   ``python cvt2utf.py "/path/to/your/repo" -b -u --exts csv``

-  Convert all .php, .js, .java, .py files to UTF-8 encoding.

   Meanwhile, those BOMs from existing UTF-encoded files will be
   **removed** .

   ``python cvt2utf.py "/path/to/your/repo" -u --exts php js java py``

-  Convert all .c and .cpp files to UTF-8 with BOMs.

   This action will also **add** BOMs to existing UTF-encoded files.

   Per `issue#3`_, Visual Studio may mandate BOM in source files. If
   BOMs are missing, then Visual Studio will unable to compile them.

   ``python cvt2utf.py "/path/to/your/repo" -b -u --exts c cpp``

-  After manually verify the new UTF-8 files are correct, you can remove
   all .bak files

   ``python cvt2utf.py "/path/to/your/repo" --cleanbak``

-  Alternatively, if you are extremely confident with everything, you
   can simply convert files without creating backups in the beginning.

   Do **NOT** run the command in this way, unless you know what you are
   doing!

   ``python cvt2utf.py "/path/to/your/repo" --overwrite``

-  Converts an individual file

   ``python cvt2utf.py "/path/to/your/repo/a.txt"``

-  Show help information

   ``python cvt2utf.py -h``

.. _issue#3: https://github.com/x1angli/convert2utf/issues/3

(Linux only) Directly run the program
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, you may want to run the program without specifying the Python
interpretor, such as:

::

    ./cvt2utf.py "/path/to/your/repo"

(Note the leading ``python`` command is missing here)

To achieve this, you first need to grant the execution permission onto
the Python, (skip this provided it already have the eXecution
permission:

::

    sudo chmod +x ./cvt2utf.py

Then activate the virtual environment:

::

    . venv/bin/activate

Next, make sure dependencies are installed

::

    pip install -r requirements.txt

Finally, execute the file: (you could add command arguments here):

::

    ./cvt2utf.py "/path/to/your/repo"

You might want to use absolute path for this program if you are running
it in an arbitrary working directory.

Miscellaneous
-------------

By default, the converted output text files will **NOT** contain BOM
(byte order mark).

However, you can use the switch ``-a`` or ``--addbom`` to explicitly
include BOM in the output text files.

To learn more, please check:
https://en.wikipedia.org/wiki/Byte\_order\_mark

FAQ
---

Why do we choose UTF-8 among all charsets?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For i18n, UTF-8 is wide spread. It is the de facto standard for
non-English texts.

Compared with UTF-16, UTF-8 is usually more compact and “with full
fidelity”. It also doesn’t suffer from the endianness issue of UTF-16.

Why do we need this tool?
^^^^^^^^^^^^^^^^^^^^^^^^^

Indeed, there are a bunch of text editors out there (such as Notepad++)
that handle various encodings of text files very well. Yet for the
purpose of **batch conversion** we need this Python script. This script
is also written for educational purpose – developers can learn from this
script to get an idea of how to handle text encoding.

When should we remove BOM?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is a list of places where BOM might cause a problem. To make your
life easy and smooth, BOMs in these files are advised to be removed. \*
**Jekyll** : Jekyll is a Ruby-based CMS that generates static websites.
Please remove BOMs in your source files. Also, remove them in your CSS
if you are SASSifying. \* **PHP**: BOMs in ``*.php`` files should be
stripped. \* **JSP**: BOMs in ``*.jsp`` files should be stripped. \* (to
be added…)

When should we add BOM?
^^^^^^^^^^^^^^^^^^^^^^^

BOMs in these files are not necessary, but it is recommended to add
them. \* **Unicode plain text file**: M$ suggests “Always prefix a
Unicode plain text file with a byte order mark”
(https://msdn.microsoft.com/en-us/library/windows/desktop/dd374101(v=vs.85).aspx)
\* **CSV**: BOMs in CSV files might be useful and necessary.

Is the current version reliable?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This code is still at its “beta” phase. We are striving to deliver high
reliable solutions to our users. You might be aware that Python’s
built-in UTF encoding/decoding plus chardet may not be very reliable.
For that reason, we suggest users create backups.