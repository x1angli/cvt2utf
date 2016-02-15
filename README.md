# Encode Your Text Files in UTF-8

This lightweight tool converts non-UTF-encoded (such as GB2312, GBK, BIG5 encoded) files, along with .java or other types of source code files, to UTF-8 encoded files.


## Installation
1. Make sure Python 3 is properly installed. 
1. Also make sure `virtualenv` is installed. (Windows: `pip install virtualenv`, Linux: `$ sudo pip install virtualenv`)
1. Clone this project onto your local hard drive, assuming the local folder name is "utf8_encode", which is the same as the project name. 
1. Run the following commands:

        cd utf8_encode
        virtualenv venv
        . venv/bin/activate
        pip install -r requirements.txt
    
    Note #1: If you place this project into a folder whose name is different from "utf8_encode", please make appropriate change to the 1st line above.
    
    Note #2: For Windows users, you need to replace the 4th line above with `venv\bin\activate`

## Configuration
Before running the code, you __must modify__ the `cvt2utf8.py` file. 

__* Tell the code where is your work space__

In the line `root_path` please point "root_path" to the folder under which you want the files to be translated to UTF8-encoded. 

__* List all the types of files you want to convert__

Just change the `ext_filter` to include the file extensions. 


## Usage
If you've done installation and configuration, simply run the following command:
        
    python cvt2utf8.py

Afterwards, you could use any text editor (e.g. [Notepad++] (https://notepad-plus-plus.org/)) to verify the text files underneath the specified folder are already converted to UTF-8.
        
## Miscellaneous

By default, the converted output text files will __NOT__ contain BOM (byte order mark). Should you want to learn what is BOM along with its implication, please check: https://en.wikipedia.org/wiki/Byte_order_mark 

## FAQ

#### Why do we choose UTF-8 among all charsets? 

__A__: For i18n, UTF-8 is wide spread. It is the defacto starndard for non-English texts.

Compared with UTF-16, UTF-8 is usually more compact and "with full fidelity". It also doesn't suffer from the endianness issue of UTF-16. 

#### Why do we need this tool?

__A__: Indeed, there are a bunch of text editors out there (such as Notepad++) that handle various encodings of text files very well. Yet for the purpose of __batch conversion__ we need this Python script. This script is also written for educational purpose -- developers can learn from this script to get an idea of how to handle text encoding.

#### Why should we remove BOMs (byte order mark) rather than add them?

__A__: Most compilers and interpreters can handle UTF-8 source code files very well, provided that those files are encoded __w/o__ BOM. Some compilers/interpreters might fail or give unexpected output whenever BOM is present. For this reason, I strongly advise the removal of BOM whenever we use UTF-8 enconing. 

Side note: of course, there are certain situations where BOMs are preferred. (For example, Microsoft Excel cannot parse correctly UTF8 w/o BOM CSV files with international characters. ) Such situations are rare. Overall, the necessity of BOM trumps other concerns. 

#### Questions? Bug reports? 

__A__: Feel free to send me an email: xl#x1ang.li (Please replace the hashtag with the "@" symbol)
