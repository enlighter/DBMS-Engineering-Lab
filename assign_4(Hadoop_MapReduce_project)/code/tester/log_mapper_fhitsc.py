#!/usr/bin/python3

import sys

def mapper():

    for line in sys.stdin:
        data = line.strip().split('\"')

        if len(data) == 3:
            first_blob, request, last_blob = data
            fb = first_blob.find('[')
            sb = first_blob.find(']')
            if fb != -1:
                first_part = first_blob[:fb]
                #print(first_part)
            else:
                #print("Unexpected line encountered")
                continue

            data_head = first_part.strip().split(' ')
            #print(data_head)
            if len(data_head) == 3:
                ip,client_id,client_name = data_head
            else:
                #print("Unexpected line encountered")
                continue

            if sb != -1:
                second_part = first_blob[fb+1:sb]
                #print(second_part)
            else:
                #print("Unexpected line encountered")
                continue
            time = second_part

            data_tail = last_blob.strip().split(" ")
            #print(data_tail)
            if len(data_tail) == 2:
                status_code, size = data_tail
            else:
                #print("Unexpected line encountered")
                continue

            request_data = request.strip().split(" ")
            if len(request_data) == 3:
                request_method, request_url,request_protocol = request_data
            else:
                continue

            if request_url.find('http://www.the-associates.co.uk') == 0:
                request_url = request_url[len('http://www.the-associates.co.uk'):]
            if request_url == '':
                request_url = '/'

            if '1' in request_protocol:
                print( "{0}\t{1}".format(request_url, 1) )


mapper()
