#!/usr/bin/python3

import sys

def reducer():
    salesTotal = 0
    no_of_sales = 0

    for line in sys.stdin:
        data = line.strip().split("\t")

        #handle fringe cases
        if len(data) != 2:
            #print("Unexpected line encountered with data = ",data, file=sys.stderr)
            continue

        thisKey, thisSale = data
        no_of_sales += 1
        salesTotal += float(thisSale)

    print("No. of sales : {0}\tTotal Sales : {1}".format(no_of_sales, salesTotal))

reducer()
