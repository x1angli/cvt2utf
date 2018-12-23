# Converts text files or source code files into UTF-8 encoding

This lightweight tool converts text files encoded in non-UTF (such as GB2312, GBK, BIG5) to UTF-8 encoded files. 
It can either be executed from command line interface(a.k.a "CLI" or "console"), or imported into other Python code.

## Installation

### Getting Started!
1. Make sure Python 3, along with pip, is properly installed. 
1. In your console, execute `pip install convert2utf` 
1. After installation, make sure the `cvt2utf` is in your PATH environment variable.
    
## Usage
There is only one mandatory argument: filename, where you can specify the directory or file name. 
* ___Directory mode___: You should put in a directory as the input, and all text files that meets the criteria underneath it will be converted to UTF-8.
* ___Single file mode___: If the input argument is just an individual file, it would be straightforwardly converted to UTF-8. 

___Examples:___

* Changes all .txt files to UTF-8 encoding. Additionally, **removes BOMs** from utf_8_sig-encoded files: 

    `cvt2utf "/path/to/your/repo" --exts txt`

* Changes all .txt files to UTF-8 encoding. But, leaves unchanged those utf_8_sig-encoded files: 

    `cvt2utf "/path/to/your/repo" --skiputf`

* Changes all .csv files to UTF-8 encoding: 

     Since BOM are used by some applications (such as Microsoft Excel), we want to add BOM

    `cvt2utf "/path/to/your/repo" -b --exts csv`

    
* Convert all .c and .cpp files to UTF-8 with BOMs. 

    This action will also __add__ BOMs to existing UTF-encoded files. 
    
    Visual Studio may mandate BOM in source files. If BOMs are missing, then Visual Studio will unable to compile them.

    `cvt2utf "/path/to/your/repo" -b --exts c cpp`
    
* Converts an individual file 

    `cvt2utf "/path/to/your/repo/a.txt"`

* After manually verify the new UTF-8 files are correct, you can remove all .bak files

    `cvt2utf cleanbak "/path/to/your/repo" `


* Alternatively, if you are extremely confident with everything, you can simply convert files without creating backups in the beginning.
    
    Use the `--nobak` option with **extra caution**!

    `cvt2utf "/path/to/your/repo" --nobak`

* Display help information

    `cvt2utf -h`

* Show version information

    `cvt2utf -v`

## Miscellaneous

### 1. About BOM

By default, the converted output text files will __NOT__ contain BOM (byte order mark). 

However, you can use the switch `-b` or `--addbom` to explicitly include BOM in the output text files. 

To learn more, please check: https://en.wikipedia.org/wiki/Byte_order_mark 

### 2. About file extensions

You should only feed text-like files to cvt2utf, while binary files (such as .exe files) **should be** left untouched. 
However, how to distinguish? Well, we use extension names. By default, files whose extentions are in the list: 
`txt, cpp, c, hpp, h, php, md, json, py` will be processed. 
You can customize this list either through editing the source code or with command line arguments.

### 3. About file size limits

We will ignore empty files. Also, we ignore files larger than 10MB. This is a reasonable limit. If you really wants to change it, feel free to do so.

## FAQ

#### Why do we choose UTF-8 among all charsets? 

For i18n, UTF-8 is wide spread. It is the de-facto standard for non-English texts.

Compared with UTF-16, UTF-8 is usually more compact and "with full fidelity". It also doesn't suffer from the endianness issue of UTF-16. 

#### Why do we need this tool?

Indeed, there are a bunch of text editors out there (such as Notepad++) that handle various encodings of text files very well. Yet for the purpose of __batch conversion__ we need this Python script. This script is also written for educational purpose -- developers can learn from this script to get an idea of how to handle text encoding.

#### When should we remove BOM?
Below is a list of places where BOM might cause a problem. To make your life easy and smooth, BOMs in these files are advised to be removed.
* __Jekyll__ : Jekyll is a Ruby-based CMS that generates static websites. Please remove BOMs in your source files. Also, remove them in your CSS if you are SASSifying.
* __PHP__: BOMs in `*.php` files should be stripped.
* __JSP__: BOMs in `*.jsp` files should be stripped. 
* (to be added...)

#### When should we add BOM?
BOMs in these files are not necessary, but it is recommended to add them.
* __Unicode plain text file__: Microsoft suggests "Always prefix a Unicode plain text file with a byte order mark" (https://msdn.microsoft.com/en-us/library/windows/desktop/dd374101(v=vs.85).aspx)
Visual Studio may mandate BOM in source files. If BOMs are missing, then Visual Studio will unable to compile them.

* __CSV__: BOMs in CSV files might be useful and necessary, especially if it is opened by Excel.

#### Is the current version reliable?
We are dedicated to deliver quality tools to friends like you. This Python package relies on chardet, which is not so intelligent in terms of recognizing file codecs. Hopefully, better solutions will appear in the future.
