Silence Stripper
================

This quick little python script uses the [pydub] library to remove the annoying
silence from the beginning and end of songs. 

Installation
============

```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

How to use
==========

Usage: 
./strip-silence.py [-h] [-r] [--target-dir TARGET_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -r                    Recursively go through directories.
  --target-dir TARGET_DIR
                        Directory to strip silence from

[pydub]:(http://pydub.com/)
