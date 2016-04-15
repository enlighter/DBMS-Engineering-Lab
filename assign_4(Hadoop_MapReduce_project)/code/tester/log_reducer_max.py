#!/usr/bin/python3

import sys

def reducer():
    hitsTotal = 0
    oldKey = None
    max_hits = 0
    max_key = None

    for line in sys.stdin:
        data = line.strip().split("\t")

        #handle fringe cases
        if len(data) != 2:
            continue

        thisKey, thisHit = data

        if oldKey and oldKey != thisKey:
            if hitsTotal > max_hits:
                max_hits = hitsTotal
                max_key = oldKey
            #print( "{0}\t{1}".format(oldKey, hitsTotal) )
            hitsTotal = 0

        oldKey = thisKey
        hitsTotal += 1

    if oldKey != None:
        if hitsTotal > max_hits:
            max_hits = hitsTotal
            max_key = oldKey
        #print( "{0}\t{1}".format(oldKey, hitsTotal) )
    print( "{0}\t{1}".format(max_key, max_hits) )

reducer()
