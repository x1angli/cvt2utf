# Encode Your Text Files in UTF-8

This lightweight tool converts non-UTF-encoded (such as GB2312, GBK, BIG5 encoded) files, along with .java or other types of source code files, to UTF-8 encoded files.


## Installation
1. Make sure Python 3 is properly installed. 
1. Also make sure `virtualenv` is installed. (Windows: `pip install virtualenv`, Linux: `$ sudo pip install virtualenv`)
1. Run the following commands

        rem Enter the folder of this project
        cd utf8_encode
        virtualenv venv
        . venv/bin/activate
        pip install -r requirements.txt
    
    Note: For Windows users, you need to replace the 4th row above with "venv\bin\activate"  

## Usage
1. Modify the `cvt2utf8.py` file to point to the root path to the folder containing the files you want to convert.
1. Run the following commands

        python cvt2utf8.py
        
## Note
By default, the converted output text files will NOT contain BOM (byte order mark). Should you have no idea of BOM, just check: https://en.wikipedia.org/wiki/Byte_order_mark 
