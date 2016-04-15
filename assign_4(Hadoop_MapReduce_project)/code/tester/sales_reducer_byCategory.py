#!/usr/bin/python3

import sys

def reducer():
    salesTotal = 0
    oldKey = None

    for line in sys.stdin:
        data = line.strip().split("\t")

        #handle fringe cases
        if len(data) != 2:
            #print("Unexpected line encountered with data = ",data, file=sys.stderr)
            continue

        thisKey, thisSale = data

        if oldKey and oldKey != thisKey:
            print( "{0}\t{1}".format(oldKey, salesTotal) )
            salesTotal = 0

        oldKey = thisKey
        salesTotal += float(thisSale)

    if oldKey != None:
        print( "{0}\t{1}".format(oldKey, salesTotal) )

reducer()
