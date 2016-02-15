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
    Note #2: For Windows users, you need to replace the 4th line above with "venv\bin\activate"

## Usage
1. Modify the `cvt2utf8.py` file to point to the root path to the folder containing the files you want to convert.
1. Run the following commands

        python cvt2utf8.py
        
## Note
By default, the converted output text files will __NOT__ contain BOM (byte order mark). Should you want to learn what is BOM along with its implication, please check: https://en.wikipedia.org/wiki/Byte_order_mark 
