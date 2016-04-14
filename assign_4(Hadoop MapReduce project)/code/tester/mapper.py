#!/usr/bin/python3

import sys

def mapper():

    for line in sys.stdin:
        # strip off extra whitespace, split on tab and put the data in an array
        data = line.strip().split("\t")

        # handle weed cases
        # what if there are not exactly 6 fields in that line?
        if len(data) != 6:
            print("Unexpected line encountered", file=sys.stderr)
            continue

        date, time, store, item, cost, payment = data
        print( "{0}\t{1}".format(store, cost) )


mapper()
