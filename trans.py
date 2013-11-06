#!/usr/bin/env python

from __future__ import print_function
from sys import version_info, stdin, argv
from platform import system
from time import clock
try:
    from thread import start_new_thread
except ImportError:
     from _thread import start_new_thread
     
__author__ = "Daniel Oelschlegel"
__copyright__ = __author__
__version__ = "0.01"
__license__ = "bsdl"

#FIXME: python 3 give a different dictionary size as python 2
#FIXME: empty queries return broken translations because of empty field(?)

if version_info[0] >= 3:
   raw_input = input
else:
    from itertools import izip as zip, imap as map
   
ENCODING = stdin.encoding if system() == "Windows" else "utf-8"

dict = {}

def trimmer(text):
    '''Remove all extra informations'''
    return text.split("[")[0].split("{")[0].strip()

def read_dictionary(file_name, start_time):
    '''Read out the dictionary file and save into RAM'''
    for line in open(file_name) if version_info[0] < 3 else open(file_name, encoding="utf-8"):
        #ignoring comments and invalid vocabulary entries
        if line.startswith("#") or line=="\n":
            continue
        
        #cloud definition recognised with pipe symbol("|")
        left_side, right_side = map(lambda x: x.split("|"), line.split("::"))

        #split for alternative identifiers separated by semicolon(";")
        collector = []
        for item in zip(left_side, right_side):
           for side_left in map(trimmer, item[0].split(";")):
                for side_right in map(trimmer, item[1].split(";")):
                    #save mapping in both search directions
                    for translation_pair in ((side_left, side_right, ">"), (side_right, side_left, "<")):
                        value = translation_pair[0].lower()
                        if value not in dict:
                            dict[value] = []
                        dict[value].append(translation_pair)
    print("\ndictionary with %d word created in %.2f seconds" % (len(dict), clock() - start_time))
           
def main(file_name):
    start_new_thread(read_dictionary, (file_name, clock()))
    ##DEBUG
    #read_dictionary(file_name, clock())
    gui()

def output(value):
    if isinstance(value, str) and system() == "Windows" and version_info[0] < 3:
        return value.decode("utf-8").encode(ENCODING)
    return value
 
def make_unicode_python2(value):
    #TODO: TEST REQUIRED UNDER LINUX
    return value.decode(ENCODING).encode("utf8") if version_info[0] < 3 else value
    
def gui():
    print("for exit press [ctrl]+[c]")
    while True:
        search_word_lower = make_unicode_python2(raw_input(": ").strip().lower())
        try:
            for item in dict[search_word_lower]:
                if item[0].lower() == search_word_lower:
                    print(output("%s %s %s"  % (item[0], item[2]*3, item[1])))
        except KeyError:
            print("word not found")

if __name__ == "__main__":
    print(__file__[:-3], __version__, "by", __author__)
    main("dictionaries/de-en.txt" if len(argv) < 2 else argv[1])
