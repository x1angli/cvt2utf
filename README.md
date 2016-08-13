# Converts text files or source code files into UTF-8 encoding

This lightweight tool converts non-UTF-encoded (such as GB2312, GBK, BIG5 encoded) files to UTF-8 encoded files. 
It can either be executed from command line (CLI), or imported into other Python code.

## Installation

### Automatic Installation (recommended)
1. Make sure Python 3, along with pip, is properly installed. 
1. In your CLI, execute `pip install convert2utf` 

### Manual Installation (for developers only)
1. Make sure Python 3 is properly installed. 
1. Clone this project, or just download the .zip file from github.com and unarchive it
1. Start CLI (command line interface), enter the local folder
1. Setup Python virtual environment with `virtualenv ...` or `python -m venv ...`
1. Run: `pip install -r requirements.txt`
    
## Usage
There is only one mandatory argument: filename, where you can specify the directory or file name. 
* ___Batch mode___: Pass in a directory as the input, and all text files that meets the criteria underneath it will be converted to UTF8-encoding.
* ___Single file mode____: If the input argument is just an individual file, it would be straightforwardly converted to UTF-8. 

___Examples:___

* Change all .txt files to UTF-8 encoding. 
    
    Those byte-order marks a.k.a. "BOM"s or "signature"s in existing UTF-8 files will be removed. 


    `python cvt2utf.py "D:\mynotebook"`
    

    Afterwards, you could use any text editor (e.g. [Notepad++] (https://notepad-plus-plus.org/)) to verify the text files underneath the specified folder are already converted to UTF-8.

* Change all .csv files to UTF-8 encoding. Since BOM are used by some applications (such as Microsoft Excel)


    `python cvt2utf.py "D:\mynotebook" --exts csv --keepbom`


* Convert all .php, .js, .java, .py files to UTF-8 encoding. 

    Also, make sure all BOMs are removed. They are really nuisance for source code files!


    `python cvt2utf.py "D:\workspace" --exts php js java py`
    

* After manually verify the new UTF-8 files are correct, you can remove all .bak files


    `python cvt2utf.py "D:\workspace" --cleanbak`


* Alternatively, if you are confident with Python's in-house encoding and decoding, you can simply convert files without creating backups.
    
    Do __NOT__ call this, unless you know what you are doing. 


    `python cvt2utf.py "D:\workspace" --overwrite`


* Converts an individual file


    `python cvt2utf.py "D:\workspace\a.txt"`


* Show help information


    `python cvt2utf.py -h`


#### (Linux only) Directly run the program

Sometimes, you may want to run the program without specifying the Python interpretor, such as:

    ./cvt2utf.py "~/mynotebooks"
    
(Note the leading `python` command is missing here)

To achieve this, you first need to grant the execution permission onto the Python, (skip this provided it already have the eXecution permission:

    sudo chmod +x ./cvt2utf.py

Then activate the virtual environment:
    
    . venv/bin/activate

Alternatively, if you already have all dependencies installed with your default python environment, or you've already activated virtualenv’s python you could skip this. 

Then, make sure dependencies are installed

    pip install -r requirements.txt

Finally, execute the file: (you could add command arguments here):

    ./cvt2utf.py "~/the/base/dir"

You might want to use absolute path for this program if you are running it in an arbitrary working directory.


#### (For developers) Programmatically use this Python module

For Python programmers who want to use this module, see below

    
    >>> from cvt2utf import Convert2Utf8
    >>> cvt2utf = Convert2Utf8(['php', 'css', 'htm', 'html', 'js'], False, False)
    >>> cvt2utf.run('D:\\workspace')
    >>> cvt2utf.run('D:\\another\\folder')
    
Note: the constructor Convert2Utf8() takes 3 arguments: the extension list, the switch to keep BOM, the direct-overwriting mode.
The usage of these arguments is same as the command-line method. 


## Miscellaneous

By default, the converted output text files will __NOT__ contain BOM (byte order mark). Should you want to learn what is BOM along with its implication, please check: https://en.wikipedia.org/wiki/Byte_order_mark 


## FAQ

#### Why do we choose UTF-8 among all charsets? 

__A__: For i18n, UTF-8 is wide spread. It is the de facto standard for non-English texts.

Compared with UTF-16, UTF-8 is usually more compact and "with full fidelity". It also doesn't suffer from the endianness issue of UTF-16. 

#### Why do we need this tool?

__A__: Indeed, there are a bunch of text editors out there (such as Notepad++) that handle various encodings of text files very well. Yet for the purpose of __batch conversion__ we need this Python script. This script is also written for educational purpose -- developers can learn from this script to get an idea of how to handle text encoding.

#### Why should we remove BOMs (byte order mark) rather than add them?

__A__: Most compilers and interpreters can handle UTF-8 source code files very well, provided that those files are encoded __w/o__ BOM. Some compilers/interpreters might fail or give unexpected output whenever BOM is present. For this reason, I strongly advise the removal of BOM whenever we use UTF-8 encoding. 

Side note: of course, there are certain situations where BOMs are preferred. (For example, Microsoft Excel cannot parse correctly UTF8 w/o BOM CSV files with international characters. ) Such situations are rare. Overall, the necessity of BOM trumps other concerns. 

#### Is the current version reliable?

__A__: This code is still at its "beta" phase. We are striving to deliver high reliable solutions to our users. You might be aware that Python's built-in UTF encoding/decoding plus chardet may not be very reliable. For that reason, we suggest users create backups, either manually duplicate the file/directory, or automatically through our package (remember, the backup feature will be short-circuited with the `--overwrite` switch)

#### What kind of files should have BOM removed?
__A__: Here is a list
* __Jekyll__ : written in Ruby. [Details] (http://jekyllrb.com/docs/windows/#installation)
* __PHP__ 
* __JSP__
* ... others....
