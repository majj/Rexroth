
#get torque data and send it to browser by websockets

import time
import asyncio
import datetime
import random
import websockets

import ast

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler #LoggingEventHandler,

import threading

import queue

## for data reading
reading_queue = queue.Queue()

## for data writing
writing_queue = queue.Queue()

import json


class EventHandler(FileSystemEventHandler):
    """
    handler for file create event
    ['event_type', 'is_directory', 'key', 'src_path']
    """
    
    #def __init__(self):
    #    pass
     
    def on_created(self, event):
        """ test """
        #print(dir(event))
        if not event.is_directory:
            #print(event.key)
            #print(event.event_type)
            print(event.src_path)
            
            file_path = event.src_path
            
            with open(file_path, 'r') as fh:
                
                data = fh.read()
                
                d = ast.literal_eval(data)
                v = d['tightening steps'][2]['angle threshold']['act']
                print(v)
                reading_queue.put({"angle act":v})
                
            
            
            reading_queue.put({"path":file_path})
        
        print("=="*20)        
        
        
    def on_moved(self, event):
        pass
        
    def on_modified(self, event):
        
        pass
        
def timer():
    
    """
    thread, timer for browser
    """
    
    while True:
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        reading_queue.put({"now":now})
        
        time.sleep(3)
        
def new_file_watcher(path):    
    """    
    thread, read torque data
    watch FTP folder and get new file creation event.
    """
    
    
    
    event_handler = EventHandler()
    
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()    
        
    try:
        while True:
            
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            reading_queue.put({"now":now})            
            
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()   
        
    observer.join()        


def open_protocol_client():
    pass
    

def opc_ua_client(url):
    """
    thread, opc ua client.
    
    """
    try:
        while True:
            msg = writing_queue.get()
            
            print("opc client - write value here")
            
            print(msg)
            
            time.sleep(1)
    except KeyboardInterrupt:
        pass    

## for client register
connected = set()


async def ws_handler(websocket, path):
    
    """
    websockets handler
    
    """
    
    connected.add(websocket)
    
    try:
        
        while True:
            
            data = reading_queue.get()        
            
            print(data)
            
            print(connected)
            print(">>>")
            
            try:
                
                await websocket.send(json.dumps(data))  
                ack = await websocket.recv()
                writing_queue.put(ack)
                print(ack)
               
            except Exception as ex:
                ## unregister here
                connected.remove(websocket)
                print(ex)

    finally:
            # Unregister.
            print("remove")
            connected.remove(websocket)
    
    print('hhh')
    
def main():
    
    """
    
    
    """
    
    #t1 = threading.Thread(target=timer)
    #t1.start()
    
    path = '../data'
    
    t2 = threading.Thread(target=new_file_watcher, args=(path,))
    t2.start()    
    
    url = "127.0.0.1"
    t3 = threading.Thread(target=opc_ua_client, args=(url,))
    t3.start()     
    
    start_server = websockets.serve(ws_handler, '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    
    main()
    
