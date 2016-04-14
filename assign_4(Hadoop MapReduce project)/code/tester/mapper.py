import sys

def mapper():
    for line in open('sales_data'):
        data = line.strip().split("\t")
        if len(data) != 6:
            print("Unexpected line encountered", file=sys.stderr)
            continue
        date, time, store, item, cost, payment = data
        print( "{0}\t{1}".format(store, cost) )

mapper()
