#!/usr/bin/env python

from __future__ import print_function
from sys import version_info, stdin, argv
from platform import system
from time import clock
from os.path import splitext
import io
     
__author__ = "Daniel Oelschlegel"
__copyright__ = __author__
__version__ = "0.01"
__license__ = "bsdl"

#FIXME: python 3 give a different dictionary size as python 2
#FIXME: empty queries return broken translations because of empty fields(?)

if version_info[0] < 3:
   from itertools import izip as zip, imap as map
   
ENCODING = stdin.encoding if system() == "Windows" else "utf-8"

def clean_entry(text):
    '''Remove all extra informations'''
    return text.split("{")[0].split("[")[0].strip()
    
def read_dictionary(file_name, start_time):
    '''Read out the dictionary file and save into global dictionary'''
    dictionary = {}
    with io.open(file_name, encoding="utf8") as dict_file:
        for line in dict_file:
            #ignoring comments and invalid vocabulary entries
            if line.startswith("#"):
                continue
            try:
                #cloud definition recognised with pipe symbol
                left_side, right_side = map(lambda x: x.split("|"), line.split("::"))
            except ValueError:
                continue
            #split for alternative identifiers separated by semicolon
            for item in zip(left_side, right_side):
               for side_left in map(clean_entry, item[0].split(";")):
                    for side_right in map(clean_entry, item[1].split(";")):
                        #save mapping in both search directions
                        for translation_pair in ((side_left, side_right, ">"), (side_right, side_left, "<")):
                            value = translation_pair[0].lower()
                            if value not in dictionary:
                                dictionary[value] = [translation_pair]
                            else:
                                dictionary[value].append(translation_pair[1:])
                            
    print("\ndictionary with %d word created in %.2f seconds" % (len(dictionary), clock() - start_time))
    return dictionary       
           
def create_output(value):
    '''Output encoding differs from used platform, terminal'''
    if isinstance(value, str) and system() == "Windows" and version_info[0] < 3:
        return value.decode("utf-8").encode(ENCODING)
    return value
 
def universal_input(value):
    '''Retrieves the user input with given value prompt as utf8 string'''
    #TODO: TEST REQUIRED UNDER LINUX
    if version_info[0] < 3:
        return unicode(raw_input(value).decode(ENCODING))
    
    return input(value)
    
def gui(dictionary):
    '''User interface with missing abort condition'''
    print("for exit press [ctrl]+[c]")
    while True:
        search_word_lower = universal_input(": ").strip().lower()
        if search_word_lower in dictionary:
            item = dictionary[search_word_lower][0]
            print(create_output("%s: %s%s") % (item[0], item[2], item[1]) , end="")
            for item in dictionary[search_word_lower][1:]:
                print(create_output(", %s%s")  % (item[1], item[0]), end="")
            print()
        else:
            print(create_output("%s not found" % search_word_lower))

def main(file_name):
    gui(read_dictionary(file_name, clock()))

if __name__ == "__main__":
    print(splitext(__file__)[0], __version__, "by", __author__)
    main("dictionaries/de-en.txt" if len(argv) < 2 else argv[1])
