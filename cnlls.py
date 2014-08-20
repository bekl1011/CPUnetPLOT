#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os

from cnl_library import CNLParser
from collections import defaultdict, deque


def list_files_in_cur_dir():
    raw_list = os.listdir()
    no_invisible = filter(lambda filename: not filename.startswith("."), raw_list)

    return sorted( no_invisible )


def get_begin(cnl_file):
    return cnl_file.get_general_header()["Date"][1]

def are_close(cnl_file1, cnl_file2):
    t1 = get_begin(cnl_file1)
    t2 = get_begin(cnl_file2)

    return abs(t1 - t2) < 2


def find_match(cnl_file, list_of_files):
    for f in list_of_files:
        if ( are_close(cnl_file, f) ):
            list_of_files.remove(f)
            return f

    return None



def merge_comments(left_file, right_file):
    if ( not right_file ):
        return left_file.get_comment()

    c1 = left_file.get_comment()
    c2 = right_file.get_comment()

    if ( c1.find(c2) >= 0 ):
        return c1

    if ( c2.find(c1) >= 0 ):
        return c2

    return c1 + " / " + c2



def print_line(left_file, right_file, long=False):
    out = ""

    if ( right_file ):
        out = "{}  {}".format(left_file.filename, right_file.filename)
    else:
        out = left_file.filename

    if ( long ):
        out += "   // " + merge_comments(left_file, right_file)

    print( out )



## MAIN ##
if __name__ == "__main__":
    #import sys

    ## Command line arguments
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs='*')
    parser.add_argument("-l", "--long", action="store_true")

    args = parser.parse_args()


    if ( args.files ):
        filenames = sorted( args.files )
    else:
        filenames = list_files_in_cur_dir()




    cnl_files = defaultdict(deque)

    ## Parse files and store them in a dict (of lists) according to their hostname.
    for filename in filenames:
        cnl_file = CNLParser(filename)
        hostname = cnl_file.get_hostname()
        cnl_files[hostname].append( cnl_file )


    ## Match.
    hostnames = sorted( cnl_files.keys() )
    left_files = cnl_files[hostnames[0]]
    right_files = cnl_files[hostnames[1]]

    for left_file in left_files:
        matching_file = find_match(left_file, right_files)
        print_line(left_file, matching_file, args.long)


    ## Print left over right files.
    if ( len(right_files) > 0 ):
        print()
        for f in right_files:
            print_line(f, None, args.long)


    ## Print files with different hostnames
    #    Note: This is not the intended usecase!
    if ( len(hostnames) > 2 ):
        print()

        for h in hostnames[2:]:
            for f in cnl_files[h]:
                print_line(f, None, args.long)





