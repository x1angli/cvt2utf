# Converts text files or source code files into UTF-8 encoding

A lightweight tool that converts txt and source code files into UTF-8 encodings.
It can either be executed from command line interface(a.k.a "CLI" or "console"), or imported into your own Python code.

## Installation

1. Make sure Python 3 (Preferably 3.7 or above) is properly installed.
   2. [Optional] Dependency management tools such as [Poetry](https://python-poetry.org/) are also recommended.
1. Install Dependencies
   2. In your console, execute `pip3 install cvt2utf`
   2. Or, `pip3 install -r "./requirements.txt"`
   2. Or, for Poetry users, run `poetry install`
1. After installation, make sure the `cvt2utf` is in your PATH environment variable.
    
## Usage
There is only one mandatory argument: filename, where you can specify the directory or file name. 
* ___Directory mode___: You should put in a directory as the input, and all text files that meets the criteria underneath it will be converted to UTF-8.
* ___Single file mode___: If the input argument is just an individual file, it would be straightforwardly converted to UTF-8. 

___Examples:___

* Changes all .txt files to UTF-8 encoding. Additionally, **removes BOMs** from utf_8_sig-encoded files: 

    `cvt2utf convert "/path/to/your/repo" `

* Changes all .php files to UTF-8 encoding. But, skip processing those utf_8_sig-encoded PHP files: 

    `cvt2utf convert "/path/to/your/repo" -ext php --skiputf`

* Changes all .csv files to UTF-8-SIG encoding.

     Since BOM are used by some applications (such as Microsoft Excel), we want to add BOM

    `cvt2utf convert "/path/to/your/repo" -bom -ext csv`

    
* Convert all .c and .cpp files to UTF-8 with BOMs. 

    This action will also __add__ BOMs to existing UTF-encoded files. 
    
    Visual Studio may mandate BOM in source files. If BOMs are missing, then Visual Studio will unable to compile them.

    `cvt2utf convert "/path/to/your/repo" -bom -ext c cpp`
    
* Converts an individual file 

    `cvt2utf convert "/path/to/your/repo/a.txt"`

* After manually verify the new UTF-8 files are correct, you can remove all .bak files

    `cvt2utf cleanbak "/path/to/your/repo" `


* Alternatively, if you are extremely confident with everything, you can simply convert files without creating backups in the beginning.
    
    Use the `--nobak` option with **extra caution**!

    `cvt2utf convert "/path/to/your/repo" --nobak`

* Display help information

    `cvt2utf -h`

* Show version information

    `cvt2utf -v`

## Usage Note

### 1. About BOM

By default, the converted output text files will __NOT__ contain BOM (byte order mark). 

However, you can use the switch `-b` or `--addbom` to explicitly include BOM in the output text files. 

### 2. About file extensions

You should only feed text-like files to cvt2utf, while binary files (such as .exe files) **should be** left untouched. 
However, how to distinguish? Well, we use extension names. By default, files with the extension `txt` will be processed.
Feel free to customize this list either through editing the source code or with command line arguments.

### 3. About file size limits

We will ignore empty files. Also, we ignore files larger than 10MB. This is a reasonable limit. If you really wants to change it, feel free to do so.

## Trivial knowledge

### 1. About BOM
To learn more about byte-order-mark (BOM), please check: https://en.wikipedia.org/wiki/Byte_order_mark 

#### 1.1 When should we remove BOM?
Below is a list of places where BOM might cause a problem. To make your life easy and smooth, BOMs in these files are advised to be removed.
* __Jekyll__ : Jekyll is a Ruby-based CMS that generates static websites. Please remove BOMs in your source files. Also, remove them in your CSS if you are SASSifying.
* __PHP__: BOMs in `*.php` files should be stripped.
* __JSP__: BOMs in `*.jsp` files should be stripped. 
* (to be added...)

#### 2 When should we add BOM?
BOMs in these files are not necessary, but it is recommended to add them.

* __Source Code in Visual Studio Projects__: 
    It is recommended in MSDN that "Always prefix a Unicode plain text file with a byte order mark" [Link](https://msdn.microsoft.com/en-us/library/windows/desktop/dd374101(v=vs.85).aspx). 
    Visual Studio may mandate BOM in source files. If BOMs are missing, then Visual Studio may not be able to compile them.

* __CSV__: 
    BOMs in CSV files might be useful and necessary, especially if it is opened by Excel.

### 2. About UTF & Unicode

![img.png](https://ask.qcloudimg.com/draft/1300884/xmwux3k6z4.jpg)
* **ASCII**: Just 1 byte. 1st byte: `00`~`7F`
* **Latin-1**: Just 1 byte. ASCII charset + (`80`~`FF`)
* **GB2312**: 2 bytes. ASCII charset + (1st byte: `A1`~`FE` (or more restrictively, `A1`~`F7`) with 2nd byte: `A1`~`FE`).
* **GBK**: 2 bytes. ASCII charset + (1st byte: `A1`~`FE` with 2nd byte: `40`~`FE`).
* **UTF-8**: Variable Length:  `0x00`~`0x7F`; `0x80`~`0x7FF`; `0x800`~`0xFFFF`; `0x10000`~`0x10FFFF`

#### See Also
* [其实你并不懂 Unicode by 纤夫张](https://zhuanlan.zhihu.com/p/53714077)
* [UTF-8 编码及检查其完整性](https://github.com/hsiaosiyuan0/blog/blob/master/%2Fposts%2Fos%2FUTF-8%20%E7%BC%96%E7%A0%81%E5%8F%8A%E6%A3%80%E6%9F%A5%E5%85%B6%E5%AE%8C%E6%95%B4%E6%80%A7.md)


## FAQ

#### Why do we choose UTF-8 among all charsets? 

It is the de-facto standard for i18n.

Compared with UTF-16, UTF-8 is usually more compact and "with full fidelity". It also doesn't suffer from the endianness issue of UTF-16. 

#### Why do we need this tool?

Indeed, there are a bunch of text editors with stunning text encoding capabilities. Yet for users who want to do __batch conversions__ this tool could be handy. 

Additionally, some users gave me the feedback to bring into attention those Linux commands such as `sed`, `iconv`, `enca`. All of them have the limitation that they are Linux-only commands, and not applicable for other OS. 
* __`iconv`__ requires you to explicitly specify the "from-encoding" of the file. Moreover, it converts a single file at a time, so that you have to write a bash script for batch conversion. Worst of all, it lacks adaptability so that the set of files have to be encoded in the same character set. See [here](https://www.tecmint.com/convert-files-to-utf-8-encoding-in-linux/) for more information.
* __`recode`__ is really a nice and powerful tool. It goes further by supporting CR-LF conversion and Base64. See [here](https://stackoverflow.com/questions/64860/best-way-to-convert-text-files-between-character-sets) and [here](https://github.com/rrthomas/recode/).
* __`sed`__ can be used to add or remove BOM. It can also be used in combination with `iconv`. 
* __`enca`__ is used to detect the current encoding of a file.
