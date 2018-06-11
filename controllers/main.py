# -*- coding: utf-8 -*-

"""
get torque data and send it to browser by websockets

pyzqm: https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pushpull.html

"""

import time
import asyncio

#import random

import threading

#import queue

## for data reading
#reading_queue = queue.Queue()

## for data writing
#writing_queue = queue.Queue()

#import msgpack

from lib.file_watcher import new_file_watcher
from lib.opc_ua_client import OPC_UA_Client

from ws_server import start_server

def timer():
    
    """
    thread, timer for browser
    """
    
    while True:
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        reading_queue.put({"now":now})
        
        time.sleep(3)       


def open_protocol_client():
    pass
    
    
def main():    
    """
    main    
    """
    
    #t1 = threading.Thread(target=timer)
    #t1.start()
    
    path = '../data'
    
    t2 = threading.Thread(target=new_file_watcher, args=(path,))
    t2.start()    
    
    url = "127.0.0.1"
    
    c = OPC_UA_Client()    
    t3 = threading.Thread(target=c.write, args=(url,))
    t3.start()    

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    
    main()
    
