#!/usr/bin/env python

from __future__ import print_function
from sys import version_info, stdin
from platform import system
from time import clock

__author__="Daniel Oelschlegel"
__version__="0.01"
__license__="bsdl"

if version_info[0] >= 3:
   raw_input = input
   
ENCODING = stdin.encoding if system() == "Windows" else "utf-8"

def trimmer(text):
    '''Remove all extra informations'''
    return text.rsplit("{")[0].rsplit("[")[0].rsplit("(")[0].strip()

def read_dictionary(file_name):
    '''Read out the dictionary file and save into RAM'''
    dict = {}
    with open(file_name) if version_info[0] < 3 else open(file_name, encoding="utf-8") as dictionary_file:
        for line in dictionary_file.readlines():
             #ignoring comments and invalid vocabulary pairs
            if line.startswith("#") or line=="\n":
                continue
            
            #cloud definition recognised with pipe symbol("|")
            left_side, right_side = map(lambda x: x.split("|"), line.split("::"))
            
            #split for alternative identifiers separated by semicolon(";")
            collector = []
            for item in zip(left_side, right_side):
                for side_left in map(trimmer, item[0].split(";")):
                    for side_right in map(trimmer, item[1].split(";")):
                        collector.append((side_left, side_right))

            #save mapping in both search directions
            for item in collector:
                for translation_pair in ((item[0], item[1], ">"), (item[1], item[0], "<")):
                    value = translation_pair[0].lower().__hash__()
                    if value not in dict:
                        dict[value] = []
                    dict[value].append(translation_pair)
    return dict
           
def main(file_name):
    start_time = clock()
    gui(read_dictionary(file_name), clock() - start_time)

def output(value):
    if isinstance(value, str) and system() == "Windows" and version_info[0] < 3:
        return value.decode("utf-8").encode(ENCODING)
    return value
 
def make_unicode_python2(value):
    #TEST REQUIRED UNDER LINUX
    return value.decode(ENCODING).encode("utf8") if version_info[0] < 3 else value
    
def gui(dict, time_in_sec):
    print("dictionary with %d word created in %.2f seconds" % 
        (len(dict), time_in_sec))
    print("for abort press [ctrl]+[c]")
    while True:
        search_word_lower = make_unicode_python2(raw_input(": ").strip().lower())
        try:
            for item in dict[search_word_lower.__hash__()]:
                if item[0].lower() == search_word_lower:
                    print(output("%s %s %s"  % (item[0], item[2]*3, item[1])))
        except KeyError:
            print("word not found")

if __name__ == "__main__":
    main("dictionaries/de-en.txt")
