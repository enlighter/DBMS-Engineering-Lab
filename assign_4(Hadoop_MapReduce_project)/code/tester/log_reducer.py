#!/usr/bin/python3

import sys

def reducer():
    hitsTotal = 0
    oldKey = None

    for line in sys.stdin:
        data = line.strip().split("\t")

        #handle fringe cases
        if len(data) != 2:
            continue

        thisKey, thisHit = data

        if oldKey and oldKey != thisKey:
            print( "{0}\t{1}".format(oldKey, hitsTotal) )
            hitsTotal = 0

        oldKey = thisKey
        hitsTotal += 1

    if oldKey != None:
        print( "{0}\t{1}".format(oldKey, hitsTotal) )

reducer()
